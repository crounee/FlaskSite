from sqlalchemy import create_engine
from sqlalchemy.orm import Session,sessionmaker,scoped_session,declarative_base
from sqlalchemy.engine import URL



url = URL.create('postgresql',
                 'postgres',
                 'admin',
                 'my_postgres',
                 '5432')

engine = create_engine(url)
session = scoped_session(sessionmaker(bind=engine))


Base = declarative_base()
Base.query = session.query_property()

def init_db():
    from . import models
    models.Base.metadata.create_all(engine)
    

