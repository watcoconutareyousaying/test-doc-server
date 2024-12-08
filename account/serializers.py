from rest_framework import serializers
from account.models import UserData


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['id', 'email', 'name', 'password']
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if password:
            user = UserData.objects.create(
                email=validated_data['email'], name=validated_data['name'])
            user.set_password(password)
            user.save()
            return user
        else:
            raise serializers.ValidationError("Password is required")
