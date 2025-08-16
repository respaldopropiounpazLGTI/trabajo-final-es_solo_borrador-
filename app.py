# Recordá que debes correr la aplicación en la terminal con el siguiente comando:
# flask --app app run

from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

DATA_FILE = "vuelos.json"

# Crea una función cargar_datos() que:
def cargar_datos():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Función auxiliar: guardar datos  
def guardar_datos(datos):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

    
# Consigna 1:
# Crea un endpoint de inicio GET / que retorne:
# {"mensaje": "API de Vuelos"} en formato JSON
@app.route("/", methods=["GET"])
def inicio():
    #pass
     """
    Endpoint inicial de la API. Retorna un mensaje de bienvenida.
    """
     return jsonify({"mensaje": "API de Vuelos"})

# Consigna 2:
# Crea un endpoint GET /api/vuelos que:
# 1. Cargue todos los datos usando cargar_datos()
# 2. Retorne los datos en formato JSON usando jsonify()
# 3. Aplique el método str.title() al campo "destino" de cada vuelo, de modo que se devuelva con la primera letra en mayúscula.
@app.route("/api/vuelos", methods=["GET"])
def listar_vuelos():
    #pass
    vuelos = cargar_datos()
    # Aplico .title() al campo "destino" de cada vuelo
    vuelos_con_formato = []
    for vuelo in vuelos:
        vuelo_formateado = vuelo.copy()
        if "destino" in vuelo_formateado and isinstance(vuelo_formateado["destino"], str):
            vuelo_formateado["destino"] = vuelo_formateado["destino"].title()
        vuelos_con_formato.append(vuelo_formateado)
    return jsonify(vuelos_con_formato)




# Consigna 3:
# Crea un endpoint GET /api/vuelos/<int:vuelo_id> que:
# 1. Cargue todos los datos
# 2. Busque el vuelo con el ID especificado
# 3. Si lo encuentra, retorne el vuelo en JSON
# 4. Si no lo encuentra, retorne {"error": "Vuelo no encontrado"} con código 404
# 5. Aplique el método str.title() al campo "destino" del vuelo, de modo que se devuelva con la primera letra en mayúscula.
@app.route("/api/vuelos/<int:vuelo_id>", methods=["GET"])
def obtener_vuelo(vuelo_id):
    #pass
    vuelos = cargar_datos()
    vuelo_encontrado = None
    for vuelo in vuelos:
        if vuelo.get("id") == vuelo_id:
            vuelo_encontrado = vuelo
            break
    
    if vuelo_encontrado:
        # Aplica .title() al destino del vuelo encontrado
        vuelo_encontrado["destino"] = vuelo_encontrado["destino"].title()
        return jsonify(vuelo_encontrado)
    else:
        return jsonify({"error": "Vuelo no encontrado"}), 404















# Consigna 4:
# Crea un endpoint POST /api/vuelos que:
# 1. Obtenga los datos JSON de la petición con request.get_json()
# 2. Valide que el campo "destino" esté presente y no esté vacío
# 3. Si no está, retorne {"error": "El campo 'destino' es obligatorio"} con código 400
# 4. Cargue los datos existentes
# 5. Asigne un ID automático: último ID + 1, o 1 si no hay datos
# 6.  Asigne valores por defecto: capacidad=100, vendidos=0 si no se especifican.
#     Convierta siempre el campo "destino" a minúsculas antes de guardar usando el método str.lower().
# 7. Agregue el nuevo vuelo a la lista
# 8. Guarde los datos actualizados
# 9. Retorne el nuevo vuelo con código 201
# 10. Minuscula
@app.route("/api/vuelos", methods=["POST"])
def agregar_vuelo():
    #pass
    nuevo_vuelo = request.get_json()
    if not nuevo_vuelo or "destino" not in nuevo_vuelo or not nuevo_vuelo["destino"].strip():
        return jsonify({"error": "El campo 'destino' es obligatorio"}), 400

    vuelos = cargar_datos()
    if vuelos:
        ultimo_id = max(vuelo["id"] for vuelo in vuelos)
        nuevo_id = ultimo_id + 1
    else:
        nuevo_id = 1
    vuelo_a_guardar = {
        "id": nuevo_id,
        "destino": nuevo_vuelo["destino"].strip().lower(),
        "capacidad": nuevo_vuelo.get("capacidad", 100),
        "vendidos": nuevo_vuelo.get("vendidos", 0)
    }
    try: 
        vuelo_a_guardar["capacidad"] = int(vuelo_a_guardar["capacidad"])
        vuelo_a_guardar["vendidos"] = int(vuelo_a_guardar["vendidos"])
    except (ValueError, TypeError):
        return jsonify({"error": "Capacidad y vendidos deben ser números enteros"}), 400
    vuelos.append(vuelo_a_guardar)
    guardar_datos(vuelos)
    return jsonify(vuelo_a_guardar), 201







