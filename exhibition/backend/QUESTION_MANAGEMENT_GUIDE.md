# 題目管理系統開發指南

## 概述

本指南說明如何將現有的靜態題目系統擴充為動態題目管理系統，讓管理者可以自由地新增、編輯、刪除題目，而不需要修改程式碼。

## 當前問題分析

目前的題目系統存在以下問題：

1. 題目資料硬編碼在程式中，不易維護
2. 新增題目需要修改程式碼和重新部署
3. 無法動態調整題目內容和順序
4. 媒體檔案管理鬆散

## 系統架構設計

### 1. 資料模型增強

#### 現有模型優化

```python
# trips/models.py
class Question(models.Model):
    number = models.PositiveIntegerField(unique=True)
    batch = models.CharField(max_length=100, default="第一天")  # 梯次
    route = models.CharField(max_length=1, choices=[('A', 'A路線'), ('B', 'B路線'), ('C', 'C路線')])
    title = models.CharField(max_length=100)  # 廠商名稱
    icon = models.ImageField(upload_to='vendor_icons/', blank=True)  # 廠商圖標（本地儲存）
    question = models.TextField()  # 題目文字
    question_image = models.ImageField(upload_to='questions/', blank=True)  # 題目圖片
    choiceA = models.CharField(max_length=200)
    choiceB = models.CharField(max_length=200)
    choiceC = models.CharField(max_length=200)
    choiceD = models.CharField(max_length=200)
    answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])
    explanation = models.TextField(blank=True)  # 題目說明
    points = models.PositiveIntegerField(default=10)  # 題目分數
    is_active = models.BooleanField(default=True)  # 是否啟用
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['number']

    def __str__(self):
        return f"題目 {self.number}: {self.question[:30]}..."
```

#### 新增相關模型

```python
class Vendor(models.Model):
    """廠商資訊模型"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='vendor_logos/', blank=True)
    website = models.URLField(blank=True)
    contact_info = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class GameLevel(models.Model):
    """遊戲關卡模型"""
    number = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    target_image = models.ImageField(upload_to='targets/')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    route = models.CharField(max_length=1, choices=[('A', 'A路線'), ('B', 'B路線'), ('C', 'C路線')])
    batch = models.CharField(max_length=50, default="第一天")
    is_active = models.BooleanField(default=True)
    unlock_condition = models.TextField(blank=True)  # 解鎖條件
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"關卡 {self.number}: {self.name}"
```

### 2. 管理後台設計

#### 自訂管理介面

```python
# trips/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Question, Vendor, GameLevel

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ['question', 'choiceA', 'choiceB', 'choiceC', 'choiceD', 'answer', 'points']

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    inlines = [QuestionInline]

@admin.register(GameLevel)
class GameLevelAdmin(admin.ModelAdmin):
    list_display = ['number', 'name', 'vendor', 'route', 'batch', 'is_active']
    list_filter = ['route', 'batch', 'is_active', 'vendor']
    search_fields = ['name', 'description', 'vendor__name']
    readonly_fields = ['preview_target']

    def preview_target(self, obj):
        if obj.target_image:
            return format_html('<img src="{}" width="200" height="150" />', obj.target_image.url)
        return "無目標圖片"

    preview_target.short_description = "目標圖片預覽"

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['number', 'title', 'question', 'route', 'batch', 'is_active', 'points']
    list_filter = ['route', 'batch', 'is_active', 'created_at']
    search_fields = ['question', 'title', 'choiceA', 'choiceB', 'choiceC', 'choiceD']
    list_editable = ['is_active', 'points']
    readonly_fields = ['preview_question_image', 'created_at', 'updated_at']

    fieldsets = (
        ('基本資訊', {
            'fields': ('number', 'title', 'route', 'batch', 'points', 'is_active')
        }),
        ('題目內容', {
            'fields': ('question', 'question_image', 'preview_question_image')
        }),
        ('選項設定', {
            'fields': ('choiceA', 'choiceB', 'choiceC', 'choiceD', 'answer', 'explanation')
        }),
        ('時間資訊', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def preview_question_image(self, obj):
        if obj.question_image:
            return format_html('<img src="{}" width="300" height="200" />', obj.question_image.url)
        return "無題目圖片"

    preview_question_image.short_description = "題目圖片預覽"
```

### 3. API 擴充

#### 題目管理 API

