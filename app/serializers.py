from django.contrib.auth.models import User
from rest_framework import serializers

from app.models import Audio, AudioDuration


class AudioDurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioDuration
        fields = [
            "start_time",
            "end_time",
        ]


class AudioSerializer(serializers.ModelSerializer):

    duration = AudioDurationSerializer()

    class Meta:
        model = Audio
        fields = [
            "id",
            "type",
            "high_volume",
            "low_volume",
            "video_component_id",
            "url",
            "duration",
        ]

    def create(self, validated_data):
        audio_duration_data = validated_data.pop("duration")
        audio = Audio.objects.create(**validated_data)
        AudioDuration.objects.create(audio_element=audio, **audio_duration_data)
        return audio

    def update(self, instance, validated_data):
        audio_duration_data = validated_data.pop("duration")

        instance.type = validated_data.get("type")
        instance.high_volume = validated_data.get("high_volume")
        instance.low_volume = validated_data.get("low_volume")
        instance.url = validated_data.get("url")
        instance.save()

        audio_duration = instance.duration
        audio_duration.start_time = audio_duration_data.get("start_time")
        audio_duration.end_time = audio_duration_data.get("end_time")
        audio_duration.save()

        return instance

    def validate(self, data):
        """
        Check that start is before finish.
        #"""
        if data["type"] != "video_music" and data["video_component_id"]:
            raise serializers.ValidationError("This audio type must not have an video_component_id")
        if data["type"] == "video_music" and not data["video_component_id"]:
            raise serializers.ValidationError("Video Music type must have an video_component_id")
        if data["type"] == "video_music" and data["url"]:
            raise serializers.ValidationError("The audio file have to be null")
        if data["type"] != "video_music" and not data["url"]:
            raise serializers.ValidationError("The audio file is require")

        return data

    def validate_type(self, value):
        """
        Check that the blog post is about Django.
        """
        if value not in Audio.AudioType:
            raise serializers.ValidationError("invalid audio type")
        return value
