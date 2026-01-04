from http import HTTPStatus

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.service.entry import create_entry, get_entries
from api.transport.response.entry import PaginatedEntriesResponse, EntryResponse
from api.transport.response.pagination import PaginationLinksResponse
from api.transport.response.user import UserResponse


class EntryAPIView(APIView):

    def get(self, request: Request):
        next_cursor = request.query_params.get("next_cursor", None)
        previous_cursor = request.query_params.get("previous_cursor", None)

        if next_cursor is not None and previous_cursor is not None:
            return Response({"error": "next_cursor and previous_cursor can not be provided at the same time."}, status=HTTPStatus.BAD_REQUEST)

        paginated_entries_result = get_entries(next_cursor, previous_cursor)

        entries_response = []
        for entry in paginated_entries_result.entries:
            entries_response.append(
                EntryResponse(
                    user=UserResponse(
                        name=entry.user.name,
                    ),
                    subject=entry.subject,
                    message=entry.message,
                )
            )

        next_link = None
        if paginated_entries_result.next_cursor is not None:
            next_link = f"/api/entry/?next_cursor={paginated_entries_result.next_cursor}"

        previous_link = None
        if paginated_entries_result.previous_cursor is not None:
            previous_link = f"/api/entry/?previous_cursor={paginated_entries_result.previous_cursor}"

        payload = PaginatedEntriesResponse(
            links=PaginationLinksResponse(next_link=next_link, previous_link=previous_link),
            entries=entries_response,
        ).serialize()
        return Response(payload, status=HTTPStatus.OK)

    def post(self, request: Request):
        request_data = request.data

        subject: str | None = request_data.get("subject", None)
        message: str | None = request_data.get("message", None)
        user_name: str | None = request_data.get("name", None)

        if subject is None or len(subject.strip()) == 0:
            return Response({"error": "invalid subject"}, status=HTTPStatus.BAD_REQUEST)

        if message is None or len(message.strip()) == 0:
            return Response({"error": "invalid message"}, status=HTTPStatus.BAD_REQUEST)

        if user_name is None or len(user_name.strip()) == 0:
            return Response({"error": "invalid user_name"}, status=HTTPStatus.BAD_REQUEST)

        create_entry(subject.strip(), message.strip(), user_name.strip())

        payload = {"status": True}
        return Response(payload, status=HTTPStatus.OK)
