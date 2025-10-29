from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
# ...existing code...

@csrf_exempt
def manage(request):
    # 取得登入者手機
    phone = request.session.get('manage_phone')
    company = None
    if phone:
        user = ManageUser.objects.filter(phone=phone).first()
        if user:
            company = user.company
    if not company:
        return HttpResponse('請先登入')
    # 取得所有 title=公司名稱的 Questions
    questions = Question.objects.filter(title=company)
    if request.method == 'POST':
        # 編輯題目
        for q in questions:
            q.question = request.POST.get(f'question_{q.id}', q.question)
            q.choiceA = request.POST.get(f'choiceA_{q.id}', q.choiceA)
            q.choiceB = request.POST.get(f'choiceB_{q.id}', q.choiceB)
            q.choiceC = request.POST.get(f'choiceC_{q.id}', q.choiceC)
            q.choiceD = request.POST.get(f'choiceD_{q.id}', q.choiceD)
            q.answer = request.POST.get(f'answer_{q.id}', q.answer)
            q.icon = request.POST.get(f'icon_{q.id}', q.icon)
            q.save()
        return HttpResponse('儲存成功')
    return render(request, 'manage/company_questions.html', {'questions': questions, 'company': company})
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ManageUser

# ...existing code...

@csrf_exempt
def manage_login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        action = request.POST.get('action')
        company = request.POST.get('company')
        if action == 'register':
            if ManageUser.objects.filter(phone=phone).exists():
                return HttpResponse('此手機已註冊')
            if not company:
                return HttpResponse('請輸入公司名稱')
            ManageUser.objects.create(phone=phone, password=password, company=company)
            request.session['manage_phone'] = phone
            return redirect('/manage/')
        elif action == 'login':
            user = ManageUser.objects.filter(phone=phone, password=password).first()
            if user:
                request.session['manage_phone'] = phone
                return redirect('/manage/')
            else:
                return HttpResponse('手機或密碼錯誤')
    return render(request, 'manage/login.html')
from rest_framework.decorators import api_view

