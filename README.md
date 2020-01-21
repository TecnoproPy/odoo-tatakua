# odoo-paraguay

[![Build Status](https://travis-ci.com/jobiols/odoo-paraguay.svg?token=77F3WzCbdXWpLDSsuTxX&branch=13.0)](https://travis-ci.com/jobiols/odoo-paraguay)

Localizacion de Odoo - Paraguay v13

## El repositorio tiene los siguientes branch que trabajan de la siguiente manera;

- **master** Contiene los ultimos fuentes y la documentacion.
- **13.0** Contiene los modulos obtenidos del Sistema de Integracion Continua con el proceso de testing de Quality Assurance (CI/QA).
- **13.0-nightly** Contiene los modulos compilados por el Sistema de Integracion Continua (CI).
- **13.0-dev** Es la rama de desarrollo principal.
- **13.0-#** Donde "#" es el numero de issue en desarrollo. Una vez finalizado el desarrollo/arreglo del issue, se realiza el merge (union) con la rama 13.0-dev.

## Sobre los modulos

- **l10n_py** : Account Chart
- **l10n_py_invoice_document** : Definicion de tipos de documento

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
