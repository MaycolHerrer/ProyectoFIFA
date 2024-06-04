#Dante Aliste
#Pia Godoy
#Hermann Muller
#Maycol Herrera
#Ricardo Steelhearts
import os
import requests
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

def remplazarVocales(s): #Aqui definimos una tupla de reemplazos el primer elemento el es que vamos a cambiar con el segundo elemento
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
        s = s.replace(a, b).replace(a.upper(), b.upper()) #Aqui remplazamos cada elemento del a por el b tanto ara mayusculas como minisculas
    return s

datosJugadores = pd.read_csv('fifa.csv', encoding='windows-1252') #Aqui Cargamos el documento con el encoding para los caracteres

datosJugadores = datosJugadores.astype(str).map(remplazarVocales) # Convertimos todas las columnas a cadena y aplicamos remplazarVocales a todos los valores

datosJugadores = datosJugadores.rename(columns=remplazarVocales) # Quitamos espacios en blanco de los nombres de las columnas y convertir a minusculas
datosJugadores.columns = [col.strip().lower() for col in datosJugadores.columns] # renombramos las columnas limpiando los espacios con stripy convertir en minuscula con lower
datosJugadores = datosJugadores.map(str.lower) #aplicamos y convertimos cada cadena de texto a minúsculas.
print(datosJugadores.info())
## Opcion 1##
#Descripcion: El usuario selecciona a un monto y el programa busca a todos los jugadores con un sueldo mayor al monto seleccionado
def jugadoressueldomayor(monto):
# Usar expresiones regulares para limpiar conjunto de caracteres
#datosJugadores['sueldo'] = datosJugadores['sueldo'].str.replace(r'\D', '', regex=True).replace('', 0).astype(int)
    datosJugadores['sueldo'] = datosJugadores['sueldo'].astype(str).str.strip() #convertimos la columna sueldo a cadena y luego aplicamos strip para limpiar espacios
    datosJugadores['sueldo'] = datosJugadores['sueldo'].replace(',', '').replace('', '0').astype(int) #remplazamos las , con cadenas vacias luego con 0 y convertimos todos a int
    jugadores = datosJugadores[datosJugadores['sueldo'] > monto]
    if not jugadores.empty: #si no hay valores vacios
        print(jugadores[['nombre jugador', 'sueldo']])
    else:
        print(f"No hay jugadores con un sueldo mayor a {monto}.")
## Opcion 2##
#Descripcion: Mostrar la edad promedio de un equipo seleccionado por el usuario 
def edadpromedioequipo(equipo):
    datosJugadores['edad'] = datosJugadores['edad'].astype(int) 
    jugadores = datosJugadores[datosJugadores['club'].str.contains(equipo, case=False)] #selecciomos las filas de datosJugadores donde el valor en la columna club contiene el valor de equpo ignorando las diferencias de mayúsculas y minúsculas.
    if not jugadores.empty:
        edadpromedio = jugadores['edad'].mean() #para optener el promedio
        edadpromedio = round(edadpromedio, 2) #Para que redondee a 2 decimales
        print(f'La edad promedio de los jugadores del equipo que contiene "{equipo}" es de {edadpromedio} años.')
    else:
        print(f'No se encontraron jugadores para el equipo que contiene "{equipo}".')
## Opcion 3##
#Descripcion: Mostrar jugadores cuyo nombre comienza con la letra y nacionalidad seleccionada por el usuario
def jugadoresletranacionalidad(letra, nacionalidad):
    if len(letra) == 1:#asegura que la variable letra solo posea un solo caracter
        jugadores = datosJugadores[(datosJugadores['nombre jugador'].str.startswith(letra)) & (datosJugadores['nacionalidad'] == nacionalidad)]# Hace un filtro al dataframe datosJugadores para que busque jugadores con la letra inicial del jugador y su nacionalidad
        print(jugadores[['nombre jugador', 'nacionalidad']])#imprime los resultados obtenidos en pantalla
    else:
        print("La letra debe ser solo un carácter")
##Opcion 4##
#Descripcion: Opcion que muestra jugadores a préstamo
def jugadoresaprestamo(): #muestra los jugadores que estan prestados por algun club
    jugadores = datosJugadores[datosJugadores['prestado por'].notna()] #con el notnat devuelve verdadero o falso si es prestado por un equipo
    print(jugadores[['nombre jugador', 'prestado por']])
