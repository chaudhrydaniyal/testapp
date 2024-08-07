
from rest_framework import serializers
from accounts.models import  User
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer
from django.contrib.auth.hashers  import make_password
import logging
log = logging.getLogger("main")


class RegisterSerializer(serializers.ModelSerializer):
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)
    # referral_code = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('id', 'email', 'password',)
        extra_kwargs = {'password': {'write_only': True}, 'organizations': {'write_only': True}}

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.
        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)

    def create(self, validated_data):
        # print(f"========================> {validated_data}")
        # if not "confirm-password" in validated_data:
        #     raise serializers.ValidationError({"error": "confirmation password is required"})
        # confirm_password = validated_data.pop("confirm-password")
        # if not confirm_password == validated_data["password"]:
        #     raise serializers.ValidationError({"error": "password is not matched with confirmation password"})

        user = User.objects.create(**validated_data)
        return user
