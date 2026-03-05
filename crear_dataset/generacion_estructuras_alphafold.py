#Generación de estructuras 3D de mi set de datos mediante AlphaFold

# Instalar ColabFold si no está instalado
!pip install -q condacolab
import condacolab
condacolab.install()

!conda install -y -c conda-forge -c bioconda colabfold

import os
import shutil
from google.colab import files

#Generación y descarga de estructuras con AF
# Crear carpetas necesarias
os.makedirs("input", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Subir el archivo multifasta
uploaded = files.upload()

# Obtener el nombre del archivo subido
fasta_file = list(uploaded.keys())[0]
shutil.move(fasta_file, f"input/{fasta_file}")

# Ejecutar ColabFold para generar estructuras
!colabfold_batch input/{fasta_file} output/

# Comprimir resultados en un archivo ZIP
shutil.make_archive("protein_structures_nr_80", 'zip', "output")

# Descargar el archivo ZIP
display(files.download("protein_structures_nr_80.zip"))
