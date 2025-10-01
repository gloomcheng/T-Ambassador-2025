from django.contrib import admin
from .models import Question, UserProfile, Post

# Register your models here.
admin.site.register(Question)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('gender', 'phone')  # 显示用户信息

admin.site.register(UserProfile, UserProfileAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')  # 显示Post的信息
    search_fields = ('user__phone', 'content')  # 添加搜索功能，可以根据用户电话和内容搜索
    list_filter = ('created_at', 'updated_at')  # 过滤器，可以按创建时间和更新时间过滤

admin.site.register(Post, PostAdmin)
