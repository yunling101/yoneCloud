#!/usr/bin/env python
# -*- coding: utf-8 -*-

from webserver.UserManage.models import User, Permission, Role
from rest_framework import serializers
from webserver.common.mixins import BulkSerializerMixin


class UserSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    last_login = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)

    class Meta:
        model = User
        list_serializer_class = serializers.ListSerializer
        exclude = ("password", )

    def get_role(self, username):
        try:
            user = User.objects.get(username=username)
            role = Role.objects.get(id=user.role_id).name
            return role
        except:
            pass
        return None


class UserCreateSerialize(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "nickname", "email", "is_active", "is_superuser", "role_id")

    # def create(self, validated_data):
    #     if validated_data.get("sid") is None:
    #         validated_data["sid"] = Api.get_sid(6)
    #     return User.objects.create_user(**validated_data)

    # def update(self, instance, validated_data):
    #     return instance


class UserChangePasswordSerialize(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("password", )


class PermissionSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Permission
        list_serializer_class = serializers.ListSerializer
        fields = "__all__"


class PermissionCreateSerialize(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ("name", "menu", "view", "comment")


class RoleSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Role
        list_serializer_class = serializers.ListSerializer
        fields = "__all__"


class RoleCreateSerialize(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("name", "comment")
