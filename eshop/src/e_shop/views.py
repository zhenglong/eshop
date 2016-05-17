# -*- coding: utf-8 -*-
'''
Created on Mar 28, 2015

@author: tristan
'''
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
import json
import apis
import requests
from requests.auth import HTTPBasicAuth
from e_shop import facades
from django.contrib.auth.models import User
from oauth2_provider.models import AbstractApplication, Application
import uuid
from e_shop.viewModels import UserViewModel
from e_shop.apis import FacadeFactory

class TabIndex(object):
    category_management,product_param_maintain,my_product,registration_info,brand_management,discount_management, sale_statistics=range(7)

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

class BaseView(View):
    @staticmethod
    def json_result(data, code, message):
        return HttpResponse(content=json.dumps({'code':code, 'message':message, 'data':data}),
                                    content_type='application/json')

class OAuthAccessor:
    oauth_host = 'http://localhost:8000'
    @staticmethod
    def register_application(user):
        my_app = Application()
        my_app.name = str(uuid.uuid4())
        #my_app.client_id = generate_client_id()
        #my_app.client_secret = generate_client_secret()
        my_app.client_type = AbstractApplication.CLIENT_CONFIDENTIAL
        my_app.authorization_grant_type = AbstractApplication.GRANT_PASSWORD
        my_app.user_id = user.id
        my_app.save()
        return OAuthAccessor.get_application(user)
    @staticmethod
    def get_application(user):
        return facades.OAuthProxy().get(user.id)

    @staticmethod
    def access_token(user, password):
        app = OAuthAccessor.get_application(user)
        r = requests.post(OAuthAccessor.oauth_host + '/o/token/', {
                                                             'grant_type':'password',
                                                             'username':user.username,
                                                             'password':password
                                                             },
                          auth=HTTPBasicAuth(app.client_id, app.client_secret))
        return r.json()


class user_profile(LoginRequiredMixin, BaseView):
    def get(self, request):
        template = loader.get_template('admin/user_profile.jinja')
        context = RequestContext(request, fill_common_info({'title':u'编辑用户资料'}, request))
        return HttpResponse(template.render(context))

class account_register(BaseView):
    def post(self, request):
        data = json.loads(request.body)
        user_name = data['userName']
        password = data['password']
        user = User.objects.create_user(user_name, user_name+'@eshop.com', password=password)
        FacadeFactory(user).get_obj(facades.UserFacade).save(UserViewModel({'name':user_name, 'auth_user_id':user.id}))
        return BaseView.json_result(None, code = apis.StatusCodeExtension.success, message = None)

class account_logout(BaseView):
    def post(self, request):
        logout(request)
        return BaseView.json_result(None, code = apis.StatusCodeExtension.success, message = None)

class account_login(BaseView):
    def get(self, request):
        template = loader.get_template('login.jinja')
        context = RequestContext(request, {'title':u'我的网店'})
        return HttpResponse(template.render(context))

    def post(self, request):
        data = json.loads(request.body)
        user_name = data['userName']
        password = data['password']

        user = authenticate(username= user_name, password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                my_app = OAuthAccessor.get_application(user)
                if my_app is None:
                    OAuthAccessor.register_application(user)
                request.session['access_token'] = OAuthAccessor.access_token(user, password)
                return BaseView.json_result(None, message=None, code=apis.StatusCodeExtension.success)
            else:
                # Return a 'disabled account' error message
                return BaseView.json_result(None, message=u'帐号没有激活', code=apis.StatusCodeExtension.fail)
        else:
            # Return an 'invalid login' error message
            return BaseView.json_result(None, message=u'帐号或密码错误', code=apis.StatusCodeExtension.fail)

def home_index(request):
    template = loader.get_template('home_index.jinja')
    return HttpResponse(template.render({'title':u'主页'}, request))

def commodity_detail(request, commodity_id):
    template = loader.get_template('commodity_detail.jinja')
    return HttpResponse(template.render({'title':u'宝贝详情'}, request))

def fill_common_info(extra_data, request):
    extra_data['ac'] = request.session['access_token']
    return extra_data

@login_required
def category_list(request):
    template = loader.get_template('admin/category_list.jinja')
    return HttpResponse(template.render(fill_common_info({'title':u'分类管理','activeNav':TabIndex.category_management}, request), request))

@login_required
def commodity_meta_list(request):
    template = loader.get_template('admin/commodity_meta_list.jinja')
    return HttpResponse(template.render(fill_common_info({'title':u'产品参数维护', 'activeNav':TabIndex.product_param_maintain}, request), request))

@login_required
def commodity_list(request):
    template = loader.get_template('admin/commodity_list.jinja')
    return HttpResponse(template.render(fill_common_info({'title':u'我的宝贝', 'activeNav':TabIndex.my_product}, request), request))

@login_required
def add_commodity(request):
    template = loader.get_template('admin/add_commodity.jinja')
    return HttpResponse(template.render(fill_common_info({'title':u'我的宝贝', 'activeNav':TabIndex.my_product}, request), request))

@login_required
def update_commodity(request, commodity_id):
    template = loader.get_template('admin/add_commodity.jinja')
    return HttpResponse(template.render(fill_common_info({'title':u'我的宝贝', 'activeNav':TabIndex.my_product, 'commodity_id':commodity_id}, request), request))

@login_required
def brand_list(request):
    template = loader.get_template('admin/brand_list.jinja')
    return HttpResponse(template.render(cfill_common_info({'title':u'品牌管理', 'activeNav':TabIndex.brand_management}, request), request))

@login_required
def discount_list(request):
    template = loader.get_template('admin/discount_list.jinja')
    return HttpResponse(template.render(fill_common_info({'title':u'营销活动', 'activeNav':TabIndex.discount_management}, request), request))

@login_required
def statistics_index(request):
    template = loader.get_template('admin/statistics_index.jinja')
    return HttpResponse(template.render(fill_common_info({'title':u'销售额汇总', 'manualSetup':True, 'activeNav':TabIndex.sale_statistics}, request), request))

@login_required
def statistics_commodity_index(request):
    template = loader.get_template('admin/statistics_commodity_index.jinja')
    return HttpResponse(template.render(fill_common_info({'title':u'单品分析', 'manualSetup':True, 'activeNav':TabIndex.sale_statistics}, request), request))

@login_required
def statistics_category_index(request):
    template = loader.get_template('admin/statistics_category_index.jinja')
    return HttpResponse(template.render(fill_common_info({'title':u'分类汇总', 'manualSetup':True, 'activeNav':TabIndex.sale_statistics}, request), request))
