from uuid import uuid4, UUID

from sqlalchemy import Column, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Item(Base):
    __tablename__ = "item"

    id: Mapped[str] = mapped_column(primary_key=True, unique=True)
    description: Mapped[str]

    search_results = relationship("SearchResult", back_populates="item")

    def __repr__(self):
        return f"<Item (id={self.id}, description={self.description}) >"


class SearchResult(Base):
    __tablename__ = "search_result"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    search_id: Mapped[str] = mapped_column(nullable=False)
    similarity = Column(Float, nullable=False)

    # relationships
    item_id: Mapped[str] = mapped_column(ForeignKey("item.id"), nullable=False)
    item = relationship("Item", back_populates="search_results")
