from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Topic, Lesson, LessonQuestion, LessonQuestionOption, UserLessonProgress, LessonComment, \
    LessonCommentReply, InstructorRequest
from django.contrib.auth.models import User

from django.http import JsonResponse
import json, math


def home(request):
    return render(request, 'main/home.html')


def topics(request):
    if not request.user.is_authenticated:
        return render(request, 'main/home.html', {'no_auth_message': True})

    all_topics = Topic.objects.order_by('id')
    context = {'topics': all_topics}
    return render(request, 'main/topics.html', context)


def lessons(request, lesson_id):
    if not request.user.is_authenticated:
        return render(request, 'main/home.html', {'no_auth_message': True})

    lesson = Lesson.objects.get(id=lesson_id)
    context = {'lesson': lesson}
    return render(request, 'main/lessons.html', context)


def lesson_quizzes(request, lesson_id):
    if not request.user.is_authenticated:
        return render(request, 'main/home.html', {'no_auth_message': True})

    lesson = Lesson.objects.get(id=lesson_id)
    context = {'lesson': lesson}
    return render(request, 'main/lesson_quizzes.html', context)


def instructor(request):
    if request.user.is_superuser:
        all_topics = Topic.objects.all()
        all_lessons = Lesson.objects.all()
        all_quizzes = LessonQuestion.objects.all()
        context = {'topics': all_topics, 'lessons': all_lessons, 'quizzes': all_quizzes}
        return render(request, 'main/admin.html', context)
    else:
        return render(request, 'main/home.html')


def create_topic(request):
    if not request.user.is_superuser:
        return render(request, 'main/home.html')

    if request.method == 'POST':
        topic = request.POST.get('topic')
        published = request.POST.get('published')
        score = request.POST.get('min_passing_score')

        new_topic = Topic(name=topic, published=published, min_passing_score=score)
        new_topic.save()
    topics = Topic.objects.all()

    return render(request, 'main/refreshTemplate/topic_template.html', {'topics': topics})


def edit_topic(request, topic_id):
    if not request.user.is_superuser:
        return render(request, 'main/home.html')

    topic = Topic.objects.get(id=topic_id)
    lesson = Lesson.objects.filter(topic=topic_id)

    context = {'topics': topic, 'lessons': lesson}
    return render(request, 'main/add_lesson.html', context)


def delete_topic(request):
    if not request.user.is_superuser:
        return render(request, 'main/home.html')
    if request.method == 'POST':
        topic_id = request.POST.get('topic_id')
        topic = Topic.objects.get(id=topic_id)
        topic.delete();
        t = Topic.objects.all()
        return render(request, 'main/refreshTemplate/topic_template.html', {'topics': t})


def create_lesson(request):
    if not request.user.is_superuser:
        return render(request, 'main/home.html')

    if request.method == 'POST':
        lname = request.POST.get('lname')
        desc = request.POST.get('desc')
        minScore = request.POST.get('min_score')
        quizNum = request.POST.get('quiz_num')
        published = request.POST.get('published')
        ide = request.POST.get('ide')
        topic_id = request.POST.get('topic')
        topic = Topic.objects.get(id=topic_id)

        new_lesson = Lesson(name=lname, published=published, content_description=desc, needs_IDE=ide, topic=topic,
                            wanted_number_quiz_questions=quizNum, min_passing_score=minScore)
        new_lesson.save()
        lesson = Lesson.objects.filter(topic=topic)
    return render(request, 'main/refreshTemplate/lesson_template.html', {'lessons': lesson})


def edit_lesson(request, lesson_id):
    if not request.user.is_superuser:
        return render(request, 'main/home.html')

    if request.method == 'POST':
        lesson = Lesson.objects.get(id=lesson_id)
        lesson.name = request.POST.get('lname')
        lesson.content_description = request.POST.get('desc')
        lesson.min_passing_score = request.POST.get('min_score')
        lesson.wanted_number_quiz_questions = request.POST.get('quiz_num')
        lesson.published = request.POST.get('published')
        lesson.needs_IDE = request.POST.get('ide')
        lesson.save()
        return render(request, 'main/refreshTemplate/lesson_edit_template.html', {'lesson': lesson})

    else:
        lesson = Lesson.objects.get(id=lesson_id)
        quiz = LessonQuestion.objects.filter(lesson=lesson_id)

        context = {'lesson': lesson, 'quizzes': quiz}
        return render(request, 'main/add_quizzes.html', context)


