import requests
from requests.structures import CaseInsensitiveDict
import json
from datetime import date

base_URL = 'https://testing2.bacan.uy/index.php/rest/'
username = 'adminbacan1'
password = 'pqWE922.22'


def get_token(username, password):

    payload = {'username': username, 'password': password}
    headers = {'Content-Type': 'application/json'}
    r = requests.request('POST', base_URL + 'default/V1/integration/admin/token', params = payload, headers=headers)
    token = r.text
    #print(r.content)

    print("get_token")
    return(token)

def get_ordenes(status, token):

    payload = {'searchCriteria[filter_groups][0][filters][0][field]': 'status', 
    'searchCriteria[filter_groups][0][filters][0][value]': status,
    'searchCriteria[sortOrders][0][field]' : 'increment_id', 
    'fields': 'items[increment_id,entity_id]',

    #para restringir cantidad de resultados
    'searchCriteria[filter_groups][0][filters][0][field]' : 'entity_id', 
    'searchCriteria[filter_groups][0][filters][0][value]' : '5356', 
    'searchCriteria[filter_groups][0][filters][0][condition_type]' : 'gt'
    }

    headers = CaseInsensitiveDict()  
    headers["Content-Type"] = "application/json"  
    headers["Authorization"] = 'Bearer '+ token  


    r = requests.request('GET', base_URL + 'default/V1/orders', headers=headers, params=payload) 

    #print(r.url)   #Final URL location of Response.

    print("get_ordenes")
    return(r)  #devuleve la orden pendiente

def get_detalle_order(id, token):

    payload = {'searchCriteria[sortOrders][0][field]': 'increment_id', 
    'fields': 'items[increment_id,entity_id]', 
    'searchCriteria[sortOrders][0][field]' : 'increment_id', 
    'fields': 'customer_firstname,customer_lastname,customer_taxvat,base_currency_code,items[name,qty_ordered,sku,item_id,product_id,original_price,price,row_total,row_total_incl_tax,tax_percent],billing_address,payment[method],extension_attributes[shipping_assignments[shipping[address]]]'
    }

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = 'Bearer '+ token

    #print(headers)

    r = requests.request('GET', base_URL + 'default/V1/orders/'+id, headers=headers, params=payload)
    #print(r.url)
    
    data = r.json()

    file_name = str(id)+str('.json')

    with open(file_name, 'w') as f:  #abre el archivo que tiene ese nombre--> lo abre para poder escribir en el
        json.dump(data, f)

    #print(r.content)

    print("get_detalle_order")   
    return (r)

def alta_publicaciones(nombre_archivo, token):

    publicacion_a_agregar = open(nombre_archivo, "r")  #abre el archivo en forma de lectura
    content_a_agregar = publicacion_a_agregar.read()   #ejecuta la aciion de leer el archivo abierto anteriormente
    jsondecoded = json.loads(content_a_agregar)   #decodificamos el json

    payload = {}

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = 'Bearer '+ token

    body = jsondecoded

    r = requests.request('POST', base_URL + 'default/V1/products', headers=headers, json=body, params=payload)
    print("alta_publicaciones")

def update_stock(sku, nombre_archivo, token):

    stock_a_modificar = open(nombre_archivo, "r")
    content_a_modificar = stock_a_modificar.read()
    jsondecoded = json.loads(content_a_modificar)

    payload = {}

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = 'Bearer '+ token

    body = jsondecoded

    r = requests.request('PUT', base_URL + 'default/V1/products/' + sku +'/stockItems/1' , headers=headers, json=body, params=payload)
    print("update_stock")

def update_price(nombre_archivo, token):

    precio_a_modificar = open(nombre_archivo, "r")
    content_a_modificar = precio_a_modificar.read()
    jsondecoded = json.loads(content_a_modificar)

    payload = {}

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = 'Bearer '+ token

    body = jsondecoded

    r = requests.request('POST', base_URL + 'default/V1/products/base-prices' , headers=headers, json=body, params=payload)
    print("update_price")

def get_new_customers(token):
    today = date.today()
    payload = {'searchCriteria[filter_groups][0][filters][0][field]' : 'created_at', 
    'searchCriteria[filter_groups][0][filters][0][value]' : str(today) + ' 00:00:00', 
    'searchCriteria[filter_groups][0][filters][0][condition_type]' : 'gt'}

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = 'Bearer '+ token

    r = requests.request('GET', base_URL + 'default/V1/customers/search', headers=headers, params=payload)

    print("get_new_customers")
    #print(r.content)

    return r

#def update_imagen(datos, token):




if __name__ == "__main__":

    t = get_token(username, password)
    token = t.replace('"', '')

    ordenes_pendientes = get_ordenes('processing', token)

    for (k, v) in ordenes_pendientes.json().items():
        #print(type(v))
        for linea in v:
            detalle_orden = get_detalle_order(str(linea['entity_id']), token)
            #print(linea['entity_id'])


    #alta_publicaciones("base_de_datos/publicacion_nueva.json", token)

    #update_stock("11038" ,"base_de_datos/stock_a_modificar.json", token)

    #update_price("base_de_datos/precio_a_modificar.json", token)

    #get_new_customers(token)




