import requests
import sys
import csv
import json
import time,string,os, datetime


# ---------------------------------------------
# Variables que se deben adaptar a cada entorno
# ---------------------------------------------
# limite: numero máx de endpoints por consulta. <=1000
limite=1000
# IP del ClearPass
ip="10.150.0.44"
# Token para consultar ClearPass
token="Bearer aaaabbbbccccddddeeeeffffgggghhhhiiiijjjjjkkkk"
# Nombre del fichero para CSV
nombre_fichero="resultado"
# ---------------------------------------------


# ---------------------------------------------
# Vamos a ignorar los mensajes de warning
# ---------------------------------------------
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# ---------------------------------------------


# ---------------------------------------------
# Samos la fecha para ponerla en el nombre del fichero
# ---------------------------------------------
now = datetime.datetime.now()
fecha_fichero = time.strftime("%Y%m%d_%H%M%S")
# ---------------------------------------------


# ---------------------------------------------
# Otras variables
# ---------------------------------------------
# Nombre para el fichero CSV
fichero_csv=str(nombre_fichero)+"_"+str(fecha_fichero)+".csv"
# Sacamos la cantidad total
calcular_cantidad="true"
# Offset de la consulta
offset=0
# ---------------------------------------------


# ---------------------------------------------
# Cabeceras para las consultas requests
# ---------------------------------------------
headers = {
	'Content-type': 'application/json',
	'Authorization':  token 
}
data = '{}'
# ---------------------------------------------


# ---------------------------------------------
# Funcion para hacer las consultas
# ---------------------------------------------
def consulta(offset):
	global limite, ip, header, data, calcular_cantidad
	url="https://"+str(ip)+":443/api/endpoint?filter=%7B%7D&sort=%2Bid&offset="+str(offset)+"&limit="+str(limite)+"&calculate_count="+str(calcular_cantidad)
	response = requests.get(url, headers=headers, verify=False)
	return response
# ---------------------------------------------	
	
	
# ---------------------------------------------
# Inicio del Script
# ---------------------------------------------
# LLamamos a la consulta la primera vez
#response = consulta(offset)
# Variables de control
j=0
actual=0
salida=list()
# Bucle para hacer las consultas 
while j == 0:
	# LLamada a la consulta
	response = consulta(offset)
	# Carga de JSON en diccionarios
	datos=json.loads(response.text)
	# Sacamos la cantidad de datos
	cantidad=datos['count']
	# Nos quedamos con los items
	datos=datos['_embedded']['items']
	# Añadimos los datos consultados a los que hubiera antes
	salida=salida+datos
	# Contamos cuantos resultados han venido
	datos_rx=len(datos)
	# Sacamos item actual en el bucle
	actual=offset+datos_rx
	# Mostramos info de los datos que han salido hasta ahora
	print("\tRecibidas: "+str(offset)+" - "+str(actual)+" entidades de un total de "+str(cantidad))
	# Preparamos el offset para siguiente consulta
	offset=actual
	# Si no hay mas datos, preparamos para salir del bucle
	if offset>=cantidad:
		# marcamos salida de bucle
		j=1
# ---------------------------------------------


# ---------------------------------------------
# Indicamos datos para exportar a CSV
print("Datos para procesar: "+str(len(salida)))
datos=salida
# ---------------------------------------------


# ---------------------------------------------
# Limpiamos los datos recibidos
# ---------------------------------------------
claves=list()
resultado=list()
resultado_fila=dict()	
print("Limpiando datos recibidos...")
# recorremos todos los elemenos
for element in datos:
	# Quitamos los links que vienen en el array
	element.pop("_links",None)
	# Los atributos los ponemos como variables adicionales
	element.update(element["attributes"])
	# Quitamos el array puro de atributos
	element.pop("attributes",None)
	# Sacamos una lista con todas las claves existentes
	for clave in element.keys():
		if (clave in claves) == False:
			claves.append(clave)
# ---------------------------------------------


# ---------------------------------------------
# Ordenar y rellenar keys si estan vacias
# ---------------------------------------------
print("Ordenando datos para la exportacion...")
# Recorremos todos los datos
for fila in datos:
	# Reiniciamos la fila
	resultado_fila=dict()
	# para cada una de las claves
	for key in claves:
		# Se mira si existe en esta fila
		if key in fila:
			# Se le pone el valor encontrado
			resultado_fila[key]=fila[key]
		else:
			# Se deja el valor a null
			resultado_fila[key]=""
	# Se guarda en los resultados la fila
	resultado.append(resultado_fila)
# ---------------------------------------------


# ---------------------------------------------
# Generaracion del CSV
# ---------------------------------------------
print('\033[1;32mGenerando CSV...\033[1;m')
# Abrimos el fichero en modo escritura
datos_fichero = open(fichero_csv, 'w')
# Preparamos el fichero csv
csvwriter = csv.writer(datos_fichero)
# Inicializamos el bucle
count = 0
# Para cada linea de datos
for emp in resultado:
	# Comprobamos si es la primera linea
	if count == 0:
		# Sacamos los Keys
		header = emp.keys()
		# Lo ponemos como cabecera
		csvwriter.writerow(header)
		count += 1
	# Sacamos los valores de esta linea	
	contenido=emp.values()
	# Añadimos los valores al fichero CSV
	csvwriter.writerow(emp.values())
# Cerramos el fichero CSV	
datos_fichero.close()
# Mostramos informacion del fichero generado
print('\033[1;32mFichero CSV generado: '+fichero_csv+' \033[1;m')
# ---------------------------------------------