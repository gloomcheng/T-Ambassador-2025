from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Booth, Question
from .serializers import BoothSerializer, QuestionSerializer


# 🔹 攤位 ViewSet：讓使用者能看到/管理自己的攤位
class BoothViewSet(viewsets.ModelViewSet):
    """
    攤位管理 ViewSet
    攤位使用者登入後只能看到自己的攤位資料
    """
    serializer_class = BoothSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 攤位使用者只能看到自己擁有的攤位
        return Booth.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # 自動把攤位歸屬到目前登入的使用者
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        """
        自訂 API：
        /booths/{id}/questions/ → 取得該攤位底下的所有題目
        """
        booth = self.get_object()
        questions = booth.questions.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


# 🔹 題目 ViewSet：讓攤位使用者可以 CRUD 自己攤位底下的題目
class QuestionViewSet(viewsets.ModelViewSet):
    """
    題目管理 ViewSet
    攤位使用者只能看到/編輯自己攤位底下的題目
    """
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 攤位使用者只能看到自己的攤位底下的題目
        queryset = Question.objects.filter(booth__owner=self.request.user)

        # 可選擇用 ?booth_id= 篩選特定攤位
        booth_id = self.request.query_params.get('booth_id')
        if booth_id:
            queryset = queryset.filter(booth_id=booth_id)
        return queryset

    def perform_create(self, serializer):
        # 攤位 ID 來自 request.data
        booth_id = self.request.data.get('booth_id')
        if not booth_id:
            return Response(
                {'error': '需要提供 booth_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        booth = get_object_or_404(Booth, id=booth_id, owner=self.request.user)
        serializer.save(booth=booth)

    def perform_update(self, serializer):
        # 只能編輯自己攤位的題目
        instance = self.get_object()
        if instance.booth.owner != self.request.user:
            raise PermissionError("你沒有權限修改這個題目。")
        serializer.save()

    def perform_destroy(self, instance):
        # 只能刪除自己攤位的題目
        if instance.booth.owner != self.request.user:
            raise PermissionError("你沒有權限刪除此題目。")
        instance.delete()
