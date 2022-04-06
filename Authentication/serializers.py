from rest_framework import serializers
from Authentication.models import MyUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True
    )

    class Meta:
        model = MyUser
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError("The Username should only alphanumeric characters")
        return attrs
        # return super().validate(attrs)

    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)


class EmailVerificationerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = MyUser
        fields = ['token']
