# odoo-paraguay

[![Build Status](https://travis-ci.com/jobiols/odoo-paraguay.svg?token=77F3WzCbdXWpLDSsuTxX&branch=13.0)](https://travis-ci.com/jobiols/odoo-paraguay)

Localizacion de Odoo - Paraguay v13

## El repositorio tiene los siguientes branch que trabajan de la siguiente manera;

- **13.0** Version estable de produccion.
- **master** desarrollos inestables para la siguiente version de odoo.
- **13.0.nombre-branch#nro-issue** branch donde se esta desarrollando / corrigiendo un issue

## Sobre los modulos

- **l10n_py** : Plantillado de las cuentas contables impuestos etc de la localizacion
- **l10n_py_invoice_document** : Definicion de tipos de documento facturas, notas de credito, etc
- **l10n_py_reports** : Documentos a imprimir como ser facturas, Definicion de tipos de documento
- **l10n_py_vat_book** : Libros de IVA

## Futuros modulos
- **l10n_py_pos** : Punto de Venta
- **l10n_py_account_accountant** : Contabilidad
- **l10n_py_purchase** : Compras
- **l10n_py_sale** : Ventas
- **l10n_py_web_site** : Sitio Web
- **l10n_py_mrp** : Fabricacion

## Testing Server

http://ec2-54-233-138-43.sa-east-1.compute.amazonaws.com:8069

- Database: TecnoproEV13
- Email: tecnopro@tecnopro.com.py 
- Pass: 1234567890

- Documentacion de timbrado:
https://drive.google.com/drive/folders/1gIXyOiICRADUTDMV43tNosxwJwEz_292?usp=sharing

- Directorio de modulos
/odoo/custom/addons

- Log
 tail -f /var/log/odoo/odoo-server.log
