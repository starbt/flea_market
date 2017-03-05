from django.contrib import admin
from market.models import Category,Goods,UserProfile,Comment
# Register your models here.

admin.site.register(Category)
admin.site.register(Goods)
admin.site.register(UserProfile)
admin.site.register(Comment)