# Consigna 5:
# Crea un endpoint PUT /api/vuelos/<int:vuelo_id> que:
# 1. Obtenga los datos JSON de la petición
# 2. Cargue todos los datos existentes
# 3. Busque el vuelo por ID
# 4. Si lo encuentra, actualice sus campos con vuelo.update().
#    Convierta siempre el campo "destino" a minúsculas antes de actualizar usando el método str.lower()
# 5. Guarde los datos actualizados y retorne el vuelo actualizado
# 6. Si no lo encuentra, retorne {"error": "Vuelo no encontrado"} con código 404
# 7. Minuscula
@app.route("/api/vuelos/<int:vuelo_id>", methods=["PUT"])
def actualizar_vuelo(vuelo_id):
    #pass
    vuelos = cargar_datos()
    datos_actualizacion = request.get_json()
    
    for vuelo in vuelos:
        if vuelo.get("id") == vuelo_id:
            if "destino" in datos_actualizacion:
                datos_actualizacion["destino"] = datos_actualizacion["destino"].lower()
            vuelo.update(datos_actualizacion)
            guardar_datos(vuelos)
            return jsonify(vuelo)
            
    return jsonify({"error": "Vuelo no encontrado"}), 404












# Consigna 6:
# Crea un endpoint DELETE /api/vuelos/<int:vuelo_id> que:
# 1. Cargue todos los datos
# 2. Filtre los datos excluyendo el vuelo con el ID especificado (opcionalmente podés usar listas por comprensión).
# 3. Compare si las listas tienen el mismo tamaño (no se eliminó nada)
# 4. Si son iguales, retorne {"error": "Vuelo no encontrado"} con código 404
# 5. Si son diferentes, guarde los datos filtrados
# 6. Retorne {"mensaje": f"Vuelo {vuelo_id} eliminado correctamente"}
@app.route("/api/vuelos/<int:vuelo_id>", methods=["DELETE"])
def eliminar_vuelo(vuelo_id):
    #pass
    vuelos = cargar_datos()
    vuelos_antes_filtro = len(vuelos)
    vuelos = [vuelo for vuelo in vuelos if vuelo.get("id") != vuelo_id]
    if len(vuelos) == vuelos_antes_filtro:
        return jsonify({"error": "Vuelo no encontrado "}), 404
    else:
        guardar_datos(vuelos)
        return jsonify({"mensaje ": f"Vuelo {vuelo_id} eliminado"})
























# Consigna 7:
# Crear un endpoint POST /vender que:
# 1. Obtenga los datos JSON de la petición.
# El campo id del vuelo se envía en el body del request, por ejemplo:
# {
#   "id": 1
# }
# Tips: en Flask se obtiene así:
# datos = request.get_json()
# vuelo_id = datos.get("id")
# 2. Cargue todos los vuelos existentes.
# 3. Busque el vuelo por su id.
# 4. Si no lo encuentra, devuelva {"error": "Vuelo no encontrado"} con código 404.
# 5. Verifique que vendidos < capacidad:
#   - Si hay lugar disponible, incremente "vendidos" en 1.
#   - Si el vuelo está completo (vendidos >= capacidad), devuelva {"error": "Vuelo completo"} con código 400.
# 6. Guarde los datos actualizados.
# 7. Devuelva el vuelo actualizado en formato JSON.
@app.route("/api/vender", methods=["POST"])
def vender_vuelo():
    #pass
    datos = request.get_json() 
    vuelo_id = datos.get("id")
    if not vuelo_id:
        return jsonify({"error": "El valor  'id' es obligatorio"}), 400
    
    vuelos = cargar_datos()
    vuelo_encontrado = None
    for vuelo in vuelos:
        if vuelo.get("id") == vuelo_id:
            vuelo_encontrado = vuelo
            break

    if not vuelo_encontrado:
        return jsonify({"error": "Vuelo no encontrado "}), 404
    if vuelo_encontrado["vendidos"] >= vuelo_encontrado["capacidad"]:
        return jsonify({"error": "este vuelo esta  completo "}), 400
    vuelo_encontrado["vendidos"] += 1
    guardar_datos(vuelos)
    return jsonify(vuelo_encontrado)

if __name__ == "__main__":
    # Asegura que el archivo vuelos.json existe al iniciar la aplicación
    if not os.path.exists(DATA_FILE):
        guardar_datos([])
    app.run(debug=True)



if __name__ == "__main__":
    if not os.path.exists(DATA_FILE):
        guardar_datos([])
    app.run(debug=True)


# EJEMPLOS DE CÓMO PROBAR LA API:

# Crear vuelo:
# curl -X POST http://localhost:5000/api/vuelos \
#   -H "Content-Type: application/json" \
#   -d '{"destino": "Buenos Aires", "capacidad": 150}'

# Listar vuelos:
# curl http://localhost:5000/api/vuelos

# Ver vuelo específico:
# curl http://localhost:5000/api/vuelos/1

# Actualizar vuelo:
# curl -X PUT http://localhost:5000/api/vuelos/1 \
#   -H "Content-Type: application/json" \
#   -d '{"destino": "Córdoba", "vendidos": 25}'

# Eliminar vuelo:
# curl -X DELETE http://localhost:5000/api/vuelos/1

#Vender vuelo:
#curl -X POST http://localhost:5000/vender \
#  -H "Content-Type: application/json" \
#  -d '{"id": 1}'