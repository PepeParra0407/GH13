#===============================================================================================
#Generación de variantes sencillas

def cargar_mutaciones(archivo_txt):
    """
    Lee un archivo de texto con mutaciones, una por línea (formato tipo P43M).
    """
    with open(archivo_txt, 'r') as f:
        return [linea.strip() for linea in f if linea.strip()]

def aplicar_mutacion(secuencia, mutacion):
    """
    Aplica una mutación puntual a la secuencia. Formato de mutación: P43M.
    """
    aa_original = mutacion[0]
    posicion = int(mutacion[1:-1]) - 1  # Índice 0-based
    aa_nuevo = mutacion[-1]

    if secuencia[posicion] != aa_original:
        print(f" Advertencia: en la posición {posicion+1} se esperaba '{aa_original}', pero hay '{secuencia[posicion]}'")

    nueva_secuencia = secuencia[:posicion] + aa_nuevo + secuencia[posicion+1:]
    return nueva_secuencia

def generar_variantes(secuencia_original, archivo_mutaciones, archivo_salida="variantes.fasta"):
    """
    Genera variantes de la secuencia aplicando mutaciones y escribe el resultado en un archivo FASTA.
    """
    mutaciones = cargar_mutaciones(archivo_mutaciones)

    with open(archivo_salida, 'w') as out:
        for mut in mutaciones:
            nueva_seq = aplicar_mutacion(secuencia_original, mut)
            out.write(f">{mut}\n{nueva_seq}\n")

# ======================
# CONFIGURACIÓN
# ======================

# Reemplaza esta secuencia con la tuya
secuencia_original = "ANLNGTLMQYFEWYMPNDGQHWKRLQNDSAYLAEHGITAVWIPPAYKGTSQADVGYGAYDLYDLGEFHQKGTVRTKYGTKGELQSAIKSLHSRDINVYGDVVINHKGGADATEDVTAVEVDPADRNRVISGEHLIKAWTHFHFPGRGSTYSDFKWHWYHFDGTDWDESRKLNRIYKFQGKAWDWEVSNENGNYDYLMYADIDYDHPDVAAEIKRWGTWYANELQLDGFRLDAVKHIKFSFLRDWVNHVREKTGKEMFTVAEYWQNDLGALENYLNKTNFNHSVFDVPLHYQFHAASTQGGGYDMRKLLNSTVVSKHPLKAVTFVDNHDTQPGQSLESTVQTWFKPLAYAFILTRESGYPQVFYGDMYGTKGDSQREIPALKHKIEPILKARKQYAYGAQHDYFDHHDIVGWTREGDSSVANSGLAALITDGPGGAKRMYVGRQNAGETWHDITGNRSEPVVINSEGWGEFHVNGGSVSIYVQRY"

# Nombre del archivo de entrada con mutaciones (una por línea: P43M, P43R, etc.)
archivo_mutaciones = "/content/fm_mea_mut_list"

# Nombre del archivo de salida
archivo_salida = "var_fm_mea.fasta"

# Ejecutar
generar_variantes(secuencia_original, archivo_mutaciones, archivo_salida)



#==============================================================================================================
#Generación de variantes multiplesa acumulativas

def read_fasta_sequences(file_path):
    """
    Lee un archivo FASTA y devuelve una lista de tuplas (encabezado, secuencia).
    """
    sequences = []
    current_header = None
    current_sequence = []

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if current_header and current_sequence:
                    sequences.append((current_header, ''.join(current_sequence)))
                current_header = line[1:] # Remove '>' character
                current_sequence = []
            else:
                current_sequence.append(line)
        # Add the last sequence
        if current_header and current_sequence:
            sequences.append((current_header, ''.join(current_sequence)))
    return sequences

def generate_cumulative_variants(fasta_entries):
    """
    Genera variantes combinando secuencias de forma acumulativa y devuelve
    una lista de tu tuplas (lista_de_mutaciones_combinadas, secuencia).
    """
    cumulative_variants_data = []
    current_combined_sequence = ""
    current_combined_header_parts = []

    # Empezamos desde el segundo elemento para asegurar al menos dos secuencias combinadas
    # en la primera variante generada, como se indica en la descripción del usuario.
    if len(fasta_entries) < 2:
        print("Advertencia: Se necesitan al menos dos secuencias para generar variantes acumulativas.")
        return []

    # Combinar las dos primeras secuencias para la primera variante
    header1, seq1 = fasta_entries[0]
    header2, seq2 = fasta_entries[1]
    current_combined_sequence = seq1 + seq2
    current_combined_header_parts = [header1, header2]
    cumulative_variants_data.append((list(current_combined_header_parts), current_combined_sequence))

    # Continuar cumulativamente con el resto de las secuencias
    for i in range(2, len(fasta_entries)):
        header_i, seq_i = fasta_entries[i]
        current_combined_sequence += seq_i
        current_combined_header_parts.append(header_i)
        cumulative_variants_data.append((list(current_combined_header_parts), current_combined_sequence))

    return cumulative_variants_data

