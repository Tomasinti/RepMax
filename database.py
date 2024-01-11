import os
from deta import Deta
from uuid import uuid4
from dotenv import load_dotenv

load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY")

deta = Deta(DETA_KEY)
db = deta.Base("repmax")


def insertar_periodo(fecha, ejercicio, peso, repeticiones, rm):
    nuevo_id = str(uuid4())
    
    # Insertar el nuevo registro con el ID único asociado al nombre del ejercicio
    db.put({"key": nuevo_id, "fecha": fecha, "ejercicio": ejercicio, "peso": peso, "repeticiones": repeticiones, "rm": rm, "id": nuevo_id})

    return nuevo_id  # Devolver el ID generado

def obtener_proximo_id():
    ultimo_registro = db.fetch(1, order_by=["-id"]).items
    if ultimo_registro:
        ultimo_id = ultimo_registro[0]["id"]
        return str(int(ultimo_id) + 1)
    else:
        return "1"
    
def eliminar_periodo(id):
    # Eliminar directamente el registro asociado al ID
    db.delete(id)

def buscar_periodos():
    res = db.fetch()
    return res.items

def traer_periodos(nuevo_id):
    return db.get(nuevo_id)