from __future__ import annotations

from typing import TYPE_CHECKING

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from app.core.configurations import settings
from app.domain.services.notification_service import NotificationService
from scripts.run_yoyo_migrations import logger

if TYPE_CHECKING:
    from app.domain.services.product_update_event import ProductUpdateEvent


class AwsSESNotificationService(NotificationService):

    def __init__(self, region_name: str | None = None) -> None:
        self.client = boto3.client(
            "ses",
            region_name=region_name or settings.SES_REGION_NAME,
        )

    def notify(
        self,
        sender_email: str,
        recipient_email: str,
        event: ProductUpdateEvent,
    ) -> None:
        subject = f"Product updated: {event.product_id}"
        body_text = (
            f"The product with ID: {event.product_id} was updated.\n"
            f"Updated fields: {', '.join(event.changes)}"
        )

        try:
            self.client.send_email(
                Source=sender_email,
                Destination={"ToAddresses": [recipient_email]},
                Message={
                    "Subject": {"Data": subject},
                    "Body": {"Text": {"Data": body_text}},
                },
            )

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code")
            error_message = e.response.get("Error", {}).get("Message")
            logger.info(f"SES ClientError [{error_code}]: {error_message}")

        except BotoCoreError as e:
            logger.info(f"SES BotoCoreError: {e}")
