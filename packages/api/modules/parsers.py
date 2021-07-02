from .classes import InvoiceParser, CreditNoteParser


def parse_invoice(invoice_dict):
    return str(InvoiceParser(invoice_dict))


def parse_credit_note(credit_note_dict):
    return str(CreditNoteParser(credit_note_dict))
