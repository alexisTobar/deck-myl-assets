from pymongo import MongoClient

# PEGA TU URI AQUÍ
MONGO_URI = "mongodb+srv://admin:Admin123@cluster0.5wobyyu.mongodb.net/deckmyl?appName=Cluster0" 

client = MongoClient(MONGO_URI)

print("🔍 BASES DE DATOS ENCONTRADAS:")
dbs = client.list_database_names()
print(dbs)

print("-" * 30)

for db_name in dbs:
    if db_name in ['admin', 'local']: continue # Saltamos las del sistema
    
    db = client[db_name]
    print(f"📂 DENTRO DE LA BASE DE DATOS: '{db_name}'")
    cols = db.list_collection_names()
    
    for col in cols:
        count = db[col].count_documents({})
        print(f"   └── Colección '{col}': tiene {count} documentos")

print("-" * 30)