import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

class CConexion:
    @staticmethod
    def ConexionBaseDeDatos():
        try:
            conexion = mysql.connector.connect(
                host='127.0.0.1',  # Host de la base de datos (generalmente 'localhost')
                user='root',       # Tu nombre de usuario de MySQL
                password='root',   # Tu contraseña de MySQL
                database='clientesdb'  # Nombre de la base de datos a la que quieres conectarte
            )
            if conexion.is_connected():
                print("Conexión exitosa")
                return conexion
        except Error as e:
            print("Error al conectar a la base de datos", e)
            return None

class CClientes:
    @staticmethod
    def ingresarClientes(nombres, apellidos, sexo):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            if cone is not None:
                cursor = cone.cursor()
                sql = "INSERT INTO usuarios VALUES (NULL, %s, %s, %s);"
                valores = (nombres, apellidos, sexo)
                cursor.execute(sql, valores)
                cone.commit()
                print(cursor.rowcount, "Registro ingresado")
                cone.close()
            else:
                print("Error: No se pudo establecer la conexión")
        except mysql.connector.Error as error:
            print("Error de acceso a datos: {}", format(error))

    @staticmethod
    def mostrarClientes():
        try:
            cone = CConexion.ConexionBaseDeDatos()
            if cone is not None:
                cursor = cone.cursor()
                sql = "SELECT * FROM usuarios;"
                cursor.execute(sql)
                registros = cursor.fetchall()
                cone.close()
                return registros
            else:
                print("Error: No se pudo establecer la conexión")
                return []
        except mysql.connector.Error as error:
            print("Error de acceso a datos: {}", format(error))
            return []

class formularioClientes:
    base = None
    texBoxId = None
    texBoxNombres = None
    texBoxApellidos = None
    combo = None
    groupBox = None
    tree = None

def formulario():
    global base
    global texBoxId
    global texBoxNombres 
    global texBoxApellidos
    global combo
    global groupBox
    global tree

    try:
        base = tk.Tk()
        base.geometry("1200x300")
        base.title("Formulario Python")

        groupBox = LabelFrame(base, text="Datos de Personal", padx=5, pady=5)
        groupBox.grid(row=0, column=0, padx=10, pady=10)

        labelId = Label(groupBox, text="Id: ", width=13, font=("arial", 12)).grid(row=0, column=0)
        texBoxId = Entry(groupBox)
        texBoxId.grid(row=0, column=1)

        labelNombres = Label(groupBox, text="Nombres: ", width=13, font=("arial", 12)).grid(row=1, column=0)
        texBoxNombres = Entry(groupBox)
        texBoxNombres.grid(row=1, column=1)

        labelApellidos = Label(groupBox, text="Apellidos: ", width=13, font=("arial", 12)).grid(row=2, column=0)
        texBoxApellidos = Entry(groupBox)
        texBoxApellidos.grid(row=2, column=1)

        labelSexo = Label(groupBox, text="Sexo: ", width=13, font=("arial", 12)).grid(row=3, column=0)
        seleccionSexo = tk.StringVar()
        combo = ttk.Combobox(groupBox, values=["Masculino", "Femenino"], textvariable=seleccionSexo)
        combo.grid(row=3, column=1)
        seleccionSexo.set("Masculino")

        Button(groupBox, text="Guardar", width=10, command=guardarRegistros).grid(row=4, column=0)
        Button(groupBox, text="Modificar", width=10, command=cargarDatos).grid(row=4, column=1)
        Button(groupBox, text="Eliminar", width=10, command=eliminarRegistro).grid(row=4, column=2)


        groupBoxLista = LabelFrame(base, text="Lista de Personal", padx=5, pady=5)
        groupBoxLista.grid(row=0, column=1, padx=5, pady=5)

        tree = ttk.Treeview(groupBoxLista, columns=("Id", "Nombres", "Apellidos", "Sexo"), show="headings", height=5)
        tree.column("# 1", anchor=CENTER)
        tree.heading("# 1", text="Id")
        tree.column("# 2", anchor=CENTER)
        tree.heading("# 2", text="Nombres")
        tree.column("# 3", anchor=CENTER)
        tree.heading("# 3", text="Apellidos")
        tree.column("# 4", anchor=CENTER)
        tree.heading("# 4", text="Sexo")
        tree.pack()

        # Insertar datos en el treeview
        for row in CClientes.mostrarClientes():
            tree.insert("", "end", values=row)

        base.mainloop()

    except ValueError as error:
        print("Error al mostrar la interfaz, error: {}".format(error))

