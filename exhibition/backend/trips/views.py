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
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            user_profile = serializer.save()
            return Response(UserProfileSerializer(user_profile).data, status=status.HTTP_201_CREATED)
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

        if level is None:
            return Response({"error": "缺少 level 或 data 参数"}, status=status.HTTP_400_BAD_REQUEST)

        # 初始化 content 作為一個空字典（若之前沒有設置 content）
        if post.content is None:
            post.content = {}

        content = post.content

        # 檢查關卡是否存在並更新或創建對應的內容
        if level in content:
            if level_status is not None:
                content[level]['status'] = level_status
            if user_answer is not None:
                content[level]['user_answer'] = user_answer
            if correct_answer is not None:
                content[level]['correct_answer'] = correct_answer
        else:
            content[level] = {
                'status': level_status or '',
                'user_answer': user_answer or '',
                'correct_answer': correct_answer or ''
            }

        # 保存更新
        post.content = content
        post.save()

        return Response(content[level], status=status.HTTP_200_OK)


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