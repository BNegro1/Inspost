import pyautogui
import time
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Autenticar y acceder a Google Drive
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# Descargar imágenes de la carpeta de Google Drive
folder_id = 'YOUR_FOLDER_ID'
file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()

# Descargar archivos a la carpeta local
download_path = './downloaded_images'
os.makedirs(download_path, exist_ok=True)

for file in file_list:
    file.GetContentFile(os.path.join(download_path, file['title']))

# Configuración de pyautogui
pyautogui.PAUSE = 1  # Pausa de 1 segundo entre cada comando

# Función para iniciar sesión en Instagram
def login_instagram(username, password):
    pyautogui.hotkey('ctrl', 't')
    pyautogui.write('https://www.instagram.com')
    pyautogui.press('enter')
    time.sleep(5)

    # Manejar posibles ventanas emergentes
    if pyautogui.locateOnScreen('path/to/accept_cookies_button.png'):
        pyautogui.click(pyautogui.locateCenterOnScreen('path/to/accept_cookies_button.png'))
        time.sleep(2)

    pyautogui.write(username)
    pyautogui.press('tab')
    pyautogui.write(password)
    pyautogui.press('enter')
    time.sleep(5)

# Función para subir una imagen a Instagram
def upload_image(image_path, caption):
    if pyautogui.locateOnScreen('path/to/upload_button.png'):
        pyautogui.click(pyautogui.locateCenterOnScreen('path/to/upload_button.png'))
    else:
        print("Upload button not found.")
        return
    
    time.sleep(2)
    
    pyautogui.write(image_path)
    pyautogui.press('enter')
    time.sleep(2)
    
    if pyautogui.locateOnScreen('path/to/next_button.png'):
        pyautogui.click(pyautogui.locateCenterOnScreen('path/to/next_button.png'))
    else:
        print("Next button not found.")
        return
    
    time.sleep(2)
    
    if pyautogui.locateOnScreen('path/to/share_button.png'):
        pyautogui.click(pyautogui.locateCenterOnScreen('path/to/share_button.png'))
    else:
        print("Share button not found.")
        return
    
    pyautogui.write(caption)
    pyautogui.click(pyautogui.locateCenterOnScreen('path/to/share_button.png'))
    time.sleep(5)

# Main Script
username = os.getenv('INSTAGRAM_USERNAME')
password = os.getenv('INSTAGRAM_PASSWORD')
login_instagram(username, password)

for image in os.listdir(download_path):
    image_path = os.path.join(download_path, image)
    caption = f'New post: {image}'
    upload_image(image_path, caption)
    time.sleep(60)  # Esperar un minuto antes de subir la siguiente imagen
