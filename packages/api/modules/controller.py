from flask import Blueprint, request, abort
from modules import printer
from .parsers import parse_invoice, parse_credit_note
from json import dumps, loads
from .auth import requires_auth

api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/print/invoice', methods=['POST'])
@requires_auth
def print_invoice():
    json_req = loads(request.json)
    string = parse_invoice(json_req['invoice'])
    printer.write_string_to_printer(string)
    return dumps({"printed_invoice": string})


@api_blueprint.route('/print/credit_note', methods=['POST'])
@requires_auth
def print_credit_note():
    json_req = loads(request.json)
    string = parse_credit_note(json_req['credit_note'])
    printer.write_string_to_printer(string)
    return dumps({"printed_credit_note": string})


@api_blueprint.route('/print/report/<report>', methods=['POST'])
@requires_auth
def print_report(report):
    if report not in ['x', 'y']:
        abort(400)

    printer.write_string_to_printer('I0X' if report == 'x' else 'I0Z')
    return dumps(f'{report.upper()} Report printed successfully')
