import os

if 'ZOHO_AUTH' in os.environ:
    zoho_auth = os.environ['ZOHO_AUTH']
    zoho_org = os.environ['ZOHO_ORG']
else:
    raise(Exception("Por favor ingresar credenciales de zoho en config.py o en variables de entorno ZOHO_AUTH y ZOHO_ORG"))

if 'ADMIN_USERNAME' in os.environ:
    admin_username = os.environ['ADMIN_USERNAME']
    admin_password = os.environ['ADMIN_PASSWORD']
else:
    raise(Exception("Por favor ingresar credenciales de usuario en variables de entorno ADMIN_USERNAME y PASSWORD"))

db_url="sqlite:///gatomalo.db"
