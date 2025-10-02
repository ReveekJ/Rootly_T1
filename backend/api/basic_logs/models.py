from datetime import datetime
import uuid
from uuid import UUID

from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.api.basic_logs.enums import LogLevel, LogSection
from backend.db.db_config import Base


class LogLineModel(Base):
    __tablename__ = 'log_lines'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4())

    timestamp: Mapped[str] = mapped_column(nullable=False)
    level: Mapped[str] = mapped_column(nullable=False)
    section: Mapped[LogSection] = mapped_column(Enum(LogSection), nullable=True)
    tf_req_id: Mapped[str] = mapped_column(nullable=True)
    request_body: Mapped[str] = mapped_column(nullable=True)
    response_body: Mapped[str] = mapped_column(nullable=True)
    raw: Mapped[str] = mapped_column(nullable=False)

    log_id: Mapped[UUID] = mapped_column(ForeignKey("logs.id"))
    log: Mapped["LogModel"] = relationship("LogModel", back_populates="lines")


class LogModel(Base):
    __tablename__ = 'logs'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4())
    name: Mapped[str] = mapped_column(default=str(datetime.now()))
    user_id: Mapped[str]

    lines: Mapped[list["LogLineModel"]] = relationship(
        "LogLineModel",
        back_populates="log",
    )
