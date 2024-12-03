import logging
from typing import TYPE_CHECKING

import requests
from celery import shared_task
from django.apps import apps
from django.db import transaction

if TYPE_CHECKING:
    from api.models import Purchase, Report, User

logger = logging.getLogger(__name__)


def login_and_fetch_data(endpoint_login, credentials, endpoint_data):
    try:
        login_response = requests.post(endpoint_login, params=credentials, verify=False)
        login_response.raise_for_status()

        token = login_response.json().get("access_token")

        if token:
            headers = {"Authorization": f"Bearer {token}"}
            data_response = requests.get(endpoint_data, headers=headers, verify=False)
            data_response.raise_for_status()

            return data_response.json()
        else:
            logger.error("Token não foi obtido do login.")
            return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na tarefa de login e busca de dados: {e}")
        return None


def store_user_and_purchases(data):
    user_data = data["data"]
    user_name = user_data["name"]
    user_email = user_data["email"]
    purchases_data = user_data.get("purchases", [])

    User: "User" = apps.get_model("api", "User")
    Purchase: "Purchase" = apps.get_model("api", "Purchase")

    with transaction.atomic():
        user, created = User.objects.get_or_create(
            email=user_email, defaults={"name": user_name, "user_type": "user"}
        )

        for purchase_data in purchases_data:
            Purchase.objects.get_or_create(
                id=purchase_data["id"],
                defaults={
                    "user": user,
                    "item": purchase_data["item"],
                    "price": purchase_data["price"],
                },
            )


def store_admin_and_reports(data):
    admin_data = data["data"]
    admin_name = admin_data["name"]
    admin_email = admin_data["email"]
    reports_data = admin_data.get("reports", [])

    User: "User" = apps.get_model("api", "User")
    Report: "Report" = apps.get_model("api", "Report")

    with transaction.atomic():
        admin, created = User.objects.get_or_create(
            email=admin_email, defaults={"name": admin_name, "user_type": "admin"}
        )

        for report_data in reports_data:
            Report.objects.get_or_create(
                id=report_data["id"],
                defaults={
                    "user": admin,
                    "title": report_data["title"],
                    "status": report_data["status"],
                },
            )


@shared_task
def task_fetch_user_data():
    endpoint_login = "https://api-onecloud.multicloud.tivit.com/fake/token"
    credentials = {"username": "user", "password": "L0XuwPOdS5U"}
    endpoint_data = "https://api-onecloud.multicloud.tivit.com/fake/user"

    json = login_and_fetch_data(endpoint_login, credentials, endpoint_data)
    logger.info(json)

    store_user_and_purchases(json)


@shared_task
def task_fetch_admin_data():
    endpoint_login = "https://api-onecloud.multicloud.tivit.com/fake/token"
    credentials = {"username": "admin", "password": "JKSipm0YH"}
    endpoint_data = "https://api-onecloud.multicloud.tivit.com/fake/admin"

    json = login_and_fetch_data(endpoint_login, credentials, endpoint_data)
    logger.info(json)

    store_admin_and_reports(json)
