import os
import requests
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

def remplazarVocales(s):
    reemplazos = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("?", "ć"),
        ("€", ""),
        (",", ""),
        ("-", "")
    )
    for a, b in reemplazos:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

# Cargar datos del archivo CSV
datosJugadores = pd.read_csv('fifa.csv', encoding='windows-1252')

# Convertir todas las columnas a str y aplicar remplazarVocales a todos los valores
datosJugadores = datosJugadores.astype(str).applymap(remplazarVocales)

# Quitar espacios en blanco de los nombres de las columnas y convertir a minúsculas
datosJugadores = datosJugadores.rename(columns=remplazarVocales)
datosJugadores.columns = [col.strip().lower() for col in datosJugadores.columns]
datosJugadores = datosJugadores.applymap(str.lower)

print(datosJugadores.info())

def jugadoressueldomayor(monto):
# Usar expresiones regulares para limpiar conjunto de caracteres
#datosJugadores['sueldo'] = datosJugadores['sueldo'].str.replace(r'\D', '', regex=True).replace('', 0).astype(int)
    datosJugadores['sueldo'] = datosJugadores['sueldo'].str.strip()
    datosJugadores['sueldo'] = datosJugadores['sueldo'].replace(',', '').replace('', '0').astype(int)
    jugadores = datosJugadores[datosJugadores['sueldo'] > monto]
    print(jugadores[['nombre jugador', 'sueldo']])

def edadpromedioequipo(equipo):
    datosJugadores['edad'] = datosJugadores['edad'].astype(int)
    jugadores = datosJugadores[datosJugadores['club'].str.contains(equipo, case=False)]
    if not jugadores.empty:
        edadpromedio = jugadores['edad'].mean()
        print(f'La edad promedio de los jugadores del equipo que contiene "{equipo}" es de {edadpromedio} años.')
    else:
        print(f'No se encontraron jugadores para el equipo que contiene "{equipo}".')

def jugadoresletranacionalidad(letra, nacionalidad):
    if len(letra) == 1:
        jugadores = datosJugadores[(datosJugadores['nombre jugador'].str.startswith(letra)) & (datosJugadores['nacionalidad'] == nacionalidad)]
        print(jugadores[['nombre jugador', 'nacionalidad']])
    else:
        print("La letra debe ser solo un carácter")

def jugadoresaprestamo():
    jugadores = datosJugadores[datosJugadores['prestado por'].notna()]
    print(jugadores[['nombre jugador', 'prestado por']])

def jugadoresmenorestaturaequipo(equipo):
    jugadores = datosJugadores[datosJugadores['club'] == equipo]
    if not jugadores.empty:
        menorEstatura = jugadores.loc[jugadores['altura (cm)'].idxmin()]
        print(menorEstatura[['nombre jugador', 'altura (cm)']])
    else:
        print(f"No se encontraron jugadores para el equipo {equipo}")
    
def fotojugadores(nombre):
    jugador = datosJugadores[datosJugadores['nombre jugador'] == nombre]
    if not jugador.empty:
        fotourl = jugador.iloc[0]['foto jugador']
        response = requests.get(fotourl)
        if response.status_code == 200:  # Verificar si la solicitud fue exitosa
            tempfile = "tempimage.jpg"  # Guardar la imagen en un archivo temporal
            with open(tempfile, "wb") as f:
                f.write(response.content)
            imagen = Image.open(tempfile)  # Abrir la imagen con PIL
            imagen.show()
            os.remove(tempfile)  # Eliminar el archivo temporal
        else:
            print("La solicitud no fue exitosa. Código de estado:", response.status_code)
    else:
        print("Jugador no encontrado")
        
def graficojugadorespornacionalidad(nacionalidad):
    # Obtener conteo de jugadores por nacionalidad
    conteo = datosJugadores['nacionalidad'].value_counts()

    # Verificar si la nacionalidad especificada está en los datos
    if nacionalidad in conteo.index:
        # Obtener conteo de jugadores de la nacionalidad especificada
        conteo_especifico = conteo[nacionalidad]
    else:
        print(f'No hay jugadores de {nacionalidad}')
        return

    # Obtener las o más comunes (excluyendo la nacionalidad especificada)
    top5 = conteo.drop(nacionalidad).head(5)

    # Concatenar la nacionalidad especificada con las o más comunes
    too = pd.concat([top5, pd.Series({nacionalidad: conteo_especifico})])

    # Mostrar el gráfico con las 5
    plt.bar(too.index, too, color=['blue'] * 5 + ['red'])  
    plt.xlabel('Nacionalidad')
    plt.ylabel('Número de jugadores')
    plt.title(f'Número de jugadores por nacionalidad (Top 5 + {nacionalidad})')
    plt.xticks(rotation=45)  
    plt.show()

