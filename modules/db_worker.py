from sqlalchemy.sql import exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from models.models import *
import os
import logging

engine = create_engine(db_url, convert_unicode=True)
Base.metadata.create_all(engine)
session_maker = sessionmaker(bind=engine)
logger = logging.getLogger('db_worker')

def find_or_create_cliente_from_dict(session,cliente):
    instance = session.query(Cliente).filter(Cliente.empresa == cliente['empresa']).first()
    if not instance:
        instance = Cliente.from_dict(cliente)
        session.add(instance)
        session.commit()
    return instance

def find_factura(session,factura_id):
    instance = session.query(Factura).filter(Factura.id == factura_id).first()
    return instance

def create_factura(session,cliente,productos):
    if isinstance(cliente,dict):
        cliente = find_or_create_cliente_from_dict(session,cliente)
    if isinstance(cliente,Cliente):
        factura = Factura(cliente)
        session.add(factura)
        session.commit()
        session.refresh(factura)
        productos = factura.create_productos_from_dict(productos)
        session.add_all(productos)
        session.commit()
    return factura,productos,cliente

def create_nota(session,factura_id,legacy_id):
    nota = NotaDeCredito(factura_id,legacy_id)
    session.add(nota)
    session.commit()
    session.refresh(nota)
    return nota
   

def all_facturas(session):
    facturas = session.query(Factura).all()
    return facturas
