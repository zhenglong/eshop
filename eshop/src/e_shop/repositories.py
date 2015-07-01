# -*- coding: utf-8 -*-
'''
Created on Apr 13, 2015

@author: tristan
'''
from e_shop.session import Session 
from e_shop.models import Category, Commodity, UploadFile, CommodityMeta,\
    CommodityUploadFile, Discount, Brand, OAuthApplication, User

class BaseRepository(object):
    def __init__(self, *args, **kwargs):
        self._session = Session()

class CategoryRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super(CategoryRepository, self).__init__(*args, **kwargs)
    def list(self, param):
        result = self._session.query(Category)
        result = result.filter_by(parent_category_id=param.categoryId)
        if (param.user_id > 0):
            result = result.filter_by(user_id=param.user_id)
        return result.all()
    def get(self, entity_id):
        return self._session.query(Category).get(entity_id)
    def save(self, entity):
        self._session.begin(subtransactions=True)
        try:
            if (not entity.id or int(entity.id) < 1):
                entity.id = None # it's important to set primary key to None here
                self._session.add(entity)
            else:
                entityInDb=self._session.query(Category).get(entity.id)
                if entityInDb.name <> entity.name:
                    entityInDb.name = entity.name
            self._session.commit()
            return entity.id
        except:
            self._session.rollback()
            raise
    def delete(self, entity_id):
        self._session.begin(subtransactions=True)
        try:
            self._session.delete(self._session.query(Category).get(entity_id))
            self._session.commit()
        except:
            self._session.rollback()
            raise

class CommodityMetaRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super(CommodityMetaRepository, self).__init__(*args, **kwargs)
    def list(self, param):
        query = self._session.query(CommodityMeta);
        if (param.keyword):
            query = query.filter(CommodityMeta.name.contains(param.keyword))
        if (param.category_id):
            query = query.filter(CommodityMeta.category_id == param.category_id)
        if (param.user_id > 0):
            query = query.filter(CommodityMeta.user_id == param.user_id)
        result = query.all()
        if not param.includeFields:
            for v in result:
                v.fields = []
        return result
    def get(self, entity_id):
        return self._session.query(CommodityMeta).get(entity_id)
    def save(self, entity):
        self._session.begin(subtransactions=True)
        try:
            if (not entity.id or int(entity.id) < 1): 
                entity.id = None
                self._session.add(entity)
            else:
                old = self._session.query(CommodityMeta).get(entity.id)
                old.name = entity.name
                old.category_id = entity.category_id
                deleted = []
                for o in old.fields:
                    found = False
                    for n in entity.fields:
                        if o.id == n.id:
                            found = True
                            o.field_name = n.field_name
                            o.field_type = n.field_type
                            o.note = n.note
                            entity.fields.remove(n)
                            break
                    if not found:
                        deleted.append(o)
                for d in deleted:
                    self._session.delete(d)
                added = map(lambda f:f, entity.fields)
                for a in added:
                    if not a.id or a.id < 1:
                        a.meta = None
                        a.meta_id = entity.id
                        self._session.add(a)
            self._session.commit()
            return entity.id
        except:
            self._session.rollback()
            raise
    def delete(self, entity_id):
        self._session.begin(subtransactions=True)
        try:
            entity = self._session.query(CommodityMeta).get(entity_id)
            for c in entity.fields:
                self._session.delete(c)
            self._session.delete(entity)
            self._session.commit()
        except:
            self._session.rollback()
            raise
    def batch_delete(self, entity_ids):
        for entity_id in entity_ids:
            self.delete(entity_id)

class CommodityRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super(CommodityRepository, self).__init__(*args, **kwargs)
    def list(self, param):
        '''
        query by keyword, category
        '''
        query = self._session.query(Commodity).filter(Commodity.is_off_shelve == param.is_off_shelve);
        if (param.keyword):
            query = query.filter(Commodity.name.contains(param.keyword))
        if (param.category_id):
            query = query.filter(Commodity.category_id == param.category_id)
        if param.user_id > 0:
            query = query.filter(Commodity.user_id == param.user_id)
        return query.all()
    def get(self, entity_id):
        return self._session.query(Commodity).get(entity_id)
    def save(self, entity):
        self._session.begin(subtransactions=True)
        try:
            if (not entity.id or int(entity.id) < 1): 
                entity.id = None
                self._session.add(entity)
            else:
                old = self._session.query(Commodity).get(entity.id)
                old.name = entity.name
                old.description = entity.description
                old.category_id = entity.category_id
                old.base_price = entity.base_price
                old.stock = entity.stock
                isMetaChanged = old.meta_id != entity.meta_id 
                old.meta_id = entity.meta_id
                old.brand_id = entity.brand_id
                if isMetaChanged:
                    #delete all the commodity details and insert new ones
                    while len(old.details)>0:
                        self._session.delete(old.details.pop())
                    for d in map(lambda d:d, entity.details):
                        d.commodity_id = old.id
                        d.commodity=None
                        self._session.add(d)
                else:
                    #update all the commodity details
                    for o in old.details:
                        for n in entity.details:
                            if o.custom_field_id == n.custom_field_id:
                                o.value = n.value
                                entity.details.remove(n)
                                break
            self._session.commit()
            return entity.id
        except:
            self._session.rollback()
            raise
    def delete(self, entity_id):
        self._session.begin(subtransactions=True)
        file_names = []
        try:
            entity = self._session.query(Commodity).get(entity_id)
            # delete details
            while(len(entity.details)>0):
                self._session.delete(entity.details.pop())
            # delete files 
            file_ids = self.delete_file(entity_id)
            for file_id in file_ids:
                file_names.append(UploadFileRepository().delete(file_id))
            # delete itself
            self._session.delete(entity)
            self._session.commit()
            return file_names
        except:
            self._session.rollback()
            raise
    def batch_delete(self, entity_ids):
        file_names=[]
        for entity_id in entity_ids:
            temp = self.delete(entity_id)
            file_names = file_names + temp
        return file_names
    def shelve(self, entity_id, is_off_shelve):
        self._session.begin(subtransactions=True)
        try:
            entity = self._session.query(Commodity).get(entity_id)
            entity.is_off_shelve = is_off_shelve
            self._session.commit()
        except:
            self._session.rollback()
            raise
    def batch_shelve(self, entity_ids, is_off_shelve):
        for entity_id in entity_ids:
            self.shelve(entity_id, is_off_shelve)
    def delete_file(self, commodity_id, file_id = 0):
        self._session.begin(subtransactions=True)
        try:
            file_ids = []
            entities = self._session.query(CommodityUploadFile).filter(CommodityUploadFile.commodity_id == commodity_id)
            if file_id > 0:
                entities = entities.filter(CommodityUploadFile.file_id == file_id)
            for entity in entities:
                file_ids.append(entity.file_id)
                self._session.delete(entity)
            self._session.commit()
            return file_ids
        except:
            self._session.rollback()
            raise
    def add_file(self, commodity_id, file_id, file_type):
        self._session.begin(subtransactions=True)
        try:
            entity = CommodityUploadFile()
            entity.commodity_id = commodity_id
            entity.file_id = file_id
            entity.type = file_type
            self._session.add(entity)
            self._session.commit()
        except:
            self._session.rollback()
            raise
class BrandRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super(BrandRepository, self).__init__(*args, **kwargs)
    def get(self, entity_id):
        return self._session.query(Brand).get(entity_id)
    def list(self, param):
        query = self._session.query(Brand);
        if (param.name):
            query = query.filter(Brand.name.contains(param.name) or Brand.company_name.contains(param.name))
        if (param.user_id > 0):
            query = query.filter(Brand.user_id == param.user_id)
        return query.all()
    def save(self, entity):
        self._session.begin(subtransactions=True)
        try:
            if (not entity.id or int(entity.id) < 1): 
                entity.id = None
                self._session.add(entity)
            else:
                old = self._session.query(Brand).get(entity.id)
                old.name = entity.name
                old.company_name = entity.company_name
            self._session.commit()
            return entity.id
        except:
            self._session.rollback()
            raise
    def delete(self, entity_id):
        self._session.begin(subtransactions=True)
        file_names = []
        try:
            entity = self._session.query(Brand).get(entity_id)
            # delete files 
            file_ids = self.delete_file(entity_id)
            for file_id in file_ids:
                file_names.append(UploadFileRepository().delete(file_id))
            # delete itself
            self._session.delete(entity)
            self._session.commit()
            return file_names
        except:
            self._session.rollback()
            raise
    def add_file(self, brand_id, file_id, file_type):
        self._session.begin(subtransactions=True)
        try:
            brand = self.get(brand_id)
            brand.uploadFiles.append(UploadFileRepository().get(file_id))
            self._session.commit()
        except:
            self._session.rollback()
            raise
    def delete_file(self, brand_id, file_id = 0):
        self._session.begin(subtransactions=True)
        try:
            brand = self.get(brand_id)
            file_ids = []
            if file_id>0:
                f = UploadFileRepository().get(file_id)
                brand.uploadFiles.remove(f)
                file_ids.append(file_id)
            else:
                while(len(brand.uploadFiles) >0):
                    f = brand.uploadFiles.pop()
                    file_ids.append(f.id)
            self._session.commit()
            return file_ids
        except:
            self._session.rollback()
            raise
    
class UploadFileRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super(UploadFileRepository, self).__init__(*args, **kwargs)
    def get(self, entity_id):
        return self._session.query(UploadFile).get(entity_id)
    def save(self, entity):
        self._session.begin(subtransactions=True)
        try:
            if (not entity.id or entity.id < 1):
                entity.id= None
                self._session.add(entity)
            else:
                pass # shouldn't be here
            self._session.commit()
            return entity.id
        except:
            self._session.rollback()
            raise
    def delete(self, entity_id):
        self._session.begin(subtransactions=True)
        try:
            entity = self._session.query(UploadFile).get(entity_id)
            self._session.delete(entity)
            self._session.commit()
            return entity.name
        except:
            self._session.rollback()
            raise

class DiscountRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super(DiscountRepository, self).__init__(*args, **kwargs)
    def get(self, entity_id):
        return self._session.query(Discount).get(entity_id)
    def list(self, param):
        query = self._session.query(Discount);
        if (param.start_date is not None):
            query = query.filter(Discount.start_date <= query.start_date)
        if (param.end_date is not None):
            query = query.filter(Discount.end_date is None or Discount.end_date <= param.end_date)
        return query.all()
    def save(self, entity):
        self._session.begin(subtransactions=True)
        try:
            if (not entity.id or entity.id < 1):
                entity.id= None
                self._session.add(entity)
            else:
                old = self._session.query(Discount).get(entity.id)
                old.discount = entity.discount
                old.note = entity.note
                old.type = entity.type
                old.start_date = entity.start_date
                old.end_date = entity.end_date
                old.is_all_applied=entity.is_all_applied
                old.name = entity.name
                old.limit_per_user = entity.limit_per_user
            self._session.commit()
            return entity.id
        except:
            self._session.rollback()
            raise
    def delete(self, entity_id):
        self._session.begin(subtransactions=True)
        try:
            self._session.delete(self._session.query(UploadFile).get(entity_id))
            self._session.commit()
        except:
            self._session.rollback()
            raise

class UserRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super(UserRepository, self).__init__(*args, **kwargs)
    def get(self, entity_id):
        return self._session.query(User).get(entity_id)
    def get_from_auth_id(self, auth_id):
        return self._session.query(User).filter(User.auth_user_id == auth_id).first()
    def save(self, entity):
        self._session.begin(subtransactions=True)
        try:
            if (not entity.id or entity.id < 1):
                entity.id= None
                self._session.add(entity)
            else:
                old = self._session.query(User).get(entity.id)
                if old.auth_user_id != entity.auth_user_id:
                    return
                old.name = entity.name
                old.mobile = entity.mobile
                old.tel = entity.tel
                old.address = entity.address
            self._session.commit()
            return entity.id
        except:
            self._session.rollback()
    def add_file(self, user_id, file_id, file_type):
        self._session.begin(subtransactions=True)
        try:
            user = self.get(user_id)
            user.uploadFiles.append(UploadFileRepository().get(file_id))
            self._session.commit()
        except:
            self._session.rollback()
            raise

class OAuthRepository(BaseRepository):
    def __init__(self, *args, **kwargs):
        super(OAuthRepository, self).__init__(*args, **kwargs)
    
    def get(self, user_id):
        return self._session.query(OAuthApplication).filter(OAuthApplication.user_id == user_id).first()