def jugadoresyclubesporfechacontrato(fecha, año):
    jugadores = datosJugadores[(datosJugadores['fecha contratacion'] == fecha) & (datosJugadores['contrato valido hasta'] == año)]
    print(jugadores[['nombre jugador', 'club', 'fecha contratacion', 'contrato Valido Hasta']])

 ### Opción 9 ###   
def modificaratributosjugador(datosJugadores, nNombre, nvalor=None, nsueldo=None, nposicion=None, ncarareal=None):
    # Usamos el método loc para encontrar el índice de la fila donde está el jugador
    JugadorFiltrado = datosJugadores[datosJugadores['nombre jugador'] == nNombre].index
    # Iniciamos un contador para imprimir el mensaje final solo si hay al menos 1 cambio
    contador = 0
    
    # Cambiar los atributos si tienen un valor diferente de None
    if nvalor is not None:
        datosJugadores.loc[JugadorFiltrado, 'valor'] = nvalor
        contador += 1
    if nsueldo is not None:
        datosJugadores.loc[JugadorFiltrado, 'sueldo'] = nsueldo
        contador += 1
    if nposicion is not None:
        datosJugadores.loc[JugadorFiltrado, 'posicion'] = nposicion
        contador += 1
    if ncarareal is not None:
        datosJugadores.loc[JugadorFiltrado, 'cara real'] = ncarareal
        contador += 1
    
    # Guardar los cambios en el archivo CSV
    datosJugadores.to_csv('fifa.csv', index=False)
    
    if contador > 0:
        print("Atributos modificados exitosamente")
    else:
        print("No hubo cambios")

def promediopotencialporequipo():
    equipos = datosJugadores['club'].unique()
    for equipo in equipos:
        jugadores = datosJugadores[datosJugadores['club'] == equipo]
        if not jugadores.empty:
            maxpotencial = jugadores['Potential'].max()
            minpotencial = jugadores['Potential'].min()
            promediopotencial = (maxpotencial + minpotencial) / 2
            print(f"Promedio de potencial en {equipo}: {promediopotencial}")

def top5jugadoresporletra(letra):
    jugadores = datosJugadores[datosJugadores['nombre jugador'].str.contains(letra)]
    top5jugadores = jugadores.nlargest(5, 'sueldo')
    print(top5jugadores[['nombre jugador', 'sueldo']])
    
### OPCIÓN 13 ###
def numerojugadorespieizquierdo():
    # Filtro de pie izquierdo
    PieIzquierdo = datosJugadores[datosJugadores['pie preferido'] == 'left']
    # Cuento con shape (cuenta la cantida de filas que hay en la columna)
    ContadorPie = PieIzquierdo.shape[0]
    # Imprimo
    print(f"Cantidad de jugadores con el pie izquierdo: {ContadorPie}")

###opcion 10###
def anadirjugadorclub(jugador, club):

    # Verificar si el jugador está en el archivo de datos
    if jugador not in datosJugadores['nombre jugador'].values:
        print(f'El jugador {jugador} no está en la base de datos.')
        return

    # Verificar si el club está en el archivo de datos
    if club not in datosJugadores['club'].values:
        print(f'El club {club} no está en la base de datos.')
        return
    
    # Actualizar el club del jugador
    datosJugadores.loc[datosJugadores['nombre jugador'] == jugador, 'club'] = club
    
    # Guardar los cambios en el archivo CSV
    datosJugadores.to_csv('fifa.csv')
    
    print(f'El jugador {jugador} ha sido agregado al club {club}.')

### Opción 14 ###
def promediopornacionalidad(datosJugadores):
    nacionalidad = input("Ingrese la nacionalidad para mostrar el promedio de edad, altura y peso: ")
    jugadores = datosJugadores[datosJugadores['nacionalidad'] == nacionalidad]
    datosJugadores['edad'] = jugadores['edad'].astype(int)
    datosJugadores['altura (cm)'] = jugadores['altura (cm)'].astype(int)
    datosJugadores['peso (kg)'] = jugadores['peso (kg)'].astype(int)
    if not jugadores.empty:
        promedios = datosJugadores[['edad', 'altura (cm)', 'peso (kg)']].mean()
        print("Promedio de edad:", f"{promedios['edad']:.1f}")
        print("Promedio de altura en cm:", f"{promedios['altura (cm)']:.1f}")
        print("Promedio de peso en kg:", f"{promedios['peso (kg)']:.1f}")
    else:
        print('No se encontraron jugadores para esa nacionalidad.')

