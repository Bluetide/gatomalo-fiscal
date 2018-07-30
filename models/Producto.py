from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import Sequence
from sqlalchemy.types import Unicode
from models.database import Base
from models.database import db_session
from modules import printer
from decimal import Decimal

class Producto:

    def __init__(self, nombre,cantidad,tasa,precio, descuento = None):
        self.nombre = nombre
        self.tasa = tasa

        # Convert to string and then Decimal to avoid Floating Point imprecision
        self.cantidad = Decimal(str(cantidad))
        self.precio = Decimal(str(precio))

        # Parse "discount" field
        if descuento is None:
            #No Discount
            self.descuento = Decimal('0')
        elif "%" in str(descuento):
            # Percentage discount
            percent = Decimal(str(descuento).replace("%", ''))
            self.descuento = round(self.precio*(percent/100), 2)
        else:
            # Absolute value discount
            self.descuento = round(Decimal(str(descuento)), 2)

    def get_tasa(self):
        return self.tasa
        # if self.tasa == 0:
        #     return " "
        # elif self.tasa == 1:
        #     return "!"
        # elif self.tasa == 2:
        #     return "\""
        # elif self.tasa == 3:
        #     return "3"

    def get_descuento(self):
        return "q-%09d" % self.descuento.shift(2)

    # Used for Not Fiscal documents. Output is unformatted text.
    def simple_output(self):

        # Attributes to export
        output_array = [
            self.nombre,
            str(self.cantidad),
            '${:,.2f}'.format(self.precio)
        ]

        # Add discount if it exists
        if (self.descuento):
            output_array.append("-" + str(self.descuento))

        return ' '.join(output_array)

    def __str__(self):
        price_as_cents = str(round(self.precio,2))
        if self.descuento > 0:
          return "%s%010d%05d%03d%s\n%s" % ('@PrintLineItem|',self.get_tasa(),price_as_cents,self.cantidad,0,self.nombre,self.get_descuento())
        else:
          return "\n".join(['@PrintLineItem|'+ self.nombre[:20] + '|' + str(self.cantidad) + '|'+ price_as_cents[:11] + '|' + self.get_tasa() + '|M'])
