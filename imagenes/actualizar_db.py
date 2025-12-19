from pymongo import MongoClient
import re

# --- CONFIGURACIÓN ---
# 1. Pega tu URI de Mongo (la misma que usaste para descargar)
MONGO_URI = "mongodb+srv://admin:Admin123@cluster0.5wobyyu.mongodb.net/deckmyl?appName=Cluster0" 

# 2. Nombre exacto de la base de datos y colección
DB_NAME = "deckmyl"
COLLECTION_NAME = "cards"

# 3. ⚠️ TU NUEVA URL DE GITHUB (vía jsDelivr)
# Cuando crees el repo 'deck-myl-assets' y subas la carpeta, la URL será así.
# IMPORTANTE: Reemplaza TU_USUARIO_GITHUB con tu nombre de usuario real.
BASE_URL = "https://cdn.jsdelivr.net/gh/TU_USUARIO_GITHUB/deck-myl-assets/imagenes_webp/"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def limpiar_nombre(nombre):
    if not nombre: return "sin_nombre"
    nombre = nombre.lower()
    nombre = re.sub(r'[^a-z0-9]', '_', nombre)
    nombre = re.sub(r'_+', '_', nombre)
    return nombre.strip('_')

print("🚀 Conectando a MongoDB para actualizar enlaces...")

cards = collection.find()
total = collection.count_documents({})
updates = 0

for card in cards:
    # Obtenemos el nombre para generar el mismo link que el archivo descargado
    nombre_limpio = limpiar_nombre(card.get('name'))
    
    # Creamos la nueva URL apuntando a TU GitHub con formato .webp
    nueva_url = f"{BASE_URL}{nombre_limpio}.webp"
    
    # Actualizamos el campo 'imgUrl' (que es el que usa tu app)
    # También agregamos 'imageUrl' y 'img' por si acaso los usas en otro lado
    collection.update_one(
        {'_id': card['_id']},
        {'$set': {
            'imgUrl': nueva_url,    # <--- El campo principal
            'imageUrl': nueva_url,  # <--- Respaldo
            'img': nueva_url        # <--- Respaldo
        }}
    )
    
    updates += 1
    if updates % 100 == 0:
        print(f"✅ {updates}/{total} cartas actualizadas...")

print(f"🏁 ¡LISTO! {updates} cartas ahora apuntan a tu servidor propio en GitHub.")