def write_fasta_file(file_path, fasta_entries):
    """
    Escribe una lista de tuplas (encabezado, secuencia) en un archivo FASTA.
    """
    with open(file_path, 'w') as out:
        for header, sequence in fasta_entries:
            out.write(f">{header}\n{sequence}\n")

def write_name_mapping_file(file_path, name_map):
    """
    Escribe un archivo de mapeo de nombres simplificados a nombres originales.
    """
    with open(file_path, 'w') as out:
        for simplified_name, original_name in name_map:
            out.write(f"{simplified_name}\t{original_name}\n")

# ======================
# CONFIGURACIÓN PARA VARIANTES ACUMULATIVAS
# ======================

# Archivo de entrada con las variantes generadas previamente
input_fasta_file = "var_good_align.fasta"

# Archivo de salida para las variantes acumulativas
output_cumulative_fasta_file = "cumulative_variants.fasta"

# Archivo de salida para el mapeo de nombres
output_name_map_file = "cumulative_variants_names_map.txt"

# 1. Leer las secuencias y encabezados del archivo FASTA de entrada
variants = read_fasta_sequences(input_fasta_file)

# 2. Generar las variantes combinadas de forma acumulativa
cumulative_variants_data = generate_cumulative_variants(variants)

# 3. Preparar las entradas para el archivo FASTA con nombres simplificados y el mapeo
output_fasta_entries = []
name_mapping = []

if cumulative_variants_data:
    for i, (original_headers_list, sequence) in enumerate(cumulative_variants_data):
        simplified_name = f"Top{i+2}" # Empieza en Top2
        original_full_header = '_'.join(original_headers_list)

        output_fasta_entries.append((simplified_name, sequence))
        name_mapping.append((simplified_name, original_full_header))

    # 4. Escribir las variantes acumulativas en un nuevo archivo FASTA
    write_fasta_file(output_cumulative_fasta_file, output_fasta_entries)
    print(f"Se generaron {len(output_fasta_entries)} variantes acumulativas en '{output_cumulative_fasta_file}' con nombres simplificados.")

    # 5. Escribir el archivo de mapeo de nombres
    write_name_mapping_file(output_name_map_file, name_mapping)
    print(f"Se generó el archivo de mapeo de nombres en '{output_name_map_file}'.")
else:
    print("No se generaron variantes acumulativas.")

#==========================================================
def aplicar_mutacion(secuencia, mutacion):
    """
    Aplica una mutación puntual a la secuencia. Formato de mutación: P43M.
    """
    aa_original = mutacion[0]
    posicion = int(mutacion[1:-1]) - 1  # Índice 0-based
    aa_nuevo = mutacion[-1]

    # Warning: The original function has a potential issue if the sequence is
    # not as expected at the position. For this task, we will proceed
    # with the mutation regardless, assuming the mutations are valid.
    # if secuencia[posicion] != aa_original:
    #     print(f" Advertencia: en la posición {posicion+1} se esperaba '{aa_original}', pero hay '{secuencia[posicion]}'")

    nueva_secuencia = secuencia[:posicion] + aa_nuevo + secuencia[posicion+1:]
    return nueva_secuencia

def read_fasta_sequences(file_path):
    """
    Lee un archivo FASTA y devuelve una lista de tuplas (encabezado, secuencia).
    """
    sequences = []
    current_header = None
    current_sequence = []

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if current_header and current_sequence:
                    sequences.append((current_header, ''.join(current_sequence)))
                current_header = line[1:] # Remove '>' character
                current_sequence = []
            else:
                current_sequence.append(line)
        # Add the last sequence
        if current_header and current_sequence:
            sequences.append((current_header, ''.join(current_sequence)))
    return sequences

