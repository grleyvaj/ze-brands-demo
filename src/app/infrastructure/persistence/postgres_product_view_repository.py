from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.sqltypes import BigInteger

from app.core.logging_config import logger
from app.domain.helpers.datetime_generator import get_now_datetime
from app.domain.helpers.ulid_generator import generate_ulid
from app.domain.repositories.product_view_repository import ProductViewRepository
from app.infrastructure.db.database_repository import DatabaseRepository
from app.infrastructure.entity.product_view_entity import ProductViewCountEntity


class PostgresProductViewRepository(ProductViewRepository):

    def __init__(self, database_repository: DatabaseRepository) -> None:
        self.database_repository = database_repository

    def increment_view(self, product_id: str) -> None:
        session = self.database_repository.get_db_session()
        try:
            stmt = select(ProductViewCountEntity).where(
                ProductViewCountEntity.product_id == product_id,
            )
            view = session.execute(stmt).scalar_one_or_none()
            date_now = get_now_datetime()

            if view:
                view.view_count += 1
                view.updated_at = date_now
            else:
                view = ProductViewCountEntity(
                    id=generate_ulid(),
                    product_id=product_id,
                    view_count=BigInteger().python_type(1),
                    created_at=date_now,
                    updated_at=date_now,
                )
                session.add(view)

            session.commit()
        except SQLAlchemyError:
            logger.exception(f"Error incrementing view for product {product_id}")
            session.rollback()
            raise

    def delete_views_by_product_id(self, product_id: str) -> None:
        session = self.database_repository.get_db_session()
        try:
            session.query(ProductViewCountEntity).filter(
                ProductViewCountEntity.product_id == product_id,
            ).delete(synchronize_session=False)
            session.commit()
        except SQLAlchemyError:
            logger.exception(f"Error deleting views for product {product_id}")
            session.rollback()
            raise
