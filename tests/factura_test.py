import random
import re
import unittest
from bs4 import BeautifulSoup,SoupStrainer
from decimal import Decimal
from datetime import datetime
from time import sleep
from models.models import *
from modules import db_worker

db_url = os.environ['panadata_testing']
engine = create_engine(db_url, convert_unicode=True)
Base.metadata.create_all(engine)
session_maker = sessionmaker(bind=engine)

class TestFacturacion(unittest.TestCase):

    def setUp(self):
        self.session = session_maker()
        self.productos = [{'nombre':'Arroz Por Libra','cantidad':50,'tasa':1,'precio':2.75},{'nombre':'Pollo Por Libra','cantidad':50,'tasa':1,'precio':3.75}]
        self.cliente = {'empresa':'Super Ventas SA %s' % random.randint(1,1000000000000000000000000000),'direccion':'Calle 50, Panama','telefono':5072151515,'ruc':'IU14SD5FYB823APD','id':random.randint(1,100)}
        self.json = {'factura': {'cliente':self.cliente, 'productos':self.productos}}

    def test_find_or_create_cliente_from_dict(self):
        cliente = db_worker.find_or_create_cliente_from_dict(self.session,self.cliente)
        self.assertTrue(cliente.empresa == self.cliente['empresa'])
        cliente2 = db_worker.find_or_create_cliente_from_dict(self.session,self.cliente)
        self.assertTrue(cliente == cliente2)

    def test_create_factura(self):
        factura,produtos,cliente = db_worker.create_factura(self.session,self.cliente,self.productos)
        self.assertTrue(factura.cliente_id == cliente.id)
        self.assertTrue(len(factura.productos) == 2)
        self.assertTrue(all([p.factura_id == factura.id for p in factura.productos]))

if __name__ == '__main__':
    unittest.main()
