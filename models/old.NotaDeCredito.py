from datetime import datetime
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import Sequence
from sqlalchemy.types import Unicode
from models.database import Base
from models.database import db_session
from modules import printer

class NotaDeCredito(Base):
    __tablename__ = 'notas_de_credito'

    id = Column(Integer, primary_key=True)
    zoho_id = Column(Unicode)
    print_date = Column(DateTime)

    def __init__(self, legacy_id, factura_object):
        self.legacy_id = int(legacy_id)
        self.factura = factura_object
        self.zoho_id = factura_object.zoho_id

    def get_factura(self):
        return "jFTFBX110002122-%08d" % self.legacy_id

    def get_productos_str(self):
        return "\n".join(['d' + str(producto) for producto in self.factura.productos])

    def print(self):
        printer.write_string_to_printer(str(self))
        self.print_date = datetime.now()
        db_session.add(self)
        db_session.commit()

    def get_descuento(self):
        return "q-%09d" % self.factura.descuento.shift(2)

    def __str__(self):
        factura = "\n".join([self.get_factura(),str(self.factura.cliente),self.get_productos_str(), "3",  self.get_descuento(),"101\r\n"])
        return factura
