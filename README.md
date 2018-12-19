# gatomalo
Integración opensource con factura fiscal de Panamá

## Instalación en linux
El instalador de Linux corre un script que descarga las dependencias e instala GATOMALO como un servicio de linux.
```bash
curl -sSL https://raw.githubusercontent.com/Bluetide/gatomalo-fiscal/master/setup.sh | bash
```

## Instalación usando source

1. Descargar repo e instalar dependencias
  ```bash
  git clone git@github.com:Bluetide/gatomalo-fiscal.git gatomalo
  cd gatomalo
  python3 -m venv venv
  source venv/bin/activate
  pip install --upgrade wheel pip
  pip install -r requirement.txt
  ```

2. Configurar variables de entorno
  ```bash
  export ZOHO_AUTH='xyz'
  export ZOHO_ORG='xyz'
  export ADMIN_USERNAME='admin'
  export ADMIN_PASSWORD='somethingyoucanrememberbutitsnotsohardtoguess'
  ```

6. Ejecutar gatomalo
  ```bash
  python3 app.py
  ```



## Usage Instructions
### Manual commands

1. To send a Factura JSON:
  ```bash
  curl http://localhost:5000/facturas_api --data     @fact.json -H 'Content-Type: application/json'
  ```

2. To print Reporte X y Z
  got to `cd /gatomalo` and run
  ```bash
  sudo ./tfunilx SendCmd I0X
  sudo ./tfunilx SendCmd I0Z
  ```

3. to create a Nota de Credito (devolucion)
  ```bash
   curl http://192.168.1.3:5000/nota --data     @dev.json -H 'Content-Type: application/json'
  ```
  Si la impresion fue de manera manual, hay que hacer una nota de credito con los campos necesarios, y enviarlo manual ejecutando desde la consola el comando de la impresora.

4. dev.json default format:
    factura_id: es el número que se encuentra en localhost:5000/facturas
    legacy_id: es el número impreso en la factura fiscal
    ```json
    {"nota": {
    "factura_id":104,
    "legacy_id":140
    }}
    ```

5. reporte con rango de fechas de facturas impresas
    ```
    fecha de inicio YYYMMDD
    fecha de fin yyymmdd
    RfYYYMMDDyyymmdd
    ejemplo (del 1ero de enero de 2014 hasta el 1ero de diciembre de 2014.
    sudo ./tfunilx SendCmd Rf01401010150401
    ```

## Credits
Ivan Barria Grimaldo @ibarria0

Roberto Zubieta @zubietaroberto

Carlos Raul Piad @Carlospiad

Special thanks to:
- Cat designed by <a href="http://www.thenounproject.com/misirlou">misirlou</a> from the <a href="http://www.thenounproject.com">Noun Project</a>
