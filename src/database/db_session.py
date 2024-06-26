from sqlalchemy.orm import Session

from src.database import LocalSession


class DBSession:  # pragma: no cover
    _session: Session = None

    def create(self):
        self._session = LocalSession()

    def close(self):
        self._session.close()

    def get(self):
        return self._session

    def rollback(self):
        return self._session.rollback()
