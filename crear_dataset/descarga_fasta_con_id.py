import requests
import os

#Ejemplo para 3 ids 
def descargar_fasta_uniprot(uniprot_id):
    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.fasta"
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        print(f"No se pudo descargar el archivo para {uniprot_id}. Status code: {response.status_code}")
        return None

# Ejemplo de uso
uniprot_ids = ["Q97SQ7", "A0A1S9DH83", "G8N704"]
output_file = "/ruta/al/directorio/secuencias_concatenadas.fasta"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w') as file:
    for uniprot_id in uniprot_ids:
        fasta_data = descargar_fasta_uniprot(uniprot_id)
        if fasta_data:
            file.write(fasta_data)
            file.write("\n")  # Agrega una línea nueva entre secuencias si es necesario

open(output_file, "r").read()



#==============================================================================================================
#723 secuencias

def descargar_fasta_uniprot(uniprot_id):
    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.fasta"
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        print(f"No se pudo descargar el archivo para {uniprot_id}. Status code: {response.status_code}")
        return None

# Ejemplo de uso
uniprot_ids = ["P38939", "Q24642", "Q9UV07", "A0A5S8WFA7", "A6N9J4", "Q9KFR4", "O30565", "B9MPC3", "Q3BJY5", "A4UU35", "A4UU36", "Q2L6M1", "P14014", "C4MH58",
               "Q9K5L6", "Q9K5L5", "F1C3F8", "P70983", "P70983", "I3P686", "D9ZEF2", "D9ZEH9", "A0A096X8F5", "Q8UWE5", "Q8UWE3", "Q45643", "Q06307", "P38536",
               "P16950", "P36905", "I1WWV6", "C5IGQ7", "B3Y970", "Q9EZZ4", "A0A4Q0LMV5", "R4NSY4", "R4NSY4", "Q5JID9", "B8H6N5", "B6F2H1", "A0A9W5IPR0", "Q9ZEU2",
               "B1XIU7", "Q9RVT9", "A0A915Q9D7", "D7CVD0", "A0A6G5T628", "A0A0A0BUC7", "Q1J0W0", "A0A4P8XUU6", "A0A6G7H4A2", "Q1GY12", "O04196", "C5VVZ9", "C5VVZ9", "Q0R5Z4",
               "Q0R5Z4", "A0A4V0YGL6", "U5CJP3", "B0X223", "Q1AQI6", "Q08131", "O24397", "Q9RQI5", "O66936", "Q93HU3", "Q9XIS4", "Q9XIS5", "D0MJW1", "P30924",
               "W8SQR9", "Q9XGB3", "O04074", "Q84XW7", "Q59833", "P93691", "Q59832", "O24421", "Q08047", "P07762", "P32775", "P30537", "P30538", "Q59242",
               "P30539", "P07762", "Q10625", "Q9LTP8", "Q40663", "A7L832", "Q9M0S5", "O82982", "Q84AP9", "B1PHW8", "B1PHX0", "Q08341", "P29964", "Q5JJ59",
               "Q48398", "Q48398", "Q9X2F4", "I3ZTQ5", "Q5BLZ7", "Q5BLZ6", "Q3HW59", "Q9WX32", "A0A7U9P668", "Q9HHC8", "Q2YI50", "B6YV58", "Q99040", "Q99040",
               "T1SIF2", "B9A1J7", "G0GBS4", "P76041", "D7BAR0", "E4PMA5", "A0A059Q746", "Q6T308", "Q96VA4", "Q8GQC5", "C0JIC9", "Q9RTB7", "Q1IZQ3", "A0A5P2ALW6",
               "Q8NKQ3", "P35574", "Q6FSK0", "Q06625", "P35573", "Q55262", "Q72LF2", "Q6XE44", "B1WVF3", "B1WZK4", "S5UGW5", "B1WPM8", "Q8ZA75", "Q8ZA75",
               "A9BGH1", "P16954", "G7CL00", "P9WQ17", "Q60015", "A0A7D6JPT0", "A0A7D6JVY3", "Q5FI02", "A0P8W9", "Q8YAE6", "O06994", "Q6UEE8", "C0JP82", "C0JP83",
               "P22630", "A0A3P8MUS3", "D5KR60", "Q6PMJ3", "Q45516", "O82953", "A0A411J1E3", "Q66T78", "O06915", "A0A023U8M0", "Q06812", "P08137", "A0A385FPX0", "P20845",
               "Q84CG0", "Q53786", "Q53633", "P08486", "O65947", "P27350", "Q847N0", "Q60102", "O50200", "Q9U406", "Q6YF33", "Q99KE6", "Q8C5B4", "P91778",
               "A9ZPM0", "P08117", "Q7X9T1", "P17859", "Q9N2P9", "Q41770", "D9ZE49", "D9ZE62", "D9ZEB5", "D9ZED5", "D4N3A2", "G4Y5W9", "P21567", "Q9KWY6",
               "A0A2U8ZSD8", "P09794", "P22998", "O86876", "P97179", "P96992", "Q59222", "Q9R9H7", "P30270", "Q59964", "Q7CLU8", "O93648", "Q66SB4", "Q8QGW2",
               "P30292", "Q8IA45", "Q98942", "Q8I7A5", "Q9U0F6", "Q9U0F9", "Q05884", "M9TI89", "Q65MX0", "A9YDD9", "J9PXA2", "E5RKQ5", "E2G4G0", "B1VK33",
               "Q9NKZ3", "Q9NKZ2", "Q8N0P8", "Q8N0P9", "Q8MM52", "Q8MM99", "Q8N0Q6", "Q8N0Q5", "Q8MM52", "Q8N0Q4", "Q8MLY6", "Q8MM99", "Q8MM99", "Q8MM52",
               "Q8MM52", "Q8MM52", "Q8N0R0", "Q8N0Q9", "Q8N0Q8", "Q8MM52", "Q9NKZ5", "Q8MM99", "Q8N0Q7", "Q8MLY6", "Q8MLY6", "Q9NKY9", "Q9N6Q7", "A5Y589",
               "P00689", "Q99N59", "A7LGW4", "O04964", "P19269", "Q6WUB6", "P0C1B3", "Q96TH4", "I7I8P3", "Q9NKZ2", "Q8N0P7", "Q8N0P5", "Q8N0P6", "Q8MM40",
               "Q8N0Q0", "Q8MM80", "Q8MM80", "Q8MM40", "Q8N0Q2", "Q8N0Q1", "Q8MM40", "Q8MM80", "Q8N0Q3", "Q8MLX9", "Q8MM40", "Q9NKZ4", "Q8MM40", "Q8MM80",
               "Q8MM80", "Q9NKZ4", "Q9NKZ4", "Q9NKZ4", "Q8MM40", "Q8MM40", "Q8MM40", "Q8MLX9", "Q8MM40", "Q9NKY8", "Q9N6Q7", "P0C1B3", "A0A6C0V1X1", "J9QPI9",
               "Q9I9H6", "Q9NKZ1", "Q9N651", "Q9NKY7", "Q9NKY5", "P0C1B4", "Q9NKZ0", "Q9N651", "Q9NKY6", "C0LW29", "C0LW29", "A0A023I4U3", "H9B4I9", "P41131",
               "Q5I942", "P30269", "Q9XCV8", "Q79AD6", "Q6XR91", "Q76CT3", "G9DA07", "Q0Z8K1", "V5ISH0", "D6R179", "Q8U3I9", "P23671", "A0A0G2T4B5", "Q8DT08",
               "Q9S5Y2", "A0A142I5C4", "F2VRZ2", "Q5I943", "Q6GWE2", "Q5JB42", "Q3LB10", "Q9UV09", "R4P3U1", "Q92394", "Q9BPT3", "B8Y1H0", "A8VWC5", "A0A0A0WA73",
               "E2JEW8", "P00691", "Q6GWE2", "Q5JB42", "Q3LB10", "Q9UV09", "Q9X1Y3", "Q92394", "Q9BPT3", "B8Y1H0", "A8VWC5", "A0A0A0WA73", "E2JEW8", "P00691",
               "Q4Z8Q4", "M4I6P6", "Q9L4I9", "Q4A3E0", "Q06SN3", "Q76L99", "Q76L96", "Q208A7", "Q208A7", "S6BGD1", "Q8I9K6", "Q8I9K5", "Q6TXT5", "A1YR25",
               "A8QL62", "A5CVD5", "V9P2Q6", "Q60051", "D5BG23", "D5BG32", "Q5JER7", "O13296", "Q9SW26", "O24781", "G8IJA7", "B0LVG1", "Q8NKR4", "Q8JZK3",
               "Q8NKR5", "Q2KJQ1", "A0A2U8ZUR1", "A7U965", "Q6FJV0", "Q5KTR5", "A0A5S8WFA8", "Q9Y197", "Q9ZAP8", "J9PQD2", "L7Y1I6", "A9UJ60", "L8AW48", "L8AXN1",
               "A0A218MJE6", "O68875", "Q01117", "Q8J1E4", "L8B068", "P25718", "Q8LJQ6", "A0A2P1ANM2", "P83053", "P56271", "H2N0D4", "A0A075M165", "S7Z6T2", "Q5MB94",
               "Q23932", "Q0J184", "D4L684", "M9TI89", "Q9RQT8", "Q82AS5", "D4P4Y7", "Q08806", "P29750", "A0A097QS36", "C0LZX2", "B4X9V8", "Q2QC88", "B5BQC3",
               "Q9NJP1", "O18408", "A7M087", "Q93C66", "Q67C51", "Q52414", "B6RB08", "Q52413", "P26612", "P14898", "Q0D9J1", "Q9AGG5", "P14899", "Q0J182",
               "Q0J528", "Q9AGG4", "Q02905", "P0C1B3", "Q02906", "Q8WSG9", "U3NE54", "A0A173N065", "O50582", "A8QWV3", "Q26855", "O50583", "I3QII4", "A0A873P8R1",
               "Q53641", "P27940", "S5ZJ19", "A0A0C4WYD9", "Q53I75", "A0A1B3IKE0", "Q45517", "Q9L872", "P38158", "Q93CA0", "A0A1S6JYL1", "A0A3E2CLU2", "Q2L6M0", "B1YHL8",
               "Q08295", "P40439", "P40439", "P40884", "Q9P8G8", "P53341", "Q02751", "P07265", "Q9AI60", "A0A8X6EH34", "A0A0E3N392", "A9YDV2", "P94451", "Q60027",
               "Q96WT4", "Q95WY5", "A0A0N9LWV3", "A0A0P0GJC2", "Q21NA9", "Q25BT8", "A1IHL0", "J9SJ08", "Q25BT7", "D2XNP9", "A4GVI6", "Q25BT6", "A0A2Z5WH92", "P21517",
               "A0A369WGC9", "B9MLT9", "Q76LB0", "Q5U9V9", "Q59239", "Q5U9W0", "Q9F5W3", "P27036", "P30921", "P09121", "G0ZI10", "G0ZI11", "Q6S3E3", "F1DPT1",
               "Q0JW31", "A0A097CPM3", "Q5ZEQ7", "Q9RM63", "O80403", "Q8W547", "C0JID0", "P15067", "Q8NNT0", "Q31S51", "O32611", "P26501", "P10342", "A0A075BIV0",
               "Q84L53", "Q41742", "Q47NP5", "O05152", "L0C9D3", "Q7X8Q2", "G9HXG8", "A0A0B6VSY7", "Q6XNK5", "Q6XNK6", "Q6XKX6", "Q9AI64", "Q8KR84", "Q5FKB1",
               "Q9S7S8", "Q93XN7 ", "P21517", "Q9R9H8", "Q68KL3", "C0LZ63", "A7DWA8", "Q52PU5", "I1VWI0", "Q04977", "Q45490", "A0A2L1CF09", "D6E1Y4", "Q5FI03",
               "A0A1V0JEK9", "A0A831DZN3", "Q046J8", "Q046J8", "F9URM8", "X5CPN2", "A1S075", "O06988", "I6RE37", "Q45574", "Q5GIA5", "Q9RHR1", "A0A076EBZ6", "Q8NNR9",
               "Q9UWN9", "Q9AJN7", "Q9UWN8", "Q9LC79", "B6ZIV0", "A8QX07", "O52519", "Q6SZP7", "Q53688", "Q7LX98", "Q9RX51", "Q9AJN6", "A8QX08", "Q44316",
               "Q4JQI8", "E1ANS4", "B6ZIU9", "P95867", "O52520", "Q6SZP6", "Q8NNR1", "Q03658", "Q52516", "Q0KKZ7", "A0A386IRT1", "P22963", "B5MEM6", "Q1JUA3",
               "Q60224", "A0A143HRA0", "A2QB23", "Q1KLC8", "Q1J4B1", "D6DYI9", "P21543", "Q57482", "Q9AIV2", "B1PHW9", "Q8A1G0", "Q9AF93", "Q9F237", "P29093",
               "Q9F4G4", "Q76CZ0", "Q5FMB7", "P21332", "Q45101", "P29094", "Q5SL12", "P53051", "Q9AI62", "B0FZ47", "T1W7I3", "C1K2X6", "W8SKF6", "Q98PS5",
               "A0A0D4CME6", "Q6XQ00", "R4I4I6", "G9JLV4", "Q9F236", "Q5KW24", "Q5FIF2", "Q7X834", "O69008", "Q7DI19", "I3WU34", "P07811", "C0LLG9", "O33840",
               "Q6QHE9", "Q8A762", "A0A0B5JT51", "Q41386", "D4L6Z8", "D4L7L5", "Q9F930", "Q72ID4", "D0YTI0", "O81638", "Q8GTR4", "Q9XDB5", "U3MXZ5", "Q8GJ67",
               "K9L0H1", "Q59319", "A0A075FE92", "Q8DZ94", "O34587", "Q9P9A0", "A0A0C5GWS2", "A0A482PRE5", "Q8KLP1", "Q9AVL7", "O04074", "Q9FUU7", "A9ZPD1", "Q9ZTB7",
               "Q9ZTB6", "Q0H3F1", "G4T4R6", "A0A6C7EEG6", "D9TT09", "A0A077JI83", "A0A386IRS6", "A0A077JF78", "A0A0H3C6Q6", "Q6UVM5", "Q8P5I2", "A0A077JM77", "Q8PGX2", "P13080",
               "Q7PYT9", "B0XAA1", "B5ABD8", "Q4L2Q1", "S5YEW8", "D0VX20", "Q2PS28", "Q9XBR0", "B2BS85", "P10249", "Q03Z66", "P10249", "Q7WWP8", "Q14EH6",
               "Q59495", "M9ZS93", "A5A8M5", "Q8G6U7", "Q84BY1", "Q84HQ2", "B8Y3Y0", "F2R410", "F2R411", "Q9RST7", "Q6L2Z7", "A8QX00", "B6E9W1", "B1PK99",
               "B8YM30", "P72235", "A4FTT7", "Q9LAS5", "O06458", "Q9RA59", "D1CE96", "C1D169", "C1D169", "A0R6E0", "P9WQ19", "C1AZS6", "Q47SE5", "A8WAD0",
               "Q5SL15", "Q65MI2", "Q9F8X2", "P39795", "P28904", "C4X1I2", "J7H256", "J7H7V3", "J7H570"]
output_file = "/ruta/al/directorio/secuencias_concatenadas.fasta"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w') as file:
    for uniprot_id in uniprot_ids:
        fasta_data = descargar_fasta_uniprot(uniprot_id)
        if fasta_data:
            file.write(fasta_data)
            file.write("\n")  # Agrega una línea nueva entre secuencias si es necesario

open(output_file, "r").read()



#===============================================================================================================
#secuencias faltantes
import requests
import os

def descargar_fasta_uniprot(uniprot_id):
    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.fasta"
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        print(f"No se pudo descargar el archivo para {uniprot_id}. Status code: {response.status_code}")
        return None

uniprot_ids = ["Q93XN7"]
output_file = "/ruta/al/directorio/secuencias_concatenadas.fasta"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w') as file:
    for uniprot_id in uniprot_ids:
        fasta_data = descargar_fasta_uniprot(uniprot_id)
        if fasta_data:
            file.write(fasta_data)
            file.write("\n")  # Agrega una línea nueva entre secuencias si es necesario

open(output_file, "r").read()
