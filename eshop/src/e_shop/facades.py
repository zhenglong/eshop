# -*- coding: utf-8 -*-
'''
Created on Apr 16, 2015

@author: tristan
'''

from e_shop.viewModels import CategoryViewMode, CommodityViewModel,\
    CommodityQueryModel, UploadFileViewModel, CategoryQueryViewModel,\
    CommodityMetaQueryModel, CommodityMetaViewModel,\
    CommodityCustomFieldViewModel, CommodityDetailViewModel, BrandQueryModel,\
    BrandViewModel, OAuthApplicationViewModel, UserViewModel,\
    DiscountQueryViewModel, DiscountViewModel
from e_shop.repositories import CategoryRepository, CommodityRepository, UploadFileRepository,\
    CommodityMetaRepository, BrandRepository, OAuthRepository, UserRepository,\
    DiscountRepository
from e_shop.mapper import obj_map
from e_shop.models import Category, Commodity, UploadFile, CommodityMeta,\
    CommodityCustomField, CommodityDetail, Brand, User
from datetime import datetime

class BaseFacade(object):
    def __init__(self, context):
        self._context = context
    
    def is_accessable(self, entity):
        return entity.user_id == self._context.user_id

class CategoryFacade(BaseFacade):
    def __init__(self, context):
        self._repository = CategoryRepository()
        super(CategoryFacade, self).__init__(context)
    @staticmethod
    def to_flat(items, result):
        for item in items:
            result.append(item)
            if item.children is not None and len(item.children) > 0:
                CategoryFacade.to_flat(item.children, result)
    def list(self, param=None):
        if (not param):
            param = CategoryQueryViewModel()
        else:
            param = CategoryQueryViewModel(param)
        if (param.listFlat):
            param.includeChildren = True
        param.user_id = self._context.user_id
        entities = self._repository.list(param)
        result = []
        mapper = {}
        mapper[Category] = CategoryViewMode
        if param.includeChildren:
            if param.listFlat:
                temp = []
                self.__class__.to_flat(entities, temp)
                for r in temp:
                    r.children = []
                    result.append(obj_map(r, CategoryViewMode, mapper=mapper))
            else:
                for e in entities:
                    result.append(obj_map(e, CategoryViewMode, mapper=mapper))
        else:
            for e in entities:
                e.children = []
                result.append(obj_map(e, CategoryViewMode))
        return result
    def get(self, entity_id):
        entity = self._repository.get(entity_id)
        if (entity is None) or (not self.is_accessable(entity)):
            return None
        return obj_map(entity, CategoryViewMode)
    def save(self, viewModel):
        mapper = {}
        mapper[type(viewModel)] = Category
        if viewModel.children is not None:
            c = []
            for v in viewModel.children:
                c.append(CategoryViewMode(v))
            viewModel.children = c
        entity = obj_map(viewModel, Category, mapper=mapper)
        olds = self._repository.list(CategoryQueryViewModel({'includeChildren':True, 'categoryId':viewModel.id}))
        for o in olds:
            isFound = False
            for e in entity.children:
                if o.id == e.id:
                    isFound = True
                    break
            if not isFound:
                self._repository.delete(o.id)
        children = []
        for c in entity.children:
            children.append(c)
        result = []
        for e in children:
            e.parent_category_id = entity.id
            e.parent = None
            e.user_id = self._context.user_id
            result.append(self._repository.save(e))
        return result
    def delete(self, entity_id):
        if self._repository.get(entity_id) is None:
            return
        return self._repository.delete(entity_id)

