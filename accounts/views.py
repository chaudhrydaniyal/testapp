from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import (
        RegisterSerializer
)
from rest_framework.permissions import SAFE_METHODS
# Create your views here.


class RegisterViewset(viewsets.ModelViewSet):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['post'] 
    def get_serializer_class(self):
        if self.request is None:
            return RegisterSerializer
        elif not self.request.method in SAFE_METHODS:
            return RegisterSerializer
        return RegisterSerializer


    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.save()
    #     user.code = ''.join([str(rand.randint(0, 999)).zfill(3) for _ in range(2)])
    #     user.save()
    #     token = AccessToken().for_user(user)
    #     refresh = RefreshToken().for_user(user)
    #     code = user.code
    #     body = "Hi " + request.data['email'] + " Here is your register account code\n" + str(code)
    #     data = {"subject": 'Email Verification', "body": body, "to": [request.data['email']],
    #                 'html_message': "Hi " + request.data['email'] + " Here is your register account code\n" + str(code),
    #                 'from': 'From <noreply@likeminded.one>', 'plain_message': ''}
    #     print(user.profile)
    #     Util.send_grid_email(data)

    #     return Response(
    #         {
    #             "user": UserSerializer(user, context=self.get_serializer_context()).data,
    #             "refresh": str(refresh),
    #             "access": str(token)

    #         }
    #     )