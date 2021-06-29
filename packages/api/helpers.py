from json import dumps
from modules import db_worker, printer
from models.Cliente import Cliente as Client
from models.models import Factura as Invoice
from models.Producto import Producto as Product


def respond_json(err=None, content={}, status=200):
    if err:
        content['error'] = str(err)

    content['status'] = status

    return dumps(content)


def parse_invoice(json, session):
    client = Client.from_dict(json['factura']['cliente'])
    invoice = Invoice(client)
    products = [Product(product) for product in json['factura']['productos']]

    print(client)
    print(invoice)
    print(products)

    # invoice, products, client = db_worker.create_factura(
    # session, client, products)

    # return invoice, products, client
