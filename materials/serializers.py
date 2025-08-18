from rest_framework import serializers

from .models import Course, Lesson, Subscription
from .validators import UrlsValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [UrlsValidator(field=["video_url", "name", "description"])]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = "__all__"
        validators = [UrlsValidator(field=["name", "description"])]

    def get_count_lessons(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_is_subscribed(self, course):
        request = self.context.get("request")
        return Subscription.objects.filter(user=request.user, course=course).exists()
