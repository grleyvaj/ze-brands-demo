from app.core.configurations import settings
from app.domain.enums.code_enum import ErrorCodeEnum
from app.domain.exceptions.data_validation_exception import DataValidationError
from app.domain.models.product import Product
from app.domain.repositories.brand_repository import BrandRepository
from app.domain.repositories.product_repository import ProductRepository
from app.domain.services.notification_service import NotificationService
from app.domain.services.product_update_event import ProductUpdateEvent
from app.domain.use_cases.products.edit.product_update_input import ProductUpdateInput


class ProductUpdateUseCase:

    def __init__(
        self,
        product_repository: ProductRepository,
        brand_repository: BrandRepository,
        notification_service: NotificationService,
    ) -> None:
        self.product_repository = product_repository
        self.brand_repository = brand_repository
        self.notification_service = notification_service

    def update_product(
        self,
        product_id: str,
        update_input: ProductUpdateInput,
    ) -> Product:
        self._apply_business_validation(product_id, update_input)
        self._notify_changes(product_id, update_input)
        return self.product_repository.update(
            product_id=product_id,
            product_update=update_input,
        )

    def _apply_business_validation(
        self,
        product_id: str,
        update_input: ProductUpdateInput,
    ) -> None:
        if not self.brand_repository.exists_by_id(update_input.brand_id):
            raise DataValidationError(
                code=ErrorCodeEnum.BRAND_NOT_FOUND,
                location=["brand_id"],
                message=f"Brand with ID '{update_input.brand_id}' not found",
            )

        product_by_sku = self.product_repository.find_by_sku(update_input.sku)
        if product_by_sku and product_by_sku.id != product_id:
            raise DataValidationError(
                code=ErrorCodeEnum.ALREADY_EXIST_PRODUCT_SKU,
                location=["sku"],
                message=f"Product with SKU '{update_input.sku}' already exists",
            )

    def _notify_changes(
        self,
        product_id: str,
        update_input: ProductUpdateInput,
    ) -> None:
        existing_product = self.product_repository.find_by_id(product_id)
        if not existing_product:
            return

        changes = {}
        if existing_product.name != update_input.name:
            changes["name"] = {
                "old": existing_product.name,
                "new": update_input.name,
            }
        if existing_product.sku != update_input.sku:
            changes["sku"] = {
                "old": existing_product.sku,
                "new": update_input.sku,
            }
        if existing_product.price != update_input.price:
            changes["price"] = {
                "old": existing_product.price,
                "new": update_input.price,
            }
        if existing_product.brand_id != update_input.brand_id:
            changes["brand_id"] = {
                "old": existing_product.brand_id,
                "new": update_input.brand_id,
            }

        if changes:
            event = ProductUpdateEvent(
                product_id=product_id,
                changes=changes,
            )
            self.notification_service.notify(
                sender_email=settings.SES_SENDER_EMAIL,
                recipient_email=settings.SES_RECIPIENT_EMAIL,
                event=event,
            )
