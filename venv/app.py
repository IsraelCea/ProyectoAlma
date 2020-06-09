#https://www.youtube.com/watch?v=W2kAF9pKPPE
import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
from tkinter import ttk
from tkinter import *
from cassandra.cluster import Cluster
from numpy import random

import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure



class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs
                       )


        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        #container.grid_rowconfigure(0, weight=1)
        #container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Cuentas, Empresas, Proveedores):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Cuentas")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class Cuentas(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Cuentas", font=controller.title_font).grid(row=0, column=0,sticky=W,padx=10)
        #label.pack(side="top", fill="x", pady=10)

        # Cuadro Opciones
        cuadro = LabelFrame(self)
        #cuadro = Frame(self)
        cuadro.grid(row=1, column=0,columnspan=1, padx=10,pady=10, sticky=W+E)
        # Input 1
        Label(cuadro, text='Cuenta:').grid(row=0, column=0, padx=10,pady=10)
        self.cuentaentry = Entry(cuadro,width=30)
        self.cuentaentry.grid(row=0, column=1,columnspan=1,padx=10, pady=10, sticky=W+E)
        self.cuentaentry.focus()
        # Periodos
        Label(cuadro, text='Periodo:').grid(row=1, column=0, padx=10,pady=10)
        #Combobox Periodos
        combop = ttk.Combobox(cuadro,width=25,values=["2013","2014","2015","2016","2017","2018"])
        self.comboperiodo = combop
        self.comboperiodo.grid(row=1, column=1, columnspan=1, padx=10,pady=10, sticky=W+E)
        # Botón Query
        ttk.Button(cuadro, text = 'Query', width=20,command=self.deploy_chart).grid(row=1,column=2,columnspan=1,padx=40,sticky=W+E)

        # Tabla
        tree = ttk.Treeview(self,height=10, columns=2)
        self.tabla = tree
        self.tabla.grid(row=2, column=0, padx=10, pady=10,sticky=W+E)
        self.tabla.heading('#0', text='Cuenta', anchor=CENTER)
        self.tabla.column("#0", minwidth=300, width=300, stretch=NO)
        self.tabla.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tabla.heading('#1', text='Transacciones Totales')
        self.tabla.column("#1", minwidth=190, width=190, stretch=NO)

        # Cuadro Gráficos
        cuadrograf=LabelFrame(self,width=200,height=230,background='grey100',text='Transacciones en CLP')
        cuadrograf.grid(row=2, column=1, columnspan=4, rowspan=2,padx=10, pady=10, sticky=W + E)
        self.cuadrografico=cuadrograf

        #Cuadro cuadratura
        cuadrocuad=LabelFrame(self,width=600,height=50,text='Cuadratura')
        cuadrocuad.grid(row=4, column=0, columnspan=5, rowspan=2,padx=10, pady=10, sticky=W + E)

        #Tabla cuadratura
        framecuad=ttk.Treeview(cuadrocuad,height=1,columns=('1','2','3','4','5'), selectmode='extended')
        framecuad.grid(row=0, column=0, padx=10, pady=10, sticky= W+E)
        framecuad.heading("#0", text="Debe Nominal")
        framecuad.column("#0",minwidth=100,width=120,stretch=FALSE)
        framecuad.heading("1", text="Haber Nominal")
        framecuad.column("1",minwidth=100,width=120, stretch=NO)
        framecuad.heading("2", text="Balance Nominal")
        framecuad.column("2",minwidth=100,width=120, stretch=NO)
        framecuad.heading("3", text="Debe Real")
        framecuad.column("3",minwidth=100,width=120, stretch=NO)
        framecuad.heading("4", text="Haber Real")
        framecuad.column("4",minwidth=100,width=120, stretch=NO)
        framecuad.heading("5", text="Balance Real")
        framecuad.column("5",minwidth=100,width=120, stretch=NO)
        self.frcuad=framecuad


        #Acceso a otras secciones
        button1 = tk.Button(self, text="Cuentas", width=10, background='grey60',
                            command=lambda: controller.show_frame("Cuentas")).grid(row=0, column=1,padx=2.5,pady=0)
        button2 = tk.Button(self, text="Empresa", width=10,
                            command=lambda: controller.show_frame("Empresas")).grid(row=0, column=2,padx=2.5,pady=0)
        button3 = tk.Button(self, text="Proveedores", width=10,
                            command=lambda: controller.show_frame("Proveedores")).grid(row=0, column=3, padx=2.5, pady=0)
        #button4 = tk.Button(self, text="Usuarios", width=10,
        #                    command=lambda: controller.show_frame("Usuarios")).grid(row=0, column=4,padx=2.5,pady=0)

        self.get_movs()
        #vercta='Ventas Departamentos'
        #per=2014
        #self.gen_chart(vercta,per)

    #Inserta en la casilla cuenta, la cuenta seleccionada desde la tabla
    def on_tree_select(self, event):
        print("selected items:")
        self.cuentaentry.delete(0, tk.END)
        for item in self.tabla.selection():
            item_text = self.tabla.item(item, "text")
            print(item_text)
        self.cuentaentry.insert(0, item_text)

    #run_query conecta a cassandra y corre las consultas
    def run_query(self,query, parameters=()):
        cluster = Cluster(['127.0.0.1'], port=9042)
        keyspace = 'proyectoalma'
        connection = cluster.connect(keyspace)
        result = connection.execute(query, parameters)
        return result

    def get_movs(self):
        #limpiando datos
        records = self.tabla.get_children()
        for element in records:
            self.tabla.delete(element)
        #consultando datos
        numrandom=random.randint(1,10)
        numrandomstring = str(numrandom)
        print('EL NUMERO GENERADO ES: '+numrandomstring)
        query = 'SELECT DISTINCT ctanombre FROM movimientos LIMIT '+numrandomstring
        db_rows = self.run_query(query)
        cuentas = [['Ventas Departamentos', 19034], ['Banco BCI', 19829], ['Facturas Por Pagar', 23025],
                   ['Deudores por Venta Hipotecario Mutuo UF', 30244], ['Deudores por Venta Anticipo Venta UF', 38380],
                   ['DIFERENCIA DE CAMBIO FUNCIONAL', 39472], ['Facturas por Pagar (APROBADAS)', 46795],
                   ['Banco Chile', 58633], ['Cheques Por Cobrar', 67964], ['Anticipo Ventas Clientes UF', 534773]]
        #for row in db_rows:
        #    print(row)
        #    self.tabla.insert('',0, text = row[0], values=row[0])
        for cta in cuentas:
            self.tabla.insert('',0, text = cta[0], values=cta[1])
        lacuenta='Deudores por Venta Hipotecario Mutuo UF'
        #sumadebe=self.sumar_debe(lacuenta)
        print ("la cuenta es:" + lacuenta)
        #print("el monto es:" + str(sumadebe))