```python
# trips/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.filter(is_active=True)
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = Question.objects.all()
        route = self.request.query_params.get('route', None)
        batch = self.request.query_params.get('batch', None)

        if route is not None:
            queryset = queryset.filter(route=route)
        if batch is not None:
            queryset = queryset.filter(batch=batch)

        return queryset.order_by('number')

    @action(detail=False, methods=['get'])
    def by_level(self, request):
        level = request.query_params.get('level', None)
        if level is not None:
            question = get_object_or_404(Question, number=level, is_active=True)
            serializer = self.get_serializer(question)
            return Response(serializer.data)
        return Response({"error": "請提供關卡號碼"}, status=400)

class VendorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vendor.objects.filter(is_active=True)
    serializer_class = VendorSerializer

class GameLevelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GameLevel.objects.filter(is_active=True).select_related('vendor')
    serializer_class = GameLevelSerializer

    def get_queryset(self):
        queryset = GameLevel.objects.filter(is_active=True).select_related('vendor')
        route = self.request.query_params.get('route', None)
        batch = self.request.query_params.get('batch', None)

        if route is not None:
            queryset = queryset.filter(route=route)
        if batch is not None:
            queryset = queryset.filter(batch=batch)

        return queryset.order_by('number')
```

### 4. 媒體檔案管理

#### 自訂檔案上傳處理

```python
# trips/models.py
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class QuestionImageStorage(FileSystemStorage):
    def __init__(self):
        super().__init__(location=os.path.join(settings.MEDIA_ROOT, 'questions'))

class VendorIconStorage(FileSystemStorage):
    def __init__(self):
        super().__init__(location=os.path.join(settings.MEDIA_ROOT, 'vendor_icons'))

class TargetImageStorage(FileSystemStorage):
    def __init__(self):
        super().__init__(location=os.path.join(settings.MEDIA_ROOT, 'targets'))

# 在模型中使用
class Question(models.Model):
    question_image = models.ImageField(
        upload_to='questions/',
        storage=QuestionImageStorage(),
        blank=True
    )
```

### 5. 題目匯入匯出功能

#### CSV 匯入匯出

```python
# trips/management/commands/import_questions.py
import csv
from django.core.management.base import BaseCommand
from trips.models import Question, Vendor

class Command(BaseCommand):
    help = '匯入題目資料從 CSV 檔案'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='CSV 檔案路徑')

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # 建立或更新廠商
                vendor, created = Vendor.objects.get_or_create(
                    name=row['廠商名稱'],
                    defaults={
                        'description': row.get('廠商描述', ''),
                        'website': row.get('廠商網站', ''),
                    }
                )

                # 建立題目
                Question.objects.update_or_create(
                    number=row['題號'],
                    defaults={
                        'title': row['廠商名稱'],
                        'route': row['路線'],
                        'batch': row['梯次'],
                        'question': row['題目'],
                        'choiceA': row['選項A'],
                        'choiceB': row['選項B'],
                        'choiceC': row['選項C'],
                        'choiceD': row['選項D'],
                        'answer': row['答案'],
                        'explanation': row.get('說明', ''),
                        'points': int(row.get('分數', 10)),
                    }
                )

        self.stdout.write(
            self.style.SUCCESS(f'成功匯入題目資料從 {csv_file}')
        )
```

### 6. 前端題目編輯器

#### Django Admin 樣式自訂

```css
/* trips/static/admin/css/question_editor.css */
.question-preview {
    max-width: 100%;
    height: auto;
    border: 1px solid #ddd;
    margin: 10px 0;
}

.option-field {
    margin-bottom: 15px;
}

.answer-highlight {
    background-color: #e8f5e8;
    padding: 5px;
    border-radius: 3px;
}
```

#### JavaScript 預覽功能

```javascript
// trips/static/admin/js/question_preview.js
(function($) {
    $(document).ready(function() {
        function updatePreview() {
            const question = $('#id_question').val();
            const choiceA = $('#id_choiceA').val();
            const choiceB = $('#id_choiceB').val();
            const choiceC = $('#id_choiceC').val();
            const choiceD = $('#id_choiceD').val();
            const answer = $('#id_answer').val();

            let preview = `<div class="question-preview">
                <h4>題目預覽：</h4>
                <p><strong>題目：</strong>${question}</p>
                <div class="options">
                    <p><strong>A:</strong> ${choiceA}</p>
                    <p><strong>B:</strong> ${choiceB}</p>
                    <p><strong>C:</strong> ${choiceC}</p>
                    <p><strong>D:</strong> ${choiceD}</p>
                </div>
                <p><strong>正確答案：</strong> ${answer}</p>
            </div>`;

            $('#question-preview').html(preview);
        }

        // 監聽表單變更
        $('#id_question, #id_choiceA, #id_choiceB, #id_choiceC, #id_choiceD, #id_answer').change(updatePreview);

        // 初始預覽
        updatePreview();
    });
})(django.jQuery);
```

### 7. 題目驗證與測試

#### 自訂驗證邏輯

