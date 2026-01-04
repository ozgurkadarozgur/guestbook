from http import HTTPStatus

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.service.entry import get_users_entry_statuses
from api.transport.response.user import AllUsersEntryStatusesResponse, UserEntryStatusResponse


class UserAPIView(APIView):

    def get(self, request: Request):
        users_entry_statuses = get_users_entry_statuses()

        users_entry_statuses_response = []
        for users_entry_status in users_entry_statuses:
            users_entry_statuses_response.append(
                UserEntryStatusResponse(
                    username=users_entry_status.name,
                    last_entry=users_entry_status.last_entry,
                    total_entry_count=users_entry_status.total_entry_count,
                )
            )

        payload = AllUsersEntryStatusesResponse(users=users_entry_statuses_response).serialize()
        return Response(payload, status=HTTPStatus.OK)
