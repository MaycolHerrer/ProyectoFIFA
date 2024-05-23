from PIL import Image, ImageFilter, ImageOps, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import statistics as stats
import pandas as pd

# Ruta del archivo Excel
rutaArchivo = 'datos.xlsx'

def moduloPandas(datos): 
    dataFrame = pd.read_excel(datos) 
    print("filas del dataFrame:")
    print(dataFrame.head())  
    
    promedioEdad = dataFrame['Edad'].mean()
    print("\nEl promedio de las edades es:", promedioEdad)

    dataFrame["Edad al cuadrado"] = dataFrame["Edad"] ** 2 
    print("\nLa nueva columna asignada es:")
    print(dataFrame)
    
    mostrarF = dataFrame[dataFrame["Edad"] > 30] 
    print("\nLas filas con edad > 30:")
    print(mostrarF)
    
    dataFrame.to_csv('datos_filtrados.csv', index=False)
    print("\nDataFrame guardado EXITOSAMENTE en 'datos_filtrados.csv'")
    
    return dataFrame["Edad"].tolist()

# Pillow: 5 funciones
def operaciones_pillow(nombre, ruta_imagen):
    # Crear una imagen en blanco de 200x200 pixeles con fondo blanco
    img = Image.new('RGB', (200, 200), color='white')
    
    # Dibujar un rectángulo azul con bordes negros dentro de la imagen
    dibujoRectangulo = ImageDraw.Draw(img)
    dibujoRectangulo.rectangle([50, 50, 150, 150], outline='black', fill='blue')
    
    # Añadir texto Hola con el nombre de la persona en la parte superior de la imagen
    fuente = ImageFont.load_default()
    dibujoRectangulo.text((60, 10), f"Hola {nombre}", fill='black', font=fuente)
    
    # Intentar abrir la imagen de la persona con la ruta seleccionada
    if ruta_imagen:
        personaImg = Image.open(ruta_imagen)
        # Redimensionar la imagen de la persona  a 100x100 pixeles para que pueda caer en el cuadro
        personaImg = personaImg.resize((100, 100))
        # Pegar la imagen de la persona dentro del cuadro
        img.paste(personaImg, (50, 50))
    else:
        dibujoRectangulo.text((60, 80), "Imagen no encontrada", fill='red', font=fuente)
    
    # Aplicar filtro de borde en la imagen
    bordesImagen = img.filter(ImageFilter.FIND_EDGES)
    
    # Guardar la imagen en otro archivo llamado imagenProcesada
    bordesImagen.save('imagenProcesada.png')
    
    # Mostrar las imágen de la persona llamada
    img.show()

# Función para mostrar la imagen de una persona basándose en el nombre de quien la busca
def mostrar_imagen(nombre, ruta_imagen=None):
    # Llamar a la función de operaciones con Pillow e incluir la imagen de la persona
    operaciones_pillow(nombre, ruta_imagen)
    
# Matplotlib: 5 funciones
def matplotlib_plotting(dataFrame):
    # Crear un gráfico de dispersión de nombres con las edades
    plt.figure(figsize=(8, 6))
    plt.scatter(dataFrame['Nombres'], dataFrame['Edad'], color='blue', label='Edad')
    # Añadir etiquetas y título
    plt.title('Gráfico de Edades por Nombre')
    plt.xlabel('Nombres')
    plt.ylabel('Edades')
    # Rotar las etiquetas del eje x para mejorar la legibilidad
    plt.xticks(rotation=45, ha='right')
    # Mostrar el gráfico
    plt.show()

# Función de la librería statistics con 5 funciones
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
dataFrame = pd.read_excel(rutaArchivo) 
dataFrameEdad = moduloPandas(rutaArchivo)
statistics(dataFrameEdad)
matplotlib_plotting(dataFrameEdad)
mostrar_imagen("Nombre de la persona", "ruta/de/la/imagen.jpg")  # Cambia "Nombre de la persona" y la ruta de la imagen