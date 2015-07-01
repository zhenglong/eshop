# -*- coding: utf-8 -*-
'''
Created on Apr 16, 2015

@author: tristan
'''

from rest_framework.serializers import Serializer, CharField
from rest_framework.fields import IntegerField, DecimalField,\
    DateTimeField

class RecursiveField(Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context = self.context)
        return serializer.data

class CategorySerializer(Serializer):
    name = CharField(max_length=50)
    id = IntegerField()
    children = RecursiveField(many = True)

class CommodityDetailSerializer(Serializer):
    id = IntegerField()
    commodity_id = IntegerField()
    custom_field_id = IntegerField()
    field_name = CharField(max_length=50)
    field_type = IntegerField()
    note = CharField(max_length=200)
    value = CharField(max_length=50)

class UploadFileSerializer(Serializer):
    id=IntegerField()
    name=CharField(max_length=50)
    path=CharField(max_length=200)
    format=CharField(max_length=10)
    size=IntegerField()
    created_date = DateTimeField()
    thumbnail = CharField(max_length=200)

class CommoditySerializer(Serializer):
    id=IntegerField()
    name = CharField(max_length=50)
    base_price = DecimalField(19, 10)
    discount_price = DecimalField(19, 10)
    brand_id = IntegerField()
    brand_name = CharField(max_length=50)
    stock = IntegerField()
    meta_id = IntegerField()
    category_id = IntegerField()
    description = CharField()
    details = CommodityDetailSerializer(many = True)
    photos = UploadFileSerializer(many = True)

class BrandSerializer(Serializer):
    id=IntegerField()
    name = CharField(max_length=50)
    company_name = CharField(max_length=50)
    photos = UploadFileSerializer(many = True)

class CommodityCustomFieldSerializer(Serializer):
    id = IntegerField()
    field_name = CharField(max_length=50)
    field_type = IntegerField()
    meta_id = IntegerField()
    note = CharField(max_length=500)

class CommodityMetaSerializer(Serializer):
    id=IntegerField()
    name = CharField(max_length=50)
    category_id = IntegerField()
    fields = CommodityCustomFieldSerializer(many = True)
    
class UserSerializer(Serializer):
    id = IntegerField()
    name = CharField(max_length=50)
    mobile = CharField(max_length=50)
    tel = CharField(max_length=50)
    address = CharField(max_length=200)

class AjaxResultSerializer(Serializer):
    data = CharField()
    code = IntegerField()
    message = CharField()