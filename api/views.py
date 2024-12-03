import base64
import json

from django.contrib.auth import authenticate
from django.db.models import Prefetch
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import User

from .models import Purchase, Report, User


class TokenObtainWithBasicAuth(APIView):
    permission_classes = []

    def post(self, request):
        auth = request.headers.get("Authorization").split()

        if len(auth) == 2 and auth[0].lower() == "basic":
            username, password = base64.b64decode(auth[1]).decode("utf-8").split(":")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "refresh": str(refresh),
                        "token": str(refresh.access_token),
                    }
                )

        return Response({"detail": "Invalid credentials"}, status=401)


class DataView(APIView):
    permission_classes = [IsAuthenticated]

    def __gather_data_as_dict(self):
        users = User.objects.all().prefetch_related(
            Prefetch("reports", queryset=Report.objects.all()),
            Prefetch("purchases", queryset=Purchase.objects.all()),
        )

        data = {"users": []}

        for user in users:
            user_info = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "user_type": user.user_type,
                "reports": [],
                "purchases": [],
            }

            for report in user.reports.all():
                user_info["reports"].append(
                    {"id": report.id, "title": report.title, "status": report.status}
                )

            for purchase in user.purchases.all():
                user_info["purchases"].append(
                    {
                        "id": purchase.id,
                        "item": purchase.item,
                        "price": float(purchase.price),
                    }
                )

            data["users"].append(user_info)

        return data

    def get(self, request):
        data = self.__gather_data_as_dict()
        return Response(data, status=200)
