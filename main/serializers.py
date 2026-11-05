from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Achievement, Project


class StarredSerializer(serializers.ModelSerializer):
    """Shared star fields for every model that has a starred_by relation."""

    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


class ProjectSerializer(StarredSerializer):
    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "tech_stack",
            "project_url", "project_image_url",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_tech_stack(self, value):
        return strip_tags(value)


class AchievementSerializer(StarredSerializer):
    # "category" carries the stored value ("academic"); this read-only field
    # carries the label the page shows ("Academic").
    category_display = serializers.CharField(
        source="get_category_display", read_only=True,
    )

    class Meta:
        model = Achievement
        fields = [
            "id", "title", "event", "category", "category_display",
            "description", "year",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_event(self, value):
        return strip_tags(value).strip()

    def validate_description(self, value):
        return strip_tags(value).strip()

    def validate_year(self, value):
        # The form widget limits the year in the browser; the API has to do it too.
        if not 1900 <= value <= 2100:
            raise serializers.ValidationError("Year must be between 1900 and 2100.")
        return value
