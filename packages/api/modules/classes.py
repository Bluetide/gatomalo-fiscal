from math import modf, floor
import re


class Product():
    TAX = {0: ' ', 1: '!', 2: '"', 3: "3"}

    def __init__(self, description='', quantity='1', tax='0', amount=''):
        self.description = description
        self.quantity = quantity
        self.tax = self.TAX[int(tax)]
        self.dollars = self.__dollars(amount)
        self.cents = self.__cents(amount)

    def __dollars(self, amount):
        return modf(amount)[1]

    def __cents(self, amount):
        return floor(modf(amount)[0]*100)

    def __str__(self):
        return "%s%08d%02d%05d%03d%s" % (self.tax, self.dollars, self.cents, self.quantity, 0, self.description)


class Client:
    def __init__(self, company='', address='', ruc=''):
        regex = re.compile(r"\n\s?")
        self.company = self.__company(regex.sub(", ", company))
        self.address = self.__address(regex.sub(", ", address))
        self.ruc = self.__ruc(regex.sub(", ", ruc))

    def __company(self, company):
        return "jS%s" % company

    def __address(self, address):
        return "j1Direccion: %s" % address

    def __ruc(self, ruc):
        return "jR%s" % ruc

    def __str__(self):
        return "\n".join([self.company, self.address, self.ruc])


class InvoiceParser():
    def __init__(self, invoice_dict):
        self.code = self.__code(invoice_dict['code'])
        self.client = self.__client(invoice_dict['client'])
        self.products = self.__products(invoice_dict['products'])

    def __client(self, client):
        return str(Client(**client))

    def __products(self, products):
        return "\n".join([str(Product(**product)) for product in products])

    def __code(self, code):
        return "@COD:%s" % code

    def __str__(self):
        return "\n".join([self.client, self.code, self.products, "3", "101\r\n"])


class CreditNoteParser():
    def __init__(self, credit_note_dict):
        self.invoice_id = self.__invoice_id(
            id=credit_note_dict.get('invoice_id')
        )
        self.code = self.__code(credit_note_dict.get('code', 1))
        self.client = self.__client(credit_note_dict['client'])
        self.products = self.__products_string(credit_note_dict['products'])

    def __invoice_id(self, id=1):
        return "jFTFBX110002122-%08d" % int(id if id is not None else 1)

    def __client(self, client):
        return str(Client(**client))

    def __code(self, code):
        return "ACOD:%s" % code

    def __products_string(self, products):
        return "\n".join([f"d{str(Product(**product))}" for product in products])

    def __str__(self):
        return "\n".join([
            self.invoice_id,
            self.client,
            self.code,
            self.products,
            '3',
            'q-000000000',
            "101\r\n"
        ])
