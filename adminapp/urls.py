from django.contrib import admin
from django.urls import re_path
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    # re_path(r'^$', adminapp.main, name='main'),
    re_path(r'^$', adminapp.UserListView.as_view(), name='main'),
    # re_path(r'^user/create/$', adminapp.user_create, name='user_create'),
    re_path(r'^user/create/$', adminapp.UserCreateView.as_view(), name='user_create'),
    re_path(r'^user/delete/(?P<pk>\d+)/$', adminapp.UserDeleteView.as_view(), name='user_delete'),
    re_path(r'^user/update/(?P<pk>\d+)/$', adminapp.UserUpdateView.as_view(), name='user_update'),
    re_path(r'^user/repair/(?P<pk>\d+)/$', adminapp.user_repair, name='user_repair'),

    re_path(r'^categories/$', adminapp.categories, name='categories'),
    re_path(r'^categories/create/$', adminapp.ProductCategoryCreateView.as_view(), name='category_create'),
    re_path(r'^categories/delete/(?P<pk>\d+)/$', adminapp.ProductCategoryDeleteView.as_view(), name='category_delete'),
    re_path(r'^categories/update/(?P<pk>\d+)/$', adminapp.ProductCategoryEditView.as_view(), name='category_update'),
    re_path(r'^categories/repair/(?P<pk>\d+)/$', adminapp.category_repair, name='category_repair'),

    re_path(r'^categories/(?P<category_pk>\d+)/products/$', adminapp.category_products, name='category_products'),

    re_path(r'^products/create/(?P<category_pk>\d+)/$', adminapp.product_create, name='product_create'),
    re_path(r'^product/read/(?P<pk>\d+)/$', adminapp.ProductDetailView.as_view(), name='product_read'),
    re_path(r'^product/edit/(?P<pk>\d+)/$', adminapp.product_update, name='product_update'),
    re_path(r'^product/delete/(?P<pk>\d+)/$', adminapp.product_delete, name='product_delete'),
    re_path(r'^product/repair/(?P<pk>\d+)/$', adminapp.product_repair, name='product_repair'),

]
