from pydantic import BaseModel
class Dosis(BaseModel):
    Cedula:str
    NombreVacuna:str
    Provincia:str
    Fecha_Vacunacion:str