class CommodityMetaFacade(BaseFacade):
    def __init__(self, context):
        self._repository = CommodityMetaRepository()
        super(CommodityMetaFacade, self).__init__(context)
    def list(self, param = None):
        if (not param):
            param = CommodityMetaQueryModel()
        param.user_id = self._context.user_id
        entities = self._repository.list(param)
        result = []
        map(lambda e:result.append(obj_map(e, CommodityMetaViewModel, 
                                                     mapper={
                                                             CommodityCustomField:CommodityCustomFieldViewModel
                                                             })),entities)
        return result
    def get(self, entity_id):
        entity = self._repository.get(entity_id)
        if (entity is None) or (not self.is_accessable(entity)):
            return None
        
        mapper = {
                  CommodityCustomField:CommodityCustomFieldViewModel
                  }
        return obj_map(entity, CommodityMetaViewModel, mapper = mapper)
    def save(self, viewModel):
        mapper = {
                  CommodityCustomFieldViewModel:CommodityCustomField
                  }
        viewModel.fields = map(lambda v:CommodityCustomFieldViewModel(v), viewModel.fields)
        entity = obj_map(viewModel, CommodityMeta, mapper = mapper)
        if (entity.user_id > 0 and (not self.is_accessable(entity))):
            return
        entity.user_id = self._context.user_id
        return self._repository.save(entity)
    def delete(self, entity_id):
        if (self.get(entity_id) is None):
            return
        return self._repository.delete(entity_id)
    def batch_delete(self, entity_ids):
        for entity_id in entity_ids:
            if (self.get(entity_id) is None):
                return
        return self._repository.batch_delete(entity_ids)

class CommodityFacade(BaseFacade):
    def __init__(self, context):
        self._repository = CommodityRepository()
        super(CommodityFacade, self).__init__(context)
    def list(self, param = None):
        if (not param):
            param = CommodityQueryModel()
        param.user_id = self._context.user_id
        entities = self._repository.list(param)
        return map(lambda e: obj_map(e, CommodityViewModel, rules={
                                                                   'discount_price':lambda e:e.base_price,
                                                                   'brand_name': lambda e:None if e.brand is None else e.brand.name,
                                                                   'photos':None,
                                                                   'details':None
                                                                   }), entities)
    def get(self, entity_id):
        mapper={CommodityDetail: CommodityDetailViewModel}
        entity = self._repository.get(entity_id)
        if entity is None or (not self.is_accessable(entity)):
            return None
        return obj_map(entity, CommodityViewModel, rules={
                                                          'discount_price':lambda e:e.base_price,
                                                          'brand_name': lambda e:None if e.brand is None else e.brand.name,
                                                          'photos':lambda e: map(lambda f:UploadFileViewModel({'id':f.file_id}), e.uploadFiles),
                                                          'field_name':lambda e:e.field.field_name,
                                                          'field_type':lambda e:e.field.field_type,
                                                          'node':lambda e:e.field.note
                                                          }, mapper=mapper)
    def save(self, viewModel):
        mapper={CommodityDetailViewModel: CommodityDetail}
        entity = obj_map(viewModel, Commodity, mapper=mapper)
        if entity.user_id > 0 and (not self.is_accessable(entity)):
            return
        entity.user_id = self._context.user_id
        return self._repository.save(entity)
    def delete(self, entity_id):
        if self.get(entity_id) is None:
            return
        return self._repository.delete(entity_id)
    def batch_delete(self, entity_ids):
        for entity_id in entity_ids:
            if (self.get(entity_id) is None):
                return
        return self._repository.batch_delete(entity_ids)
    def shelve(self, entity_id, is_off_shelve):
        if self.get(entity_id) is None:
            return
        return self._repository.shelve(entity_id, is_off_shelve)
    def batch_shelve(self, entity_ids, is_off_shelve):
        for entity_id in entity_ids:
            if (self.get(entity_id) is None):
                return
        return self._repository.batch_shelve(entity_ids, is_off_shelve)
    def delete_file(self, commodity_id, file_id):
        if self.get(commodity_id) is None:
            return
        return self._repository.delete_file(commodity_id, file_id)
    def add_file(self, commodity_id, file_id, file_type):
        if self.get(commodity_id) is None:
            return
        return self._repository.add_file(commodity_id, file_id, file_type)

