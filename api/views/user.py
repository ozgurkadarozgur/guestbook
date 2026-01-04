from http import HTTPStatus

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class UserAPIView(APIView):

    def get(self, request: Request):
        payload = {"status": True}
        return Response(payload, status=HTTPStatus.OK)

    def post(self, request: Request):
        payload = {"status": True}
        return Response(payload, status=HTTPStatus.OK)
