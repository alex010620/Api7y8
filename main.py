import mysql.connector
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from DatosVacunacionFirst import DatosVacunacionFirst
from Dosis import Dosis
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

server = 'vtrd.mysql.database.azure.com'
database = 'VacunateRDv'
username = 'ADMyamc@vtrd'

password = "Ya95509550"  


conexion = mysql.connector.connect(user="ADMyamc@vtrd", password="Ya95509550", host="vtrd.mysql.database.azure.com",database="VacunateRDv")

@app.get("/")
def root():
    return {'Sistema': 'ApiVacunaRD'}

@app.get("/api/ConsultarCedula/{cedula}")
def ConsultarCedula(cedula:str):
    Cedul=""
    conexion.reconnect()
    cursor = conexion.cursor()
    cursor.execute("SELECT Cedula FROM Usuarios WHERE Cedula = '"+cedula+"'")
    contenido = cursor.fetchall()
    for i in contenido:
        Cedul = i[0]
    if cedula == Cedul:
        return True
    else:
        return False

@app.post("/api/RegistrarVacunadosFirst")
def RegistrarVacunadosFirst(d:DatosVacunacionFirst):
    try:
        conexion.reconnect()
        cursor = conexion.cursor()
        sql = "INSERT INTO Usuarios(Cedula,Nombre,Apellido,Telefono,Fecha_Nacimiento,Zodiaco)VALUES('"+d.Cedula+"','"+d.Nombre+"','"+d.Apellido+"','"+d.Telefono+"','"+d.Fecha_Nacimiento+"','"+d.Zodiaco+"')"
        sql2 = "INSERT INTO Vacunas(CedulaVacunado,NombreVacuna,Provincia,Fecha_Vacunacion)VALUES('"+d.Cedula+"','"+d.NombreVacuna+"','"+d.Provincia+"','"+d.Fecha_Vacunacion+"')"
        cursor.execute(sql)
        cursor.execute(sql2)
        conexion.commit()
        return {"ok":True}
    except TypeError:
        return{"ok":False}

@app.post("/api/OtrasDosis")
def OtrasDosis(d:Dosis):
    try:
        conexion.reconnect()
        cursor = conexion.cursor()
        sql2 = "INSERT INTO Vacunas(CedulaVacunado,NombreVacuna,Provincia,Fecha_Vacunacion)VALUES('"+d.Cedula+"','"+d.NombreVacuna+"','"+d.Provincia+"','"+d.Fecha_Vacunacion+"')"
        cursor.execute(sql2)
        conexion.commit()
        return {"ok":True}
    except:
        return{"ok":False}

@app.get("/api/ConsultaDeVacunados")
def ConsultaDeVacunados():
    Datos = []
    conexion.reconnect()
    cursor = conexion.cursor()
    cursor.callproc('SP_ConsultaDeVacunados')
    conexion.commit()
    for result in cursor.stored_results():
        contenido = result.fetchall()
    for i in contenido:
        Datos.append({"IdUsuario":i[0],"Cedula":i[1],"Nombre": i[2], "Apellido": i[3], "Telefono": i[4],"Fecha_Nacimiento":i[5],"Zodiaco":i[6],"Cantidad":i[7]})
    return Datos

@app.get("/api/ConsultaDeVacunadoUnico/{NombreOApellido}")
def ConsultaDeVacunadoUnico(NombreOApellido:str):
    Datos = []
    idf = 0
    Cedula=""
    Nombre=""
    Apellido=""
    Telefono=""
    Fecha_Nacimiento=""
    Zodiaco=""
    Cantidad=""
    conexion.reconnect()
    cursor = conexion.cursor()
    cursor.execute("SELECT U.*, Count(V.IdVacuna) As Cantidaddevacunas FROM Usuarios AS U INNER JOIN Vacunas AS V ON U.Cedula = V.CedulaVacunado WHERE U.Nombre = '"+NombreOApellido+"' or U.Apellido= '"+NombreOApellido+"' GROUP BY U.idUsuario,U.Cedula, U.Nombre, U.Apellido,U.Telefono,U.Fecha_Nacimiento,U.Zodiaco")
    contenido = cursor.fetchall()
    conexion.commit()
    for i in contenido:
        idf = i[0]
        Cedula=i[1]
        Nombre= i[2]
        Apellido= i[3]
        Telefono= i[4]
        Fecha_Nacimiento=i[5]
        Zodiaco=i[6]
        Cantidad=i[7]
    cursor.execute("select NombreVacuna, Provincia,Fecha_Vacunacion from Vacunas WHERE CedulaVacunado = '"+Cedula+"'")
    contenido2 = cursor.fetchall()
    for i in contenido2:
        Datos.append({"NombreVacuna":i[0], "Provincia":i[1], "FechaVacunacion":i[2]})

    return {"idUsuario":idf,"Cedula":Cedula,"Nombre": Nombre, "Apellido": Apellido, "Telefono": Telefono,"Fecha_Nacimiento":Fecha_Nacimiento
                    ,"Zodiaco":Zodiaco,"Cantidad":Cantidad, "DatosVAcunas": Datos}

