from models.Cliente import Cliente
from models.Factura import Factura
from models.NotaDeCredito import NotaDeCredito
from models.Producto import Producto
import os
import requests
import config

zoho_url_invoices = 'https://books.zoho.com/api/v3/invoices' #RESTful URL
zoho_url_contacts = 'https://books.zoho.com/api/v3/contacts'
zoho_authtoken = config.zoho_auth
zoho_organization_id = config.zoho_org

def get_invoice_list(page):
    auth = {'authtoken':zoho_authtoken,'organization_id':zoho_organization_id, 'page': page}
    r = requests.get(zoho_url_invoices,params=auth)
    json_response = r.json()
    return json_response['invoices'], json_response['page_context']

def get_invoice_detail(post):
    url = zoho_url_invoices + "/" + post
    auth = {'authtoken':zoho_authtoken,'organization_id':zoho_organization_id}
    r = requests.get(url,params=auth)
    invoice = r.json()
    return invoice

def get_contact_detail(contact_id):
    request_url = zoho_url_contacts + "/" +  contact_id
    response = requests.get(request_url, params={
            'authtoken':zoho_authtoken,
            'organization_id':zoho_organization_id
        })
    return response.json()

def parse_cliente_from_post(post):
    empresa = post.form['factura[cliente][empresa]']
    direccion = post.form['factura[cliente][direccion]']
    telefono = post.form['factura[cliente][telefono]']
    ruc = post.form['factura[cliente][ruc]']
    return { 'empresa':empresa,'direccion':direccion,'telefono':telefono,'ruc':ruc }

def parse_productos_from_post(post):
    nombre = post.form['factura[productos][nombre]']
    cantidad = post.form['factura[productos][cantidad]']
    tasa = post.form['factura[productos][tasa]']
    precio = post.form['factura[productos][precio]']
    return { 'nombre':nombre,'cantidad':cantidad,'tasa':tasa,'precio':precio }

def parse_invoice_data(data):

    #Get variables
    customer_name = data["invoice"]["customer_name"]
    address = data["invoice"]["billing_address"]["address"]
    data["invoice"]["customer_name"]
    invoice_id = data['invoice']['invoice_id']

    # If the global discount is a percentage, parse it
    raw_discount = data['invoice']['discount']
    if isinstance(raw_discount, str):
        percentage = float(raw_discount.replace("%", ""))/100
        raw_discount = data['invoice']['sub_total'] * percentage

    # Global adjustment is calculated using both the global discount and the adjustment
    global_discount = raw_discount - data['invoice']['adjustment']

    # Try to get the extended client data for 'RUC' and phone information
    try:
        contact_id = data['invoice']['customer_id']
        raw_client = get_contact_detail(contact_id)
        client_model = parse_contact_data(raw_client)
    except Exception as e:
        # Safe defaults
        client_model = Cliente(empresa=customer_name, direccion=address)

    # Build Models
    invoice_model = Factura(invoice_id, client_model, global_discount)
    invoice_model.productos = [translate_product(p) for p in data["invoice"]["line_items"]]

    # Return the invoice Model
    return invoice_model

def parse_contact_data(raw_data):

    # Build Model
    cliente_model = Cliente(
            empresa=raw_data['contact']['contact_name'],
            direccion=raw_data['contact']['billing_address']['address']
        )

    # Parse custom fields
    for cf in raw_data['contact']['custom_fields']:
        if 'label' in cf and cf['label'] == 'Razón Social:':
            cliente_model.empresa = cf['value']
        elif 'label' in cf and cf['label'] == 'RUC:':
            cliente_model.ruc = cf['value']
        elif 'label' in cf and cf['label'] == 'DV:':
            cliente_model.dv = cf['value']

    # Parse Phone number
    for contact_person in raw_data['contact']['contact_persons']:
        if contact_person['is_primary_contact'] and 'phone' in contact_person:
            cliente_model.telefono = contact_person['phone']

    # Return
    return cliente_model


def translate_product(product):

    # Parse tax value
    if product["tax_percentage"] == 7:
        tasa = 1
    elif product["tax_percentage"] == 0:
        tasa = 0
    elif product["tax_percentage"] == 10:
        tasa = 2
    else:
        tasa = 'error'

    # Parse discount value
    if product['discount'] != 0:
        discount = product['discount']
    else:
        discount = None

    # Build item
    return Producto(
            nombre=product['name'], cantidad=product['quantity'], tasa=tasa,
            precio=product['rate'], descuento=discount
        )

def get_invoice(invoice_id):

    # Retrieve data from remote server
    raw_invoice = get_invoice_detail(invoice_id)

    # Parse and return
    return parse_invoice_data(raw_invoice)
