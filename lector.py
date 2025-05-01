
import csv

# Ruta a tu archivo CSV
csv_file_path = 'goldstandard.csv'


preguntas = []
respuestas = []

with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)

    for row in reader:
        # Unimos todas las columnas en un solo string
        joined_row = ' '.join(row)
        
        if ';' in joined_row:
            pregunta, respuesta = joined_row.split(';', 1)
            preguntas.append(pregunta.strip())
            respuestas.append(respuesta.strip())
        else:
            # Si no hay punto y coma, consideramos que no hay respuesta
            preguntas.append(joined_row.strip())
            respuestas.append("")

# Imprimimos resultados
print("PREGUNTAS:")
for q in preguntas:
    print(q)

print("\nRESPUESTAS:")
for r in respuestas:
    print("-", r)
