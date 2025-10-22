import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from trips.models import Question

def check_questions():
    errors = []
    for q in Question.objects.all():
        missing = []
        if not q.question:
            missing.append('question')
        if not q.choiceA:
            missing.append('choiceA')
        if not q.choiceB:
            missing.append('choiceB')
        if not q.choiceC:
            missing.append('choiceC')
        if not q.choiceD:
            missing.append('choiceD')
        if not q.answer:
            missing.append('answer')
        if missing:
            errors.append(f'編號 {q.number} 缺少: {", ".join(missing)}')
    if errors:
        print('題目資料缺失：')
        for e in errors:
            print(e)
    else:
        print('所有題目資料完整！')

if __name__ == '__main__':
    check_questions()