def delete_lesson(request):
    if not request.user.is_superuser:
        return render(request, 'main/home.html')

    if request.method == 'POST':
        lesson_id = request.POST.get('lesson_id')
        lesson = Lesson.objects.get(id=lesson_id)
        lesson.delete()
        l = Lesson.objects.all()
        return render(request, 'main/refreshTemplate/lesson_template.html', {'lessons': l})

def create_question(request, lesson_id):
    if not request.user.is_superuser:
        return render(request, 'main/home.html')

    if request.method == 'POST':
        title = request.POST.get('title')
        question = request.POST.get('question')
        published = request.POST.get('published')
        question_type = request.POST.get('question_type')
        difficulty = request.POST.get('difficulty')
        lesson = Lesson.objects.get(id=lesson_id)
        o = request.POST['options']
        options = json.loads(o)
        lesson_question = LessonQuestion(name=title, published=published, question=question,
                                         question_type=question_type,
                                         difficulty=difficulty, lesson=lesson)
        lesson_question.save()

        for option in options:
            option_name = option['option_name']
            option_answer = option['option_answer']
            if option_name != '':
                question_option = LessonQuestionOption(option=option_name, option_correct=option_answer,
                                                       lesson_question=lesson_question)
                question_option.save()

        quiz = LessonQuestion.objects.filter(lesson=lesson_id)
        return render(request, 'main/refreshTemplate/quiz_template.html', {'quizzes': quiz})

    if request.method == 'GET':
        return render(request, 'main/refreshTemplate/quiz_form.html')

def delete_question(request):
    if not request.user.is_superuser:
        return render(request, 'main/home.html')

    if request.method == 'POST':
        question_id = request.POST.get('quiz_id')
        question = LessonQuestion.objects.get(id=question_id)
        question.delete()
        q = LessonQuestion.objects.all()
        return render(request, 'main/refreshTemplate/quiz_template.html', {'quizzes': q})


def publish_topic(request):
    if not request.user.is_superuser:
        return render(request, 'main/home.html')

    if request.method == 'POST':
        topic_id = request.POST.get('topic_id')
        topic = Topic.objects.get(id=topic_id)
        topic.published = not topic.published
        topic.save()
        return render(request, 'main/admin.html')


def publish_lesson(request):
    if not request.user.is_superuser:
        return render(request, 'main/home.html')

    if request.method == 'POST':
        lesson_id = request.POST.get('lesson_id')
        lesson = Lesson.objects.get(id=lesson_id)
        lesson.published = not lesson.published
        lesson.save()
        return render(request, 'main/admin.html')

def publish_question(request):
    if not request.user.is_superuser:
        return render(request, 'main/home.html')

    if request.method == 'POST':
        question_id = request.POST.get('quiz_id')
        question = LessonQuestion.objects.get(id=question_id)
        question.published = not question.published
        question.save()
        return render(request, 'main/admin.html')

def quiz_processing(request):
    if not request.user.is_authenticated:
        return render(request, 'main/home.html', {'no_auth_message': True})

    quiz = request.POST['quiz']
    quiz = json.loads(quiz)
    total_points = 0
    number_questions = 0
    lesson_obj = None

    for question in quiz:
        number_questions += 1

        for question_id, answers in question.items():
            question_obj = LessonQuestion.objects.get(id=question_id)
            correct_options = LessonQuestionOption.objects.filter(option_correct=True, lesson_question=question_obj)
            number_correct_options = len(correct_options)
            number_options_answered_correct = 0

            if not lesson_obj:
                lesson_obj = question_obj.lesson

            for answer in answers:
                for opt_id, option_choice in answer.items():
                    option_obj = LessonQuestionOption.objects.get(id=opt_id)

                    if option_obj.option_correct:
                        if isinstance(option_choice, str):
                            if option_choice == option_obj.option.strip():
                                number_options_answered_correct += 1
                        else:
                            number_options_answered_correct += 1

            total_points += number_options_answered_correct / number_correct_options

    score = (total_points / number_questions) * 100
    score = math.trunc(score)
    best_score = score
    try:
        user_progress = UserLessonProgress.objects.get(user=request.user, lesson=lesson_obj)
        best_score = user_progress.score

        if user_progress.score <= score:
            best_score = score
            user_progress.score = score
            user_progress.save()
    except UserLessonProgress.DoesNotExist:
        user_progress = UserLessonProgress(user=request.user, lesson=lesson_obj, score=score)
        user_progress.save()

    return JsonResponse({'score': score, 'best-score': best_score})


