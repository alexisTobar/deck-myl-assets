import os
import requests
import re
from pymongo import MongoClient
from PIL import Image 
from io import BytesIO
import time

# --- CONFIGURACIÓN ---
MONGO_URI = "mongodb+srv://admin:Admin123@cluster0.5wobyyu.mongodb.net/deckmyl?appName=Cluster0" # <--- ASEGÚRATE DE QUE ESTO ESTÉ BIEN
DB_NAME = "deckmyl"
COLLECTION_NAME = "cards"
OUTPUT_FOLDER = "imagenes_webp"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def limpiar_nombre(nombre):
    if not nombre: return "carta_sin_nombre"
    nombre = nombre.lower()
    nombre = re.sub(r'[^a-z0-9]', '_', nombre)
    nombre = re.sub(r'_+', '_', nombre)
    return nombre.strip('_')

cards = collection.find()
total = collection.count_documents({})
contador = 0

print(f"🔥 Iniciando escaneo de {total} cartas...")

# --- DEBUG: IMPRIMIR LA PRIMERA CARTA PARA VER SUS CAMPOS ---
print("\n🔍 REVISANDO LA ESTRUCTURA DE LA PRIMERA CARTA:")
primer_doc = collection.find_one()
print(primer_doc)
print("-" * 30 + "\n")

for card in cards:
    # ⚠️ AQUÍ ESTÁ EL CAMBIO: Buscamos en TODAS las opciones posibles
    original_url = (
        card.get('imageUrl') or 
        card.get('img') or 
        card.get('imagen') or 
        card.get('url') or 
        card.get('imgUrl')
    )
    
    nombre_carta = card.get('name', 'Desconocida')

    # Diagnóstico: Si no encuentra URL, nos avisa
    if not original_url:
        # Descomenta la siguiente línea si quieres ver en consola cuáles fallan:
        # print(f"⚠️ Saltando '{nombre_carta}': No tiene campo de imagen detectado.")
        continue

    # Filtro: Si es localhost, no podemos descargarla
    if "localhost" in original_url:
        print(f"⚠️ Saltando '{nombre_carta}': La URL es local (localhost).")
        continue

    nombre_base = limpiar_nombre(nombre_carta)
    nombre_archivo = f"{nombre_base}.webp"
    ruta_guardado = os.path.join(OUTPUT_FOLDER, nombre_archivo)

    if os.path.exists(ruta_guardado):
        # print(f"✅ Ya existe: {nombre_archivo}") # Comentado para no llenar la consola
        contador += 1
        continue

    try:
        response = requests.get(original_url, timeout=10)
        
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            
            if img.mode in ("RGBA", "P"): 
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")

            img.save(ruta_guardado, 'WEBP', quality=85, method=6)
            contador += 1
            
            # Imprimimos cada 10 cartas para que veas que avanza
            if contador % 10 == 0:
                print(f"✨ Procesadas {contador}/{total} ... (Última: {nombre_archivo})")
        else:
            print(f"❌ Error HTTP {response.status_code}: {nombre_carta}")
            
    except Exception as e:
        print(f"🔥 Error en '{nombre_carta}': {e}")
    
print(f"\n🎉 ¡Proceso finalizado! Total imágenes en carpeta: {contador}")