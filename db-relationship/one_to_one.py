# -*- coding: utf-8 -*-

import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

reload(sys)
sys.setdefaultencoding('utf-8')

engine = create_engine('sqlite:///o2o.db', echo=True)

Base = declarative_base()
db_session = scoped_session(sessionmaker(bind=engine))
Base.query = db_session.query_property()


class Parent(Base):
    __tablename__ = 'parent'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    child_id = Column(Integer, ForeignKey('child.id'))


class Child(Base):
    __tablename__ = 'child'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent = relationship('Parent', backref='child', uselist=False)


def init_db():
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///o2o.db', echo=True)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_db()