##Opcion 15 incluida por el proyecto##
def mostrar_datos_jugador(nombre_jugador):
    jugador = datosJugadores[datosJugadores['nombre jugador'] == nombre_jugador]
    if not jugador.empty:
        for columna in jugador.columns:
            print(f"{columna}: {jugador[columna].values[0]}")
    else:
        print("Jugador no encontrado")


def menu():
    while True:
        print("--- Menú ---")
        print("1. Mostrar jugadores con sueldo mayor a un número indicado")
        print("2. Mostrar edad promedio de jugadores de un equipo indicado")
        print("3. Mostrar jugadores por letra y nacionalidad")
        print("4. Mostrar jugadores a préstamo")
        print("5. Mostrar jugadores de menor estatura de un equipo indicado")
        print("6. Mostrar la foto de un jugador indicado")
        print("7. Mostrar gráfico con número de jugadores por nacionalidad")
        print("8. Mostrar jugadores y sus clubes por fecha de contratación y año")
        print("9. Modificar atributos de un jugador indicado")
        print("10. Agregar jugador a un club indicado")
        print("11. Mostrar promedio de potencial por equipo")
        print("12. Mostrar top 5 jugadores que ganan más dinero por letra indicada")
        print("13. Mostrar número de jugadores con pie izquierdo")
        print("14. Mostrar promedio de edad, altura y peso por nacionalidad")
        print("15. Mostrar todos los datos de un jugador(incluida por el proyecto)")
        print("0. Salir")

        opcion = int(input("Seleccione una opción: "))
        
        if opcion == 0:
            break
        elif opcion == 1:
            monto = int(input("Ingrese el sueldo: "))
            jugadoressueldomayor(monto)
        elif opcion == 2:
            equipo = input("Ingrese el equipo: ")
            edadpromedioequipo(equipo)
        elif opcion == 3:
            letra = input("Ingrese la letra: ")
            nnacionalidad = input("Ingrese la nacionalidad: ")
            jugadoresletranacionalidad(letra, nnacionalidad)
        elif opcion == 4:
            jugadoresaprestamo()
        elif opcion == 5:
            equipo = input("Ingrese el equipo: ")
            jugadoresmenorestaturaequipo(equipo)
        elif opcion == 6:
            nombre = input("Ingrese el nombre del jugador: ")
            fotojugadores(nombre)
        elif opcion == 7:
            nnacionalidad = input("Ingrese la nacionalidad: ")
            graficojugadorespornacionalidad(nnacionalidad)
        elif opcion == 8:
            fecha = input("Ingrese la fecha de contratación (AAAA-MM-DD): ")
            año = int(input("Ingrese el año de contrato válido: "))
            jugadoresyclubesporfechacontrato(fecha, año)
        elif opcion == 9:
            nNombre = input("Ingrese el nombre del jugador: ")
            nvalor = input("Ingrese el valor en numeros enteros (deje vacío si no desea modificar): ")
            nsueldo = input("Ingrese el sueldo en numeros enteros (deje vacío si no desea modificar): ")
            nposicion = input("Ingrese la posición (deje vacío si no desea modificar): ")
            ncarareal = input("Ingrese si tiene cara real (Yes/No, deje vacío si no desea modificar): ")
            modificaratributosjugador(datosJugadores, nNombre, nvalor, nsueldo, nposicion, ncarareal)
        elif opcion == 10:
            jugador = input("Ingrese el nombre del jugador: ")
            # Obtener el club actual del jugador
            club_actual = datosJugadores.loc[datosJugadores['nombre jugador'] == jugador, 'club'].iloc[0]
            print(f'El jugador {jugador} está actualmente en el club {club_actual}.')
            club = input("Ingrese el nombre del club: ")
            anadirjugadorclub(jugador, club)
        elif opcion == 11:
            promediopotencialporequipo()
        elif opcion == 12:
            letra = input("Ingrese la letra: ")
            top5jugadoresporletra(letra)
        elif opcion == 13:
            numerojugadorespieizquierdo()
        elif opcion == 14:
            promediopornacionalidad(datosJugadores)
        elif opcion == 15:
            nombre_jugador = input("Ingrese el nombre del jugador: ")
            mostrar_datos_jugador(nombre_jugador)
            
        else:
            print("Opción no válida. Intente de nuevo.")

menu()