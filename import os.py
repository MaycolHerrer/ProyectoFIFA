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


def jugadoressueldomayor(monto):
    datosJugadores['sueldo'] = datosJugadores['sueldo'].str.strip()
    datosJugadores['sueldo'] = datosJugadores['sueldo'].replace(',', '').replace('', '0').astype(int)
    jugadores = datosJugadores[datosJugadores['sueldo'] > monto]
    print(jugadores[['nombre jugador', 'sueldo']])


def menu():
    while True:
        print("Bienvenidos a nuestro programa de FIFA de proyecto, intoduzca una opcion numerica para efectuar una accion")
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
            mostrarDatosJugador(nombre_jugador)
            
        else:
            print("Opción no válida. Intente de nuevo.")

menu()