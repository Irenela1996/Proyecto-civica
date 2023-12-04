import datetime
import os
import threading
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.action_chains import ActionChains

NO_SUCH_ELEMENT = "No se ha encontrado el elemento"
# ELEMENTOS
REJECT = (By.XPATH, '//button[contains(., "Rechazar todo")]')
TITLE = (By.ID, "video-title")
PELICULA = (By.ID, "thumbnail")
TIPO_PELICULA = (By.CLASS_NAME, "grid-movie-renderer-metadata")
COMPRA_O_ALQUILER = (By.CLASS_NAME, "style-scope ytd-badge-supported-renderer")
TIEMPO = (By.ID, "text")


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")

    # Inicializar el navegador
    service = Service()
    ChromeDriverManager().install()
    # Creamos el driver
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    return driver


def cargar_pagina(driver, pagina):
    print(f"Cargando página {pagina}...")
    # Cargamos la página
    driver.get(pagina)

    esperar_un_elemento(driver, 10, REJECT)
    driver.find_element(*REJECT).click()
    return driver


def hacer_scroll(driver):
    SCROLL_PAUSE_TIME = 0.5
    # se hace un scroll de 400px
    driver.execute_script("window.scrollBy(0, 400);")
    time.sleep(SCROLL_PAUSE_TIME)


def get_titulos(driver):
    esperar_un_elemento(driver, 10, TITLE)
    # Cogemos todos los elementos cuyo id sea video-title
    videos = driver.find_elements(*TITLE)
    print(f"Se han encontrado {len(videos)} vídeos")
    # Guardamos los títulos de los vídeos en un array
    titulos = []

    for video in videos:
        titulos.append(video.text)
    return titulos


def get_tipo_pelicula(driver):
    esperar_un_elemento(driver, 10, TIPO_PELICULA)
    # Cogemos todos los elementos cuya clase sea grid-movie-renderer-metadata
    tipos = driver.find_elements(*TIPO_PELICULA)
    # Guardamos los tipos de los vídeos en un array
    tipos_videos = []
    year = []
    for tipo in tipos:
        # El texto viene así: Drama • 2023
        # Separamos el texto por el caracter •
        # Y nos quedamos con el primer elemento
        # Que es el tipo de película
        tipos_videos.append(tipo.text.split("•")[0])
        # Y nos quedamos con el segundo elemento
        # Que es el año
        year.append(tipo.text.split("•")[1])
    return tipos_videos, year


def get_compra_o_alquiler_edad(driver):
    esperar_un_elemento(driver, 10, COMPRA_O_ALQUILER)
    # Cogemos todos los elementos cuya clase sea style-scope ytd-badge-supported-renderer
    compras = driver.find_elements(*COMPRA_O_ALQUILER)
    # Guardamos los tipos de los vídeos en un array
    compras_videos = []
    edad = []

    for compra in compras:
        # si lo que nos devuelve es un elemento vacio, pasamos al siguiente
        if compra.text == "":
            continue
        # Si no, lo separamos por el caracter \n
        # Y nos quedamos con el primer elemento
        # Que es el tipo de compra
        # Y nos quedamos con el segundo elemento
        # Que es la edad
        if len(compra.text.split("\n")) == 2:
            compras_videos.append(compra.text.split("\n")[0])
            edad.append(compra.text.split("\n")[1])
    return compras_videos, edad


def get_duracion(driver, titulos):
    # Cogemos la duración de cada vídeo
    esperar_un_elemento(driver, 10, TIEMPO)
    time_v = driver.find_elements(*TIEMPO)
    duracion = []
    for t in time_v:
        if len(titulos) != len(duracion):
            hacer_scroll(driver)
        if t.text == "":
            continue
        duracion.append(t.text)
    print(f"Se han encontrado {len(duracion)} duraciones")
    return duracion


def get_url(driver):
    # Cogemos la url de cada vídeo, es decir, cogemos la href del elemento PELICULA
    esperar_un_elemento(driver, 10, PELICULA)
    peli = driver.find_elements(*PELICULA)
    urls = []
    for url in peli:
        urls.append(url.get_attribute("href"))
    # Le quitamos el primer elemento a url, ya que es "None"
    urls.pop(0)
    # Le quitamos el último elemento a url, ya que es "None"
    urls.pop(-1)
    return urls


def write_csv(titulos, tipos_videos, compras_videos, year, duracion, edad, urls):
    # Guardamos los datos en un fichero csv
    # Creamos el fichero
    fichero = open("videos.csv", "w")
    # Escribimos la cabecera
    fichero.write("Titulo,Tipo,Compra_o_alquiler,Year,Tiempo,Edad,URL\n")
    # Escribimos los datos
    # hasta que no queden elementos por escribir
    print(
        str(len(titulos))
        + ","
        + str(len(tipos_videos))
        + ","
        + str(len(compras_videos))
        + ","
        + str(len(year))
        + ","
        + str(len(duracion))
        + ","
        + str(len(edad))
        + ","
        + str(len(urls))
    )

    for i in range(len(titulos)):
        fichero.write(
            f"{titulos[i]},{tipos_videos[i]},{compras_videos[i]},{year[i]},{duracion[i]},{edad[i]},{urls[i]}\n"
        )
    # Cerramos el fichero
    fichero.close()
    print("Fichero creado correctamente")


def esperar_un_elemento(driver, time, element):
    try:
        WebDriverWait(driver, time).until(EC.presence_of_element_located(element))
    except:
        print(NO_SUCH_ELEMENT + " " + str(element))
        raise


def cerrar_navegador(driver):
    driver.close()
    driver.quit()
    print("Navegador cerrado correctamente")
