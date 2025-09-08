from sqlalchemy.orm import Session

from app.infrastructure.db.session import SessionLocal


class DatabaseRepository:
    """
    Base repository that manages the SQLAlchemy session and common utilities.
    """

    def __init__(self) -> None:
        self._session: Session | None = None

    def get_db_session(self) -> Session:
        if self._session is None:
            self._session = SessionLocal()
        return self._session

    def commit(self) -> None:
        try:
            self.get_db_session().commit()
        except Exception:
            self.get_db_session().rollback()
            raise

    def add_and_commit(self, entity) -> None:  # noqa: ANN001
        self.get_db_session().add(entity)
        self.commit()

    def rollback(self) -> None:
        self.get_db_session().rollback()

    def close(self) -> None:
        if self._session:
            self._session.close()
            self._session = None
