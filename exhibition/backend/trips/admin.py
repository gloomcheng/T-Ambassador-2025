from django.contrib import admin

from django.utils.html import format_html
from .models import Question, UserProfile, Post

# QuestionAdmin 顯示 icon 縮圖
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('is_open', 'number', 'date', 'title', 'icon_preview', 'question', 'answer')
    list_display_links = ('number', 'date', 'title', 'icon_preview', 'question', 'answer')
    list_editable = ('is_open',)
    def open_selected(self, request, queryset):
        queryset.update(is_open=True)
        self.message_user(request, "已批次開放所選題目！")
    open_selected.short_description = "開放所選題目"

    def close_selected(self, request, queryset):
        queryset.update(is_open=False)
        self.message_user(request, "已批次關閉所選題目！")
    close_selected.short_description = "關閉所選題目"

    list_filter = ['date', 'route']
    search_fields = ('title', 'question')
    # ICON 預覽插入 Title 與 Icon 欄位之間
    fields = ['number', 'date', 'route', 'title', 'icon_preview_inline', 'icon', 'question', 'choiceA', 'choiceB', 'choiceC', 'choiceD', 'answer']
    readonly_fields = ['icon_preview_inline']
    actions = ['delete_selected', 'open_selected', 'close_selected']
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            actions['delete_selected'] = (
                actions['delete_selected'][0],
                '刪除所選題目',
                actions['delete_selected'][2],
            )
        return actions

    class Media:
        js = ('trips/custom_action_label.js',)

    def icon_preview_inline(self, obj):
        icon_url = str(obj.icon) if obj.icon else ''
        if icon_url:
            if 'github.com' in icon_url and '/blob/' in icon_url:
                icon_url = icon_url.replace('/blob/', '/raw/')
            elif not icon_url.startswith('http') and not icon_url.startswith('/'):
                from django.conf import settings
                icon_url = settings.MEDIA_URL + icon_url
            return format_html('<img src="{}" style="height:40px;max-width:60px;object-fit:contain;margin-bottom:8px;" />', icon_url)
        return ''
    icon_preview_inline.short_description = 'ICON 預覽'

    def icon_preview(self, obj):
        if obj.icon:
            url = str(obj.icon)
            # github blob 連結自動轉 raw
            if 'github.com' in url and '/blob/' in url:
                url = url.replace('/blob/', '/raw/')
            elif not url.startswith('http') and not url.startswith('/'):
                from django.conf import settings
                url = settings.MEDIA_URL + url
            return format_html('<img src="{}" style="height:40px;max-width:60px;object-fit:contain;" />', url)
        return ''
    icon_preview.short_description = 'Icon 預覽'

admin.site.register(Question, QuestionAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('gender', 'phone')  # 显示用户信息

admin.site.register(UserProfile, UserProfileAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')  # 显示Post的信息
    search_fields = ('user__phone', 'content')  # 添加搜索功能，可以根据用户电话和内容搜索
    list_filter = ('created_at', 'updated_at')  # 过滤器，可以按创建时间和更新时间过滤

admin.site.register(Post, PostAdmin)
