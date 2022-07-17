import sqlalchemy
from .db_session import SqlAlchemyBase


class Lesson(SqlAlchemyBase):
    __tablename__ = 'lesson1'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, unique=True)
    finnish = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    russian = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    lesson_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    contained_words = sqlalchemy.Column(sqlalchemy.String, nullable=True)