class BrandFacade(BaseFacade):
    def __init__(self, context):
        self._repository = BrandRepository()
        super(BrandFacade, self).__init__(context)
    def get(self, entity_id):
        entity = self._repository.get(entity_id)
        if (entity is None or (not self.is_accessable(entity))):
            return None
        return obj_map(entity, BrandViewModel)
    def list(self, param = None):
        if (not param):
            param = BrandQueryModel()
        param.user_id = self._context.user_id
        entities = self._repository.list(param)
        return map(lambda e: obj_map(e, BrandViewModel, rules={
                                                                   'photos':lambda e: map(lambda f:UploadFileViewModel({'id':f.id}), e.uploadFiles),
                                                                   }), entities)
    def save(self, viewModel):
        entity = obj_map(viewModel, Brand)
        if (entity.user_id > 0 and (not self.is_accessable(entity))):
            return
        return self._repository.save(entity)
    def delete(self, entity_id):
        entity = self.get(entity_id)
        if entity is None:
            return
        return self._repository.delete(entity_id)
    def delete_file(self, brand_id, file_id):
        entity = self.get(brand_id)
        if entity is None:
            return
        return self._repository.delete_file(brand_id, file_id)
    def add_file(self, brand_id, file_id, file_type):
        entity = self.get(brand_id)
        if entity is None:
            return
        return self._repository.add_file(brand_id, file_id, file_type)

class UploadFileFacade(BaseFacade):
    def __init__(self, context):
        self._repository = UploadFileRepository()
        super(UploadFileFacade, self).__init__(context)
    def get(self, entity_id):
        entity = self._repository.get(entity_id)
        if (entity is None or (not self.is_accessable(entity))):
            return None
        return obj_map(entity, UploadFileViewModel)
    def save(self, viewModel):
        entity = obj_map(viewModel, UploadFile)
        if self._context is not None:
            entity.user_id = self._context.user_id
        return self._repository.save(entity)
    def delete(self, entity_id):
        entity = self.get(entity_id)
        if entity is None:
            return
        return self._repository.delete(entity_id)

class UserFacade(BaseFacade):
    def __init__(self, context):
        self._repository = UserRepository()
        super(UserFacade, self).__init__(context)
    def get(self, entity_id):
        entity = self._repository.get(entity_id)
        if entity is None:
            return None
        return obj_map(entity, UserViewModel, rules={
                                                     'photos':lambda e: map(lambda f:obj_map(f, UploadFileViewModel), e.uploadFiles)
                                                     })
    @staticmethod
    def get_from_auth_id(auth_id):
        entity = UserRepository().get_from_auth_id(auth_id)
        if entity is None:
            return None
        return obj_map(entity, UserViewModel, rules={
                                                     'photos':lambda e: map(lambda f:obj_map(f, UploadFileViewModel), e.uploadFiles)
                                                     })
    def save(self, viewModel):
        entity = obj_map(viewModel, User)
        self._repository.save(entity)
    def add_file(self, file_id, file_type):
        entity = self.get(self._context.user_id)
        if entity is None:
            return
        return self._repository.add_file(self._context.user_id, file_id, file_type)
    def delete_all_files(self):
        entity = self.get(self._context.user_id)
        if entity is None:
            return
        return self._repository.delete_all_files(self._context.user_id)

class DiscountFacade(BaseFacade):
    def __init__(self, context):
        self._repository = DiscountRepository()
        super(DiscountFacade, self).__init__(context)
    def list(self, param = None):
        if (param == None):
            param = DiscountQueryViewModel(start_date=datetime.today())
        param.user_id = self._context.user_id
        entities = self._repository.list(param)
        return map(lambda e:obj_map(e, DiscountViewModel), entities)

class OAuthProxy(BaseFacade):
    def __init__(self):
        self._repository = OAuthRepository()
    def get(self, user_id):
        entity = self._repository.get(user_id)
        if entity is None:
            return None
        return obj_map(entity, OAuthApplicationViewModel)