# this should throw an exceptions instead of redirect
def create_lesson_comment(request):
    if not request.user.is_authenticated:
        return render(request, 'main/home.html', {'no_auth_message': True})

    if request.method != 'POST':
        return render(request, 'main/home.html')

    username = request.POST.get('username')
    user = User.objects.get(username=username)
    lesson_id = request.POST.get('lesson_id')
    lesson_foreign_key = Lesson.objects.get(id=lesson_id)
    body = request.POST.get('body')
    new_comment = LessonComment(user=user, lesson=lesson_foreign_key, body=body)
    new_comment.save()

    comments = LessonComment.objects.filter(lesson=lesson_foreign_key)
    return render(request, 'main/refreshTemplate/lesson_comments.html', {'comments': comments})


# this could be updated to use the delete method
# this should also throw exceptions instead of delete
def delete_lesson_comment(request):
    if not request.user.is_authenticated:
        return render(request, 'main/home.html', {'no_auth_message': True})

    if request.method != 'POST':
        return render(request, 'main/home.html')

    comment_id = request.POST.get('comment_id')
    comment = LessonComment.objects.get(id=comment_id)

    # this needs to be tested
    if request.user != comment.user:
        return render(request, 'main/home.html')

    lesson_foreign_key = comment.lesson
    comment.delete()

    comments = LessonComment.objects.filter(lesson=lesson_foreign_key)
    return render(request, 'main/refreshTemplate/lesson_comments.html', {'comments': comments})


# this should throw an exception instead of redirect
def create_lesson_comment_reply(request):
    if not request.user.is_authenticated:
        return render(request, 'main/home.html', {'no_auth_message': True})

    if request.method != 'POST':
        return render(request, 'main/home.html')

    comment_id = request.POST.get('comment_id')
    comment_foreign_key = LessonComment.objects.get(id=comment_id)
    body = request.POST.get('body')
    new_comment_reply = LessonCommentReply(user=request.user, parent=comment_foreign_key, body=body)
    new_comment_reply.save()

    replies = LessonCommentReply.objects.filter(parent=comment_foreign_key)
    return render(request, 'main/refreshTemplate/lesson_comment_replies.html', {'replies': replies})


# this should throw an exception instead of redirect
def delete_lesson_comment_reply(request):
    if not request.user.is_authenticated:
        return render(request, 'main/home.html', {'no_auth_message': True})

    if request.method != 'POST':
        return render(request, 'main/home.html')

    reply_id = request.POST.get('reply_id')
    reply = LessonCommentReply.objects.get(id=reply_id)

    if request.user != reply.user:
        return render(request, 'main/home.html')

    comment_foreign_key = reply.parent
    reply.delete()

    replies = LessonCommentReply.objects.filter(parent=comment_foreign_key)
    return render(request, 'main/refreshTemplate/lesson_comment_replies.html', {'replies': replies})


# this should throw an exception instead of redirect
def instructor_request(request):
    if not request.user.is_authenticated:
        return render(request, 'main/home.html', {'no_auth_message': True})

    if request.method != 'POST':
        return render(request, 'main/home.html')

    pref_name = request.POST.get('pref_name')
    email = request.POST.get('email')
    reason = request.POST.get('reason')

    new_request = InstructorRequest(user=request.user, pref_name=pref_name, email=email, reason=reason, status="pending")
    new_request.save()

    return render(request, 'main/refreshTemplate/instructorRequest.html')