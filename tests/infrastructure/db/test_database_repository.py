from unittest.mock import MagicMock, patch

import pytest

from app.infrastructure.db.database_repository import DatabaseRepository


class TestDatabaseRepository:

    def test_get_db_session_returns_same_instance(self) -> None:
        repo = DatabaseRepository()

        with patch(
            "app.infrastructure.db.database_repository.SessionLocal",
        ) as mock_session_local:
            mock_session = MagicMock()
            mock_session_local.return_value = mock_session

            session1 = repo.get_db_session()
            session2 = repo.get_db_session()

            assert session1 is session2
            mock_session_local.assert_called_once()

    def test_commit_success(self) -> None:
        repo = DatabaseRepository()
        mock_session = MagicMock()
        repo._session = mock_session

        repo.commit()

        mock_session.commit.assert_called_once()
        mock_session.rollback.assert_not_called()

    def test_commit_rollback_on_exception(self) -> None:
        repo = DatabaseRepository()
        mock_session = MagicMock()
        repo._session = mock_session
        mock_session.commit.side_effect = Exception("DB error")

        with pytest.raises(Exception, match="DB error"):
            repo.commit()

        mock_session.rollback.assert_called_once()

    def test_add_and_commit(self) -> None:
        repo = DatabaseRepository()
        mock_session = MagicMock()
        repo._session = mock_session

        entity = object()
        repo.add_and_commit(entity)

        mock_session.add.assert_called_once_with(entity)
        mock_session.commit.assert_called_once()

    def test_rollback(self) -> None:
        repo = DatabaseRepository()
        mock_session = MagicMock()
        repo._session = mock_session

        repo.rollback()

        mock_session.rollback.assert_called_once()

    def test_close(self) -> None:
        repo = DatabaseRepository()
        mock_session = MagicMock()
        repo._session = mock_session

        repo.close()

        mock_session.close.assert_called_once()
        assert repo._session is None
