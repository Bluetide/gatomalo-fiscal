#!flask/bin/python
from flask import Flask
from flask import jsonify
from flask import request
from flask import abort
from flask import render_template
from flask import Response
from flask import request
from flask import redirect
from flask import url_for
from modules import printer
from modules import cloud_accounting
from modules import db_worker
import os
import json
from functools import wraps
from models.database import init_db
from models.database import db_session
from models.Cliente import Cliente
from models.Factura import Factura
from models.NotaDeCredito import NotaDeCredito
from models.Producto import Producto
from datetime import datetime, timedelta
from time import sleep
import config
# tinydb is like mongodb ,by: lay
from tinydb import TinyDB, Query

db = TinyDB('./db/db.json')
table = db.table("gatomalo")
# init_db()

#logger = logging.getLogger('flask')
facturas = []

app = Flask(__name__)

auth_username = config.admin_username
auth_password = config.admin_password

def check_auth(username, password):
    return username == auth_username and password == auth_password

def authenticate():
    return Response('Porfavor ingresar credenciales', 401, {'WWW-Authenticate': 'Basic realm=""'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

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

@app.route('/facturas_api', methods = ['POST'])
def make_factura():
    #print(request.json)
    session = db_worker.session_maker()
    if request.json and 'factura' in request.json:
        productos = request.json['factura']['productos']
        cliente =  request.json['factura']['cliente']
    elif request.form:
        cliente = parse_cliente_from_post(request)
        productos = parse_productos_from_post(request)
    else:
        abort(400)
    try:

        factura,productos,cliente = db_worker.create_factura(session,cliente,productos)
    except Exception as e:
            raise(e)
            session.rollback()
    printer.write_string_to_printer(str(factura))
    return str(factura)


@app.route('/')
@app.route('/<page>')
@requires_auth
def index(page=1):
    IdPrinted = []
    invoice_list, page_context = cloud_accounting.get_invoice_list(page)
    json.dumps(invoice_list)
    # printed_invoices = set([f.zoho_id for f in db_session.query(Factura).all()])
    for d in table.all():
        IdPrinted.append(d['ZohoId'])
    json.dumps(IdPrinted)
    
    return render_template('index.html',
        invoices=invoice_list, printed=IdPrinted, page_context=page_context)
# elay working to show invoice details through api cloud counting
@app.route('/info/<invoice_id>')
@requires_auth
def info(invoice_id):
    factura = cloud_accounting.get_invoice_detail(invoice_id)
    contact = cloud_accounting.get_contact_custom_detail(factura)
    json.dumps(factura)
    return render_template('show.html',data=factura, contact_invoice = contact)

@app.route('/custom_invoice') #get view
@requires_auth
def customInvoice():
    return render_template('customInvoice.html')

@app.route('/custom_invoice_api', methods = ['POST'])
@requires_auth
def customform():
        print(request.get_json())
        session = db_worker.session_maker()
        if request.json and 'factura' in request.json:
            productos = request.json['factura']['productos']
            cliente =  request.json['factura']['cliente']
        elif request.form:
            cliente = parse_cliente_from_post(request)
            productos = parse_productos_from_post(request)
        else:
            abort(400)
        try:
            factura,productos,cliente = db_worker.create_factura(session,cliente,productos)
        except Exception as e:
                raise(e)
                session.rollback()
        printer.write_string_to_printer(str(factura))
        return str(factura)
#------------------

@app.route('/test_no_fiscal/<id_test>', methods = ['POST'])
@requires_auth
def nofisca(id_test):
    id, ErrorData = cloud_accounting.get_invoice(id_test)
    if ErrorData == 'Error':
        json.dumps(id)
        return jsonify(data=id)
    else:
        print(id)
        result = id.print_no_fiscal()
        printer.write_string_to_printer(str(result))
        return result


# end funct

@app.route('/print_today')
@requires_auth
def print_today():
    today = datetime.now().strftime('0%y%m%d')
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('0%y%m%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('0%y%m%d')
    printer.write_string_to_printer('Rs%s%s' % (today,tomorrow))
    sleep(1)
    return redirect(url_for('index'))

@app.route('/create_invoice_json/<invoice_id>')
@requires_auth
def create_invoice_json(invoice_id):
    data=cloud_accounting.get_invoice_detail(invoice_id)
    proforma_number = data["invoice"]["invoice_number"]

    return Response(data,
            mimetype='application/json',
            headers={'Content-Disposition':'attachment;filename='+proforma_number+'.json'})

@app.route('/print_gatomalo/<invoice_id>')
@requires_auth
def print_gatomalo(invoice_id):
    factura, ErrorData = cloud_accounting.get_invoice(invoice_id)
    # table.insert({"id": '156'})
    # table.all()
    if ErrorData == 'Error':
        json.dumps(factura)
        return jsonify(data=factura)
    else:
        table.insert({"ZohoId": invoice_id})
        factura.print()
        return jsonify(data=str(factura))

@app.route('/nota_credito', methods = ['POST'])
@requires_auth
def post_credit_note():
    # Make sure we have the correct arguments
    if not 'invoice_id' in request.form or not 'fiscal_id' in request.form:
        abort(400)

    #get the arguments
    invoice_id = request.form['invoice_id']
    fiscal_id = request.form['fiscal_id']

    # Make sure parameters are usable
    if not len(invoice_id) > 0 and len(fiscal_id) > 0:
        abort(400)
    else:
        # Get the invoice from remote serverer
        invoice = cloud_accounting.get_invoice(invoice_id)
        nota_credito = NotaDeCredito(fiscal_id, invoice)
        print(nota_credito)
        nota_credito.print()
        #print(jsonify(nota_credito))
        # Return response
        return jsonify(data=str(nota_credito))

@app.route('/reporteX')
@requires_auth
def reporteX():
    printer.write_string_to_printer('I0X')
    return redirect(url_for('index'))

@app.route('/reporteZ')
@requires_auth
def reporteZ():
    printer.write_string_to_printer('I0Z')
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error = error)
@app.errorhandler(500)
def internal_error(error):
    return render_template('404.html', error = error)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