#Cuenta la cantidad de movimientos por cuenta
    def count_mov_cta(self):
        #Distingue las cuentas
        query = 'SELECT DISTINCT ctanombre FROM movimientos'
        db_rows = self.run_query(query)
        cuentas = []
        cuentas_cant=[]
        for row in db_rows:
            print(row)
            cuentas.append(row[0])
            #self.tabla.insert('',0, text = row[0], values=row[0])
        print(cuentas)
        for cta in cuentas:
            ctalocal=[cta]
            query_c = "SELECT count(ctanombre) FROM movimientos where ctanombre='" + cta + "'"
            print(query_c)
            cantidad = self.run_query(query_c)
            ctalocal.append(cantidad[0][0])
            cuentas_cant.append(ctalocal)
            print (ctalocal)
        cuentas_cant.sort(key=lambda x: x[1])
        print(cuentas_cant)

    def sumar_debe(self,cta,inicio,fin):
        montototal=0
        cuenta= str(cta)
        i=str(inicio)
        f=str(fin)
        query= "select movconmontolocaldebe from movimientos where ctanombre='"+cuenta+"' and fechaingreso>'"+i+"' and fechaingreso<'"+f+"' ALLOW FILTERING"
        print (query)
        montos=self.run_query(query)
        for monto in montos:
            montototal+=monto[0]
        return montototal

    def debe_anual(self,cta,inicio,fin):
        montototal=0
        cuenta = str(cta)
        i = str(inicio)
        f = str(fin)
        query = "select movconmontolocaldebe from movimientos where ctanombre='" + cuenta + "' and fechaingreso>'" + i + "' and fechaingreso<'" + f + "' ALLOW FILTERING"
        print(query)
        montos = self.run_query(query)
        for monto in montos:
            montototal += monto[0]
        return montototal

    def sumar_haber(self,cta,inicio,fin):
        montototal=0
        cuenta= str(cta)
        i=str(inicio)
        f=str(fin)
        query= "select movconmontolocalhaber from movimientos where ctanombre='"+cuenta+"' and fechaingreso>'"+i+"' and fechaingreso<'"+f+"' ALLOW FILTERING"
        print (query)
        montos=self.run_query(query)
        for monto in montos:
            montototal+=monto[0]
        return montototal

    def haber_anual(self,cta,inicio,fin):
        montototal=0
        cuenta = str(cta)
        i = str(inicio)
        f = str(fin)
        query = "select movconmontolocalhaber from movimientos where ctanombre='" + cuenta + "' and fechaingreso>'" + i + "' and fechaingreso<'" + f + "' ALLOW FILTERING"
        print(query)
        montos = self.run_query(query)
        for monto in montos:
            montototal += monto[0]
        return montototal

    def debe_anual_r(self,cta,inicio,fin):
        montototal=0
        cuenta = str(cta)
        i = str(inicio)
        f = str(fin)
        query = "select MovConMontoConvDebe from movimientos where ctanombre='" + cuenta + "' and fechaingreso>'" + i + "' and fechaingreso<'" + f + "' ALLOW FILTERING"
        print(query)
        montos = self.run_query(query)
        for monto in montos:
            montototal += monto[0]
        return montototal

    def haber_anual_r(self,cta,inicio,fin):
        montototal=0
        cuenta = str(cta)
        i = str(inicio)
        f = str(fin)
        query = "select MovConMontoConvHaber from movimientos where ctanombre='" + cuenta + "' and fechaingreso>'" + i + "' and fechaingreso<'" + f + "' ALLOW FILTERING"
        print(query)
        montos = self.run_query(query)
        for monto in montos:
            montototal += monto[0]
        return montototal

    #Graficos
    #Genera los montos de debe y haber para cada mes en el periodo seleccionado
    def gen_chart(self,cuenta,periodo):
        cantidades=[]
        meses=['-01-01','-02-01','-03-01','-04-01','-05-01','-06-01',
               '-07-01','-08-01','-09-01','-10-01','-11-01','-12-01']
        fechas=[]
        meses_let=['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dec']
        montos=[]
        periodo_int=int(periodo)
        periodo_siguiente=periodo_int=periodo_int+1
        anio_sig=str(periodo_siguiente)+meses[0]
        for m in meses:
            mes=str(periodo)+m
            fechas.append(mes)
        for fecha in fechas:
            indice= fechas.index(fecha)
            if indice<11:
                cantidad=self.sumar_debe(cuenta,fecha,fechas[indice+1])
                #print("monto del mes "+str(indice+1)+":"+str(cantidad))
                montos.append(cantidad)
            else:
                cantidad=self.sumar_debe(cuenta,fecha,anio_sig)
                #print("monto del mes" + str(indice+1) + ":" + str(cantidad))
                montos.append(cantidad)
        print('Meses')
        print(meses_let)
        print('Montos')
        print(montos)
        self.plot(meses_let,montos)

    def plot (self,mes,cuenta):
        #limpia el cuadro de graficos
        for w in self.cuadrografico.winfo_children():
            w.destroy()

        fig = Figure(figsize=(3,2)) #size:wide,height
        a = fig.add_subplot(111)
        a.bar(mes, cuenta, color='red')

        #a.set_title ("Transacciones en pesos", fontsize=11)
        a.set_ylabel("Monto", fontsize=6)
        a.set_xlabel("Mes", fontsize=6)
        a.tick_params(labelsize=6)
        canvas = FigureCanvasTkAgg(fig, master=self.cuadrografico)
        canvas.get_tk_widget().pack()
        canvas.draw()

    def deploy_chart(self):
        cuenta = self.cuentaentry.get()
        periodo = self.comboperiodo.get()
        #print(cuenta)
        #print(periodo)
        self.gen_chart(cuenta,periodo)
        self.balance()
        #aquí grafica
        #self.plot()

    def balance(self):
        datos = self.frcuad.get_children()
        for dato in datos:
            self.frcuad.delete(dato)
        cuenta = self.cuentaentry.get()
        periodo = self.comboperiodo.get()
        enero=str(periodo)+'-01-01'
        diciembre=str(periodo)+'-12-31'
        debeanual=self.debe_anual(cuenta,enero,diciembre)
        haberanual = self.haber_anual(cuenta, enero, diciembre)
        saldo_nominal=int(haberanual)-int(debeanual)
        debeanual_r=self.debe_anual_r(cuenta,enero,diciembre)
        haberanual_r = self.haber_anual_r(cuenta, enero, diciembre)
        saldo_real=int(haberanual_r)-int(debeanual_r)
        #haberanualform=("{:.}".format(haberanual))
        self.frcuad.insert('',0,text=("{:,}".format(debeanual)),values=(("{:,}".format(haberanual)),("{:,}".format(saldo_nominal)),("{:,}".format(debeanual_r)),("{:,}".format(haberanual_r)),("{:,}".format(saldo_real))))
        #self.tabla.insert('', 0, text=cta[0], values=cta[1])