##Opcion 5##
#Descripcion: Mostrar jugadores de menor estatura en un equipo seleccionado por el usuario

def jugadoresmenorestaturaequipo(equipo):
    jugadores = datosJugadores[datosJugadores['club'] == equipo]
    if not jugadores.empty:
        menorEstatura = jugadores.loc[jugadores['altura (cm)'].idxmin()] # con el idxmin devuelve el indice del valor minimo
        print(menorEstatura[['nombre jugador', 'altura (cm)']])
    else:
        print(f"No se encontraron jugadores para el equipo {equipo}")
##Opcion 6## 
#Descripcion: Mostrar una foto del jugador seleccionado por el usuario
def fotojugadores(nombre):
    jugador = datosJugadores[datosJugadores['nombre jugador'] == nombre]
    if not jugador.empty:
        fotourl = jugador.iloc[0]['foto jugador'] #buscamos el id de la columna jugador y accedemos al valor que tiene en foto jugador
        response = requests.get(fotourl)  # un código de estado HTTP de 200 indica una solicitud exitosa
        if response.status_code == 200:  # verificar si la solicitud fue exitosa
            tempfile = "tempimage.jpg"  # guardamos la imagen en un archivo temporal
            with open(tempfile, "wb") as f: #abrimos un archivo en modo de escritura binaria para guardar la imagen descargada.
                f.write(response.content) #el contenido de la respuesta de la solicitud se escribe en el archivo temporal.
            imagen = Image.open(tempfile)  # abrimos la imagen con pillow
            imagen.show() # la mostramos
            os.remove(tempfile)  # eliminamos el archivo temporal
        else:
            print("La solicitud no fue exitosa. Código de estado:", response.status_code)
    else:
        print("Jugador no encontrado")
##Opcion 7##  
#mostrar grafico que muestre jugadores con nacionalidad seleccionada por el usuario
def graficojugadorespornacionalidad(nacionalidad):
    conteo = datosJugadores['nacionalidad'].value_counts() # Obtenemos conteo de jugadores por nacionalidad
    if nacionalidad in conteo: # verificamos si la nacionalidad especificada está en los datos
        conteoEspecifico = conteo[nacionalidad] # Obtener conteo de jugadores de la nacionalidad especificada
    else:
        print(f'No hay jugadores de {nacionalidad}')
        return
    # Obtenemos las 5 nacionalidades más comunes, excluyendo la nacionalidad especificada
    top5 = conteo.drop(nacionalidad).head(5) #se excluye la nacionalidad del conteo con drop y se seleccionan las 5 primeras de nacionalidad
    # Agregar la nacionalidad especificada a las 5 más comunes
    top5[nacionalidad] = conteoEspecifico
    plt.bar(top5.index, top5, color=['blue'] * 5 + ['red'])# Crea un grafico de barras usando las nacionalidades como indice
    plt.xlabel('nacionalidad')# Añade una etiqueta al eje x llamandose nacionalidad
    plt.ylabel('Numero de jugadores')# Añade una etiqueta en el eje Y llamado numero de jugadores
    plt.title(f'numero de jugadores por nacionalidad (top 5 y {nacionalidad})')# Añade un titulo al grafico
    plt.xticks(rotation=45)# Realiza una rotacion de 45° grados para mejorar la legibilidad
    plt.show()# Muestra el grafico
##Opcion 8##
#Descripcion: Mostrar jugadores y sus clubes para aquellos jugadores que tienen una fecha de contratación y un año de contrato valido indicado por el usuario
def jugadoresyclubesporfechacontrato(fecha, año):
    jugadores = datosJugadores[(datosJugadores['fecha contratacion'] == fecha) & (datosJugadores['contrato valido hasta'] == año)]# esta funcion le aplica un filtro al archivo para buscar jugadores que cumplan con las condiciones
    print(jugadores[['nombre jugador', 'club', 'fecha contratacion', 'contrato Valido Hasta']])# Imprime los jugadores que cumplieron con las condiciones asignadas