```python
# trips/validators.py
from django.core.exceptions import ValidationError

def validate_question_choices(value):
    """驗證題目選項不為空"""
    if not value or value.strip() == '':
        raise ValidationError('選項內容不能為空')

def validate_answer_in_choices(question):
    """驗證答案在選項中"""
    choices = [question.choiceA, question.choiceB, question.choiceC, question.choiceD]
    if question.answer not in ['A', 'B', 'C', 'D']:
        raise ValidationError('答案必須是 A、B、C 或 D')
    if not choices[ord(question.answer) - ord('A')]:
        raise ValidationError(f'答案 {question.answer} 對應的選項不能為空')
```

#### 題目測試指令

```python
# trips/management/commands/test_questions.py
from django.core.management.base import BaseCommand
from trips.models import Question

class Command(BaseCommand):
    help = '測試題目資料完整性'

    def handle(self, *args, **options):
        questions = Question.objects.filter(is_active=True)

        errors = []
        for question in questions:
            try:
                # 檢查必要欄位
                if not all([question.question, question.choiceA, question.choiceB,
                           question.choiceC, question.choiceD, question.answer]):
                    errors.append(f'題目 {question.number}: 有空白欄位')

                # 檢查答案有效性
                if question.answer not in ['A', 'B', 'C', 'D']:
                    errors.append(f'題目 {question.number}: 答案無效')

            except Exception as e:
                errors.append(f'題目 {question.number}: {str(e)}')

        if errors:
            self.stdout.write(
                self.style.ERROR(f'發現 {len(errors)} 個錯誤：')
            )
            for error in errors:
                self.stdout.write(self.style.ERROR(f'  - {error}'))
        else:
            self.stdout.write(
                self.style.SUCCESS(f'所有 {len(questions)} 個題目都通過驗證')
            )
```

### 8. 部署與維護

#### 資料遷移

```python
# trips/management/commands/migrate_question_data.py
from django.core.management.base import BaseCommand
from trips.models import Question

class Command(BaseCommand):
    help = '將舊題目資料遷移到新結構'

    def handle(self, *args, **options):
        # 假設舊資料在某處，需要根據實際情況調整
        old_questions = [
            # 舊題目資料結構
        ]

        for old_q in old_questions:
            Question.objects.create(
                number=old_q['number'],
                title=old_q['vendor'],
                route=old_q['route'],
                batch=old_q['batch'],
                question=old_q['question'],
                choiceA=old_q['choiceA'],
                choiceB=old_q['choiceB'],
                choiceC=old_q['choiceC'],
                choiceD=old_q['choiceD'],
                answer=old_q['answer'],
                points=10,
                is_active=True
            )

        self.stdout.write(
            self.style.SUCCESS('題目資料遷移完成')
        )
```

## 開發步驟

### 第一階段：資料模型重構

1. 修改現有的 `Question` 模型
2. 新增 `Vendor` 和 `GameLevel` 模型
3. 執行資料遷移

### 第二階段：管理後台開發

1. 設計自訂管理介面
2. 新增圖片預覽功能
3. 實作批次操作功能

### 第三階段：API 擴充

1. 建立題目管理 API
2. 新增題目查詢過濾器
3. 實作題目統計功能

### 第四階段：媒體管理

1. 設定檔案上傳儲存
2. 新增圖片壓縮功能
3. 實作檔案清理機制

### 第五階段：測試與優化

1. 建立題目驗證測試
2. 效能優化查詢
3. 錯誤處理完善

## 使用指南

### 管理者操作說明

1. **登入管理後台**
   訪問 `/admin/` 登入系統

2. **管理廠商**
   - 在「廠商」頁面新增、編輯廠商資訊
   - 上傳廠商圖標和相關資料

3. **管理題目**
   - 在「題目」頁面瀏覽所有題目
   - 使用搜尋和過濾功能快速找到目標題目
   - 點擊「編輯」修改題目內容
   - 使用批次操作啟用/停用題目

4. **匯入匯出題目**

   ```bash
   # 匯入題目
   python manage.py import_questions questions.csv

   # 測試題目
   python manage.py test_questions

   # 匯出題目
   python manage.py export_questions questions_backup.csv
   ```

## 技術規格

- **Django 版本**: 5.0+
- **Python 版本**: 3.11+
- **支援的圖片格式**: JPG, PNG, WebP
- **最大檔案大小**: 5MB per file
- **支援的瀏覽器**: Chrome 90+, Firefox 88+, Safari 14+

## 未來擴充建議

1. **題目版本控制**：追蹤題目修改歷史
2. **協作編輯**：支援多人同時編輯題目
3. **題目預覽**：即時預覽題目在前端的顯示效果
4. **智慧題庫**：基於難度、知識點自動推薦題目
5. **數據分析**：統計題目答題正確率和熱門程度

這個開發指南提供了完整的題目管理系統解決方案，讓管理者能夠靈活地管理遊戲內容，而不需要修改程式碼。
