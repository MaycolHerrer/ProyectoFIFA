import os
import requests
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
# Cargar datos del archivo CSV
datosJugadores = pd.read_csv('fifa.csv', index_col='ID', encoding='windows-1252')
# Usar expresiones regulares para limpiar conjunto de caracteres
datosJugadores['Sueldo'] = df['Sueldo'].str.replace(r'\D', '', regex=True).replace('', 0).astype(int)
print(datosJugadores.info())

def jugadores_sueldo_Mayor(monto):
    jugadores = datosJugadores[datosJugadores['Sueldo'] > monto]
    print(jugadores[['Nombre Jugador', 'Sueldo']])

def edad_promedio_equipo(equipo):
    jugadores = datosJugadores[datosJugadores['Club'] == equipo]
    edad_promedio = jugadores['Edad'].mean()
    print(f'Edad promedio de los jugadores del equipo {equipo}: {edad_promedio}')

def jugadores_letra_nacionalidad(letra, nacionalidad):
    if len(letra) == 1:
        jugadores = datosJugadores[(datosJugadores['Nombre Jugador'].str.startswith(letra)) & (df['Nacionalidad'] == nacionalidad)]
        print(jugadores[['Nombre Jugador', 'Nacionalidad']])
    else:
        print("La letra debe ser solo un carácter")

def jugadores_a_prestamo():
    jugadores = datos_jugadores[datos_jugadores['Prestado Por'].notna()]
    print(jugadores[['Nombre Jugador', 'Prestado Por']])

def jugadores_menor_estatura_equipo(equipo):
    jugadores = datos_jugadores[datos_jugadores['Club'] == equipo]
    if not jugadores.empty:
        menorEstatura = jugadores.loc[jugadores['Altura (cm)'].idxmin()]
        print(menorEstatura[['Nombre Jugador', 'Altura (cm)']])
    else:
        print(f"No se encontraron jugadores para el equipo {equipo}")
    
def foto_jugadores(nombre):
    jugador = datosJugadores[datosJugadores['Nombre Jugador'] == nombre]
    if not jugador.empty:
        foto_url = jugador.iloc[0]['Foto Jugador']
        response = requests.get(foto_url)
        response.raise_for_status()  # Genera una excepción si la solicitud no fue exitosa (código de estado diferente de 200)
        temp_file = "temp_image.jpg"  # Guardar la imagen en un archivo temporal
        with open(temp_file, "wb") as f:
            f.write(response.content)
        imagen = Image.open(temp_file)  # Abrir la imagen con PIL
        imagen.show()
        os.remove(temp_file)  # Eliminar el archivo temporal
    else:
        print("Jugador no encontrado")

def grafico_jugadores_por_nacionalidad(nacionalidad):
    jugadores = datosJugadores[datosJugadores['Nacionalidad'] == nacionalidad]
    conteo = jugadores['Nombre Jugador'].nunique()  # Contar la cantidad de valores únicos en la columna 'Nombre Jugador'
    print(f'Cantidad de jugadores de {nacionalidad}: {conteo}')
    plt.bar([nacionalidad], [conteo])
    plt.xlabel('Nacionalidad')
    plt.ylabel('Número de jugadores')
    plt.title(f'Número de jugadores de {nacionalidad}')
    plt.show()

def jugadores_y_clubes_por_fecha_contrato(fecha, año):
    jugadores = datosJugadores[(datosJugadores['Fecha Contratacion'] == fecha) & (datosJugadores['Contrato Valido Hasta'] == año)]
    print(jugadores[['Nombre Jugador', 'Club', 'Fecha Contratacion', 'Contrato Valido Hasta']])

def modificar_atributos_jugador(nombre, valor=None, sueldo=None, posicion=None, cara_real=None):
    idx = datosJugadores[datosJugadores['Nombre Jugador'] == nombre].index
    if not idx.empty:
        if valor is not None:
            datosJugadores.at[idx[0], 'Valor'] = valor
        if sueldo is not None:
            datosJugadores.at[idx[0], 'Sueldo'] = sueldo
        if posicion is not None:
            datosJugadores.at[idx[0], 'Posicion'] = posicion
        if cara_real is not None:
            datosJugadores.at[idx[0], 'Cara Real'] = caraReal
        print("Atributos modificados")
    else:
        print("Jugador no encontrado")

def promedio_potencial_por_equipo():
    equipos = datosJugadores['Club'].unique()
    for equipo in equipos:
        jugadores = df[df['Club'] == equipo]
        if not jugadores.empty:
            max_potencial = jugadores['Potential'].max()
            min_potencial = jugadores['Potential'].min()
            promedio_potencial = (max_potencial + min_potencial) / 2
            print(f"Promedio de potencial en {equipo}: {promedio_potencial}")

def top_5_jugadores_por_letra(letra):
    jugadores = datosJugadores[datosJugadores['Nombre Jugador'].str.contains(letra)]
    top_5_jugadores = jugadores.nlargest(5, 'Sueldo')
    print(top_5_jugadores[['Nombre Jugador', 'Sueldo']])

def numero_jugadores_pie_izquierdo():
    jugadoresIzquierdos = datosJugadores[datosJugadores['Pie Preferido'] == 'left'].shape[0]
    print(f"Número de jugadores con pie izquierdo: {jugadoresIzquierdos}")