## Opción 9 ##  
#Descripcion: Modificar atributos de valor, sueldo y posición y cara real de un jugador indicado por el usuario
def modificaratributosjugador(datosJugadores, nNombre, nvalor=None, nsueldo=None, nposicion=None, ncarareal=None):
    JugadorFiltrado = datosJugadores[datosJugadores['nombre jugador'] == nNombre].index   # usamos el método loc para encontrar el indice de la fila donde está el jugador
    # Iniciamos un contador para imprimir el mensaje final solo si hay al menos 1 cambio
    contador = 0 # Cambiar los atributos si tienen un valor diferente de None
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
    datosJugadores.to_csv('fifa.csv', index=False)    # Guardamos los cambios en el archivo csv   
    if contador > 0:
        print("Atributos modificados exitosamente")
    else:
        print("No hubo cambios")
###Opcion 10###
#Descripcion: Opcion que agrega un jugador en un club indicado por el usuario
def anadirjugadorclub(jugador, club):
    if jugador not in datosJugadores['nombre jugador'].values:  # Verificamos si el jugador no está en el archivo de datos
        print(f'El jugador {jugador} no está en la base de datos.')
        return #Si esta sigue
    datosJugadores.loc[datosJugadores['nombre jugador'] == jugador, 'club'] = club  #actualizamos el club del jugador
    datosJugadores.to_csv('fifa.csv') #guardamos los cambios en el archivo CSV
    print(f'El jugador {jugador} ha sido agregado al club {club}.')
##Opcion 11##
#Descripcion: Opcion que muestra el promedio de pontencial entre los jugadores de mayor y menor potencial por cada equipo
def promediopotencialporequipo():
    equipo = input("Ingrese el nombre del equipo: ")  # solicitar al usuario el nombre del equipo
    jugadores = datosJugadores[datosJugadores['club'].str.contains(equipo, case=False)].copy() #para crear una copia del df y evita cambios
    if not jugadores.empty:  # verificar si hay jugadores en el equipo seleccionado
        jugadores['potential'] = jugadores['potential'].astype(int)  # Convertir a enteros
        maxPotencial = jugadores['potential'].max()  # Encontrar el maximo y mínimo potencial entre los jugadores del equipo
        minPotencial = jugadores['potential'].min()
        promediopotencial = (maxPotencial + minPotencial) / 2  # Calcular el promedio de potencial del equipo actual
        print(f"promedio de potencial en {equipo}: {promediopotencial}")
    else:
        print(f"No se encontraron jugadores para el equipo {equipo}")
##Opcion 12##
#Descripcion: Opcion que muestra a los 5 jugadores que ganan mas dinero y que en sus nombres contienen sus nombre y/o apellidos una letra indicada por el usuario
def top5jugadoresporletra(letra):
    datosJugadores['sueldo'] = datosJugadores['sueldo'].astype(str).str.strip()# convertimos la columna sueldo a cadena y luego aplicamos strip para limpiar espacios
    datosJugadores['sueldo'] = datosJugadores['sueldo'].replace(',', '').replace('', '0').astype(int)# remplazamos las , con cadenas vacias luego con 0 y convertimos todos a in
    jugadores = datosJugadores[datosJugadores['nombre jugador'].str.contains(letra)]# se utiliza para verificar si la letra está presente en el nombre del jugador
    top5jugadores = jugadores.nlargest(5, 'sueldo')# Encuentra los 5 jugadores con los salarios más altos entre los jugadores filtrados
    print(top5jugadores[['nombre jugador', 'sueldo']])# Imprime los nombres de los jugadores y sus salarios de los 5 jugadores principales   
##Opcion 13##
#Descripcion: mostrar jugadores cuyo pie preferido es el pie izquierdo
def numerojugadorespieizquierdo():
    PieIzquierdo = datosJugadores[datosJugadores['pie preferido'] == 'left']# Filtramos por pie izquierdo
    ContadorPie = PieIzquierdo.shape[0]    # contaos con shape la cantida de filas que hay en la columna
    print(f"Cantidad de jugadores con el pie izquierdo: {ContadorPie}")
