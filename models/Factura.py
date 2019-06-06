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
from time import sleep
from decimal import Decimal

class Factura(Base):
    __tablename__ = 'facturas'

    id = Column(Integer, primary_key=True)
    zoho_id = Column(Unicode)
    print_date = Column(DateTime)

    def __init__(self, cloud_id, cliente_object, descuento = 0):
        self.cliente = cliente_object
        self.descuento = Decimal(str(descuento))
        self.zoho_id = cloud_id

    def print(self):
        printer.write_string_to_printer(str(self))
        sleep(5)
        #printer.write_string_to_printer(str(self.print_no_fiscal()))
        self.print_date = datetime.now()
        db_session.add(self)
        db_session.commit()

    def codigo(self):
        return "@%s" % self.zoho_id[-35:]

    def get_descuento(self):
        return "q-%09d" % self.descuento.shift(2)

    def create_productos_from_dict(self,productos):
        self.productos = [Producto(producto['nombre'],producto['cantidad'],producto['tasa'],producto['precio']) for producto in productos]
        return self.productos

    def get_productos_str(self):
        return "\n".join([str(producto) for producto in self.productos])

    def get_total(self):
        return sum([p.precio * p.cantidad for p in self.productos]) - self.descuento

    def has_nota_de_credito(self):
        if hasattr(self, 'nota_de_credito'):
            return True
        else:
            return False

    def to_json(self):
        json = {'cliente':self.cliente.empresa,'productos' : [p.nombre for p in self.productos], 'total':float(self.get_total()), 'nota_de_credito': self.has_nota_de_credito() }
        return json

    def __str__(self):
        factura = "\n".join([str(self.cliente),self.codigo(),self.get_productos_str(),"3", self.get_descuento(),"101\r\n"])
        return factura

    def print_no_fiscal(self):
        print(self)
        lines = []
        lines.append( '800' + self.cliente.empresa)
        lines.extend(['800' + p.simple_output() for p in self.productos])
        if self.descuento != 0:
            lines.append( '800descuento: ${:,.2f}'.format(self.descuento))
        lines.append( '80¡total: ${:,.2f}'.format(self.get_total()))
        lines.append( '810FIN\r\n')
        return '\n'.join(lines)

    def para_nota(self):
        factura = "\n".join([str(self.cliente),self.get_productos_str(),"101\r\n"])
        return factura
