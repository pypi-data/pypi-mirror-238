from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)

from ...database import Base


class OCRJobModel(Base):
    __tablename__ = "ocr_jobs"

    id = Column(Integer, primary_key=True)
    job_id = Column(String(128), nullable=False)
    bucket_name = Column(String(128), nullable=False)
    key_name = Column(String(256), nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
