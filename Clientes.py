from Conexion import *

class CClientes:

    def mostrarClientes():
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            cursor.execute("select *  from usuarios") 
            miResultado = cursor.fetchall()
            cone.commit()
            cone.close()
            return miResultado
        except mysql.connector.Error as error:
            print("Error de mostrar datos: {}", format(error))


    def ingresarClientes(nombres, apellidos, sexo):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = "INSERT INTO usuarios VALUES (NULL, %s, %s, %s);" 
            # la variable valores tiene que ser una tupla (un array que no se puede modificar)
            # como mínima expresión es: (valor,) la coma hace que sea una tupla
            # las tuplas son listas inmutables
            valores = (nombres, apellidos, sexo)
            cursor.execute(sql, valores)
            cone.commit()
            print(cursor.rowcount, "Registro ingresado")
            cone.close()
        except mysql.connector.Error as error:
            print("Error de acceso de datos: {}", format(error))
