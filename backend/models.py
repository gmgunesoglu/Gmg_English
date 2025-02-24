from sqlalchemy import func, Index, Column, String
from sqlmodel import SQLModel, Field, Relationship, Text, CHAR
from typing import Optional, List


class ReadingUnit(SQLModel, table=True):
    __tablename__ = "reading_unit"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=1, max_length=35, nullable=False)

    reading_texts: List["ReadingText"] = Relationship(back_populates="reading_unit")

    __table_args__ = (
        Index("reading_unit_ui_1", func.md5(Column("name", String)), unique=True),
    )


class ReadingText(SQLModel, table=True):
    __tablename__ = "reading_text"

    id: Optional[int] = Field(default=None, primary_key=True)
    reading_unit_id: int = Field(foreign_key="reading_unit.id", nullable=False)
    title: str = Field(min_length=1, max_length=70, nullable=False)
    context: str = Field(sa_type=Text, nullable=False)

    reading_unit: Optional["ReadingUnit"] = Relationship(back_populates="reading_texts")
    reading_quests: List["ReadingQuest"] = Relationship(back_populates="reading_text")

    __table_args__ = (
        Index("reading_text_ui_1", func.md5(Column("context", Text)), unique=True),
        Index("reading_text_ui_2", "reading_unit_id", func.md5(Column("title", String)), unique=True),
    )


class ReadingQuest(SQLModel, table=True):
    __tablename__ = "reading_quest"

    id: Optional[int] = Field(default=None, primary_key=True)
    reading_text_id: int = Field(foreign_key="reading_text.id", nullable=False)
    quest: str = Field(min_length=5, max_length=400, nullable=False)
    option_a: str = Field(min_length=1, max_length=100, nullable=False)
    option_b: str = Field(min_length=1, max_length=100, nullable=False)
    option_c: str = Field(min_length=1, max_length=100, nullable=False)
    option_d: str = Field(min_length=1, max_length=100, nullable=False)
    correct_option: str = Field(sa_type=CHAR(1), nullable=False)
    justification : str = Field(min_length=10, max_length=500, nullable=False)

    reading_text: Optional["ReadingText"] = Relationship(back_populates="reading_quests")

    __table_args__ = (
        Index("reading_quest_ui_1", "reading_text_id", func.md5(Column("quest", String)), unique=True),
    )