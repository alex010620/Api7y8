from Conexion import conexion
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
@app.get("/")
def root():
    return {'Sistema': 'VacunaRD'}

@app.get("/api/ConsultarCedula/{cedula}")
def ConsultarCedula(cedula:str):
    Cedul=""
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
        cursor = conexion.cursor()
        TablaUser = (d.Cedula,d.Nombre,d.Apellido,d.Telefono,d.Fecha_Nacimiento,d.Zodiaco)
        TablaVacuna = (d.Cedula,d.NombreVacuna,d.Provincia,d.Fecha_Vacunacion)
        sql = '''INSERT INTO Usuarios(Cedula,Nombre,Apellido,Telefono,Fecha_Nacimiento,Zodiaco)VALUES(?,?,?,?,?,?)'''
        sql2 = '''INSERT INTO Vacunas(CedulaVacunado,NombreVacuna,Provincia,Fecha_Vacunacion)VALUES(?,?,?,?)'''
        cursor.execute(sql, TablaUser)
        cursor.execute(sql2, TablaVacuna)
        conexion.commit()
        return {"ok":True}
    except TypeError:
        return{"ok":False}

@app.post("/api/OtrasDosis")
def OtrasDosis(d:Dosis):
    try:
        cursor = conexion.cursor()
        TablaVacuna = (d.Cedula,d.NombreVacuna,d.Provincia,d.Fecha_Vacunacion)
        sql2 = '''INSERT INTO Vacunas(CedulaVacunado,NombreVacuna,Provincia,Fecha_Vacunacion)VALUES(?,?,?,?)'''
        cursor.execute(sql2, TablaVacuna)
        conexion.commit()
        return {"ok":True}
    except:
        return{"ok":False}

@app.get("/api/ConsultaDeVacunados")
def ConsultaDeVacunados():
    Datos = []
    cursor = conexion.cursor()
    cursor.execute('SP_ConsultaDeVacunados')
    contenido = cursor.fetchall()
    conexion.commit()
    for i in contenido:
        Datos.append({"Cedula":i[1],"Nombre": i[2], "Apellido": i[3], "Telefono": i[4],"Fecha_Nacimiento":i[5]
                    ,"Zodiaco":i[6],"Cantidad":i[7]})
    return Datos

@app.get("/api/ConsultaDeVacunadoUnico/{NombreOApellido}")
def ConsultaDeVacunadoUnico(NombreOApellido:str):
    Datos = []
    Cedula=""
    Nombre=""
    Apellido=""
    Telefono=""
    Fecha_Nacimiento=""
    Zodiaco=""
    Cantidad=""
    cursor = conexion.cursor()
    cursor.execute("SP_ConsultaDeVacunadoUnico '"+NombreOApellido+"'")
    contenido = cursor.fetchall()
    conexion.commit()
    for i in contenido:
        Cedula=i[1]
        Nombre= i[2]
        Apellido= i[3]
        Telefono= i[4]
        Fecha_Nacimiento=i[5]
        Zodiaco=i[6]
        Cantidad=i[7]
    cursor.execute("select NombreVacuna, Provincia,Fecha_Vacunacion from [dbo].[Vacunas] WHERE CedulaVacunado = '"+Cedula+"'")
    contenido2 = cursor.fetchall()
    for i in contenido2:
        Datos.append({"NombreVacuna":i[0], "Provincia":i[1], "FechaVacunacion":i[2]})

    return {"Cedula":Cedula,"Nombre": Nombre, "Apellido": Apellido, "Telefono": Telefono,"Fecha_Nacimiento":Fecha_Nacimiento
                    ,"Zodiaco":Zodiaco,"Cantidad":Cantidad, "DatosVAcunas": Datos}

@app.get("/api/VacunadosPorProvincia/{provincia}")
def VacunadosPorProvincia(provincia:str):
    Datos = []
    cursor = conexion.cursor()
    cursor.execute("SP_VacunadosPorProvincia '"+provincia+"'")
    contenido = cursor.fetchall()
    conexion.commit()
    for i in contenido:
        Datos.append({"ok":True,"Cedula":i[0],"Nombre": i[1], "Apellido": i[2], "Telefono": i[3],"NombreVacuna":i[4],
                    "Provincia":i[5],"Fecha_Vacunacion":i[6]})
    if Datos == []:
        return {"ok":False}
    else:
        return Datos

