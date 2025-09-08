from __future__ import annotations

from sqlalchemy import exists, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.logging_config import logger
from app.domain.enums.code_enum import ErrorCodeEnum
from app.domain.exceptions.resource_not_found_exception import ResourceNotFoundError
from app.domain.models.product import Product, ProductView
from app.domain.repositories.product_repository import ProductRepository
from app.domain.use_cases.products.create.product_create_input import ProductCreateInput
from app.domain.use_cases.products.edit.product_update_input import ProductUpdateInput
from app.infrastructure.db.database_repository import DatabaseRepository
from app.infrastructure.entity.product_entity import ProductEntity
from app.infrastructure.entity.product_view_entity import ProductViewCountEntity
from app.infrastructure.persistence.mappers.product_mapper import ProductMapper


class PostgresProductRepository(ProductRepository):

    def __init__(self, database_repository: DatabaseRepository) -> None:
        self.database_repository = database_repository

    def create(self, product_create: ProductCreateInput) -> Product:
        session = self.database_repository.get_db_session()
        try:
            product_entity = ProductMapper.map_to_entity(product_create)
            session.add(product_entity)
            session.commit()
        except SQLAlchemyError:
            logger.exception("Error creating product")
            session.rollback()
            raise

        return ProductMapper.map_to_model(product_entity)

    def exists_by_sku(self, sku: str) -> bool:
        session = self.database_repository.get_db_session()
        try:
            stmt = select(exists().where(ProductEntity.sku == sku))
            return session.scalar(stmt)
        except SQLAlchemyError:
            logger.exception(f"Error checking existence of product with SKU: {sku}")
            raise

    def find_by_id(self, product_id: str) -> Product | None:
        session = self.database_repository.get_db_session()
        try:
            stmt = select(ProductEntity).where(ProductEntity.id == product_id)
            result = session.execute(stmt).scalar_one_or_none()
            return ProductMapper.map_to_model(result) if result is not None else None
        except SQLAlchemyError:
            logger.exception(f"Error getting product with ID: {product_id}")
            raise

    def find_by_sku(self, sku: str) -> Product | None:
        session = self.database_repository.get_db_session()
        try:
            stmt = select(ProductEntity).where(ProductEntity.sku == sku)
            result = session.execute(stmt).scalar_one_or_none()
            return ProductMapper.map_to_model(result) if result is not None else None
        except SQLAlchemyError:
            logger.exception(f"Error getting product with SKU: {sku}")
            raise

    def update(self, product_id: str, product_update: ProductUpdateInput) -> Product:
        session = self.database_repository.get_db_session()
        try:
            stmt = select(ProductEntity).where(ProductEntity.id == product_id)
            product_entity = session.execute(stmt).scalar_one_or_none()

            if product_entity is None:
                raise ResourceNotFoundError(
                    code=ErrorCodeEnum.PRODUCT_NOT_FOUND,
                    location=["product_id"],
                    message=f"No product found with ID: {product_id}.",
                )

            update_data = product_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(product_entity, field, value)

            session.commit()
            session.refresh(product_entity)

            return ProductMapper.map_to_model(product_entity)

        except SQLAlchemyError:
            logger.exception(f"Error updating product with ID: {product_id}")
            session.rollback()
            raise

    def delete_by_id(self, user_id: str) -> None:
        session = self.database_repository.get_db_session()
        try:
            entity = session.get(ProductEntity, user_id)
            if not entity:
                return
            session.delete(entity)
            session.commit()
        except SQLAlchemyError:
            logger.exception(f"Error deleting product with ID: {user_id}")
            session.rollback()
            raise

    def list_products(self, brand_id: str | None = None) -> list[ProductView]:
        session = self.database_repository.get_db_session()
        try:
            stmt = select(
                ProductEntity.id,
                ProductEntity.name,
                ProductViewCountEntity.view_count,
            ).join(
                ProductViewCountEntity,
                ProductViewCountEntity.product_id == ProductEntity.id,
                isouter=True,
            )

            if brand_id:
                stmt = stmt.where(ProductEntity.brand_id == brand_id)

            results = session.execute(stmt).all()

            return [
                ProductView(
                    id=prod_id,
                    name=name,
                    view=view_count or 0,
                )
                for prod_id, name, view_count in results
            ]

        except SQLAlchemyError:
            logger.exception(f"Error listing products for brand_id={brand_id}")
            raise