def guardarRegistros():
    global texBoxNombres, texBoxApellidos, combo, tree
    try:
        if texBoxNombres is None or texBoxApellidos is None or combo is None:
            print("Los widgets no están inicializados")
            return

        nombres = texBoxNombres.get()
        apellidos = texBoxApellidos.get()
        sexo = combo.get()

        if not nombres.strip():
            messagebox.showerror("Error", "El campo 'Nombres' no puede estar vacío")
            return

        if not apellidos.strip():
            messagebox.showerror("Error", "El campo 'Apellidos' no puede estar vacío")
            return

        if not sexo.strip():
            messagebox.showerror("Error", "El campo 'Sexo' no puede estar vacío")
            return

        CClientes.ingresarClientes(nombres, apellidos, sexo)
        messagebox.showinfo("Información", "Los datos fueron guardados")
        
        actualizarTreeview()
        texBoxNombres.delete(0, END)
        texBoxApellidos.delete(0, END)

    except ValueError as error:
        print("Error al ingresar los datos {}".format(error))

def actualizarTreeview():
    global tree

    try:
        # Borrar todos los elementos actuales del Treeview
        tree.delete(*tree.get_children())

        # Obtener los nuevos datos que deseamos mostrar
        datos = CClientes.mostrarClientes()

        # Insertar los nuevos datos en el Treeview
        for row in datos:
            tree.insert("", "end", values=row)
    except mysql.connector.Error as error:
        print("Error al actualizar la tabla {}".format(error))

def cargarDatos():
    try:
        seleccion = tree.focus()  # Obtiene el item seleccionado en el treeview
        datos = tree.item(seleccion, 'values')  # Obtiene los valores de la fila seleccionada
        texBoxId.delete(0, END)
        texBoxId.insert(END, datos[0])  # Inserta el ID en el campo correspondiente
        texBoxNombres.delete(0, END)
        texBoxNombres.insert(END, datos[1])  # Inserta los nombres en el campo correspondiente
        texBoxApellidos.delete(0, END)
        texBoxApellidos.insert(END, datos[2])  # Inserta los apellidos en el campo correspondiente
        combo.set(datos[3])  # Selecciona el sexo en el combobox
    except IndexError:
        messagebox.showerror("Error", "Por favor seleccione un registro para modificar.")

def modificarRegistro():
    try:
        id_cliente = texBoxId.get()
        nombres = texBoxNombres.get()
        apellidos = texBoxApellidos.get()
        sexo = combo.get()

        if not id_cliente:
            messagebox.showerror("Error", "Por favor seleccione un registro para modificar.")
            return

        if not nombres.strip():
            messagebox.showerror("Error", "El campo 'Nombres' no puede estar vacío")
            return

        if not apellidos.strip():
            messagebox.showerror("Error", "El campo 'Apellidos' no puede estar vacío")
            return

        if not sexo.strip():
            messagebox.showerror("Error", "El campo 'Sexo' no puede estar vacío")
            return

        cone = CConexion.ConexionBaseDeDatos()
        if cone is not None:
            cursor = cone.cursor()
            sql = "UPDATE usuarios SET nombres=%s, apellidos=%s, sexo=%s WHERE id=%s"
            valores = (nombres, apellidos, sexo, id_cliente)
            cursor.execute(sql, valores)
            cone.commit()
            print(cursor.rowcount, "Registro actualizado")
            cone.close()

            messagebox.showinfo("Información", "Registro modificado correctamente")

            # Actualizar el treeview eliminando el registro antiguo y añadiendo el nuevo
            actualizarTreeview()

            texBoxId.delete(0, END)
            texBoxNombres.delete(0, END)
            texBoxApellidos.delete(0, END)
            combo.set("Masculino")  # Reiniciar el combobox a su valor por defecto
        else:
            print("Error: No se pudo establecer la conexión")
    except mysql.connector.Error as error:
        print("Error al modificar registro: {}".format(error))

def eliminarRegistro():
    try:
        seleccion = tree.focus()  # Obtiene el item seleccionado en el treeview
        datos = tree.item(seleccion, 'values')  # Obtiene los valores de la fila seleccionada
        id_cliente = datos[0]  # Obtiene el ID del registro seleccionado

        if not id_cliente:
            messagebox.showerror("Error", "Por favor seleccione un registro para eliminar.")
            return

        if messagebox.askyesno("Confirmar eliminación", "¿Está seguro de eliminar este registro?"):
            cone = CConexion.ConexionBaseDeDatos()
            if cone is not None:
                cursor = cone.cursor()
                sql = "DELETE FROM usuarios WHERE id=%s"
                valor = (id_cliente,)
                cursor.execute(sql, valor)
                cone.commit()
                print(cursor.rowcount, "Registro eliminado")
                cone.close()

                messagebox.showinfo("Información", "Registro eliminado correctamente")
                actualizarTreeview()
            else:
                print("Error: No se pudo establecer la conexión")
    except mysql.connector.Error as error:
        print("Error al eliminar registro: {}".format(error))

formulario()
