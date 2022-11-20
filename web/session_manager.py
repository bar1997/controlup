from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///127.0.0.1', echo=True)

Session = sessionmaker(bind=engine)


class SessionManager(object):
    def __init__(self):
        self.session = Session()
