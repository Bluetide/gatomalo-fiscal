from sqlalchemy.orm import deferred
from sqlalchemy import Column, Integer, Sequence, Date, ForeignKey
from sqlalchemy.orm import relationship,backref
from sqlalchemy.types import Unicode, UnicodeText, BigInteger, Date, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
import os

from datetime import datetime
from math import modf,ceil,floor

db_url = "sqlite:///gatomalo.db"
Base = declarative_base()
engine = create_engine(db_url, convert_unicode=True, echo=True)
Base.metadata.create_all(engine)
session_maker = sessionmaker(bind=engine)

class Factura(Base):
    __tablename__ = 'facturas'
    id = Column(Integer, Sequence('factura_id_seq'), primary_key=True)
    nota_de_credito = relationship('NotaDeCredito', uselist=False, backref='factura')
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    zoho_id = Column(Integer)
    print_date = Column(DateTime)
    descuento = Column(Integer)
    productos = relationship('Producto')
    cliente = relationship('Cliente')
    created_at = Column(Date, default=datetime.now)
    updated_at = Column(Date, default=datetime.now, onupdate=datetime.now)

    def __init__(self, cliente):
        self.cliente_id = cliente.id
        self.descuento = 0

    @classmethod
    def with_productos(self, cliente, productos):
        self.cliente_id = cliente.id
        p = [Producto(self.id, producto['nombre'],producto['cantidad'],producto['tasa'],producto['precio']) for producto in productos]
        return (self,p)

    def codigo(self):
        return "@COD:%06d" % self.id

    def get_descuento(self):
        return "p-%04d" % self.descuento

    def create_productos_from_dict(self,productos):
        return [Producto(self.id, producto['nombre'],producto['cantidad'],producto['tasa'],producto['precio']) for producto in productos]

    def get_productos_str(self):
        return "\n".join([str(producto) for producto in self.productos])

    def get_total(self):
        return sum([p.precio for p in self.productos])

    def has_nota_de_credito(self):
        if self.nota_de_credito:
            return True
        else:
            return False

    def to_json(self):
        json = {'cliente':self.cliente.empresa,'productos' : [p.nombre for p in self.productos], 'total':float(self.get_total()), 'nota_de_credito': self.has_nota_de_credito() }
        return json

    def __str__(self):
        factura = "\n".join([str(self.cliente),self.codigo(),self.get_productos_str(),self.get_descuento(),"101\r\n"])
        return factura

    def para_nota(self):
        factura = "\n".join([str(self.cliente),self.get_productos_str(),"101\r\n"])
        return factura

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, Sequence('cliente_id_seq'), primary_key=True)
    empresa = Column(Unicode, unique=True)
    direccion = Column(Unicode)
    telefono = Column(Unicode)
    ruc = Column(Unicode)
    facturas = relationship('Factura')
    created_at = Column(Date, default=datetime.now)
    created_at = Column(Date, default=datetime.now)
    updated_at = Column(Date, default=datetime.now, onupdate=datetime.now)

    def __init__(self, empresa, direccion, telefono, ruc):
        self.empresa = empresa
        self.direccion = direccion
        self.telefono = telefono
        self.ruc = ruc

    @classmethod
    def from_dict(self,cliente):
        return self(cliente['empresa'],cliente['direccion'],cliente['telefono'],cliente['ruc'])

    def get_empresa(self):
        return "jS%s" % self.empresa

    def get_direccion(self):
        return "j1Direccion: %s" % self.direccion

    def get_telefono(self):
        return "j2Telefono: %s" % str(self.telefono)

    def get_ruc(self):
        return "jR%s" % self.ruc

    def __str__(self):
        return "\n".join([self.get_empresa(),self.get_direccion(),self.get_telefono(),self.get_ruc()])

    def __repr__(self):
        return "\n".join([self.get_empresa(),self.get_direccion(),self.get_telefono(),self.get_ruc()])


class NotaDeCredito(Base):
    __tablename__ = 'notas_de_credito'
    id = Column(Integer, Sequence('nota_de_credito_id_seq'), primary_key=True)
    zoho_id = Column(Unicode)
    print_date = Column(DateTime)
    factura_id = Column(Integer, ForeignKey('facturas.id'), unique=True)
    legacy_id = Column(Integer)
    created_at = Column(Date, default=datetime.now)
    updated_at = Column(Date, default=datetime.now, onupdate=datetime.now)

    def __init__(self, factura_id, legacy_id):
        self.factura_id = factura_id
        self.legacy_id = legacy_id

    def get_factura(self):
        return "jFTFBX110002122-%08d" % self.legacy_id

    def get_productos_str(self):
        return "\n".join(['d' + str(producto) for producto in self.factura.productos])

    def __str__(self):
        factura = "\n".join([self.get_factura(),str(self.factura.cliente),self.get_productos_str(),"101\r\n"])
        return factura

class Producto(Base):
    __tablename__ = 'productos'
    id = Column(Integer, Sequence('producto_id_seq'), primary_key=True)
    factura_id = Column(Integer, ForeignKey('facturas.id'))
    nombre = Column(Unicode)
    cantidad = Column(Integer)
    tasa = Column(Integer)
    precio = Column(Numeric(8,2))
    created_at = Column(Date, default=datetime.now)
    updated_at = Column(Date, default=datetime.now, onupdate=datetime.now)

    def __init__(self,factura_id,nombre,cantidad,tasa,precio):
        self.factura_id = factura_id
        self.nombre = nombre
        self.cantidad = cantidad
        self.tasa = tasa
        self.precio = precio

    def get_tasa(self):
        if self.tasa == 0:
            return " "
        elif self.tasa == 1:
            return "!"
        elif self.tasa == 2:
            return "\""
        elif self.tasa == 3:
            return "3"

    def precio_entero(self):
        return modf(self.precio)[1]

    def precio_decimal(self):
        return floor(modf(self.precio)[0]*100)

    def __str__(self):
        return "%s%08d%02d%05d%03d%s" % (self.get_tasa(),self.precio_entero(),self.precio_decimal(),self.cantidad,0,self.nombre)
