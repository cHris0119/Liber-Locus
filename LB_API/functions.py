import base64
import re
import os
import time
from PIL import Image



def int_id():
    # Obtener el tiempo actual en segundos desde la época (timestamp)
    timestamp = int(time.time())
    # Formatear el timestamp como DDMMSS
    formatted_time = time.strftime("%d%H%m%S", time.localtime(timestamp))
    # Convertir la cadena formateada a un número entero
    return int(formatted_time)

def intCreation(id):
    # Obtener el tiempo actual en segundos desde la época (timestamp)
    timestamp = int(time.time())
    # Formatear el timestamp como DDMMSS
    formatted_time = time.strftime("%d%H%m", time.localtime(timestamp))
    idCreate = str(id) + formatted_time
    return int(idCreate)


def validacionCE(passw):
    special_characters_pattern = r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\]'
    
    if re.search(special_characters_pattern, passw):
        return True
    else:
        return False
    
def validacionMAYUS(passw):
    mayus = r'[ABCDEFGHIJKLMNOPQRSTUVWXYZ]'
    
    if re.search(mayus, passw):
        return True
    else:
        return False
    
def validacionNum(passw):
    num = r'[1234567890]'
    
    if re.search(num, passw):
        return True
    else:
        return False
    
    
def get_image_format(image_path):
    try:
        with Image.open(image_path) as img:
            return img.format
    except Exception as e:
        # Manejar excepciones si ocurre algún error al abrir la imagen
        return None

def base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
            image_base64 = base64.b64encode(image_data)
            return image_base64.decode('utf-8')  # Decodificar a cadena
    else:
        return None