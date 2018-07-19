from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DDL
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import Sequence
from sqlalchemy import event
from sqlalchemy.ext.declarative import declarative_base
import config

SQLALCHEMY_DATABASE_URI = config.db_url

engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True,echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from models.Cliente import Cliente
    from models.Factura import Factura
    from models.NotaDeCredito import NotaDeCredito
    from models.Producto import Producto

    Base.metadata.create_all(bind=engine)
