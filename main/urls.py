from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('instructor', views.instructor, name='instructor'),
    path('topics', views.topics, name='topics'),
    path('add/topics', views.create_topic, name='create_topic'),
    path('edit/topic/(<topic_id>\d+)', views.edit_topic, name='edit_topic'),
    path('edit/topic/publish', views.publish_topic, name='publish_topic'),
    path('delete/topic', views.delete_topic, name='delete_topic'),
    path('add/lessons', views.create_lesson, name='create_lesson'),
    path('edit/lesson/(<lesson_id>\d+)', views.edit_lesson, name='edit_lesson'),
    path('delete/lesson', views.delete_lesson, name='delete_lesson'),
    path('edit/lesson/publish', views.publish_lesson, name='publish_lesson'),
    path('add/questions/(<lesson_id>\d+)', views.create_question, name='create_question'),
    path('delete/question', views.delete_question, name='delete_question'),
    path('edit/question/publish', views.publish_question, name='publish_question'),
    path('lessons/(<lesson_id>\d+)', views.lessons, name='lessons'),
    path('lesson_quizzes/(<lesson_id>\d+)', views.lesson_quizzes, name='lesson_quizzes'),
    path('validate/lesson_quiz', views.quiz_processing, name='quiz_processing'),
    path('lesson/submit/comment', views.create_lesson_comment, name='create_lesson_comment'),
    path('lesson/delete/comment', views.delete_lesson_comment, name='delete_lesson_comment'),
    path('lesson/submit/comment/reply', views.create_lesson_comment_reply, name='create_lesson_comment_reply'),
    path('lesson/delete/comment/reply', views.delete_lesson_comment_reply, name='delete_lesson_comment_reply'),
    path('home/instructorRequest', views.instructor_request, name='instructor_request')
]
