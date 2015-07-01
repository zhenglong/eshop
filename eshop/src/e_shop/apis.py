# -*- coding: utf-8 -*-
'''
Created on Apr 16, 2015

@author: tristan
'''
from rest_framework.views import APIView
from rest_framework.response import Response
import facades,serializers
from e_shop.viewModels import CommodityQueryModel, UploadFileViewModel,\
    CategoryViewMode, CommodityMetaQueryModel,\
    CommodityMetaViewModel, CommodityViewModel, BrandViewModel, BrandQueryModel,\
    ApplicationContext, UserViewModel
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from rest_framework import status,permissions
from datetime import datetime
import os
from rest_framework.renderers import JSONRenderer
from e_shop.renders import PNGRenderer, JPEGRenderer
from PIL import Image
from PIL.Image import ANTIALIAS
from StringIO import StringIO
from abc import ABCMeta, abstractmethod
from django.http.response import HttpResponse
from e_shop.utility import to_bool
from oauth2_provider.ext.rest_framework.authentication import OAuth2Authentication
from oauth2_provider.ext.rest_framework.permissions import TokenHasReadWriteScope

class StatusCodeExtension(object):
    success = 280
    fail = 281
    warning = 282

class FileType(object):
    commodity = 10
    brand = 20
    user = 30
    
class FacadeFactory(object):
    def __init__(self, user):
        self._ctx = None
        if user is not None:
            my_user = facades.UserFacade.get_from_auth_id(user.id)
            if my_user is not None:
                self._ctx = ApplicationContext({'user_id' : my_user.id})
    def get_obj(self, facade_cls):
        return facade_cls(self._ctx)
