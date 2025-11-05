from django.db.models import Count
# 市集列表 API：只回傳有 6 題開放題目的市集
from datetime import date as dtdate
from django.db.models import Q
def market_list(request):
    today = dtdate.today()
    qs = Question.objects.filter(is_open=True).filter(Q(date=today) | Q(date__isnull=True))
    markets = (
        qs.values('route')
        .annotate(open_count=Count('id'))
        .filter(open_count__gte=6)
        .values_list('route', flat=True)
    )
    return JsonResponse({'markets': list(markets)})
from django.http import JsonResponse
from .models import Question
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import random

@csrf_exempt
def market_questions(request):
    """
    根據市集名稱 (route) 回傳隨機 6 筆該市集的題目(含圖片icon路徑、number)
    GET 參數: ?market=市集名稱
    回傳: { questions: [ {number, icon, title, ...}, ... ] }
    """
    market = request.GET.get('market')
    print('[market_questions] 市集:', market)
    if not market:
        print('[market_questions] 缺少市集參數')
        return JsonResponse({'error': '缺少市集參數'}, status=400)
    from datetime import date as dtdate
    today = dtdate.today()
    qs = Question.objects.filter(route=market)
    # 只取今天的題目或持續開放題目（date 為 null）
    qs = qs.filter(Q(date=today) | Q(date__isnull=True))
    total = qs.count()
    if total == 0:
        print('[market_questions] 查無題目')
        return JsonResponse({'questions': []})
    sample = random.sample(list(qs), min(6, total))
    data = [
        {
            'number': q.number,
            'icon': q.icon,
            'title': q.title,
            'question': q.question,
            'choiceA': q.choiceA,
            'choiceB': q.choiceB,
            'choiceC': q.choiceC,
            'choiceD': q.choiceD,
            'answer': q.answer,
        }
        for q in sample
    ]
    print('[market_questions] 回傳:', {'questions': data})
    return JsonResponse({'questions': data})
