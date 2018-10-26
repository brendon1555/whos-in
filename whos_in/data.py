import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):

    __tablename__ = 'users'
    name = Column(String(255), primary_key=True)
    is_in = Column(Boolean(), default=False)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# connection
engine = create_engine('sqlite:///whos_in.db')

# create metadata
Base.metadata.create_all(engine)

# create session
Session = sessionmaker(bind=engine)
session = Session()


from sqlalchemy.ext.declarative import DeclarativeMeta
class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)