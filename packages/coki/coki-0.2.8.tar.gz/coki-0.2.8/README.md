# Coki: una herramienta de CLI para revisar precios de cocos

## Requisitos
- Python >= 3.9
- Cuenta en app.cocos.capital (la versión nueva, no la vieja)

## Instalación:
- Asegurarse que sea en una terminal con permisos de Administrador (así los scripts quedan en el PATH)

```
$ pip install coki 
```

### Generación de credenciales

- Una vez instalado, hay que generar el archivo `coki_credentials.txt`, que contiene el usuario y la clave de tu cuenta encriptados
  - La encriptación es con una clave default estática (es decir, todos encriptan con la misma).
  - Esto evita tener archivos guardados con la clave escrita (y encontrarlos directamente por su contenido), pero se puede hacer el proceso inverso para obtenerla
  - Se puede generar una clave de encriptación particular para mayor seguridad (todavía no está implementado)  
  
```
$ coki-gen-credentials <user> <password> [--key <encryption_key>]
```
- Con este script se genera `coki_credentials.txt`, para luego obtener la token de JWT que utiliza la api de cocos.

## Uso:

```
$ coki --help
#    usage: coki.py [-h] [--currency CURRENCY] [--plazo PLAZO] ticker
#
#    coki es una CLI para consultar precios en cocos
#
#    positional arguments:
#    ticker                Ticker a consultar
#
#    optional arguments:
#    -h, --help            show this help message and exit
#    --currency CURRENCY, -C CURRENCY
#                            Moneda del ticker. Por default lo infiere de la última letra del Ticker (pero va a fallar en       
#                            casos como AMD)
#    --plazo PLAZO, -P PLAZO
#                            Plazo de la operación

$ coki GOGLD
         GOGLD - Cedear Google inc. - USD
         Last: 2.53 - High: 2.7 - Low: 2.5 - Volume: 5,203
╭────────────────┬─────────────────┬────┬────────────────┬───────────────╮
│   Cant. compra │   Precio compra │    │   Precio venta │   Cant. venta │
├────────────────┼─────────────────┼────┼────────────────┼───────────────┤
│            193 │            2.53 │    │           2.59 │           129 │
│            776 │            2.52 │    │           2.61 │          1221 │
│              8 │            2.48 │    │           2.63 │          1097 │
│             60 │            2.47 │    │           2.66 │            27 │
│              2 │            2.46 │    │           2.67 │           100 │
╰────────────────┴─────────────────┴────┴────────────────┴───────────────╯

$ coki AMD -C ARS
         AMD - Cedear Advanced Micro Devices, Inc. - ARS
         Last: 9,960 - High: 10,180 - Low: 9,901 - Volume: 8,699
╭────────────────┬─────────────────┬────┬────────────────┬───────────────╮
│   Cant. compra │   Precio compra │    │   Precio venta │   Cant. venta │
├────────────────┼─────────────────┼────┼────────────────┼───────────────┤
│              5 │            9960 │    │       10004.50 │          4000 │
│             29 │            9959 │    │       10005.00 │             4 │
│              1 │            9958 │    │       10008.00 │           850 │
│           2500 │            9957 │    │       10013.00 │          2500 │
│             12 │            9935 │    │       10100.00 │           137 │
╰────────────────┴─────────────────┴────┴────────────────┴───────────────╯
```
