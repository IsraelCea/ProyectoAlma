from tkinter import ttk
from tkinter import *
from cassandra.cluster import Cluster
from numpy import random

class Datos:


    def __init__(self,window):
        self.wind = window
        self.wind.title('Finanzas empresa')
        #self.wind.iconbitmap('C:\Users\Usuario\Desktop\U\A y P masivo de datos\Proyecto\Entrega2\fin.png')

        #Creando frame
        frame = LabelFrame(self.wind, text = 'Título del recuadro')
        frame.grid(row =0 , column = 0, columnspan =3, pady = 20)

        # Input 1
        Label(frame, text='Algo').grid(row=1, column=0)
        self.algo = Entry(frame)
        self.algo.focus()
        self.algo.grid(row=1, column=1)
        # Input 2
        Label(frame, text='Otra cosa').grid(row=2, column=0)
        self.otra = Entry(frame)
        self.otra.grid(row=2, column=1)

        #Tabla
        self.tree = ttk.Treeview(height = 10,columns = 2 )
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Algo', anchor = CENTER)
        self.tree.heading('#1', text = 'Otra Cosa')

        # Botón
        ttk.Button(frame, text = 'este es el botón', command = self.get_movs).grid(row=3, columnspan=2, sticky= W + E)
        #ttk.Button(frame, text='este es el botón').grid(row=3, columnspan=2, sticky=W + E)
        self.get_movs()

    #run_query conecta a cassandra y corre las consultas
    def run_query(self, query, parameters=()):
        cluster = Cluster(['127.0.0.1'], port=9042)
        keyspace = 'proyectoalma'
        connection = cluster.connect(keyspace)
        result = connection.execute(query, parameters)
        return result

    def get_movs(self):
        #limpiando datos
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #consultando datos
        numrandom=random.randint(1,10)
        numrandomstring = str(numrandom)
        print('EL NUMERO GENERADO ES: '+numrandomstring)
        query = 'SELECT * FROM movimientos LIMIT '+numrandomstring
        db_rows = self.run_query(query)
        for row in db_rows:
            print(row)
            self.tree.insert('',0, text = row[20], values=row[1])




if __name__ == '__main__':
    ventana = Tk()
    application = Datos(ventana)
    ventana.mainloop()
