import tools_selenium as t

PAGINA = "https://www.youtube.com/feed/storefront?bp=EgCSAQMI4gKiBQIoBQ%3D%3D"

if __name__ == "__main__":
    titulos = []
    tipos_videos = []
    compras_videos = []
    year = []
    duracion = []
    edad = []
    url = []

    # Abrimos el navegador
    driver = t.get_driver()
    print("Cargando página...")
    t.cargar_pagina(driver, PAGINA)
    print("Cogiendo títulos...")
    titulos = t.get_titulos(driver)
    print("Cogiendo tipos de vídeos y el año...")
    tipos_videos, year = t.get_tipo_pelicula(driver)
    print("Cogiendo si es de compra o alquiler y la edad...")
    compras_videos, edad = t.get_compra_o_alquiler_edad(driver)
    print("Cogiendo duración de la película...")
    duracion = t.get_duracion(driver, titulos)
    print("Cogiendo url de la película...")
    url = t.get_url(driver)
    print("Cerrando navegador...")
    t.cerrar_navegador(driver)
    print("Guardando datos en un csv...")

    t.write_csv(titulos, tipos_videos, compras_videos, year, duracion, edad, url)
