#Para descarga de estructuras desde uniprot.

import os
import requests
import zipfile

def get_alphafold_model_url(uniprot_id):
    """
    Consulta la API de AlphaFold y obtiene la URL del modelo PDB si está disponible.

    Args:
        uniprot_id (str): ID de UniProt de la proteína.

    Returns:
        str: URL de descarga del modelo PDB o None si no está disponible.
    """
    base_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
    try:
        response = requests.get(base_url, timeout=30)
        response.raise_for_status()
        data = response.json()
        if data:
            model_url = data[0]['pdbUrl']
            return model_url
        else:
            print(f"❌ No se encontró modelo AlphaFold para {uniprot_id}")
            return None
    except requests.RequestException as e:
        print(f"Error consultando AlphaFold para {uniprot_id}: {e}")
        return None

def download_alphafold_model(pdb_dir, uniprot_id):
    """
    Descarga un modelo AlphaFold desde su URL si está disponible.

    Args:
        pdb_dir (str): Directorio donde se guardarán los archivos PDB.
        uniprot_id (str): ID de UniProt de la proteína.

    Returns:
        bool: True si la descarga fue exitosa, False en caso contrario.
    """
    model_url = get_alphafold_model_url(uniprot_id)
    if not model_url:
        return False

    output_file = os.path.join(pdb_dir, f"{uniprot_id}.pdb")
    if os.path.exists(output_file):
        print(f"Ya existe: {output_file}")
        return True

    try:
        response = requests.get(model_url, timeout=30)
        response.raise_for_status()
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"Descargado: {output_file}")
        return True
    except requests.RequestException as e:
        print(f"Fallo en {uniprot_id}: {e}")
        return False

def main(list_file):
    """
    Función principal que coordina la descarga de modelos AlphaFold.

    Args:
        list_file (str): Ruta al archivo que contiene los IDs de UniProt.
    """
    pdb_dir = "alphafold_models"
    os.makedirs(pdb_dir, exist_ok=True)

    with open(list_file, 'r') as f:
        uniprot_ids = [line.strip() for line in f if line.strip()]

    success, failed = [], []
    for uniprot in uniprot_ids:
        if download_alphafold_model(pdb_dir, uniprot):
            success.append(uniprot)
        else:
            failed.append(uniprot)

    zip_filename = "alphafold_models_bacillus.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in os.listdir(pdb_dir):
            zipf.write(os.path.join(pdb_dir, file), file)

    print(f"\n✅ Descargados: {len(success)}")
    print(f"❌ Fallidos: {len(failed)}")

    if failed:
        with open("failed_downloads_bacillus.txt", 'w') as f:
            f.writelines(f"{id}\n" for id in failed)
        print("Lista de fallos guardada en failed_downloads.txt")

    print(f"Modelos comprimidos en {zip_filename}")

# Para ejecución en Google Colab:
list_file = "/content/ID_bacillus.txt"
main(list_file)

# Para ejecución en local:
# if __name__ == "__main__":
#     import sys
#     if len(sys.argv) != 2:
#         print("Uso: python script.py <archivo_lista_uniprot>")
#         sys.exit(1)
#     main(sys.argv[1])

