import requests

def obtener_informacion_usuario(data):
    url = f"http://18.225.55.46/api/{data}"
    respuesta = requests.get(url)

    if respuesta.status_code == 200:  # 200 indica éxito en la solicitud
        datos = respuesta.json()  # Convertir la respuesta JSON a un diccionario de Python
        return datos
    else:
        print(f"Error al obtener la información del usuario: {respuesta.status_code}")
        return None

# Utilizar la función para obtener información del usuario
nombre_usuario = "product/table/count"
informacion_usuario = obtener_informacion_usuario(nombre_usuario)
print (informacion_usuario)