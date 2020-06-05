from cassandra.cluster import Cluster
import subprocess

#Iniciar servidor de Cassandra
#subprocess.call([r'C:\Users\Usuario\Desktop\U\A y P masivo de datos\Proyecto\Entrega2\cassandra.lnk'])

cluster = Cluster(['127.0.0.1'],port=9042)
keyspace = 'proyectoalma'
connection = cluster.connect(keyspace)

cuentas = connection.execute('SELECT DISTINCT ctanombre FROM movimientos LIMIT 10')
#for cuenta in cuentas:
#	print (cuenta.ctanombre)
datos = connection.execute('SELECT * FROM movimientos LIMIT 10')
print ('AQUI VA')
print (datos[1].ctanombre)