from flask import render_template, redirect, url_for, Blueprint, request, flash
from modules import db_worker, printer
from .helpers import respond_json, parse_invoice
from .modules.parsers import parse_invoice, parse_credit_note
from json import dumps

api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/print_invoice', methods=['POST'])
def print_invoice():
    string = parse_invoice(request.json['invoice'])
    printer.write_string_to_printer(string)
    return dumps({"printed_invoice": string})


@api_blueprint.route('/print_credit_note', methods=['POST'])
def print_credit_note():
    string = parse_credit_note(request.json)
    printer.write_string_to_printer({"printed_credit_note": string})
