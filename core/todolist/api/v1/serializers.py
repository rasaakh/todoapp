from rest_framework import serializers
from ...models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "user",
            "title",
            "title",
            "complete",
            "created_date",
            "updated_date",
        ]
        read_only_fields = ["user"]

    def get_absolot_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def create(self, validated_data):
        validated_data["user"] = self.context.get("request").user
        return super().create(validated_data)
    
