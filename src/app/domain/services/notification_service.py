from abc import ABC, abstractmethod

from app.domain.services.product_update_event import ProductUpdateEvent


class NotificationService(ABC):

    @abstractmethod
    def notify(
        self,
        sender_email: str,
        recipient_email: str,
        event: ProductUpdateEvent,
    ) -> None:
        raise NotImplementedError
