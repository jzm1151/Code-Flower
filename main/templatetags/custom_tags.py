from django import template
from django.contrib.auth.models import User
from main.models import *

register = template.Library()

# The details of this will be ironed out later
# This needs additional error checking to make
# sure the values returned make sense
@register.simple_tag
def get_topic_progress(user_name, topic_id):
    curr_user = User.objects.get(username=user_name)
    curr_topic = Topic.objects.get(id=topic_id)
    lessons = Lesson.objects.filter(topic=curr_topic)
    total_lessons = len(lessons)
    completed_lessons = 0

    for curr_lesson in lessons:
        try:
            UserLessonProgress.objects.get(user=curr_user, lesson=curr_lesson)
            completed_lessons += 1
        except UserLessonProgress.DoesNotExist:
            pass

    if total_lessons <= 0:
        return 100.0
    else:
        return completed_lessons/total_lessons*100.0
