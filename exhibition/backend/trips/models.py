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
    number = models.PositiveIntegerField(unique=True)
    batch = models.CharField(max_length=100)  # 梯次 第一天,第二天
    route = models.CharField(max_length=1)  # 路線名稱 A,B,C
    server_id = models.CharField(max_length=50, blank=True, null=True) #ServerID
    title = models.CharField(max_length=100)  # 廠商名稱
    icon = models.URLField(blank=True)  # 廠商 icon
    question = models.CharField(max_length=100)  # 題目
    choiceA = models.CharField(max_length=100)  # 選項
    choiceB = models.CharField(max_length=100)
    choiceC = models.CharField(max_length=100)
    choiceD = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)  # 答案

    def __str__(self):
        return f"{self.number}. {self.question}"


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
        ('O', '其他'),
    ]

    ROLE_CHOICES = [
        ('user', '攤位使用者'),
        ('booth', '後臺管理者'),
    ]

    phone = models.CharField(max_length=15, primary_key=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')  # 新增這行 ✅

    def is_booth(self):
        return self.role == 'booth'

    def is_user(self):
        return self.role == 'user'

    def __str__(self):
        return f"{self.get_gender_display()} - {self.phone} ({self.get_role_display()})"


class Post(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.SET_NULL, related_name='post', null=True, blank=True)
    content = models.JSONField(default=default_content)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.user.phone} at {self.created_at}"
