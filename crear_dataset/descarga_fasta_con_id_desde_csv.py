#Para descargar las secuencias directo del excel

import pandas as pd
import requests
import os

def descargar_fasta_uniprot(uniprot_id, output_dir):
    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.fasta"
    response = requests.get(url)

    if response.status_code == 200:
        output_file = os.path.join(output_dir, f"{uniprot_id}.fasta")
        with open(output_file, 'w') as file:
            file.write(response.text)
        print(f"Archivo FASTA para {uniprot_id} guardado en {output_file}.")
    else:
        print(f"No se pudo descargar el archivo para {uniprot_id}. Status code: {response.status_code}")

# Leer el archivo Excel
def leer_ids_excel(archivo_excel, hoja, columna):
    df = pd.read_excel(archivo_excel, sheet_name=hoja)
    uniprot_ids = df[columna].tolist()
    return uniprot_ids

# Ejemplo de uso
archivo_excel = "/G y H.xlsx"  # Especifica la ruta a tu archivo Excel
hoja = "todas"  # Especifica el nombre de la hoja
columna = "Uniprot"  # Especifica el nombre de la columna que contiene los IDs de UniProt
output_dir = "/ruta/al/directorio/FASTA 2"  # Especifica el directorio donde guardar los archivos FASTA

os.makedirs(output_dir, exist_ok=True)

uniprot_ids = leer_ids_excel(archivo_excel, hoja, columna)

for uniprot_id in uniprot_ids:
    descargar_fasta_uniprot(uniprot_id, output_dir)

