from django.contrib.auth.models import Group
from rest_framework import serializers

from src.users.models import User
from src.common.serializers import ThumbnailerJSONSerializer

class UserSerializer(serializers.ModelSerializer):
    profile_picture = ThumbnailerJSONSerializer(required=False,
                                                allow_null=True,
                                                alias_target='src.users')

    groups = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'profile_picture',
            'groups'
        )
        read_only_fields = ('username', )


class CreateUserSerializer(serializers.ModelSerializer):
    profile_picture = ThumbnailerJSONSerializer(required=False, allow_null=True, alias_target='src.users')
    group = serializers.CharField(write_only=True)

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user_group_name = validated_data.pop('group')
        user = User.objects.create_user(**validated_data)
        user.groups.add(Group.objects.get(name=user_group_name))

        return user

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'auth_token',
            'profile_picture',
            'group'
        )
        read_only_fields = ('auth_token', 'group')
        extra_kwargs = {'password': {'write_only': True}}
