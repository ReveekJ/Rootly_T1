import uuid
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from backend.db.db_config import Base


class LogModel(Base):
    __tablename__ = 'logs'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    user_id: Mapped[str]
    log_analistics: Mapped[str]