# 新增 API：根據玩家手機號與題號列表，初始化 content2
@api_view(['POST'])
def init_content2(request):
    print(f"[init_content2][CALL] phone={request.data.get('phone')}, levels={request.data.get('levels')}")
    print('[init_content2] 參數:', request.data)
    from datetime import datetime
    def log_event(event, phone, levels, detail):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"[{now}] [{event}] phone={phone}, levels={levels}, {detail}")
    import logging
    import os
    log_dir = os.path.join(os.path.dirname(__file__), '../logs')
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, 'init_content2.log')
    logger = logging.getLogger("init_content2")
    logger.setLevel(logging.INFO)
    # 檢查 file_handler 是否已存在，避免重複加 handler
    if not any(isinstance(h, logging.FileHandler) and h.baseFilename == os.path.abspath(log_path) for h in logger.handlers):
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        logger.addHandler(file_handler)
    phone = request.data.get('phone')
    levels = request.data.get('levels')  # 題號列表，例：[6,7,8,9,10,11]
    # 題號排序（由小到大）
    if isinstance(levels, list):
        levels = sorted(levels, key=lambda x: int(x))
    market = request.data.get('market')  # 新增：所屬市集
    log_event("CALL", phone, levels, "API called")
    if not phone or not levels or not isinstance(levels, list) or not market:
        log_event("ERROR", phone, levels, "缺少 phone、levels 或 market")
        print('[init_content2] 回傳:', {'error': '缺少 phone、levels 或 market'})
        return Response({'error': '缺少 phone、levels 或 market'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user_profile = UserProfile.objects.get(phone=phone)
        post = Post.objects.get(user=user_profile)
    except (UserProfile.DoesNotExist, Post.DoesNotExist) as e:
        log_event("ERROR", phone, levels, f"User or Post not found, error={e}")
        print('[init_content2] 回傳:', {'error': 'User or Post not found'})
        return Response({'error': 'User or Post not found'}, status=status.HTTP_404_NOT_FOUND)
    log_event("SUCCESS", phone, levels, f"content2={post.content2}")
    # 多市集結構：post.content2 = { "A": {"data": {...}}, "B": {"data": {...}} }
    if not isinstance(post.content2, dict):
        post.content2 = {}
    # 判斷是否已有該市集資料
    if market in post.content2:
        # 強制重置所有題目狀態
        for qid, qdata in post.content2[market]['data'].items():
            qdata['status'] = None
            qdata['user_answer'] = ""
        post.save()
        print('[init_content2] 回傳:', {'content2': post.content2[market], 'msg': '已重置並載入'})
        return Response({'content2': post.content2[market], 'msg': '已重置並載入'}, status=status.HTTP_200_OK)
    # 新市集，初始化
    content2 = {}
    for level in levels:
        content2[str(level)] = {
            "status": "null",
            "user_answer": "",
            "correct_answer": ""
        }
    post.content2[market] = {
        "data": content2
    }
    post.save()
    print('[init_content2] 回傳:', {'content2': post.content2[market], 'msg': '第一次進入，已初始化市集'})
    return Response({'content2': post.content2[market], 'msg': '第一次進入，已初始化市集'}, status=status.HTTP_200_OK)
from django.http import JsonResponse
from .models import Question

def market_list(request):
    # 取得所有市集唯一值
    markets = Question.objects.values_list('route', flat=True).distinct()
    return JsonResponse({'markets': list(markets)})
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Post, Question, UserProfile
from .serializers import QuestionSerializer, UserProfileSerializer, PostSerializer


class QuestionDetailAPIView(APIView):

    def get_object(self, question_id):
        try:
            return Question.objects.get(number=question_id)
        except Question.DoesNotExist:
            return None

    def get(self, request, question_id, *args, **kwargs):
        question_instance = self.get_object(question_id)
        if not question_instance:
            return Response(
                {"res": "Object with question id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = QuestionSerializer(question_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileAPIView(APIView):
    def get(self, request):
        phone = request.query_params.get('phone')
        level = request.query_params.get('level')

        if not phone:
            return Response({"error": "缺少手機號碼"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_profile = UserProfile.objects.get(phone=phone)
        except UserProfile.DoesNotExist:
            return Response({"error": "使用者不存在"}, status=status.HTTP_404_NOT_FOUND)

        try:
            post = Post.objects.get(user=user_profile)
        except Post.DoesNotExist:
            return Response({"error": "使用者遊戲歷程不存在"}, status=status.HTTP_404_NOT_FOUND)

        user_data = UserProfileSerializer(user_profile).data

        if level:
            if not level.isdigit() or int(level) < 1 or int(level) > 29:
                return Response({"error": "無效的關卡參數"}, status=status.HTTP_400_BAD_REQUEST)

            level = str(int(level))
            content = user_data['post']['content']

            if level not in content:
                return Response({"error": "該關卡不存在"}, status=status.HTTP_404_NOT_FOUND)

            return Response({level: content[level]}, status=status.HTTP_200_OK)
        else:
            return Response(user_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        import logging
        import os
        from datetime import datetime
        log_dir = os.path.join(os.path.dirname(__file__), '../logs')
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, 'user_profile_api.log')
        logger = logging.getLogger("user_profile_api")
        logger.setLevel(logging.INFO)
        if not any(isinstance(h, logging.FileHandler) and h.baseFilename == os.path.abspath(log_path) for h in logger.handlers):
            file_handler = logging.FileHandler(log_path, encoding='utf-8')
            logger.addHandler(file_handler)
        def log_event(event, phone, detail):
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            logger.info(f"[{now}] [{event}] phone={phone}, {detail}")

        phone = request.data.get('phone')
        gender = request.data.get('gender')
        # 檢查 phone 是否已存在
        try:
            user_profile = UserProfile.objects.get(phone=phone)
            # 已註冊，直接回傳 200 OK 並帶現有資料，並加 is_duplicate 欄位
            log_event("EXIST", phone, "帳號已存在，直接登入")
            data = UserProfileSerializer(user_profile).data
            data['is_duplicate'] = True
            return Response(data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            pass
        # 若未註冊，正常建立
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            user_profile = serializer.save()
            log_event("CREATE", phone, f"新帳號註冊，性別={gender}")
            data = UserProfileSerializer(user_profile).data
            data['is_duplicate'] = False
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostUpdateAPIView(APIView):
    def patch(self, request, phone, *args, **kwargs):
        try:
            # 獲取或創建與該手機號碼相關的 user_profile 和 post
            user_profile, _ = UserProfile.objects.get_or_create(phone=phone)
            post, created = Post.objects.get_or_create(user=user_profile)
        except UserProfile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except Post.DoesNotExist:
            return Response({"error": "User post not found"}, status=status.HTTP_404_NOT_FOUND)

        level = request.data.get("level")
        level_status = request.data.get('status')
        user_answer = request.data.get('user_answer')
        correct_answer = request.data.get('correct_answer')
        market = request.data.get('market')

        if level is None or market is None:
            return Response({"error": "缺少 level 或 market 参数"}, status=status.HTTP_400_BAD_REQUEST)


        # 初始化 content2 結構（與 init_content2 一致）
        if post.content2 is None:
            post.content2 = {}
        if market not in post.content2:
            post.content2[market] = {"data": {}}
        if "data" not in post.content2[market]:
            post.content2[market]["data"] = {}

        # 寫入/更新指定題目狀態
        post.content2[market]["data"][level] = {
            'status': level_status or '',
            'user_answer': user_answer or '',
            'correct_answer': correct_answer or ''
        }

        # 保存更新
        # post.content = content  # 舊邏輯註解
        post.save()

        return Response(post.content2[market]["data"][level], status=status.HTTP_200_OK)


class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailAPIView(APIView):
    def get_object(self, phone):
        try:
            user_profile = UserProfile.objects.get(phone=phone)
            return user_profile.post
        except UserProfile.DoesNotExist:
            return None
        except Post.DoesNotExist:
            return None

    def get(self, request, phone, *args, **kwargs):
        post_instance = self.get_object(phone)
        if not post_instance:
            return Response(
                {"error": "用户不存在"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PostSerializer(post_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)