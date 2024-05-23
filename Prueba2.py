from PIL import Image, ImageDraw, ImageFont, ImageFilter
import matplotlib.pyplot as plt
import statistics as stats
import pandas as pd

# Ruta del archivo Excel
rutaArchivo = 'datos.xlsx'

def moduloPandas(datos):
    # Defino la función pandas.
    dataFrame = pd.read_excel(datos)
    
    print("Filas del DataFrame:")
    print(dataFrame.head())  # Imprimo las primeras líneas de dataFrame.
    
    # Calcular el promedio de las edades
    promedioEdad = dataFrame['Edad'].mean()
    print("\nEl promedio de las edades es:", promedioEdad)
    
    # Agregar otra columna, de edades al cuadrado
    dataFrame["Edad al cuadrado"] = dataFrame["Edad"] ** 2
    print("\nLa nueva columna asignada es:")
    print(dataFrame)
    
    # Filtrar filas con edad mayor a 30
    mostrarF = dataFrame[dataFrame["Edad"] > 30]
    print("\nLas filas con edad > 30:")
    print(mostrarF)
    
    # Guardar el DataFrame en un archivo CSV
    dataFrame.to_csv('datos_filtrados.csv', index=False)
    print("\nDataFrame guardado EXITOSAMENTE en 'datos_filtrados.csv'")
    
    # Devolver las edades para otros usos
    return dataFrame

# Pillow: 5 funciones
def operaciones_pillow(nombre, ruta_imagen):
    # Crear una imagen en blanco de 200x200 pixeles con fondo blanco
    img = Image.new('RGB', (200, 200), color='white')
    
    # Dibujar un rectángulo azul con bordes negros dentro de la imagen
    dibujoRectangulo = ImageDraw.Draw(img)
    dibujoRectangulo.rectangle([50, 50, 150, 150], outline='black', fill='blue')
    
    # Añadir texto "Hola" con el nombre de la persona en la parte superior de la imagen
    fuente = ImageFont.load_default()
    dibujoRectangulo.text((60, 10), f"Hola {nombre}", fill='black', font=fuente)
    
    # Intentar abrir la imagen de la persona con la ruta seleccionada
    try:
        personaImg = Image.open(ruta_imagen)
        # Redimensionar la imagen de la persona a 100x100 pixeles para que pueda caber en el cuadro
        personaImg = personaImg.resize((100, 100))
        # Pegar la imagen de la persona dentro del cuadro
        img.paste(personaImg, (50, 50))
    except FileNotFoundError:
        # Si no se encuentra la imagen, mostrar un mensaje de error
        dibujoRectangulo.text((60, 80), "Imagen no encontrada", fill='red', font=fuente)
    
    # Aplicar filtro de borde en la imagen con todos los detalles ya puestos
    bordesImagen = img.filter(ImageFilter.FIND_EDGES)
    
    # Guardar la imagen en otro archivo llamado "imagenProcesada"
    bordesImagen.save('imagenProcesada.png')
    
    # Mostrar la imagen de la persona
    img.show()

# Función para graficar las edades por nombres usando Matplotlib
def matplotlib_plotting(dataFrame):
    # Crear un gráfico de barras de nombres con las edades
    plt.figure(figsize=(10, 6))
    plt.bar(dataFrame['Nombres'], dataFrame['Edad'], color='blue')
    # Añadir etiquetas y título
    plt.title('Gráfico de Edades por Nombre')
    plt.xlabel('Nombres')
    plt.ylabel('Edades')
    plt.xticks(rotation=45)  # Rotar las etiquetas del eje x para mejorar la legibilidad
    plt.tight_layout()  # Ajustar el diseño para evitar superposiciones
    # Mostrar el gráfico
    plt.show()

# Función para calcular estadísticas de las edades
def statistics(edades):
    # Calcular el promedio
    promedio = stats.mean(edades)
    
    # Calcular la mediana
    mediana = stats.median(edades)
    
    # Calcular la moda
    moda = stats.mode(edades)
    
    # Calcular la desviación estándar
    stdev = stats.stdev(edades)
    
    # Calcular la varianza
    variance = stats.variance(edades)
    
    # Salida formateada
    print(f"Promedio: {promedio}")
    print(f"Mediana: {mediana}")
    print(f"Moda: {moda}")
    print(f"Desviación estándar: {stdev}")
    print(f"Varianza: {variance}")

# Llamar a las funciones
dataFrame = moduloPandas(rutaArchivo)
edades = dataFrame['Edad'].tolist()
statistics(edades)

# Solicitar nombre de la persona para mostrar la imagen
nombre_persona = input("Ingrese el nombre de la persona: ")

# Obtener la ruta de la imagen correspondiente al nombre
ruta_imagen = nombre_persona + ".jpg"

# Mostrar la imagen correspondiente
operaciones_pillow(nombre_persona, ruta_imagen)

# Graficar las edades por nombres usando Matplotlib
matplotlib_plotting(dataFrame)