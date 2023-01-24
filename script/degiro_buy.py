import json
import degiroapi
from degiroapi.product import Product
from degiroapi.order import Order
from degiroapi.utils import pretty_json


with open('config.cfg', 'r') as file:
    config = json.load(file)

id_identity = 'identity_jaap_oosterbroek'
identity = ToolsIdentity.identity_load(config, id_identity)


degiro = degiroapi.DeGiro()
degiro.login("username", "password")
#Logging out


product_id
degiro.buyorder(Order.Type.LIMIT, Product(products[0]).id, 3, 1, 30)
degiro.logout()