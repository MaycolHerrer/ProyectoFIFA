import pandas as pd
#import pillow
import matplotlib.pyplot as plt
#import statistics

# Dado un DataFrame de Pandas con datos de muestra
data = {
    'Nombre': ['Maria', 'Jose', 'Juan', 'David', 'Eva'],
    'Edad': [24, 30, 22, 35, 28],
    'Altura': [165, 180, 175, 178, 160],
    'Peso': [55, 85, 70, 78, 50]
}
df = pd.DataFrame(data)

#Establecemos una figura y sus parametros de tamano en pulgadas y su resolucion
plt.figure(figsize=(8, 6), dpi=150)
plt.bar(df['Nombre'], df['Edad'], color='Green', label='Edad')

# Añadimos etiquetas y título y mostramos la legenda
plt.xlabel('Nombre')
plt.ylabel('Edad')
plt.title('Edad de las Personas')
plt.legend()
plt.show()
