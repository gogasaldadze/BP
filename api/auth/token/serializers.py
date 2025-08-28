from rest_framework import serializers


class TokenCreateSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=128)
    password = serializers.CharField(max_length=128)


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
