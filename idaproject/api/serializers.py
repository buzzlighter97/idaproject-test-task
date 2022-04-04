from rest_framework import serializers
from .models import Image


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ImageSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Image
        fields = [
            "id",
            "name",
            "file",
            "url",
            "picture",
            "width",
            "height",
            "parent_picture",
        ]

    def create(self, validated_data):
        return Image(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get("id", instance.id)
        instance.name = validated_data.get("name", instance.name)
        instance.file = validated_data.get("file", instance.file)
        instance.url = validated_data.get("url", instance.url)
        instance.picture = validated_data.get("picture", instance.picture)
        instance.width = validated_data.get("width", instance.width)
        instance.height = validated_data.get("height", instance.height)
        instance.parent_picture = validated_data.get(
            "parent_picture", instance.parent_picture
        )
        instance.save()
        return instance


class ImageSerializerNoFile(DynamicFieldsModelSerializer):
    class Meta:
        model = Image
        fields = [
            "id",
            "name",
            "url",
            "picture",
            "width",
            "height",
            "parent_picture",
        ]

    def create(self, validated_data):
        return Image(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get("id", instance.id)
        instance.name = validated_data.get("name", instance.name)
        instance.url = validated_data.get("url", instance.url)
        instance.picture = validated_data.get("picture", instance.picture)
        instance.width = validated_data.get("width", instance.width)
        instance.height = validated_data.get("height", instance.height)
        instance.parent_picture = validated_data.get(
            "parent_picture", instance.parent_picture
        )
        instance.save()
        return instance