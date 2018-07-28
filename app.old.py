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


init_db()

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

@app.route('/')
@app.route('/<page>')
@requires_auth
def index(page=1):
    invoice_list, page_context = cloud_accounting.get_invoice_list(page)
    json.dumps(invoice_list)
    printed_invoices = set([f.zoho_id for f in db_session.query(Factura).all()])
    return render_template('index.html',
        invoices=invoice_list, printed=printed_invoices, page_context=page_context)

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
    factura = cloud_accounting.get_invoice(invoice_id)
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

        # Get the invoice from remote server
        invoice = cloud_accounting.get_invoice(invoice_id)
        nota_credito = NotaDeCredito(fiscal_id, invoice)
        nota_credito.print()

        # Return response
        return jsonify(data=str(nota_credito))

@app.route('/facturas', methods = ['GET'])
@requires_auth
def get_facturas():
    return jsonify(data=cloud_accounting.get_invoice_list())

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

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
