import requests

url = "http://localhost:8000/"


ruta_post = url + "/characters"

print("-------------CREA UNA NUEVO PERSONAJE -------------")
ruta_post = url + "characteres"
new_character = {
    "name": "Gandalf",
    "level": 10,
    "role": "Wizard",
    "charisma": 15,
    "strength": 10,
    "dexterity": 10,
}
post_response = requests.request(method="POST", url=ruta_post, data=new_character)
print(post_response.text)


print("-----------LISTAR TODOS LOS PERSONAJES-----------------")
ruta_get = url + "/charecters"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

print(
    "----------------------LISTAR TODOS LOS ARCHER, con nivel a 5 y carisma a 10------------------"
)
ruta_get = url + "charecters/?role=Archer&level=5&charisma=10"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)


print(get_response.text)
print("-------------------ACTUALIZAR POR ID-------------------")
ruta_put = url + "characteres/3"
actualizacion_personaje = {"charisma": 20, "strength": 15, "dexterity": 15}
put_response = requests.request(
    method="PUT", url=ruta_put, data=actualizacion_personaje
)
print(put_response.text)


print("-------------------ELIMINAR POR ID-------------------")
ruta_delete = url + "character/1"
delete_response = requests.request(method="DELETE", url=ruta_delete)
print(delete_response.text)

print(
    "-------------------Crear un nuevo personaje que el id sea unico y correlativo-------------------"
)

ruta_post = url + "characteres"
new_character = {
    "name": "Harry Potter",
    "level": 5,
    "role": "Magician",
    "charisma": 15,
    "strength": 10,
    "dexterity": 10,
}
post_response = requests.request(method="POST", url=ruta_post, data=new_character)
print(post_response.text)