class BaseApiView(APIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    required_scopes = []
    #parse_classes = (JSONParser)
    def ajax_result(self, data, code=StatusCodeExtension.success, message=''):
        data = JSONRenderer().render(data)
        serializer = serializers.AjaxResultSerializer({
                'data':unicode(data, 'utf-8'),
                'code':code,
                'message':message
                })
        return Response(serializer.data)

class user_profile(BaseApiView):
    def get(self, request):
        data = facades.UserFacade.get_from_auth_id(request.user.id)
        serializer = serializers.UserSerializer(data)
        return self.ajax_result(serializer.data)
    def post(self, request):
        vm = UserViewModel(request.data)
        vm.auth_user_id = request.user.id
        data = FacadeFactory(request.user).get_obj(facades.UserFacade).save(vm)
        return self.ajax_result(data, message = u'成功保存')

class category_list(BaseApiView):
    def get(self, request):
        categories = FacadeFactory(request.user).get_obj(facades.CategoryFacade).list(request.query_params)
        serializer = serializers.CategorySerializer(categories, many=True)
        return self.ajax_result(serializer.data)

class category_save(BaseApiView):
    def post(self, request):
        data = FacadeFactory(request.user).get_obj(facades.CategoryFacade).save(CategoryViewMode(request.data))
        return self.ajax_result(data, message = u'成功保存')

class commodity_meta_list(BaseApiView):
    def get(self, request):
        commodityMetas = FacadeFactory(request.user).get_obj(facades.CommodityMetaFacade).list(CommodityMetaQueryModel(request.query_params))
        serializer = serializers.CommodityMetaSerializer(commodityMetas, many=True)
        return self.ajax_result(serializer.data)

class commodity_meta_get(BaseApiView):
    def get(self, request, meta_id):
        meta = FacadeFactory(request.user).get_obj(facades.CommodityMetaFacade).get(meta_id)
        serializer = serializers.CommodityMetaSerializer(meta)
        return self.ajax_result(serializer.data)

class commodity_meta_save(BaseApiView):
    def post(self, request):
        data = FacadeFactory(request.user).get_obj(facades.CommodityMetaFacade).save(CommodityMetaViewModel(request.data))
        return self.ajax_result(data, message = u'成功保存')

class commodity_meta_delete(BaseApiView):
    def post(self, request):
        data = FacadeFactory(request.user).get_obj(facades.CommodityMetaFacade).delete(request.data)
        return self.ajax_result(data, message=u'删除成功')

class commodity_meta_batch_delete(BaseApiView):
    def post(self, request):
        data = FacadeFactory(request.user).get_obj(facades.CommodityMetaFacade).batch_delete(request.data)
        return self.ajax_result(data, message = u'批量删除成功')

class commodity_list(BaseApiView):
    def get(self, request):
        params = CommodityQueryModel(request.query_params)
        params.is_off_shelve = to_bool(params.is_off_shelve[0])
        commodities = FacadeFactory(request.user).get_obj(facades.CommodityFacade).list(params)
        serializer = serializers.CommoditySerializer(commodities, many=True)
        return self.ajax_result(serializer.data)

class commodity_save(BaseApiView):
    def post(self, request):
        viewModel= CommodityViewModel(request.data)
        data = FacadeFactory(request.user).get_obj(facades.CommodityFacade).save(viewModel)
        if viewModel.photos is not None and len(viewModel.photos)>0:
            file_type = FileType.commodity
            for file_id in viewModel.photos:
                FacadeFactory(request.user).get_obj(facades.CommodityFacade).add_file(data, file_id, file_type)
        return self.ajax_result(data, message=u'保存成功')

class commodity_get(BaseApiView):
    def get(self, request, commodity_id):
        entity = FacadeFactory(request.user).get_obj(facades.CommodityFacade).get(commodity_id)
        for p in entity.photos:
                p.thumbnail = '/api/file/' + str(p.id)
        serializer = serializers.CommoditySerializer(entity)
        return self.ajax_result(serializer.data)

class commodity_delete(BaseApiView):
    def post(self, request):
        file_names = FacadeFactory(request.user).get_obj(facades.CommodityFacade).delete(request.data)
        for file_name in file_names:
            default_storage.delete(file_name)
        return self.ajax_result(None, message=u'删除成功')

class commodity_batch_delete(BaseApiView):
    def post(self, request):
        file_names = FacadeFactory(request.user).get_obj(facades.CommodityFacade).batch_delete(request.data)
        for file_name in file_names:
            default_storage.delete(file_name)
        return self.ajax_result(None, message=u'批量删除成功')

class commodity_shelve(BaseApiView):
    def post(self, request):
        entity_id = request.data.get('commodity_id', 0)
        is_off_shelve = request.data.get('is_off_shelve', False)
        FacadeFactory(request.user).get_obj(facades.CommodityFacade).shelve(entity_id, is_off_shelve)
        return self.ajax_result(None, message=u'下架成功')

class commodity_batch_shelve(BaseApiView):
    def post(self, request):
        entity_ids = request.data.get('commodity_ids', [])
        is_off_shelve = to_bool(request.data.get('is_off_shelve', ''))
        entity_ids = map(lambda c:int(c), entity_ids)
        FacadeFactory(request.user).get_obj(facades.CommodityFacade).batch_shelve(entity_ids, is_off_shelve)
        return self.ajax_result(None, message=u'批量下架成功')

class brand_list(BaseApiView):
    def get(self, request):
        params = BrandQueryModel(request.query_params)
        brands = FacadeFactory(request.user).get_obj(facades.BrandFacade).list(params)
        for b in brands:
            for p in b.photos:
                    p.thumbnail = '/api/file/' + str(p.id)
        serializer = serializers.BrandSerializer(brands, many=True)
        return self.ajax_result(serializer.data)

class brand_delete(BaseApiView):
    def post(self, request):
        file_names = FacadeFactory(request.user).get_obj(facades.BrandFacade).delete(request.data)
        for file_name in file_names:
            default_storage.delete(file_name)
        return self.ajax_result(None, message=u'删除成功')

class brand_save(BaseApiView):
    def post(self, request):
        viewModel= BrandViewModel(request.data)
        data = FacadeFactory(request.user).get_obj(facades.BrandFacade).save(viewModel)
        if viewModel.photos is not None and len(viewModel.photos)>0:
            file_type = FileType.brand
            for file_id in viewModel.photos:
                FacadeFactory(request.user).get_obj(facades.BrandFacade).add_file(data, file_id, file_type)
        return self.ajax_result(data, message=u'保存成功')


class discount_list(BaseApiView):
    def get(self, request):
        return self.ajax_result([{
                                    'id':1,
                                    'name':u'元旦促销',
                                    'start_date':datetime(2015,1,1),
                                    'end_date':datetime(2015,1,3),
                                    'note':u'元旦真快乐',
                                    'discount':0.8
                                  },{
                                    'id':2,
                                    'name':u'妇女节促销',
                                    'start_date':datetime(2015,3,8),
                                    'end_date':datetime(2015,3,8),
                                    'note':u'妇女节促销真快乐',
                                    'discount':0.4
                                  },{
                                    'id':3,
                                    'name':u'儿童节促销',
                                    'start_date':datetime(2015,6,1),
                                    'end_date':datetime(2015,6,1),
                                    'note':u'儿童节促销真快乐',
                                    'discount':0.75
                                  },{
                                    'id':4,
                                    'name':u'国庆节促销',
                                    'start_date':datetime(2015,10,1),
                                    'end_date':datetime(2015,10,6),
                                    'note':u'国庆节促销真快乐',
                                    'discount':0.9,
                                    'is_all_applied':True,
                                    'limit_per_user':3
                                  },{
                                    'id':5,
                                    'name':u'双十节促销',
                                    'start_date':datetime(2015,10,10),
                                    'end_date':datetime(2015,10,10),
                                    'note':u'双十节促销真快乐',
                                    'discount':0.95
                                  }])

class discount_save(BaseApiView):
    def post(self):
        return self.ajax_result(None, message=u'not implemented')

class file_upload(BaseApiView):
    __metaclass__ = ABCMeta
    @abstractmethod
    def do_action(self, request, object_id, file_id):
        pass
    def do_pre_upload(self, request):
        pass
    def do_upload(self, request, file_name=u'files[]'):
        self.do_pre_upload()
        temp_file = request.FILES[file_name]
        wrapped_file = UploadedFile(temp_file)
        name = default_storage.save(None, wrapped_file)
        extension = os.path.splitext(name)[1]
        view_model = UploadFileViewModel({'name': name, 
                                         'size': default_storage.size(name),
                                         'format': extension, 
                                         'created_date': datetime.now()})
        file_id = FacadeFactory(request.user).get_obj(facades.UploadFileFacade).save(view_model)
        return file_id
    def get_object_id(self, request):
        return int(request.query_params.get('object_id', 0))
    def post(self, request):
        if request.FILES == None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        object_id = self.get_object_id(request)
        file_id = self.do_upload(request)
        self.do_action(request, object_id, file_id)
        serialier = serializers.UploadFileSerializer(UploadFileViewModel({'id':file_id, 'thumbnail':'/api/file/'+str(file_id)}))
        return self.ajax_result(serialier.data, 
                                message=u'操作成功:'+str(file_id))

class file_get(BaseApiView):
    def get(self, request, file_id):
        view_model = FacadeFactory(request.user).get_obj(facades.UploadFileFacade).get(file_id)
        view_model.path = '/api/file/'+str(view_model.id)
        serializer = serializers.UploadFileSerializer(view_model)
        return self.ajax_result(serializer.data, message=u'操作成功')

class file_data(BaseApiView):
    renderer_classes = (PNGRenderer,JPEGRenderer)
    def get(self, request, file_id):
        view_model = FacadeFactory(request.user).get_obj(facades.UploadFileFacade).get(file_id)
        #data = default_storage.open(view_model.name, 'rb')
        im = Image.open(default_storage.path(view_model.name))
        size = int(request.query_params.get('width', im.size[0])),int(request.query_params.get('height', im.size[1]))
        im.thumbnail(size, ANTIALIAS)
        sio = StringIO()
        im.save(sio, 'JPEG')
        data = sio.getvalue()
        sio.close()
        return Response(data, content_type=file_data.media_type(view_model.format))
    @staticmethod
    def media_type(fmt):
        if (not fmt):
            return 'application/octet-stream'
        fmt = fmt.lower()
        mapper = {
                  '.png':'image/png',
                  '.jpg':'image/jpeg',
                  '.jpeg':'image/jpeg'
                  }
        if mapper.has_key(fmt):
            return mapper[fmt]
        else:
            return 'application/octet-stream'

class file_delete(BaseApiView):
    __metaclass__ = ABCMeta
    def do_delete_file(self, request):
        file_id = int(request.data.get('file_id', 0))
        if file_id == 0:
            return Response(u'文件不存在', status=status.HTTP_404_NOT_FOUND)
        facade = FacadeFactory(request.user).get_obj(facades.UploadFileFacade)
        file_obj = facade.get(file_id)
        facade.delete(file_id)
        default_storage.delete(file_obj.name)
    @abstractmethod
    def do_action(self, request, object_id):
        pass
    def post(self, request):
        object_id = int(request.query_params.get('object_id', 0))
        self.do_action(request, object_id)
        self.do_delete_file(request)
        return self.ajax_result(None, message=u'操作成功')

class file_upload_from_commodity(file_upload):
    def do_action(self, request, object_id, file_id):
        if object_id>0:
            file_type = FileType.commodity
            FacadeFactory(request.user).get_obj(facades.CommodityFacade).add_file(object_id, file_id, file_type)

class file_upload_from_brand(file_upload):
    def do_action(self, request, object_id, file_id):
        if object_id>0:
            file_type = FileType.brand
            FacadeFactory(request.user).get_obj(facades.BrandFacade).add_file(object_id, file_id, file_type)

class file_upload_from_ckeditor(file_upload):
    def do_action(self, request, commodity_id, file_id):
        file_upload.do_action(self, request, commodity_id, file_id)
    def post(self, request):
        funcNum = request.query_params.get('CKEditorFuncNum')
        result = self.do_upload(request, file_name=u'upload')
        url = u'/api/file/'+str(result)
        return HttpResponse(u'<html><head></head><body><script type="text/javascript"> window.parent.CKEDITOR.tools.callFunction('+ funcNum + u', \''+ url + u'\', \'上传成功\');</script></body></html>', )
    
class file_upload_from_user(file_upload):
    def do_pre_upload(self, request):
        user = facades.UserFacade.get_from_auth_id(request.user.user_id)
        facade = FacadeFactory(request.user).get_obj(facades.UploadFileFacade)
        file_obj = user.uploadFiles.first()
        if file_obj is None:
            return
        facade.delete(file_obj.id)
        default_storage.delete(file_obj.name)
    def get_object_id(self, request):
        return facades.UserFacade.get_from_auth_id(request.user.id).id
    def do_action(self, request, object_id, file_id):
        if object_id < 1:
            return
        file_type = FileType.user
        FacadeFactory(request.user).get_obj(facades.UserFacade).add_file(file_id, file_type)

class file_delete_from_commodity(file_delete):
    def do_action(self, request, object_id):
        file_id = request.data.get('file_id',0)
        if object_id > 0:
            FacadeFactory(request.user).get_obj(facades.CommodityFacade).delete_file(object_id, file_id)

class file_delete_from_brand(file_delete):
    def do_action(self, request, object_id):
        file_id = request.data.get('file_id',0)
        if object_id > 0:
            FacadeFactory(request.user).get_obj(facades.BrandFacade).delete_file(object_id, file_id)
