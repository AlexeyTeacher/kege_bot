from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table, \
    DateTime, MetaData, BOOLEAN, Float
from sqlalchemy.orm import relationship, declarative_base, declared_attr
from sqlalchemy.dialects.postgresql import JSONB

from config import DB_SCHEMA

metadata_obj = MetaData(schema=DB_SCHEMA)
Base = declarative_base(metadata=metadata_obj)
metadata = Base.metadata


class EGENumber(Base):
    __tablename__ = 'ege_numbers'
    id = Column(Integer, primary_key=True)
    integrator_id = Column(Integer)
    task_number = Column(Integer, comment='Номер задания')
    title = Column(String, comment='Название задания')


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    integrator_id = Column(Integer)
    number_id = Column(ForeignKey(EGENumber.id, ondelete="CASCADE"))
    name = Column(String, comment='Название раздела внутри задания')


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    integrator_id = Column(Integer)
    number_id = Column(ForeignKey(EGENumber.id, ondelete="CASCADE"))
    category_id = Column(ForeignKey(Category.id, ondelete="CASCADE"))
    text = Column(String, comment='Текст задачи')
    answer = Column(String, comment='Ответ на задачу')
    files = Column(JSONB, comment='Пути к файлам и изображениям')
    created_at = Column(DateTime(timezone=True), comment='Дата и время создания')
    updated_at = Column(DateTime(timezone=True), comment='Дата и время последнего обновления')


class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True)
    number_id = Column(ForeignKey(EGENumber.id, ondelete="CASCADE"))
    url = Column(String, comment='Ссылка на видео')


class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    number_id = Column(ForeignKey(EGENumber.id, ondelete="CASCADE"))
    url = Column(String, comment='Ссылка на текстовый разбор')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String, comment='Логин как в телеграмме')
    name = Column(String, comment='Имя как в телеграмме')
    created_at = Column(DateTime(timezone=True), comment='Дата и время создания')
    updated_at = Column(DateTime(timezone=True), comment='Дата и время последнего обновления')


class Statistic(Base):
    __tablename__ = 'statistic'
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(User.id))
    number_id = Column(ForeignKey(EGENumber.id))
    category_id = Column(ForeignKey(Category.id))
    task_id = Column(ForeignKey(Task.id))
    user_answer = Column(String, comment='Логин как в телеграмме')
    is_right = Column(Boolean, comment='Правильно ли решено')
    created_at = Column(DateTime(timezone=True), comment='Дата и время создания')

