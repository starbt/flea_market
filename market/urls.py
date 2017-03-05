from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^$',views.index,name='index' ),
    url(r'^category/(?P<category_id>[\w\-]+)', views.category,name='category'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^about/', views.about,name='about'),
    url(r'^logout/$', views.user_logout,name='logout'),
    url(r'^goods/(?P<goods_id>[\w\-]+)', views.goods_page,name='goods'),
    url(r'^add_goods', views.add_goods,name='add_goods'),
    url(r'^add_comment/(?P<goods_id>[\w\-]+)', views.add_comment,name='add_comment'),
    url(r'^profile/(?P<user_id>[\w\-]+)', views.profile,name='profile'),
    url(r'^search',views.search,name='search'),
    url(r'^message/', views.display_message, name='message'),
]   

