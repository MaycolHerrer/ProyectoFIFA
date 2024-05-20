import pandas as pd
import statistics as stats
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

# Paso 1: Crear un DataFrame de Pandas con datos de muestra
data = {
    'Nombre': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
    'Edad': [24, 30, 22, 35, 28],
    'Altura': [165, 180, 175, 178, 160],
    'Peso': [55, 85, 70, 78, 50]
}
df = pd.DataFrame(data)

# Paso 2: Calcular estadísticas descriptivas utilizando statistics
media_edad = stats.mean(df['Edad'])
mediana_altura = stats.median(df['Altura'])
desviacion_estandar_peso = stats.stdev(df['Peso'])

# Paso 3: Crear una visualización usando Matplotlib
plt.figure(figsize=(10, 6))
plt.bar(df['Nombre'], df['Edad'], color='skyblue', label='Edad')
plt.xlabel('Nombre')
plt.ylabel('Edad')
plt.title('Edades de las personas')
plt.legend()
plt.savefig('edades.png')
plt.show()

# Paso 4: Combinar la imagen del gráfico con una imagen de fondo utilizando Pillow
# Cargar la imagen de fondo
fondo = Image.open('fondo.jpg')  # Asegúrate de tener una imagen llamada fondo.jpg en el mismo directorio

# Cargar el gráfico generado
grafico = Image.open('edades.png')

# Redimensionar el gráfico para que se ajuste al fondo
grafico = grafico.resize((fondo.width, fondo.height // 2))

# Crear una nueva imagen combinada
imagen_combinada = Image.new('RGB', (fondo.width, fondo.height))
imagen_combinada.paste(fondo, (0, 0))
imagen_combinada.paste(grafico, (0, fondo.height // 2))

# Añadir texto con las estadísticas descriptivas
draw = ImageDraw.Draw(imagen_combinada)
font = ImageFont.load_default()
texto = f"Estadísticas Descriptivas:\n\nMedia Edad: {media_edad}\nMediana Altura: {mediana_altura}\nDesviación Estándar Peso: {desviacion_estandar_peso}"
draw.text((10, 10), texto, fill="white", font=font)

# Guardar la imagen combinada
imagen_combinada.save('imagen_combinada.png')

# Mostrar la imagen combinada
imagen_combinada.show()