@app.get("/api/VacunadosPorProvincia/{provincia}")
def VacunadosPorProvincia(provincia:str):
    Datos = []
    conexion.reconnect()
    cursor = conexion.cursor()
    cursor.execute("SELECT U.Cedula,U.Nombre, U.Apellido,U.Telefono,V.NombreVacuna,V.Provincia,V.Fecha_Vacunacion,U.IdUsuario FROM Usuarios AS U INNER JOIN Vacunas AS V ON U.Cedula = V.CedulaVacunado WHERE V.Provincia = '"+provincia+"' GROUP BY U.Cedula, U.Nombre,U.Apellido,U.Telefono,V.NombreVacuna,V.Provincia,V.Fecha_Vacunacion,U.IdUsuario")
    contenido = cursor.fetchall()
    conexion.commit()
    for i in contenido:
        Datos.append({"ok":True,"Cedula":i[0],"Nombre": i[1], "Apellido": i[2], "Telefono": i[3],"NombreVacuna":i[4],
                    "Provincia":i[5],"Fecha_Vacunacion":i[6], "IdUsuario":[7]})
    if Datos == []:
        return {"ok":False}
    else:
        return Datos

@app.get("/api/VacunadosPorMarcaDeVacuna")
def VacunadosPorMarcaDeVacuna():
    Datos = []
    conexion.reconnect()
    cursor = conexion.cursor()
    cursor.callproc('SP_VacunadosPorMarcaDeVacuna')
    conexion.commit()
    for result in cursor.stored_results():
        contenido = result.fetchall()
    for i in contenido:
        Datos.append({"ok":True,"NombreVacuna":i[0],"Cantidad":i[1]})
    if Datos == []:
        return {"ok":False}
    else:
        return Datos



@app.get("/api/VacunadosPorZodiaco")
def VacunadosPorZodiaco():
    Datos = []
    conexion.reconnect()
    cursor = conexion.cursor()
    cursor.execute('Select Zodiaco, Count(IdUsuario) as Cantidad from Usuarios where Zodiaco = Zodiaco GROUP BY Zodiaco')
    contenido = cursor.fetchall()
    conexion.commit()
    for i in contenido:
        Datos.append({"ok":True,"Zodiaco":i[0],"Cantidad":i[1]})
    if Datos == []:
        return {"ok":False}
    else:
        return Datos



@app.delete("/api/EliminarRegistroVacunado/{IdUser}")
def EliminarRegistroVacunado(IdUser:str):
    try:
        Cedula = ""
        conexion.reconnect()
        cursor = conexion.cursor()
        cursor.execute("Select CedulaVacunado from Vacunas where IdVacuna = '"+IdUser+"'")
        contenido = cursor.fetchall()
        conexion.commit()
        for i in contenido:
            Cedula = i[0]
        cursor.execute("Delete from Usuarios where IdUsuario = '"+IdUser+"'")
        cursor.execute("Delete from Vacunas where CedulaVacunado = '"+Cedula+"'")
        return {"ok":True}
    except TypeError as e:
        return e

#CRUD PROVINCIAS

