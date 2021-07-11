from pydantic import BaseModel
class DatosVacunacionFirst(BaseModel):
    Cedula:str
    Nombre:str
    Apellido:str
    Telefono:str
    Fecha_Nacimiento:str
    Zodiaco:str
    NombreVacuna:str
    Provincia:str
    Fecha_Vacunacion:str