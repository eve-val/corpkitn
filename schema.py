from sqlalchemy import Integer, String, Boolean, create_engine
from sqlalchemy.schema import Table, Column, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
Session = sessionmaker()

def init_db(path):
    engine = create_engine('sqlite:///%s' % path)
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)

account_api_m2m = Table('account_key_m2m', Base.metadata,
    Column('account_pk', String, ForeignKey('account.account')),
    Column('api_key_pk', Integer, ForeignKey('api_key.keyid'))
)

class Account(Base):
    __tablename__ = 'account'

    account = Column(String, primary_key=True)
    is_admin = Column(Boolean)

    keys = relationship("ApiKey",
                        backref="accounts",
                        secondary=account_api_m2m)

    def __init__(self, account, is_admin=False):
        self.account = account
        self.is_admin = is_admin

    def __repr__(self):
        return "Account('%s', %s)" % (self.account, self.is_admin)

class ApiKey(Base):
    __tablename__ = 'api_key'

    keyid = Column(Integer, primary_key=True)
    vcode = Column(String, nullable=False)
    last_check = Column(Integer)

    characters = relationship("Character",
                              backref="api",
                              cascade="all, delete, delete-orphan")

    def __init__(self, key_id, vcode, last_check=None):
        self.keyid = key_id
        self.vcode = vcode
        self.last_check = last_check

    def __repr__(self):
        return "ApiKey('%s')" % self.keyid

class Character(Base):
    __tablename__ = 'character'

    name = Column(String, primary_key=True)
    corp_name = Column(String, nullable=False)
    api_key_id = Column(Integer, ForeignKey('api_key.keyid'))

    def __init__(self, name, corp_name):
        self.name = name
        self.corp_name = corp_name

    def __repr__(self):
        return "Character('%s', '%s')" % (self.name, self.corp_name)

# vim: ts=4 sts=4 sw=4 et :
