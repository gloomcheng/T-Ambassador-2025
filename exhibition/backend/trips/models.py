from django.db import models

# Create your models here.
def default_content():
    content = {}
    for i in range(1, 30):  # 關卡數
        content[str(i)] = {
            "status": "null",  # null, pass, fail
            "user_answer": "",
            "correct_answer": "",
        }
    return content


class Question(models.Model):
    is_open = models.BooleanField(default=False, verbose_name='是否開放')  # 題目是否開放
    number = models.PositiveIntegerField(unique=True)
    date = models.DateField(
        verbose_name='日期',
        blank=True,
        null=True,
        help_text='若需指定日期才填寫，否則可留空'
    )  # 哪一天
    route = models.CharField(max_length=20, verbose_name='所屬市集')  #可填中文市集名稱
    title = models.CharField(max_length=100) #廠商名稱
    icon = models.URLField(blank=True) #廠商icon
    question = models.CharField(max_length=100) #題目
    choiceA = models.CharField(max_length=100) #選項
    choiceB = models.CharField(max_length=100)
    choiceC = models.CharField(max_length=100)
    choiceD = models.CharField(max_length=100)
    answer = models.CharField(max_length=100) #答案

    def __str__(self):
        return f"{self.number}. {self.question}"

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
        ('O', '其他'),
    ]

    phone = models.CharField(max_length=15, primary_key=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.get_gender_display()} - {self.phone}"

class Post(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.SET_NULL, related_name='post', null=True, blank=True)
    content = models.JSONField(default=default_content)
    # 多市集進度：{ "A": {"data": {...}}, "B": {"data": {...}} }
    content2 = models.JSONField(default=dict)  # 初始為空 dict，動態新增市集
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        user_phone = self.user.phone if self.user else "Unknown"
        return f"Post by {user_phone} at {self.created_at}"