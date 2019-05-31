from models.Cliente import Cliente
from models.Factura import Factura
from models.NotaDeCredito import NotaDeCredito
from models.Producto import Producto
import os
import requests
import config
import json

zoho_url_invoices = 'https://books.zoho.com/api/v3/invoices' #RESTful URL
zoho_url_contacts = 'https://books.zoho.com/api/v3/contacts'
zoho_authtoken = config.zoho_auth
zoho_organization_id = config.zoho_org


def get_invoice_list(page):
    auth = {'authtoken':zoho_authtoken,'organization_id':zoho_organization_id, 'page': page, 'per_page': 30}
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

def parse_info_data(data):
    data["invoice"]["customer_name"]
    data["invoice"]["invoice_id"]
    data["invoice"]["status"]
    return data
def show_info(invoice_id):
    parse_detail = parse_info_data(invoice_id)
    return parse_detail
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
    CorrectList = []
    ErrorList = []
    x = 0
    # Build a custom field dictionary
    customLabel = ["Razón Social", "RUC", "DV", "Razón Social:", "RUC:", "DV:"]
    # Build Model
    cliente_model = Cliente(
            empresa=raw_data['contact']['contact_name'],
            direccion=raw_data['contact']['billing_address']['address']
        )
    if len(raw_data['contact']['custom_fields']) != 0 :
        print("tiene datos")
        for custom in customLabel:
            for cf in raw_data['contact']['custom_fields']:
                if custom == cf['label']: 
                    CorrectList.append(cf['label'])
                    break
                else:
                    continue
        # Parse Phone number
        for contact_person in raw_data['contact']['contact_persons']:
            if contact_person['is_primary_contact'] and 'phone' in contact_person:
                cliente_model.telefono = contact_person['phone']
        
        for chico in range(len(CorrectList)):
            for grande in range(len(customLabel)):
                if CorrectList[chico] == customLabel[grande]
                    pos = 

        print(ErrorList)

        
            
        
        print(ErrorList)
        # Insert data in array to fill fields
        # for cf in raw_data['contact']['custom_fields']:
        #     if 'label' in cf and cf['label'] == 'Razón Social':
        #         cliente_model.empresa = cf['value']
        #     elif 'label' in cf and cf['label'] == 'RUC':
        #         cliente_model.ruc = cf['value']
        #     elif 'label' in cf and cf['label'] == 'DV':
        #         cliente_model.dv = cf['value']
        #     elif 'label' in cf and cf['label'] == 'Razón Social:':
        #         cliente_model.empresa = cf['value']
        #     elif 'label' in cf and cf['label'] == 'RUC:':
        #         cliente_model.ruc = cf['value']
        #     elif 'label' in cf and cf['label'] == 'DV:':
        #         cliente_model.dv = cf['value']

        if len(CorrectList) == 3:
            return cliente_model
        elif len(CorrectList) < 3:
            return CorrectList
    else:

        return 'No existen datos'


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

# def get_contact_custom_detail(data):
#     box = []
#     contact_id = data['invoice']['customer_id']
#     raw_client = get_contact_detail(contact_id)
#     print()
#     # Parse custom fields
#     for cf in raw_client['contact']['custom_fields']:
#         if 'label' in cf and cf['label'] == 'Razón Social':
#             rz = cf['value']
#             box.append({'RazonSocial': rz})
#         elif 'label' in cf and cf['label'] == 'RUC':
#             ruc = cf['value']
#             box.append({'RUC': ruc})
#         elif 'label' in cf and cf['label'] == 'DV':
#             dv = cf['value']
#             box.append({'DV': dv})
#         if 'label' in cf and cf['label'] == 'Razón Social:':
#             rz = cf['value']
#             box.append({'RazonSocial': rz})
#         elif 'label' in cf and cf['label'] == 'RUC:':
#             ruc = cf['value']
#             box.append({'RUC': ruc})
#         elif 'label' in cf and cf['label'] == 'DV:':
#             dv = cf['value']
#             box.append({'DV': dv})
        
