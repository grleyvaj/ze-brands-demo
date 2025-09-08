from sqlalchemy import exists, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.logging_config import logger
from app.domain.models.brand import Brand
from app.domain.repositories.brand_repository import BrandRepository
from app.domain.use_cases.brands.create.brand_create_input import BrandCreateInput
from app.infrastructure.db.database_repository import DatabaseRepository
from app.infrastructure.entity.brand_entity import BrandEntity
from app.infrastructure.persistence.mappers.brand_mapper import BrandMapper


class PostgresBrandRepository(BrandRepository):

    def __init__(self, database_repository: DatabaseRepository) -> None:
        self.database_repository = database_repository

    def create(self, brand: BrandCreateInput) -> Brand:
        session = self.database_repository.get_db_session()
        try:
            brand_entity = BrandMapper.map_to_entity(brand)
            session.add(brand_entity)
            session.commit()
        except SQLAlchemyError:
            logger.exception("Error creating brand")
            session.rollback()
            raise

        return BrandMapper.map_to_model(brand_entity)

    def exists_by_id(self, brand_id: str) -> bool:
        session = self.database_repository.get_db_session()
        try:
            stmt = select(exists().where(BrandEntity.id == brand_id))
            return session.scalar(stmt)
        except SQLAlchemyError:
            logger.exception(f"Error checking existence of brand with ID: {brand_id}")
            raise

    def exists_by_name(self, name: str) -> bool:
        session = self.database_repository.get_db_session()
        try:
            stmt = select(exists().where(BrandEntity.name == name))
            return session.scalar(stmt)
        except SQLAlchemyError:
            logger.exception(f"Error checking existence of brand with name: {name}")
            raise