##Opcion 14##
#Descripcion: Mostrar promedio de edad,altura y peso de jugadores por nacionalidad
def promediopornacionalidad(datosJugadores):
    nacionalidad = input("Ingrese la nacionalidad para mostrar el promedio de edad, altura y peso: ")# Le pide al usuario la nacionalidad del equipo para poder calcular 
    jugadores = datosJugadores[datosJugadores['nacionalidad'] == nacionalidad]# Filtra los datos de jugadores para obtener solo los jugadopara asi poder calcular el promedio de los jugadoresa
    datosJugadores['edad'] = jugadores['edad'].astype(int)# Convierte las columnas de edad en un numero entero
    datosJugadores['altura (cm)'] = jugadores['altura (cm)'].astype(int)# Convierte la columna altura a tipo entero
    datosJugadores['peso (kg)'] = jugadores['peso (kg)'].astype(int)# Convierte la columna peso a tipo entero
    if not jugadores.empty:# Verifica si hay jugadores con la nacionalidad ingresada por el usuario
        promedios = datosJugadores[['edad', 'altura (cm)', 'peso (kg)']].mean()# Calcula los promedios de edad, altura y peso para los jugadores de la nacionalidad dada
        print("Promedio de edad:", f"{promedios['edad']:.1f}")# Imprime la edad promedio de los jugadores con la nacionalidad ingresada
        print("Promedio de altura en cm:", f"{promedios['altura (cm)']:.1f}")# Imprime la altura promedio de los jugadores con la nacionalidad ingresada
        print("Promedio de peso en kg:", f"{promedios['peso (kg)']:.1f}")# Imprime el peso promedio de los jugadores con la nacionalidad ingresada
    else:# Si no se encuentran jugadores para la nacionalidad ingresada, imprime un mensaje indicándolo
        print('No se encontraron jugadores para esa nacionalidad.')
##Opcion 15 incluida por el proyecto##
#Descripcion: Opcion incluida por el proyecto en el cual se muestra todos los datos de un jugador seleccionado por el usuario
def mostrarDatosJugador(nombre_jugador): 
    jugador = datosJugadores[datosJugadores['nombre jugador'] == nombre_jugador] #crea una variable que seleccione al jugador para buscarlo en el archivo
    if not jugador.empty: #si existen datos de jugador crea una iteracion en la que imprime todos los datos del jugador
        for columna in jugador.columns:
            print(f"{columna}: {jugador[columna].values[0]}")
    else: #si no existe el jugador imprime que el jugador no ha sido encontrado
        print("Jugador no encontrado")
def menu(): #creacion del menu en el que el usuario va a tener diferentes opciones enumeradas del 1 al 15 (incluyendo el 0 para salir)
    while True:
        print("Bienvenidos a nuestro programa de FIFA de proyecto, intoduzca una opcion numerica para efectuar una accion")
        print("1- Mostrar jugadores con sueldo mayor a un numero indicado")
        print("2- Mostrar edad promedio de jugadores de un equipo indicado")
        print("3- Mostrar jugadores por letra y nacionalidad")
        print("4- Mostrar jugadores a préstamo")
        print("5- Mostrar jugadores de menor estatura de un equipo indicado")
        print("6- Mostrar la foto de un jugador indicado")
        print("7- Mostrar grafico con número de jugadores por nacionalidad")
        print("8- Mostrar jugadores y sus clubes por fecha de contratación y año")
        print("9- Modificar atributos de un jugador indicado")
        print("10- Agregar jugador a un club indicado")
        print("11- Mostrar promedio de potencial por equipo")
        print("12- Mostrar top 5 jugadores que ganan más dinero por letra indicada")
        print("13- Mostrar número de jugadores con pie izquierdo")
        print("14- Mostrar promedio de edad, altura y peso por nacionalidad")
        print("15- Mostrar todos los datos de un jugador(incluida por el proyecto)")
        print("0- Salir")
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
            nsueldo = input("Ingrese el sueldo en numeros enteros (deje vacio si no desea modificar): ")
            nposicion = input("Ingrese la posición (deje vacío si no desea modificar): ")
            ncarareal = input("Ingrese si tiene cara real si no, deje vacio si no desea modificar): ")
            modificaratributosjugador(datosJugadores, nNombre, nvalor, nsueldo, nposicion, ncarareal)
        elif opcion == 10:
            jugador = input("Ingrese el nombre del jugador: ")
            club_actual = datosJugadores.loc[datosJugadores['nombre jugador'] == jugador, 'club'].iloc[0] #para obtener el club actual del jugador
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
            mostrarDatosJugador(nombre_jugador)   
        else:
            print("Opción no válida. Intente de nuevo.")

menu()
