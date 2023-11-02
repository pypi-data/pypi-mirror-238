#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: zhangkai
Email: kai.zhang1@nio.com
Last modified: 2018-06-03 00:38:17
'''

import datetime
import hashlib
import os
import random
import re
import uuid

import pymongo
import tornado.web
from bson import ObjectId
from utils import Dict, awaitable

from .application import Blueprint
from .basehandler import BaseHandler

bp = Blueprint(__name__)


class BaseHandler(BaseHandler):

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, HEAD, OPTIONS')
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header('Access-Control-Max-Age', '3600')

    def options(self):
        self.set_status(204)
        self.finish()

    def encrypt(self, password):
        return hashlib.md5(f'digua_{password}'.encode()).hexdigest()

    async def gen_code(self, email):
        code = ''.join(random.sample('0123456789', 4))
        key = f'{self.prefix}_code_{email}'
        await awaitable(self.rd.setex(key, 600, code))
        return code

    async def get_user(self, email):
        if email.find('@') >= 0:
            return await awaitable(self.db.users.find_one({'email': email}))
        else:
            return await awaitable(self.db.users.find_one({'username': email}))

    async def check_code(self):
        email = self.get_argument('email', None)
        code = self.get_argument('code', None)
        if email and code:
            key = f'{self.prefix}_code_{email}'
            if code == await awaitable(self.rd.get(key)):
                return Dict({'err': 0})
        return Dict({'err': 1, 'msg': '验证码无效'})

    async def check_username(self):
        username = self.get_argument('username', None)
        if not username:
            return Dict({'err': 1, 'msg': '请输入用户名'})
        if len(username) < 5:
            return Dict({'err': 1, 'msg': '用户名至少5个字符'})
        if len(username) > 20:
            return Dict({'err': 1, 'msg': '用户名至多20个字符'})
        if await awaitable(self.db.users.find_one({'username': username})):
            return Dict({'err': 1, 'msg': '用户名重复'})
        return Dict({'err': 0})

    async def check_email(self):
        email = self.get_argument('email', None)
        if not email:
            return Dict({'err': 1, 'msg': '请输入邮箱'})
        if len(email) > 64:
            return Dict({'err': 1, 'msg': '邮箱地址太长'})
        if email.find(' ') >= 0:
            return Dict({'err': 1, 'msg': '邮箱地址不能包含空格'})
        if not re.match(r'.*@(.*)\.(\w+)$', email):
            return Dict({'err': 1, 'msg': '请填写正确的邮箱格式'})
        if not re.search(r'@(qq.com|gmail.com|163.com|126.com|yeah.net|outlook.com|live.com|foxmail.com|hotmail.com|sina.com|vip.qq.com|139.com|icloud.com|aliyun.com|88.com|sina.cn|tom.com|live.cn|yahoo.com|189.cn|msn.com|sohu.com|yandex.com|.edu.cn|vip.163.com|msn.cn)$', email.lower()):
            return Dict({'err': 1, 'msg': '请使用常用邮箱注册'})
        if await awaitable(self.db.users.find_one({'email': email})):
            return Dict({'err': 1, 'msg': '邮箱地址重复'})
        return Dict({'err': 0})

    async def check_scene(self):
        scene = self.get_argument('scene', None)
        if not scene:
            return Dict({'err': 1, 'msg': f'scene is not defined: {scene}'})

        resp = await self.http.get(scene)
        if not resp.code == 200:
            return Dict({'err': 1, 'msg': f'get scene failed: {scene}'})

        ret = resp.json()
        if ret.err:
            return ret

        user = await awaitable(self.db.users.find_one({'openId': ret.openId}))
        if not user:
            if self.current_user:
                ret.active = True
                keys = ['active', 'openId', 'avatarUrl', 'city', 'country', 'gender', 'language', 'nickName', 'province']
                update = {k: v for k, v in ret.items() if k in keys if v}
                user = await awaitable(self.db.users.find_one_and_update({'_id': self.current_user._id}, {'$set': update}, return_document=True))
            else:
                ret.active = True
                ret.token = uuid.uuid4().hex
                ret.id = await awaitable(self.db.users.seq_id)
                ret.created_at = datetime.datetime.now().replace(microsecond=0)
                user = await awaitable(self.db.users.find_one_and_update({'openId': ret.openId}, {'$set': ret}, upsert=True, return_document=True))

        user.err = 0
        self.set_cookie('token', user.token, expires_days=365)
        return user


@bp.route("/check")
class CheckHandler(BaseHandler):

    async def get(self):
        for key, value in self.args.items():
            if hasattr(self, f'check_{key}'):
                ret = await getattr(self, f'check_{key}')()
                break
        else:
            ret = Dict({'err': 1, 'msg': 'not authorized'})
        self.finish(ret)


@bp.route("/logout")
class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_all_cookies()
        self.redirect('/')


@bp.route("/signup")
class SignupHandler(BaseHandler):

    def get(self):
        self.next = self.get_argument('next', '/')
        if self.args.from_id:
            self.set_cookie('from_id', self.args.from_id, expires_days=1)
        self.render('signup.html')

    async def post(self):
        ret = await self.check_username()
        if ret.err:
            return self.finish(ret)
        ret = await self.check_email()
        if ret.err:
            return self.finish(ret)
        if self.args.code:
            ret = await self.check_code()
            if ret.err:
                return self.finish(ret)
            self.args.pop('code')

        if not (self.args.username and self.args.password and self.args.email):
            return self.finish({'err': 1, 'msg': '信息未填写完整'})

        token = uuid.uuid4().hex
        doc = self.args.copy()
        doc.update({
            'password': self.encrypt(self.args.password),
            'token': token,
            'created_at': datetime.datetime.now().replace(microsecond=0)
        })
        try:
            user = await awaitable(self.db.users.find_one_and_update({'username': doc['username']},
                                                                     {'$set': doc},
                                                                     upsert=True,
                                                                     return_document=True))
        except pymongo.errors.DuplicateKeyError:
            missing = await awaitable(self.db.users.find_one({'id': {'$exists': 0}}))
            if not missing:
                return self.finish({'err': 1, 'msg': '用户名重复'})

            seq_id = await awaitable(self.db.users.seq_id)
            await awaitable(self.db.users.update_one({'_id': missing._id}, {'$set': {'id': seq_id}}))
            user = await awaitable(self.db.users.find_one_and_update({'username': doc['username']},
                                                                     {'$set': doc},
                                                                     upsert=True,
                                                                     return_document=True))

        update = Dict()
        if not user.id:
            if os.environ.get('MISSING_IDS'):
                ids = [int(x) for x in os.environ.get('MISSING_IDS', '').split(',')]
                exist_ids = await awaitable(self.db.users.distinct('id', {'id': {'$in': ids}}))
                missing_ids = sorted(set(ids) - set(exist_ids))
                if missing_ids:
                    update.id = missing_ids[0]

            if 'id' not in update:
                update.id = await awaitable(self.db.users.seq_id)
                if update.id == 1:
                    update.admin = True

        if update:
            await awaitable(self.db.users.update_one({'_id': user._id}, {'$set': update}))
            user.update(update)

        self.set_cookie('token', token, expires_days=365)
        self.finish({'err': 0, 'user': user})


@bp.route("/signin")
class SigninHandler(BaseHandler):

    def get(self):
        self.next = self.get_argument('next', '/')
        self.render('signin.html')

    async def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        remember = self.get_argument('remember', None)
        if not (username and password):
            return self.finish({'err': 1, 'msg': '请输入用户名和密码'})

        if username.find('@') >= 0:
            query = {'email': username, 'password': self.encrypt(password)}
        else:
            query = {'username': username, 'password': self.encrypt(password)}
        user = await awaitable(self.db.users.find_one(query))
        if not user:
            return self.finish({'err': 1, 'msg': '用户名或密码错误'})

        expires_days = 365 if remember == 'on' else None
        self.set_cookie('token', user.token, expires_days=expires_days)
        self.finish({'err': 0, 'user': user})


@bp.route("/user")
class UserHandler(BaseHandler):

    async def get(self):
        if self.current_user:
            user = {k: v for k, v in self.current_user.items() if k not in ['_id', 'password']}
            self.finish(user)
        else:
            self.finish({'err': 1, 'msg': '用户未登录'})

    @tornado.web.authenticated
    async def put(self):
        await self.del_cached_user()
        self.finish({'err': 0})

    @tornado.web.authenticated
    async def post(self):
        user = self.current_user
        old_password = self.get_argument('old_password', None)
        password = self.get_argument('password', None)
        if not (old_password and self.encrypt(old_password) == user.password):
            return self.finish({'err': 1, 'msg': '原密码错误'})
        if not password:
            return self.finish({'err': 1, 'msg': '请输入新密码'})

        await awaitable(self.db.users.update_one({'_id': user._id}, {'$set': {'password': self.encrypt(password)}}))
        self.finish({'err': 0})

    @tornado.web.authenticated
    async def delete(self):
        if not self.current_user.admin:
            return self.finish({'err': 1, 'msg': 'unauthorized'})

        await awaitable(self.db.users.delete_one({'_id': ObjectId(self.args._id)}))
        self.finish({'err': 0})


@bp.route("/reset")
class ResetHandler(BaseHandler):

    def get(self):
        self.render('reset.html')

    async def post(self):
        ret = await self.check_code()
        if ret.err:
            return self.finish(ret)

        email = self.get_argument('email', None)
        password = self.get_argument('password', None)
        if not (email and password):
            return self.finish({'err': 1, 'msg': '请输入邮箱和密码'})

        user = await self.get_user(email)
        if not user:
            return self.finish({'err': 1, 'msg': '用户不存在'})

        await awaitable(self.db.users.update_one({'_id': user._id}, {'$set': {'password': self.encrypt(password)}}))
        self.finish({'err': 0})


@bp.route(r'/active/(\w+)')
class ActiveHandler(BaseHandler):

    async def get(self, code):
        email = await awaitable(self.rd.get(f'{self.prefix}_active_{code}'))
        if email:
            token = self.get_cookie('token')
            if token:
                await awaitable(self.db.users.update_one({'token': token}, {'$set': {'email': email, 'active': True}}))
            else:
                await awaitable(self.db.users.update_one({'email': email}, {'$set': {'active': True}}))
        self.redirect('/admin')

    async def post(self, _id):
        await awaitable(self.db.users.update_one({'_id': ObjectId(_id)}, {'$set': {'active': True}}))
        self.finish({'err': 0})


@bp.route(r'/email/(\w+)')
class EmailHandler(BaseHandler):

    async def get(self, action):
        if not re.match(r'.*@(.*)\.(\w+)$', self.args.email or ''):
            return self.finish({'err': 1, 'msg': '请填写正确的邮箱格式'})

        if action == 'reset':
            user = await self.get_user(self.args.email)
            if not user:
                return self.finish({'err': 1, 'msg': '用户不存在'})
            title = f'{self.host} 重设密码邮件'
            code = await self.gen_code(self.args.email)
            content = f'您本次操作的验证码为: {code}'
        elif action == 'check':
            title = f'{self.host} 验证邮件'
            code = await self.gen_code(self.args.email)
            content = f'您本次操作的验证码为: {code}'
        elif action == 'active':
            title = f'{self.host} 激活邮件'
            code = uuid.uuid4().hex
            key = f'{self.prefix}_active_{code}'
            await awaitable(self.rd.setex(key, 600, self.args.email))
            url = f'{self.scheme}://{self.host}/active/{code}'
            content = f'请点击链接或将其复制到浏览器地址栏打开: <br><a href="{url}">{url}</a>'
        else:
            return self.finish({'err': 1, 'msg': 'action is not defined'})

        await self.app.email.send(self.args.email, title, content)
        self.finish({'err': 0})

    post = get
