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
import re

class Cliente:

    def __init__(self, empresa='', direccion='', telefono='', ruc='', dv=''):

        # Remove newlines and replace with a comma and a space.
        regex = re.compile(r"\n\s?")

        self.empresa = regex.sub(", ", empresa)
        self.direccion = regex.sub(", ", direccion)
        self.telefono = regex.sub(", ", telefono)
        self.ruc = regex.sub(", ", ruc)
        self.dv = regex.sub(", ", dv)

    @classmethod
    def from_dict(self,cliente):
        return self(cliente['empresa'],cliente['direccion'],cliente['telefono'],cliente['ruc'])

    def get_empresa(self):
        return "jS%s" % self.empresa

    def get_direccion(self):
        return "j1Direccion: %s" % self.direccion

    def get_telefono(self):
        return "j2Telefono: %s" % str(self.telefono)

    def get_ruc(self):
        return "jR%s" % self.ruc

    def __str__(self):
        return "\n".join([self.get_empresa(),self.get_direccion(),self.get_telefono(),self.get_ruc()])

    def __repr__(self):
        return "\n".join([self.get_empresa(),self.get_direccion(),self.get_telefono(),self.get_ruc()])