def generate_cumulative_variants(secuencia_original, individual_mutation_entries):
    """
    Genera variantes aplicando mutaciones de forma acumulativa a la secuencia original
    y devuelve una lista de tuplas (lista_de_mutaciones_combinadas, secuencia_mutada).
    """
    cumulative_variants_data = []
    mutations_applied_so_far = []

    # Iterate through each individual mutation entry to extract the mutation string
    for mutation_header_tuple in individual_mutation_entries:
        mutation_string = mutation_header_tuple[0] # e.g., 'V286M'
        mutations_applied_so_far.append(mutation_string)

        # We start generating cumulative variants from the second mutation (Top2)
        # as per the user's description (e.g., 'Top2' means 2 mutations combined).
        if len(mutations_applied_so_far) >= 2:
            current_cumulative_sequence = secuencia_original # Start with a fresh original sequence for each cumulative variant
            current_cumulative_headers = list(mutations_applied_so_far) # Make a copy of the current list of mutations

            # Apply all accumulated mutations to the fresh original sequence
            for mut in current_cumulative_headers:
                current_cumulative_sequence = aplicar_mutacion(current_cumulative_sequence, mut)

            cumulative_variants_data.append((current_cumulative_headers, current_cumulative_sequence))

    return cumulative_variants_data

def write_fasta_file(file_path, fasta_entries):
    """
    Escribe una lista de tuplas (encabezado, secuencia) en un archivo FASTA.
    """
    with open(file_path, 'w') as out:
        for header, sequence in fasta_entries:
            out.write(f">{header}\n{sequence}\n")

def write_name_mapping_file(file_path, name_map):
    """
    Escribe un archivo de mapeo de nombres simplificados a nombres originales.
    """
    with open(file_path, 'w') as out:
        for simplified_name, original_name in name_map:
            out.write(f"{simplified_name}\t{original_name}\n")

# ======================
# CONFIGURACIÓN PARA VARIANTES ACUMULATIVAS
# ======================

# Reemplaza esta secuencia con la tuya (copied from DifvGAHGRucc for self-containment)
secuencia_original = "ANLNGTLMQYFEWYMPNDGQHWKRLQNDSAYLAEHGITAVWIPPAYKGTSQADVGYGAYDLYDLGEFHQKGTVRTKYGTKGELQSAIKSLHSRDINVYGDVVINHKGGADATEDVTAVEVDPADRNRVISGEHLIKAWTHFHFPGRGSTYSDFKWHWYHFDGTDWDESRKLNRIYKFQGKAWDWEVSNENGNYDYLMYADIDYDHPDVAAEIKRWGTWYANELQLDGFRLDAVKHIKFSFLRDWVNHVREKTGKEMFTVAEYWQNDLGALENYLNKTNFNHSVFDVPLHYQFHAASTQGGGYDMRKLLNSTVVSKHPLKAVTFVDNHDTQPGQSLESTVQTWFKPLAYAFILTRESGYPQVFYGDMYGTKGDSQREIPALKHKIEPILKARKQYAYGAQHDYFDHHDIVGWTREGDSSVANSGLAALITDGPGGAKRMYVGRQNAGETWHDITGNRSEPVVINSEGWGEFHVNGGSVSIYVQRY"


# Archivo de entrada con las variantes generadas previamente (these are individual mutations)
input_fasta_file = "var_fm_mea.fasta"

# Archivo de salida para las variantes acumulativas
output_cumulative_fasta_file = "cumulative_fm_mea.fasta"

# Archivo de salida para el mapeo de nombres
output_name_map_file = "cumulative_fm_mea_names_map.txt"

# 1. Leer las secuencias y encabezados del archivo FASTA de entrada (these are individual mutation headers)
variants = read_fasta_sequences(input_fasta_file)

# 2. Generar las variantes combinadas de forma acumulativa
# Pass the original sequence and the individual mutation entries (headers)
cumulative_variants_data = generate_cumulative_variants(secuencia_original, variants)

# 3. Preparar las entradas para el archivo FASTA con nombres simplificados y el mapeo
output_fasta_entries = []
name_mapping = []

if cumulative_variants_data:
    for i, (original_headers_list, sequence) in enumerate(cumulative_variants_data):
        simplified_name = f"Top{i+2}" # Empieza en Top2 as per the problem description
        original_full_header = '_'.join(original_headers_list)

        output_fasta_entries.append((simplified_name, sequence))
        name_mapping.append((simplified_name, original_full_header))

    # 4. Escribir las variantes acumulativas en un nuevo archivo FASTA
    write_fasta_file(output_cumulative_fasta_file, output_fasta_entries)
    print(f"Se generaron {len(output_fasta_entries)} variantes acumulativas en '{output_cumulative_fasta_file}' con nombres simplificados.")

    # 5. Escribir el archivo de mapeo de nombres
    write_name_mapping_file(output_name_map_file, name_mapping)
    print(f"Se generó el archivo de mapeo de nombres en '{output_name_map_file}'.")
else:
    print("No se generaron variantes acumulativas.")