class Empresas(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Empresas", font=controller.title_font).grid(row=0, column=0, sticky=W, padx=10)
        # label.pack(side="top", fill="x", pady=10)

        # Cuadro Opciones
        cuadro = LabelFrame(self)
        # cuadro = Frame(self)
        cuadro.grid(row=1, column=0, columnspan=1, padx=10, pady=10, sticky=W + E)
        # Input 1
        Label(cuadro, text='Empresa:').grid(row=0, column=0, padx=10, pady=10)
        self.cuentaentry = Entry(cuadro, width=30)
        self.cuentaentry.grid(row=0, column=1, columnspan=1, padx=10, pady=10, sticky=W + E)
        self.cuentaentry.focus()
        # Periodos
        Label(cuadro, text='Periodo:').grid(row=1, column=0, padx=10, pady=10)
        # Combobox Periodos
        combop = ttk.Combobox(cuadro, width=25, values=["2013", "2014", "2015", "2016", "2017", "2018"])
        self.comboperiodo = combop
        self.comboperiodo.grid(row=1, column=1, columnspan=1, padx=10, pady=10, sticky=W + E)
        # Botón Query
        ttk.Button(cuadro, text='Query', width=20, command=self.deploy_chart).grid(row=1, column=2, columnspan=1,
                                                                                   padx=40, sticky=W + E)

        # Tabla
        tree = ttk.Treeview(self, height=10, columns=2)
        self.tabla = tree
        self.tabla.grid(row=2, column=0, padx=10, pady=10, sticky=W + E)
        self.tabla.heading('#0', text='Cuenta', anchor=CENTER)
        self.tabla.column("#0", minwidth=300, width=300, stretch=NO)
        self.tabla.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tabla.heading('#1', text='Transacciones Totales')
        self.tabla.column("#1", minwidth=190, width=190, stretch=NO)

        # Cuadro Gráficos
        cuadrograf = LabelFrame(self, width=250, height=230, background='grey100', text='Transacciones en CLP')
        cuadrograf.grid(row=2, column=1, columnspan=4, rowspan=2, padx=10, pady=10, sticky=W + E)
        self.cuadrografico = cuadrograf

        # Cuadro cuadratura
        cuadrocuad = LabelFrame(self, width=600, height=50, text='Cuadratura')
        cuadrocuad.grid(row=4, column=0, columnspan=5, rowspan=2, padx=10, pady=10, sticky=W + E)

        # Tabla cuadratura
        framecuad = ttk.Treeview(cuadrocuad, height=1, columns=('1', '2', '3', '4', '5'), selectmode='extended')
        framecuad.grid(row=0, column=0, padx=10, pady=10, sticky=W + E)
        framecuad.heading("#0", text="Debe Nominal")
        framecuad.column("#0", minwidth=100, width=120, stretch=FALSE)
        framecuad.heading("1", text="Haber Nominal")
        framecuad.column("1", minwidth=100, width=120, stretch=NO)
        framecuad.heading("2", text="Balance Nominal")
        framecuad.column("2", minwidth=100, width=120, stretch=NO)
        framecuad.heading("3", text="Debe Real")
        framecuad.column("3", minwidth=100, width=120, stretch=NO)
        framecuad.heading("4", text="Haber Real")
        framecuad.column("4", minwidth=100, width=120, stretch=NO)
        framecuad.heading("5", text="Balance Real")
        framecuad.column("5", minwidth=100, width=120, stretch=NO)
        self.frcuad = framecuad

        # Acceso a otras secciones
        button1 = tk.Button(self, text="Cuentas", width=10,
                            command=lambda: controller.show_frame("Cuentas")).grid(row=0, column=1, padx=2.5, pady=0)
        button2 = tk.Button(self, text="Empresa", width=10, background='grey60',
                            command=lambda: controller.show_frame("Empresas")).grid(row=0, column=2, padx=2.5, pady=0)
        button3 = tk.Button(self, text="Proveedores", width=10,
                            command=lambda: controller.show_frame("Proveedores")).grid(row=0, column=3, padx=2.5,
                                                                                       pady=0)
        #button4 = tk.Button(self, text="Usuarios", width=10,
        #                    command=lambda: controller.show_frame("Usuarios")).grid(row=0, column=4, padx=2.5, pady=0)

        self.get_movs()
        # vercta='Ventas Departamentos'
        # per=2014
        # self.gen_chart(vercta,per)

    # Inserta en la casilla cuenta, la cuenta seleccionada desde la tabla
    def on_tree_select(self, event):
        print("selected items:")
        self.cuentaentry.delete(0, tk.END)
        for item in self.tabla.selection():
            item_text = self.tabla.item(item, "text")
            print(item_text)
        self.cuentaentry.insert(0, item_text)

    # run_query conecta a cassandra y corre las consultas
    def run_query(self, query, parameters=()):
        cluster = Cluster(['127.0.0.1'], port=9042)
        keyspace = 'proyectoalma'
        connection = cluster.connect(keyspace)
        result = connection.execute(query, parameters)
        return result

    def get_movs(self):
        # limpiando datos
        records = self.tabla.get_children()
        for element in records:
            self.tabla.delete(element)
        # consultando datos
        numrandom = random.randint(1, 10)
        numrandomstring = str(numrandom)
        print('EL NUMERO GENERADO ES: ' + numrandomstring)
        query = 'SELECT DISTINCT ctanombre FROM movimientos LIMIT ' + numrandomstring
        db_rows = self.run_query(query)
        cuentas = [['Ventas Departamentos', 19034], ['Banco BCI', 19829], ['Facturas Por Pagar', 23025],
                   ['Deudores por Venta Hipotecario Mutuo UF', 30244], ['Deudores por Venta Anticipo Venta UF', 38380],
                   ['DIFERENCIA DE CAMBIO FUNCIONAL', 39472], ['Facturas por Pagar (APROBADAS)', 46795],
                   ['Banco Chile', 58633], ['Cheques Por Cobrar', 67964], ['Anticipo Ventas Clientes UF', 534773]]
        # for row in db_rows:
        #    print(row)
        #    self.tabla.insert('',0, text = row[0], values=row[0])
        for cta in cuentas:
            self.tabla.insert('', 0, text=cta[0], values=cta[1])
        lacuenta = 'Deudores por Venta Hipotecario Mutuo UF'
        # sumadebe=self.sumar_debe(lacuenta)
        print("la cuenta es:" + lacuenta)
        # print("el monto es:" + str(sumadebe))

    # Cuenta la cantidad de movimientos por cuenta
    def count_mov_cta(self):
        # Distingue las cuentas
        query = 'SELECT DISTINCT ctanombre FROM movimientos'
        db_rows = self.run_query(query)
        cuentas = []
        cuentas_cant = []
        for row in db_rows:
            print(row)
            cuentas.append(row[0])
            # self.tabla.insert('',0, text = row[0], values=row[0])
        print(cuentas)
        for cta in cuentas:
            ctalocal = [cta]
            query_c = "SELECT count(ctanombre) FROM movimientos where ctanombre='" + cta + "'"
            print(query_c)
            cantidad = self.run_query(query_c)
            ctalocal.append(cantidad[0][0])
            cuentas_cant.append(ctalocal)
            print(ctalocal)
        cuentas_cant.sort(key=lambda x: x[1])
        print(cuentas_cant)

    def sumar_debe(self, cta, inicio, fin):
        montototal = 0
        cuenta = str(cta)
        i = str(inicio)
        f = str(fin)
        query = "select movconmontolocaldebe from movimientos where ctanombre='" + cuenta + "' and fechaingreso>'" + i + "' and fechaingreso<'" + f + "' ALLOW FILTERING"
        print(query)
        montos = self.run_query(query)
        for monto in montos:
            montototal += monto[0]
        return montototal

    def debe_anual(self, cta, inicio, fin):
        montototal = 0
        cuenta = str(cta)
        i = str(inicio)
        f = str(fin)
        query = "select movconmontolocaldebe from movimientos where ctanombre='" + cuenta + "' and fechaingreso>'" + i + "' and fechaingreso<'" + f + "' ALLOW FILTERING"
        print(query)
        montos = self.run_query(query)
        for monto in montos:
            montototal += monto[0]
        return montototal

    def sumar_haber(self, cta, inicio, fin):
        montototal = 0
        cuenta = str(cta)
        i = str(inicio)
        f = str(fin)
        query = "select movconmontolocalhaber from movimientos where ctanombre='" + cuenta + "' and fechaingreso>'" + i + "' and fechaingreso<'" + f + "' ALLOW FILTERING"
        print(query)
        montos = self.run_query(query)
        for monto in montos:
            montototal += monto[0]
        return montototal

    def haber_anual(self, cta, inicio, fin):
        montototal = 0
        cuenta = str(cta)
        i = str(inicio)
        f = str(fin)
        query = "select movconmontolocalhaber from movimientos where ctanombre='" + cuenta + "' and fechaingreso>'" + i + "' and fechaingreso<'" + f + "' ALLOW FILTERING"
        print(query)
        montos = self.run_query(query)
        for monto in montos:
            montototal += monto[0]
        return montototal

    def debe_anual_r(self, cta, inicio, fin):
        montototal = 0
        cuenta = str(cta)
        i = str(inicio)
        f = str(fin)
        query = "select MovConMontoConvDebe from movimientos where ctanombre='" + cuenta + "' and fechaingreso>'" + i + "' and fechaingreso<'" + f + "' ALLOW FILTERING"
        print(query)
        montos = self.run_query(query)
        for monto in montos:
            montototal += monto[0]
        return montototal

    def haber_anual_r(self, cta, inicio, fin):
        montototal = 0
        cuenta = str(cta)
        i = str(inicio)
        f = str(fin)
        query = "select MovConMontoConvHaber from movimientos where ctanombre='" + cuenta + "' and fechaingreso>'" + i + "' and fechaingreso<'" + f + "' ALLOW FILTERING"
        print(query)
        montos = self.run_query(query)
        for monto in montos:
            montototal += monto[0]
        return montototal

    # Graficos
    # Genera los montos de debe y haber para cada mes en el periodo seleccionado
    def gen_chart(self, cuenta, periodo):
        cantidades = []
        meses = ['-01-01', '-02-01', '-03-01', '-04-01', '-05-01', '-06-01',
                 '-07-01', '-08-01', '-09-01', '-10-01', '-11-01', '-12-01']
        fechas = []
        meses_let = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dec']
        montos = []
        periodo_int = int(periodo)
        periodo_siguiente = periodo_int = periodo_int + 1
        anio_sig = str(periodo_siguiente) + meses[0]
        for m in meses:
            mes = str(periodo) + m
            fechas.append(mes)
        for fecha in fechas:
            indice = fechas.index(fecha)
            if indice < 11:
                cantidad = self.sumar_debe(cuenta, fecha, fechas[indice + 1])
                print("monto del mes " + str(indice + 1) + ":" + str(cantidad))
                montos.append(cantidad)
            else:
                cantidad = self.sumar_debe(cuenta, fecha, anio_sig)
                print("monto del mes" + str(indice + 1) + ":" + str(cantidad))
                montos.append(cantidad)
        print('Meses')
        print(meses_let)
        print('Montos')
        print(montos)
        self.plot(meses_let, montos)

    def plot(self, mes, cuenta):
        # limpia el cuadro de graficos
        for w in self.cuadrografico.winfo_children():
            w.destroy()

        fig = Figure(figsize=(3, 2))  # size:wide,height
        a = fig.add_subplot(111)
        a.bar(mes, cuenta, color='red')

        # a.set_title ("Transacciones en pesos", fontsize=11)
        a.set_ylabel("Monto", fontsize=6)
        a.set_xlabel("Mes", fontsize=6)
        a.tick_params(labelsize=6)
        canvas = FigureCanvasTkAgg(fig, master=self.cuadrografico)
        canvas.get_tk_widget().pack()
        canvas.draw()

    def deploy_chart(self):
        cuenta = self.cuentaentry.get()
        periodo = self.comboperiodo.get()
        # print(cuenta)
        # print(periodo)
        self.gen_chart(cuenta, periodo)
        self.balance()
        # aquí grafica
        # self.plot()

    def balance(self):
        datos = self.frcuad.get_children()
        for dato in datos:
            self.frcuad.delete(dato)
        cuenta = self.cuentaentry.get()
        periodo = self.comboperiodo.get()
        enero = str(periodo) + '-01-01'
        diciembre = str(periodo) + '-12-31'
        debeanual = self.debe_anual(cuenta, enero, diciembre)
        haberanual = self.haber_anual(cuenta, enero, diciembre)
        saldo_nominal = int(haberanual) - int(debeanual)
        debeanual_r = self.debe_anual_r(cuenta, enero, diciembre)
        haberanual_r = self.haber_anual_r(cuenta, enero, diciembre)
        saldo_real = int(haberanual_r) - int(debeanual_r)
        # haberanualform=("{:.}".format(haberanual))
        self.frcuad.insert('', 0, text=("{:,}".format(debeanual)), values=(
        ("{:,}".format(haberanual)), ("{:,}".format(saldo_nominal)), ("{:,}".format(debeanual_r)),
        ("{:,}".format(haberanual_r)), ("{:,}".format(saldo_real))))
        # self.tabla.insert('', 0, text=cta[0], values=cta[1])


class Proveedores(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Proveedores", font=controller.title_font).grid(row=0, column=0, sticky=W, padx=10)
        # label.pack(side="top", fill="x", pady=10)

        # Cuadro Opciones
        cuadro = LabelFrame(self)
        # cuadro = Frame(self)
        cuadro.grid(row=1, column=0, columnspan=1, padx=10, pady=10, sticky=W + E)
        # Input 1
        Label(cuadro, text='Proveedores:').grid(row=0, column=0, padx=10, pady=10)
        self.cuentaentry = Entry(cuadro, width=30)
        self.cuentaentry.grid(row=0, column=1, columnspan=1, padx=10, pady=10, sticky=W + E)
        self.cuentaentry.focus()
        # Periodos
        Label(cuadro, text='Periodo:').grid(row=1, column=0, padx=10, pady=10)
        # Combobox Periodos
        combop = ttk.Combobox(cuadro, width=25, values=["2013", "2014", "2015", "2016", "2017", "2018"])
        self.comboperiodo = combop
        self.comboperiodo.grid(row=1, column=1, columnspan=1, padx=10, pady=10, sticky=W + E)
        # Botón Query
        ttk.Button(cuadro, text='Query', width=20, command=self.deploy_chart).grid(row=1, column=2, columnspan=1,
                                                                                   padx=40, sticky=W + E)

        # Tabla
        tree = ttk.Treeview(self, height=10, columns=2)
        self.tabla = tree
        self.tabla.grid(row=2, column=0, padx=10, pady=10, sticky=W + E)
        self.tabla.heading('#0', text='Cuenta', anchor=CENTER)
        self.tabla.column("#0", minwidth=300, width=300, stretch=NO)
        self.tabla.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tabla.heading('#1', text='Transacciones Totales')
        self.tabla.column("#1", minwidth=190, width=190, stretch=NO)

        # Cuadro Gráficos
        cuadrograf = LabelFrame(self, width=200, height=230, background='grey100', text='Transacciones en CLP')
        cuadrograf.grid(row=2, column=1, columnspan=4, rowspan=2, padx=10, pady=10, sticky=W + E)
        self.cuadrografico = cuadrograf

        # Cuadro cuadratura
        cuadrocuad = LabelFrame(self, width=600, height=50, text='Cuadratura')
        cuadrocuad.grid(row=4, column=0, columnspan=5, rowspan=2, padx=10, pady=10, sticky=W + E)

        # Tabla cuadratura
        framecuad = ttk.Treeview(cuadrocuad, height=1, columns=('1', '2', '3', '4', '5'), selectmode='extended')
        framecuad.grid(row=0, column=0, padx=10, pady=10, sticky=W + E)
        framecuad.heading("#0", text="Debe Nominal")
        framecuad.column("#0", minwidth=100, width=120, stretch=FALSE)
        framecuad.heading("1", text="Haber Nominal")
        framecuad.column("1", minwidth=100, width=120, stretch=NO)
        framecuad.heading("2", text="Balance Nominal")
        framecuad.column("2", minwidth=100, width=120, stretch=NO)
        framecuad.heading("3", text="Debe Real")
        framecuad.column("3", minwidth=100, width=120, stretch=NO)
        framecuad.heading("4", text="Haber Real")
        framecuad.column("4", minwidth=100, width=120, stretch=NO)
        framecuad.heading("5", text="Balance Real")
        framecuad.column("5", minwidth=100, width=120, stretch=NO)
        self.frcuad = framecuad

        # Acceso a otras secciones
        button1 = tk.Button(self, text="Cuentas", width=10,
                            command=lambda: controller.show_frame("Cuentas")).grid(row=0, column=1, padx=2.5, pady=0)
        button2 = tk.Button(self, text="Empresa", width=10,
                            command=lambda: controller.show_frame("Empresas")).grid(row=0, column=2, padx=2.5, pady=0)
        button3 = tk.Button(self, text="Proveedores", width=10,  background='grey60',
                            command=lambda: controller.show_frame("Proveedores")).grid(row=0, column=3, padx=2.5,
                                                                                       pady=0)
        #button4 = tk.Button(self, text="Usuarios", width=10,
        #                   command=lambda: controller.show_frame("Usuarios")).grid(row=0, column=4, padx=2.5, pady=0)

        self.get_movs()
        # vercta='Ventas Departamentos'
        # per=2014
        # self.gen_chart(vercta,per)

    # Inserta en la casilla cuenta, la cuenta seleccionada desde la tabla
    def on_tree_select(self, event):
        print("selected items:")
        self.cuentaentry.delete(0, tk.END)
        for item in self.tabla.selection():
            item_text = self.tabla.item(item, "text")
            print(item_text)
        self.cuentaentry.insert(0, item_text)

    # run_query conecta a cassandra y corre las consultas
    def run_query(self, query, parameters=()):
        cluster = Cluster(['127.0.0.1'], port=9042)
        keyspace = 'proyectoalma'
        connection = cluster.connect(keyspace)
        result = connection.execute(query, parameters)
        return result

    def get_movs(self):
        # limpiando datos
        records = self.tabla.get_children()
        for element in records:
            self.tabla.delete(element)
        # consultando datos
        numrandom = random.randint(1, 10)
        numrandomstring = str(numrandom)
        print('EL NUMERO GENERADO ES: ' + numrandomstring)
        query = 'SELECT DISTINCT ctanombre FROM movimientos LIMIT ' + numrandomstring
        db_rows = self.run_query(query)
        cuentas = [['Ventas Departamentos', 19034], ['Banco BCI', 19829], ['Facturas Por Pagar', 23025],
                   ['Deudores por Venta Hipotecario Mutuo UF', 30244], ['Deudores por Venta Anticipo Venta UF', 38380],
                   ['DIFERENCIA DE CAMBIO FUNCIONAL', 39472], ['Facturas por Pagar (APROBADAS)', 46795],
                   ['Banco Chile', 58633], ['Cheques Por Cobrar', 67964], ['Anticipo Ventas Clientes UF', 534773]]
        # for row in db_rows:
        #    print(row)
        #    self.tabla.insert('',0, text = row[0], values=row[0])
        for cta in cuentas:
            self.tabla.insert('', 0, text=cta[0], values=cta[1])
        lacuenta = 'Deudores por Venta Hipotecario Mutuo UF'
        # sumadebe=self.sumar_debe(lacuenta)
        print("la cuenta es:" + lacuenta)
        # print("el monto es:" + str(sumadebe))

    # Cuenta la cantidad de movimientos por cuenta
    def count_mov_cta(self):
        # Distingue las cuentas
        query = 'SELECT DISTINCT ctanombre FROM movimientos'
        db_rows = self.run_query(query)
        cuentas = []
        cuentas_cant = []
        for row in db_rows:
            print(row)
            cuentas.append(row[0])
            # self.tabla.insert('',0, text = row[0], values=row[0])
        print(cuentas)
        for cta in cuentas:
            ctalocal = [cta]
            query_c = "SELECT count(ctanombre) FROM movimientos where ctanombre='" + cta + "'"
            print(query_c)
            cantidad = self.run_query(query_c)
            ctalocal.append(cantidad[0][0])
            cuentas_cant.append(ctalocal)
            print(ctalocal)
        cuentas_cant.sort(key=lambda x: x[1])
        print(cuentas_cant)

    def sumar_debe(self, cta, inicio, fin):
        montototal = 0
        cuenta = str(cta)
        i = str(inicio)
        f = str(fin)
        query = "select movconmontolocaldebe from movimientos where ctanombre='" + cuenta + "' and fechaingreso>'" + i + "' and fechaingreso<'" + f + "' ALLOW FILTERING"
        print(query)
        montos = self.run_query(query)
        for monto in montos:
            montototal += monto[0]
        return montototal

    def debe_anual(self, cta, inicio, fin):
        montototal = 0
        cuenta = str(cta)
        i = str(inicio)
        f = str(fin)
        query = "select movconmontolocaldebe from movimientos where ctanombre='" + cuenta + "' and fechaingreso>'" + i + "' and fechaingreso<'" + f + "' ALLOW FILTERING"
        print(query)
        montos = self.run_query(query)
        for monto in montos:
            montototal += monto[0]
        return montototal

    def sumar_haber(self, cta, inicio, fin):
        montototal = 0
        cuenta = str(cta)
        i = str(inicio)
        f = str(fin)
        query = "select movconmontolocalhaber from movimientos where ctanombre='" + cuenta + "' and fechaingreso>'" + i + "' and fechaingreso<'" + f + "' ALLOW FILTERING"
        print(query)
        montos = self.run_query(query)
        for monto in montos:
            montototal += monto[0]
        return montototal

    def haber_anual(self, cta, inicio, fin):
        montototal = 0
        cuenta = str(cta)
        i = str(inicio)
        f = str(fin)
        query = "select movconmontolocalhaber from movimientos where ctanombre='" + cuenta + "' and fechaingreso>'" + i + "' and fechaingreso<'" + f + "' ALLOW FILTERING"
        print(query)
        montos = self.run_query(query)
        for monto in montos:
            montototal += monto[0]
        return montototal

    def debe_anual_r(self, cta, inicio, fin):
        montototal = 0
        cuenta = str(cta)
        i = str(inicio)
        f = str(fin)
        query = "select MovConMontoConvDebe from movimientos where ctanombre='" + cuenta + "' and fechaingreso>'" + i + "' and fechaingreso<'" + f + "' ALLOW FILTERING"
        print(query)
        montos = self.run_query(query)
        for monto in montos:
            montototal += monto[0]
        return montototal

    def haber_anual_r(self, cta, inicio, fin):
        montototal = 0
        cuenta = str(cta)
        i = str(inicio)
        f = str(fin)
        query = "select MovConMontoConvHaber from movimientos where ctanombre='" + cuenta + "' and fechaingreso>'" + i + "' and fechaingreso<'" + f + "' ALLOW FILTERING"
        print(query)
        montos = self.run_query(query)
        for monto in montos:
            montototal += monto[0]
        return montototal

    # Graficos
    # Genera los montos de debe y haber para cada mes en el periodo seleccionado
    def gen_chart(self, cuenta, periodo):
        cantidades = []
        meses = ['-01-01', '-02-01', '-03-01', '-04-01', '-05-01', '-06-01',
                 '-07-01', '-08-01', '-09-01', '-10-01', '-11-01', '-12-01']
        fechas = []
        meses_let = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dec']
        montos = []
        periodo_int = int(periodo)
        periodo_siguiente = periodo_int = periodo_int + 1
        anio_sig = str(periodo_siguiente) + meses[0]
        for m in meses:
            mes = str(periodo) + m
            fechas.append(mes)
        for fecha in fechas:
            indice = fechas.index(fecha)
            if indice < 11:
                cantidad = self.sumar_debe(cuenta, fecha, fechas[indice + 1])
                print("monto del mes " + str(indice + 1) + ":" + str(cantidad))
                montos.append(cantidad)
            else:
                cantidad = self.sumar_debe(cuenta, fecha, anio_sig)
                print("monto del mes" + str(indice + 1) + ":" + str(cantidad))
                montos.append(cantidad)
        print('Meses')
        print(meses_let)
        print('Montos')
        print(montos)
        self.plot(meses_let, montos)

    def plot(self, mes, cuenta):
        # limpia el cuadro de graficos
        for w in self.cuadrografico.winfo_children():
            w.destroy()

        fig = Figure(figsize=(3, 2))  # size:wide,height
        a = fig.add_subplot(111)
        a.bar(mes, cuenta, color='red')

        # a.set_title ("Transacciones en pesos", fontsize=11)
        a.set_ylabel("Monto", fontsize=6)
        a.set_xlabel("Mes", fontsize=6)
        a.tick_params(labelsize=6)
        canvas = FigureCanvasTkAgg(fig, master=self.cuadrografico)
        canvas.get_tk_widget().pack()
        canvas.draw()

    def deploy_chart(self):
        cuenta = self.cuentaentry.get()
        periodo = self.comboperiodo.get()
        # print(cuenta)
        # print(periodo)
        self.gen_chart(cuenta, periodo)
        self.balance()
        # aquí grafica
        # self.plot()

    def balance(self):
        datos = self.frcuad.get_children()
        for dato in datos:
            self.frcuad.delete(dato)
        cuenta = self.cuentaentry.get()
        periodo = self.comboperiodo.get()
        enero = str(periodo) + '-01-01'
        diciembre = str(periodo) + '-12-31'
        debeanual = self.debe_anual(cuenta, enero, diciembre)
        haberanual = self.haber_anual(cuenta, enero, diciembre)
        saldo_nominal = int(haberanual) - int(debeanual)
        debeanual_r = self.debe_anual_r(cuenta, enero, diciembre)
        haberanual_r = self.haber_anual_r(cuenta, enero, diciembre)
        saldo_real = int(haberanual_r) - int(debeanual_r)
        # haberanualform=("{:.}".format(haberanual))
        self.frcuad.insert('', 0, text=("{:,}".format(debeanual)), values=(
        ("{:,}".format(haberanual)), ("{:,}".format(saldo_nominal)), ("{:,}".format(debeanual_r)),
        ("{:,}".format(haberanual_r)), ("{:,}".format(saldo_real))))
        # self.tabla.insert('', 0, text=cta[0], values=cta[1])




if __name__ == "__main__":
    app = SampleApp()
    app.title("Finanzas Inmobiliaria ")
    app.resizable(False, False)
    app.mainloop()