import requests
from bs4 import BeautifulSoup
import re
import tkinter as tk
from tkinter import ttk
from datetime import datetime

def actualizar_datos():
    url = "https://www.jugandoonline.com.ar/rHome.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    mis_divs = soup.findAll('a', class_="enlaces-numeros")
    datos = []

    for div in mis_divs:
        numero_match = re.search(">(\d+)<\/a>", str(div))
        if numero_match:
            datos.append(numero_match.group(1))
        else:
            datos.append('Falta')

    datos_organizados = []
    for i in range(0, len(datos), 5):
        grupo = datos[i:i+5]
        datos_organizados.append(grupo)

    titulos = ['Ciudad', 'Provincia', 'Santa Fe', 'Cordoba', 'Entre Rios', 'Mendoza']
    titulos_columnas = ['Lugar', 'Previa', 'Primera', 'Matutina', 'Vespertina', 'Nocturna']

    datos_organizados_con_titulos = [titulos_columnas] + [[titulo] + grupo for titulo, grupo in zip(titulos, datos_organizados)]

    for widget in frame_datos.winfo_children():
        widget.destroy()

    for i, grupo in enumerate(datos_organizados_con_titulos):
        for j, dato in enumerate(grupo):
            label = ttk.Label(frame_datos, text=dato, font=("Arial", 12), anchor='center')
            if i == 0 or j == 0:
                label.config(font=("Arial", 12, "bold"))
            label.grid(row=i, column=j, padx=10, pady=5, sticky='nsew')

    ahora = datetime.now().strftime("%d/%m/%Y %H:%M")
    etiqueta_ultima_actualizacion.config(text=f"Actualizado: {ahora}")

    window.after(300000, actualizar_datos)

window = tk.Tk()
window.title("Quiniela")

style = ttk.Style()
style.theme_use("clam")

style.configure("Frame.TFrame", background="#FFFFFF")
style.configure("TLabel", background="#FFFFFF", foreground="#000000", font=("Arial", 12))

frame_datos = ttk.Frame(window, style="Frame.TFrame")
frame_datos.pack(padx=10, pady=10)

etiqueta_ultima_actualizacion = ttk.Label(window, text="", font=("Arial", 10))
etiqueta_ultima_actualizacion.pack(anchor="se", padx=5, pady=5)

actualizar_datos()

btn_actualizar = ttk.Button(window, text="Actualizar", style="TButton", command=actualizar_datos)
btn_actualizar.pack(pady=+5)

window.mainloop()