#Select All
@app.get("/api/Provincias")
def Provincias():
    try:
        Datos =[]
        conexion.reconnect()
        cursor = conexion.cursor()
        cursor.execute("SELECT IdProvincia, NombreProvincia FROM Provincias")
        contenido = cursor.fetchall()
        for i in contenido:
            Datos.append({"ok":True,"IdProvincia":i[0],"NombredeProvincia":i[1]})
        if Datos == []:
            return {"ok":False}
        else:
            return Datos
    except TypeError:
        return{"ok":False}
#Create
@app.post("/api/NuevaProvincia/{Nombre}")
def NuevaProvincia(Nombre:str):
    try:
        N = ""
        conexion.reconnect()
        cursor = conexion.cursor()
        cursor.execute("SELECT NombreProvincia FROM Provincias WHERE NombreProvincia = '"+Nombre+"'")
        contenido = cursor.fetchall()
        for i in contenido:
            N = i[0]
        if Nombre == N:
            return {"ok":False}
        else:
            Provincia = (Nombre)
            sql = "INSERT INTO Provincias(NombreProvincia) VALUES ('"+Nombre+"')"
            cursor.execute(sql, Provincia)
            conexion.commit()
            return {"ok":True}
    except TypeError:
        return{"ok":False}
#UPDATE
@app.put("/api/ActualizarProvincia/{IdProvincia}/{NuevoNombre}")
def ActualizarProvincia(IdProvincia:str,NuevoNombre:str):
    try:
        conexion.reconnect()
        cursor = conexion.cursor()
        cursor.execute("Update Provincias set NombreProvincia = '"+NuevoNombre+"' where IdProvincia = '"+IdProvincia+"'")
        conexion.commit()
        return {"ok":True}
    except:
        return {"ok":False}
#Delete
@app.delete("/api/EliminarProvincia/{IdProvincia}")
def EliminarProvincia(IdProvincia:str):
    try:
        conexion.reconnect()
        cursor = conexion.cursor()
        cursor.execute("Delete from Provincias where IdProvincia = '"+IdProvincia+"'")
        conexion.commit()
        return {"ok":True}
    except:
        return {"ok":False}

#CRUD VacunasExistente

#Select All
@app.get("/api/VacunasExistente")
def VacunasExistente():
    try:
        Datos =[]
        conexion.reconnect()
        cursor = conexion.cursor()
        cursor.execute("SELECT IdVacuna, NombreVacuna FROM VacunasExistente")
        contenido = cursor.fetchall()
        for i in contenido:
            Datos.append({"ok":True,"IdVacuna":i[0],"NombreVacuna":i[1]})
        if Datos == []:
            return {"ok":False}
        else:
            return Datos
    except TypeError:
        return{"ok":False}
#Create
@app.post("/api/NuevoNombreVacuna/{Nombre}")
def NuevoNombreVacuna(Nombre:str):
    try:
        N = ""
        conexion.reconnect()
        cursor = conexion.cursor()
        cursor.execute("SELECT NombreVacuna FROM VacunasExistente WHERE NombreVacuna = '"+Nombre+"'")
        contenido = cursor.fetchall()
        for i in contenido:
            N = i[0]
        if Nombre == N:
            return {"ok":False}
        else:
            sql = "INSERT INTO VacunasExistente(NombreVacuna)VALUES('"+Nombre+"')"
            cursor.execute(sql)
            conexion.commit()
            return {"ok":True}
    except TypeError:
        return{"ok":False}
#UPDATE
@app.put("/api/ActualizarVacuna/{IdVacuna}/{NuevoNombre}")
def ActualizarVacuna(IdVacuna:str,NuevoNombre:str):
    try:
        conexion.reconnect()
        cursor = conexion.cursor()
        cursor.execute("Update VacunasExistente set NombreVacuna = '"+NuevoNombre+"' where IdVacuna = '"+IdVacuna+"'")
        conexion.commit()
        return {"ok":True}
    except:
        return {"ok":True}
#Delete
@app.delete("/api/EliminarVacuna/{IdVacuna}")
def EliminarVacuna(IdVacuna:str):
    try:
        conexion.reconnect()
        cursor = conexion.cursor()
        cursor.execute("Delete from VacunasExistente where IdVacuna = '"+IdVacuna+"'")
        conexion.commit()
        return {"ok":True}
    except:
        return {"ok":True}
