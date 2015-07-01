'''
Created on Apr 19, 2015

@author: tristan
'''
from django.conf.urls import patterns, url
import apis

urlpatterns = patterns('',
    url(r'^categories/', apis.category_list.as_view()),
    url(r'^category/', apis.category_save.as_view()),
    url(r'^commodity-metas/', apis.commodity_meta_list.as_view()),
    url(r'^commodity-meta/(?P<meta_id>\d+)',apis.commodity_meta_get.as_view()),
    url(r'^commodity-meta/delete/', apis.commodity_meta_delete.as_view()),
    url(r'^commodity-meta/batch-delete/', apis.commodity_meta_batch_delete.as_view()),
    url(r'^commodity-meta/', apis.commodity_meta_save.as_view()),
    url(r'^commodities/', apis.commodity_list.as_view()),
    url(r'^commodity/(?P<commodity_id>\d+)', apis.commodity_get.as_view()),
    url(r'^commodity/delete/', apis.commodity_delete.as_view()),
    url(r'^commodity/batch-delete/', apis.commodity_batch_delete.as_view()),
    url(r'^commodity/shelve/', apis.commodity_shelve.as_view()),
    url(r'^commodity/batch-shelve/', apis.commodity_batch_shelve.as_view()),
    url(r'^commodity/delete-file/', apis.file_delete_from_commodity.as_view()),
    url(r'^commodity/add-file/', apis.file_upload_from_commodity.as_view()),
    url(r'^commodity/', apis.commodity_save.as_view()),
    url(r'^brands/', apis.brand_list.as_view()),
    url(r'^brand/delete/', apis.brand_delete.as_view()),
    url(r'^brand/delete-file/', apis.file_delete_from_brand.as_view()),
    url(r'^brand/add-file/', apis.file_upload_from_brand.as_view()),
    url(r'^brand/', apis.brand_save.as_view()),
    url(r'^discounts/', apis.discount_list.as_view()),
    url(r'^discount/', apis.discount_save.as_view()),
    url(r'^get/(?P<file_id>\d+)', apis.file_get.as_view()),
    url(r'^file/(?P<file_id>\d+)', apis.file_data.as_view()),
    url(r'^file/upload-from-ckeditor/', apis.file_upload_from_ckeditor.as_view()),
    url(r'^user-profile/upload-photo/', apis.file_upload_from_user.as_view()),
    url(r'^user-profile/', apis.user_profile.as_view())
)