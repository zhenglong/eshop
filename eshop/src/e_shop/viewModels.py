'''
Created on Apr 16, 2015

@author: tristan
'''

class BaseViewModel(object):
    def __init__(self):
        self.user_id = None

class CategoryViewMode(BaseViewModel):
    def __init__(self, *args):
        self.name = None
        self.id = None
        self.children = list()
        super(CategoryViewMode, self).__init__()
        self.__dict__.update(*args)

class CategoryQueryViewModel(BaseViewModel):
    def __init__(self, *args):
        self.includeChildren = False
        self.listFlat = False
        self.categoryId = None
        super(CategoryQueryViewModel, self).__init__()
        self.__dict__.update(*args)

class CommodityDetailViewModel(BaseViewModel):
    def __init__(self, *args):
        self.id = None
        self.commodity_id = None
        self.custom_field_id = None
        self.field_name = None
        self.field_type = None
        self.note = None
        self.value = None
        super(CommodityDetailViewModel, self).__init__()
        self.__dict__.update(*args)

class CommodityViewModel(BaseViewModel):
    def __init__(self, *args):
        self.id = None
        self.name = None
        self.base_price = None
        self.discount_price = None
        self.brand_id = None
        self.brand_name = None
        self.stock = None
        self.meta_id = None
        self.category_id = None
        self.photos = None
        self.description = None
        self.details = None
        super(CommodityViewModel, self).__init__()
        self.__dict__.update(*args)
        if self.details is not None:
            self.details = map(lambda d:CommodityDetailViewModel(d), self.details)

class CommodityQueryModel(object):
    def __init__(self, *args):
        self.keyword = None
        self.category_id = None
        self.is_off_shelve = False
        super(CommodityQueryModel, self).__init__()
        self.__dict__.update(*args)

class CommodityMetaViewModel(BaseViewModel):
    def __init__(self, *args):
        self.id = None
        self.name = None
        self.category_id = None
        self.fields = None
        super(CommodityMetaViewModel, self).__init__()
        self.__dict__.update(*args)

class CommodityCustomFieldViewModel(BaseViewModel):
    def __init__(self, *args):
        self.id = None
        self.field_name = None
        self.field_type = None
        self.note = None
        self.meta_id = None
        self.index = None
        super(CommodityCustomFieldViewModel, self).__init__()
        self.__dict__.update(*args)

class CommodityMetaQueryModel(object):
    def __init__(self, *args):
        self.keyword = None
        self.category_id = None
        self.includeFields = False
        super(CommodityMetaQueryModel, self).__init__()
        self.__dict__.update(*args)

class BrandViewModel(object):
    def __init__(self, *args):
        self.id = None
        self.name = None
        self.company_name = None
        self.photos = None
        super(BrandViewModel, self).__init__()
        self.__dict__.update(*args)

class BrandQueryModel(BaseViewModel):
    def __init__(self, *args):
        self.name = None
        super(BrandQueryModel, self).__init__()
        self.__dict__.update(*args)
    

class UploadFileViewModel(BaseViewModel):
    def __init__(self, *args):
        self.id = None
        self.name = None
        self.path = None
        self.format = None
        self.size = None
        self.created_date = None
        self.thumbnail = None
        super(UploadFileViewModel, self).__init__()
        self.__dict__.update(*args)

class DiscountViewModel(BaseViewModel):
    def __init__(self, *args):
        self.id = None
        self.name = None
        self.start_date= None
        self.end_date = None
        self.type = None
        self.discount = None
        self.limit_per_user = None
        self.is_all_applied = None
        super(DiscountViewModel, self).__init__()
        self.__dict__.update(*args)

class DiscountQueryViewModel(BaseViewModel):
    def __init__(self, *args):
        self.start_date = None
        self.end_date = None
        super(DiscountQueryViewModel, self).__init__()
        self.__dict__.update(*args)

class UserViewModel(object):
    def __init__(self, *args):
        self.id = None
        self.name = None
        self.mobile = None
        self.tel = None
        self.address = None
        self.auth_user_id = None
        self.photo = None
        self.__dict__.update(*args)

class OAuthApplicationViewModel(BaseViewModel):
    def __init__(self, *args):
        self.client_id = None
        self.client_secret = None
        super(OAuthApplicationViewModel, self).__init__()
        self.__dict__.update(*args)

class ApplicationContext(object):
    def __init__(self, *args):
        self.user_id = None
        self.__dict__.update(*args)