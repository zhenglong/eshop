from django.conf.urls import patterns, include, url
import views
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'e_shop.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home_index, name='index'),
    url(r'^commodity-detail/(?P<commodity_id>\d+)/$', views.commodity_detail, name='commodity_detail'),
    url(r'^account/login/$', views.account_login.as_view(), name='account_login'),
    url(r'^account/logout/$', views.account_logout.as_view(), name='account_logout'),
    url(r'^account/user-profile/$', views.user_profile.as_view(), name='user_profile'),
    url(r'^account/register/$', views.account_register.as_view(), name='account_register'),
    url(r'^manage/commodity/(?P<commodity_id>\d+)/$', views.update_commodity, name='update_commodity'),
    url(r'^manage/commodity/', views.add_commodity, name='add_commodity'),
    url(r'^manage/categories/', views.category_list,name="category_list"),
    url(r'^manage/commodity-metas/', views.commodity_meta_list, name='commodity_meta_list'),
    url(r'^manage/commodities/', views.commodity_list, name='commodity_list'),
    url(r'^manage/brands/', views.brand_list, name='discount_list'),
    url(r'^manage/discounts/', views.discount_list, name='discount_list'),
    url(r'^manage/sale-statistics/', views.statistics_index, name='statistics_index'),
    url(r'^manage/sale-statistics-commodity/', views.statistics_commodity_index, name='statistics_commodity_index'),
    url(r'^manage/sale-statistics-category/', views.statistics_category_index, name='statistics_category_index'),
    url(r'^api/', include('e_shop.api_urls')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
)