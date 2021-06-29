from flask import render_template, redirect, url_for, Blueprint, request, flash
from modules import db_worker, printer
from .helpers import respond_json, parse_invoice

api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/print_invoice', methods=['POST'])
def print_invoice():
    invoice, _1, _2 = parse_invoice(request.json, db_worker.session_maker())
    try:
        # printer.write_string_to_printer(str(invoice))
        print('end')
        return respond_json(
            content={"message": "Se imprimió correctamente la factura"}
        )
    except Exception as e:
        print(e)
        return respond_json(
            err=e,
            status=500
        )


@api_blueprint.route('/print_credit_note', methods=['POST'])
def print_credit_note():
    pass