@app.get("/api/VacunadosPorMarcaDeVacuna")
def VacunadosPorMarcaDeVacuna():
    Datos = []
    cursor = conexion.cursor()
    cursor.execute('SP_VacunadosPorMarcaDeVacuna')
    contenido = cursor.fetchall()
    conexion.commit()
    for i in contenido:
        Datos.append({"ok":True,"NombreVacuna":i[0],"Cantidad":i[1]})
    if Datos == []:
        return {"ok":False}
    else:
        return Datos

@app.get("/api/VacunadosPorZodiaco")
def VacunadosPorZodiaco():
    Datos = []
    cursor = conexion.cursor()
    cursor.execute('SP_VacunadosPorZodiaco')
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
        cursor = conexion.cursor()
        cursor.execute("Delete from [dbo].[Usuarios] where IdUsuario = '"+IdUser+"'")
        conexion.commit()
        return {"ok":True}
    except:
        return {"ok":False}

#CRUD PROVINCIAS

#Select All
@app.get("/api/Provincias")
def Provincias():
    try:
        Datos =[]
        cursor = conexion.cursor()
        cursor.execute("SELECT IdProvincia, NombreProvincia FROM Provincias")
        contenido = cursor.fetchall()
        for i in contenido:
            Datos.append({"ok":True,"IdProvincia":i[0],"NombreProvincia":i[1]})
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
        cursor = conexion.cursor()
        cursor.execute("SELECT NombreProvincia FROM Provincias WHERE NombreProvincia = '"+Nombre+"'")
        contenido = cursor.fetchall()
        for i in contenido:
            N = i[0]
        if Nombre == N:
            return {"ok":False}
        else:
            Provincia = (Nombre)
            sql = '''INSERT INTO Provincias(NombreProvincia)VALUES(?)'''
            cursor.execute(sql, Provincia)
            conexion.commit()
            return {"ok":True}
    except TypeError:
        return{"ok":False}
#UPDATE
@app.put("/api/ActualizarProvincia/{IdProvincia}/{NuevoNombre}")
def ActualizarProvincia(IdProvincia:str,NuevoNombre:str):
    try:
        cursor = conexion.cursor()
        cursor.execute("Update [dbo].[Provincias] set NombreProvincia = '"+NuevoNombre+"' where IdProvincia = '"+IdProvincia+"'")
        conexion.commit()
        return {"ok":True}
    except:
        return {"ok":False}
#Delete
@app.delete("/api/EliminarProvincia/{IdProvincia}")
def EliminarProvincia(IdProvincia:str):
    try:
        cursor = conexion.cursor()
        cursor.execute("Delete from [dbo].[Provincias] where IdProvincia = '"+IdProvincia+"'")
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
        cursor = conexion.cursor()
        cursor.execute("SELECT NombreVacuna FROM VacunasExistente WHERE NombreVacuna = '"+Nombre+"'")
        contenido = cursor.fetchall()
        for i in contenido:
            N = i[0]
        if Nombre == N:
            return {"ok":False}
        else:
            Provincia = (Nombre)
            sql = '''INSERT INTO VacunasExistente(NombreVacuna)VALUES(?)'''
            cursor.execute(sql, Provincia)
            conexion.commit()
            return {"ok":True}
    except TypeError:
        return{"ok":False}
#UPDATE
@app.put("/api/ActualizarVacuna/{IdVacuna}/{NuevoNombre}")
def ActualizarVacuna(IdVacuna:str,NuevoNombre:str):
    try:
        cursor = conexion.cursor()
        cursor.execute("Update [dbo].[VacunasExistente] set NombreVacuna = '"+NuevoNombre+"' where IdVacuna = '"+IdVacuna+"'")
        conexion.commit()
        return {"ok":True}
    except:
        return {"ok":True}
#Delete
@app.delete("/api/EliminarVacuna/{IdVacuna}")
def EliminarVacuna(IdVacuna:str):
    try:
        cursor = conexion.cursor()
        cursor.execute("Delete from [dbo].[VacunasExistente] where IdVacuna = '"+IdVacuna+"'")
        conexion.commit()
        return {"ok":True}
    except:
        return {"ok":True}
