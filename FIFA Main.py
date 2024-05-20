import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos del archivo CSV
df = pd.read_csv('fifa.csv', index_col='ID', encoding='windows-1252')
df['Sueldo'] = df['Sueldo'].str.replace(r'\D', '', regex=True).replace('', 0).astype(int)

def mostrar_jugadores_con_sueldo_mayor_a(monto):
    jugadores = df[df['Sueldo'] > monto]
    print(jugadores[['Nombre Jugador', 'Sueldo']])

def mostrar_edad_promedio_equipo(equipo):
    jugadores = df[df['Club'] == equipo]
    edad_promedio = jugadores['Age'].mean()
    print(f'Edad promedio de los jugadores del equipo {equipo}: {edad_promedio}')

def mostrar_jugadores_por_letra_y_nacionalidad(letra, nacionalidad):
    jugadores = df[(df['Name'].str.startswith(letra)) & (df['Nationality'] == nacionalidad)]
    print(jugadores[['Name', 'Nationality']])

def mostrar_jugadores_a_prestamo():
    jugadores = df[df['Loaned From'].notna()]
    print(jugadores[['Name', 'Loaned From']])

def mostrar_jugadores_menor_estatura_equipo(equipo):
    jugadores = df[df['Club'] == equipo]
    menor_estatura = jugadores.loc[jugadores['Height'].idxmin()]
    print(menor_estatura[['Name', 'Height']])

def mostrar_foto_jugador(nombre):
    jugador = df[df['Name'] == nombre]
    if not jugador.empty:
        foto_url = jugador.iloc[0]['Photo']
        print(foto_url)
    else:
        print("Jugador no encontrado")

def mostrar_grafico_jugadores_por_nacionalidad(nacionalidad):
    jugadores = df[df['Nationality'] == nacionalidad]
    conteo = jugadores.shape[0]
    plt.bar([nacionalidad], [conteo])
    plt.xlabel('Nacionalidad')
    plt.ylabel('Número de jugadores')
    plt.title(f'Número de jugadores de {nacionalidad}')
    plt.show()

def mostrar_jugadores_y_clubes_por_fecha_contrato(fecha, año):
    jugadores = df[(df['Contract Valid Until'] == año) & (df['Joined'] == fecha)]
    print(jugadores[['Name', 'Club', 'Joined', 'Contract Valid Until']])

def modificar_atributos_jugador(nombre, valor=None, sueldo=None, posicion=None, cara_real=None):
    idx = df[df['Name'] == nombre].index
    if not idx.empty:
        if valor is not None:
            df.at[idx[0], 'Value'] = valor
        if sueldo is not None:
            df.at[idx[0], 'Wage'] = sueldo
        if posicion is not None:
            df.at[idx[0], 'Position'] = posicion
        if cara_real is not None:
            df.at[idx[0], 'Real Face'] = cara_real
        print("Atributos modificados")
    else:
        print("Jugador no encontrado")

def agregar_jugador(club, nombre, nacionalidad, edad, valor, sueldo, posicion, estatura, peso, pie_preferido):
    nuevo_jugador = {
        'Club': club,
        'Name': nombre,
        'Nationality': nacionalidad,
        'Age': edad,
        'Value': valor,
        'Wage': sueldo,
        'Position': posicion,
        'Height': estatura,
        'Weight': peso,
        'Preferred Foot': pie_preferido,
        # Añadir otros atributos necesarios
    }
    df = df.append(nuevo_jugador, ignore_index=True)
    print(f"Jugador {nombre} agregado al club {club}")

def mostrar_promedio_potencial_por_equipo():
    equipos = df['Club'].unique()
    for equipo in equipos:
        jugadores = df[df['Club'] == equipo]
        if not jugadores.empty:
            max_potencial = jugadores['Potential'].max()
            min_potencial = jugadores['Potential'].min()
            promedio_potencial = (max_potencial + min_potencial) / 2
            print(f"Promedio de potencial en {equipo}: {promedio_potencial}")

def mostrar_top_5_jugadores_por_letra(letra):
    jugadores = df[df['Name'].str.contains(letra)]
    top_5_jugadores = jugadores.nlargest(5, 'Wage')
    print(top_5_jugadores[['Name', 'Wage']])

def mostrar_numero_jugadores_pie_izquierdo():
    jugadores_izquierdos = df[df['Preferred Foot'] == 'Left'].shape[0]
    print(f"Número de jugadores con pie izquierdo: {jugadores_izquierdos}")

def mostrar_promedio_edad_altura_peso_por_nacionalidad():
    nacionalidades = df['Nationality'].unique()
    for nacionalidad in nacionalidades:
        jugadores = df[df['Nationality'] == nacionalidad]
        edad_promedio = jugadores['Age'].mean()
        altura_promedio = jugadores['Height'].mean()
        peso_promedio = jugadores['Weight'].mean()
        print(f"Nacionalidad: {nacionalidad}, Edad Promedio: {edad_promedio}, Altura Promedio: {altura_promedio}, Peso Promedio: {peso_promedio}")

# Menú del programa
def menu():
    while True:
        print("\n--- Menú ---")
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
            mostrar_jugadores_con_sueldo_mayor_a(monto)
        elif opcion == 2:
            equipo = input("Ingrese el equipo: ")
            mostrar_edad_promedio_equipo(equipo)
        elif opcion == 3:
            letra = input("Ingrese la letra: ")
            nacionalidad = input("Ingrese la nacionalidad: ")
            mostrar_jugadores_por_letra_y_nacionalidad(letra, nacionalidad)
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
            valor = float(valor) if valor else None
            sueldo = float(sueldo) if sueldo else None
            cara_real = True if cara_real.lower() == 'true' else (False if cara_real.lower() == 'false' else None)
            modificar_atributos_jugador(nombre, valor, sueldo, posicion, cara_real)
        elif opcion == 10:
            club = input("Ingrese el club: ")
            nombre = input("Ingrese el nombre del jugador: ")
            nacionalidad = input("Ingrese la nacionalidad: ")
            edad = int(input("Ingrese la edad: "))
            valor = float(input("Ingrese el valor: "))
            sueldo = float(input("Ingrese el sueldo: "))
            posicion = input("Ingrese la posición: ")
            estatura = float(input("Ingrese la estatura: "))
            peso = float(input("Ingrese el peso: "))
            pie_preferido = input("Ingrese el pie preferido: ")
            agregar_jugador(club, nombre, nacionalidad, edad, valor, sueldo, posicion, estatura, peso, pie_preferido)
        elif opcion == 11:
            mostrar_promedio_potencial_por_equipo()
        elif opcion == 12:
            letra = input("Ingrese la letra: ")
            mostrar_top_5_jugadores_por_letra(letra)
        elif opcion == 13:
            mostrar_numero_jugadores_pie_izquierdo()
        elif opcion == 14:
            mostrar_promedio_edad_altura_peso_por_nacionalidad()
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu()
