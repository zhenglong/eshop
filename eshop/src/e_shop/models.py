'''
Created on Apr 3, 2015

@author: tristan
'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey, UnicodeText,
                        DECIMAL, Unicode, Boolean)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.schema import Table


Base = declarative_base()

UserUploadFile=Table('user_upload_file', Base.metadata,
                     Column('user_id', Integer, ForeignKey('user.id')),
                     Column('file_id', Integer, ForeignKey('upload_file.id')))
BrandUploadFile = Table('brand_upload_file', Base.metadata,
                        Column('brand_id', Integer, ForeignKey('brand.id')),
                        Column('file_id', Integer, ForeignKey('upload_file.id')))
DiscountCommodity = Table('discount_commodity', Base.metadata,
                          Column('discount_id', Integer, ForeignKey('discount.id')),
                          Column('commodity_id', Integer, ForeignKey('commodity.id')))


class CommodityUploadFile(Base):
    __tablename__ = 'commodity_upload_file'
    commodity_id = Column('commodity_id', Integer, ForeignKey('commodity.id'), primary_key = True)
    file_id = Column('file_id', Integer, ForeignKey('upload_file.id'), primary_key = True)
    type = Column('type', Integer)

class User(Base):
    __tablename__ = 'user'
    id=Column(Integer, primary_key=True)
    name = Column(String(50, convert_unicode=True), nullable = False)
    mobile = Column(String(50, convert_unicode=True))
    tel = Column(String(50, convert_unicode=True))
    address = Column(String(200, convert_unicode=True))
    # auth_user_id is foreign key to 'auth_user.id'
    # ignore here to avoid extra model definition
    auth_user_id = Column('auth_user_id', Integer, nullable=False) 
    uploadFiles= relationship('UploadFile', secondary=UserUploadFile)
    
class UploadFile(Base):
    __tablename__='upload_file'
    id=Column(Integer, primary_key=True)
    name = Column(String(50, convert_unicode=True), nullable = False)
    path = Column(String(200, convert_unicode=True), nullable = False)
    format = Column(String(10, convert_unicode=True))
    size=Column(Integer)
    created_date = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

class Brand(Base):
    __tablename__ = 'brand'
    id=Column(Integer, primary_key=True)
    name = Column(String(50, convert_unicode=True), nullable = False)
    company_name = Column(String(50, convert_unicode=True))
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    uploadFiles= relationship('UploadFile', secondary=BrandUploadFile)

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(50, convert_unicode=True), nullable = False)
    user_id = Column(Integer, ForeignKey('user.id'))
    parent_category_id = Column(Integer, ForeignKey('category.id'))
    children = relationship('Category', backref=backref('parent', remote_side=[id]))

class CommodityMeta(Base):
    __tablename__ = 'commodity_meta'
    id = Column(Integer, primary_key=True)
    name = Column(String(50, convert_unicode=True), nullable = False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable = False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    category = relationship('Category', backref="commodityMetas")
    fields = relationship('CommodityCustomField', backref=backref('meta', remote_side=[id]))

class CommodityCustomField(Base):
    __tablename__ = 'commodity_custom_field'
    id = Column(Integer, primary_key=True)
    field_name = Column(String(50, convert_unicode=True), nullable= False)
    field_type = Column(Integer)
    meta_id = Column(Integer, ForeignKey('commodity_meta.id'), nullable = False)
    note = Column(UnicodeText)

class Commodity(Base):
    __tablename__ = 'commodity'
    id=Column(Integer, primary_key=True)
    name = Column(String(50, convert_unicode=True), nullable=False)
    description = Column(UnicodeText())
    category_id = Column(Integer, ForeignKey('category.id'))
    base_price = Column(DECIMAL(18,2), nullable = False)
    stock = Column(Integer, nullable = False)
    is_off_shelve = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable = False)
    meta_id = Column(Integer, ForeignKey('commodity_meta.id'), nullable =False)
    brand_id = Column(Integer, ForeignKey('brand.id'))
    uploadFiles= relationship('CommodityUploadFile')
    discounts = relationship('Discount', secondary = DiscountCommodity)
    category = relationship('Category', backref="commodities")
    brand = relationship('Brand', backref="commodities")
    details = relationship('CommodityDetail', backref="commodity")

class CommodityDetail(Base):
    __tablename__ = 'commodity_detail'
    id = Column(Integer, primary_key = True)
    commodity_id = Column(Integer, ForeignKey('commodity.id'), nullable = False)
    custom_field_id = Column(Integer, ForeignKey('commodity_custom_field.id'), nullable = False)
    field = relationship('CommodityCustomField')
    value = Column(Unicode(50))

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key =True)
    id_addr = Column(String(50))
    note = Column(UnicodeText, nullable = False)
    create_at = Column(DateTime, nullable = False)
    commodity_id = Column(Integer, ForeignKey('commodity.id'), nullable = False)

class Discount(Base):
    __tablename__ = 'discount'
    id = Column(Integer, primary_key = True)
    discount = Column(DECIMAL, nullable = False)
    note = Column(Unicode(50))
    type = Column(Integer)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_all_applied = Column(Boolean)
    name = Column(Unicode(50), nullable = False)
    limit_per_user = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

###########################oauth proxy model################################
class OAuthApplication(Base):
    __tablename__ = 'oauth2_provider_application'
    id = Column(Integer, primary_key = True)
    client_id = Column(Unicode(100), nullable = False, unique = True)
    redirect_uris = Column(UnicodeText, nullable = False)
    client_type = Column(Unicode(32), nullable = False)
    authorization_grant_type= Column(Unicode(32), nullable = False)
    client_secret = Column(Unicode(255), nullable = False)
    name = Column(Unicode(255), nullable = False)
    skip_authorization = Column(Boolean, nullable = False)
    user_id = Column(Integer, ForeignKey('auth_user.id'), nullable = False)
############################################################################