def promedio_edad_altura_peso_por_nacionalidad():
    nacionalidad = input("Ingrese la nacionalidad para mostrar el promedio de edad, altura y peso: ")
    jugadores = datosJugadores[datosJugadores['Nacionalidad'] == nacionalidad]
    if not jugadores.empty:
        promedios = jugadores[['Edad', 'Altura (cm)', 'Peso (Kg)']].mean()
        promedios.plot(kind='bar')
        plt.xlabel('Atributos')
        plt.ylabel('Promedio')
        plt.title(f'Promedio de Edad, Altura y Peso para {nacionalidad}')
        plt.show()
    else:
        print(f"No se encontraron jugadores para la nacionalidad {nacionalidad}")

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
        print("0. Salir")

        opcion = int(input("Seleccione una opción: "))
        
        if opcion == 0:
            break
        elif opcion == 1:
            monto = int(input("Ingrese el sueldo: "))
            mostrar_jugadores_sueldo_mayor(monto)
        elif opcion == 2:
            equipo = input("Ingrese el equipo: ")
            mostrar_edad_promedio_equipo(equipo)
        elif opcion == 3:
            letra = input("Ingrese la letra: ")
            nacionalidad = input("Ingrese la nacionalidad: ")
            mostrar_jugadores_letra_nacionalidad(letra, nacionalidad)
        elif opcion == 4:
            mostrar_jugadores_a_prestamo()
        elif opcion == 5:
            equipo = input("Ingrese el equipo: ")
            mostrar_jugadores_menor_estatura_equipo(equipo)
        elif opcion == 6:
            nombre = input("Ingrese el nombre del jugador: ")
            mostrar_foto_jugador(nombre)
        elif opcion == 7:
            nacionalidad = input("Ingrese la nacionalidad: ")
            mostrar_grafico_jugadores_por_nacionalidad(nacionalidad)
        elif opcion == 8:
            fecha = input("Ingrese la fecha de contratación (AAAA-MM-DD): ")
            año = int(input("Ingrese el año de contrato válido: "))
            mostrar_jugadores_y_clubes_por_fecha_contrato(fecha, año)
        elif opcion == 9:
            nombre = input("Ingrese el nombre del jugador: ")
            valor = input("Ingrese el valor (deje vacío si no desea modificar): ")
            sueldo = input("Ingrese el sueldo (deje vacío si no desea modificar): ")
            posicion = input("Ingrese la posición (deje vacío si no desea modificar): ")
            cara_real = input("Ingrese si tiene cara real (True/False, deje vacío si no desea modificar): ")
            valor = int(valor) if valor else None
            sueldo = int(sueldo) if sueldo else None
            cara_real = True if cara_real.lower() == 'true' else (False if cara_real.lower() == 'false' else None)
            modificar_atributos_jugador(nombre, valor, sueldo, posicion, cara_real)
        elif opcion == 10:
            club = input("Ingrese el club: ")
            nombre = input("Ingrese el nombre del jugador: ")
            nacionalidad = input("Ingrese nacionalidad: ")
            edad = int(input("Ingrese edad: "))
            overall = int(input("Ingrese el overall: "))
            potential = int(input("Ingrese el potential: "))
            valor = int(input("Ingrese el valor: "))
            sueldo = int(input("Ingrese el sueldo: "))
            pie_preferido = input("Ingrese el pie preferido: ")
            reputacion_internacional = int(input("Ingrese la reputación internacional: "))
            pie_debil = input("Ingrese el pie débil: ")
            skill_moves = int(input("Ingrese el número de Skill Moves: "))
            tipo_cuerpo = input("Ingrese el tipo de cuerpo: ")
            cara_real = input("Ingrese si tiene cara real (True/False): ").lower() == 'true'
            posicion = input("Ingrese la posición: ")
            joined = input("Ingrese la fecha de contratación (AAAA-MM-DD): ")
            prestado_por = input("Ingrese si está prestado por otro club (deje vacío si no): ")
            contrato_valido_hasta = input("Ingrese la fecha de finalización del contrato (AAAA-MM-DD): ")
            estatura = int(input("Ingrese la estatura: "))
            peso = int(input("Ingrese el peso: "))
            clausula_liberacion = input("Ingrese la cláusula de liberación: ")
            foto_jugador = input("Ingrese la URL de la foto del jugador: ")
            # Agregar el jugador al DataFrame
            datosJugadores.loc[len(df)] = [club, nombre, nacionalidad, edad, overall, potential, valor, sueldo, pie_preferido, reputacion_internacional,
                       pie_debil, skill_moves, tipo_cuerpo, cara_real, posicion, joined, prestado_por, contrato_valido_hasta,
                       estatura, peso, clausula_liberacion, foto_jugador]
            print("Jugador agregado correctamente.")
        elif opcion == 11:
            promedio_potencial_por_equipo()
        elif opcion == 12:
            letra = input("Ingrese la letra: ")
            top_5_jugadores_por_letra(letra)
        elif opcion == 13:
            numero_jugadores_pie_izquierdo()
        elif opcion == 14:
            promedio_edad_altura_peso_por_nacionalidad()
        else:
            print("Opción no válida. Intente de nuevo.")

menu()
