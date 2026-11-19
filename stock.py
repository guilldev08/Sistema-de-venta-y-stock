import csv
import os
from datetime import datetime

from productos import leer_productos, buscar_por_codigo

# Archivo donde se guarda el stock.
ARCHIVO_STOCK = "stock.csv"
# Columnas del archivo stock.csv.
COLUMNAS_STOCK = ["codigo", "cantidad", "ultima_actualizacion"]


# Muestra el menu del modulo stock y ejecuta la opcion elegida.
def menu_stock():
    limpiar_pantalla()

    # Al entrar al modulo se muestra el stock actual.
    mostrar_stock()

    while True:
        print(r"""
            1. Consultar stock
            2. Actualizar stock
            3. Atras
        """, flush=True)

        opcion = pedir_opcion(1, 3)

        if opcion == 1:
            mostrar_stock()
        elif opcion == 2:
            actualizar_stock()
        else:
            break


# Limpia la consola en Windows.
def limpiar_pantalla():
    os.system("cls")


# Pide un numero entero dentro del rango indicado.
def pedir_opcion(minimo, maximo):
    while True:
        try:
            opcion = int(input("Ingrese un número: "))
            if minimo <= opcion <= maximo:
                return opcion
            print(f"Se esperaba un número del {minimo} al {maximo}.")
        except ValueError:
            print("Se esperaba un número entero.")


# Pide una cantidad entera mayor o igual a cero.
def pedir_cantidad():
    while True:
        try:
            cantidad = int(input("Ingresar la nueva cantidad: "))
            if cantidad >= 0:
                return cantidad
            print("La cantidad no puede ser negativa.")
        except ValueError:
            print("Se esperaba un número entero.")


# Crea stock.csv con el encabezado si el archivo no existe o esta vacio.
def crear_archivo_stock_si_no_existe():
    if not os.path.exists(ARCHIVO_STOCK) or os.path.getsize(ARCHIVO_STOCK) == 0:
        with open(ARCHIVO_STOCK, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(COLUMNAS_STOCK)


# Devuelve una lista con todos los registros de stock.csv.
# Cada registro es un diccionario con estas claves:
# codigo, cantidad, ultima_actualizacion.
def leer_stock():
    crear_archivo_stock_si_no_existe()
    registros = []

    with open(ARCHIVO_STOCK, "r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for registro in lector:
            registros.append(registro)

    return registros


# Reescribe stock.csv completo (se usa al actualizar una cantidad).
def guardar_stock(registros):
    with open(ARCHIVO_STOCK, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS_STOCK)
        escritor.writeheader()
        escritor.writerows(registros)


# Busca un registro de stock por codigo dentro de una lista ya leida.
def buscar_stock_en_lista(registros, codigo):
    for registro in registros:
        if registro["codigo"].lower() == codigo.lower():
            return registro

    return None


# Busca y devuelve el registro de stock de un codigo, o None si no existe.
def buscar_stock(codigo):
    return buscar_stock_en_lista(leer_stock(), codigo)


# Muestra todos los productos con su cantidad y su ultima actualizacion.
# Los productos que todavia no tienen registro en stock.csv se muestran
# con cantidad 0 y la leyenda "sin actualizar".
def mostrar_stock():
    productos = leer_productos()

    if not productos:
        print("No hay productos registrados.")
        return

    registros = leer_stock()

    print("-" * 82)
    print(
        f"{'CODIGO':<10} {'NOMBRE':<22} {'MARCA':<15} "
        f"{'CANTIDAD':>10} {'ULTIMA ACTUALIZACION':<20}"
    )
    print("-" * 82)

    for producto in productos:
        registro = buscar_stock_en_lista(registros, producto["codigo"])

        if registro is None:
            cantidad = 0
            fecha = "sin actualizar"
        else:
            cantidad = registro["cantidad"]
            fecha = registro["ultima_actualizacion"]

        print(
            f"{producto['codigo']:<10} "
            f"{producto['nombre']:<22} "
            f"{producto['marca']:<15} "
            f"{cantidad:>10} "
            f"{fecha:<20}"
        )

    print("-" * 82)


# Pide un codigo y devuelve el producto y su registro de stock.
# Recibe la lista de registros ya leida para no abrir el archivo dos veces.
# Devuelve (None, None) si el usuario presiona Enter para volver.
def buscar_stock_por_codigo(registros):
    while True:
        print("Ingrese el código del producto (Enter para volver)")
        codigo = input().strip()

        if codigo == "":
            return None, None

        producto = buscar_por_codigo(codigo)

        if producto is not None:
            registro = buscar_stock_en_lista(registros, producto["codigo"])
            return producto, registro

        print("No existe un producto con ese código.")


# Fija la cantidad de stock de un producto y guarda la fecha y hora.
# Primero se elige un producto por su codigo (la FK de productos.csv).
# Luego se ingresa la cantidad nueva. Si el producto no tenia registro,
# se crea; si ya tenia, se reemplaza la cantidad y la fecha.
def actualizar_stock():
    productos = leer_productos()

    if not productos:
        print("No hay productos registrados.")
        return

    # Se muestra la tabla para que el usuario vea los codigos disponibles.
    mostrar_stock()

    registros = leer_stock()
    producto, registro = buscar_stock_por_codigo(registros)

    if producto is None:
        return

    # Se muestra el stock actual antes de pedir el nuevo valor.
    if registro is None:
        print(f"Stock actual de {producto['nombre']}: 0 (sin actualizar)")
    else:
        print(f"Stock actual de {producto['nombre']}: {registro['cantidad']}")
        print(f"Última actualización: {registro['ultima_actualizacion']}")

    cantidad = pedir_cantidad()
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    if registro is None:
        # El producto no tenia stock: se crea el registro.
        registros.append({
            "codigo": producto["codigo"],
            "cantidad": cantidad,
            "ultima_actualizacion": fecha,
        })
    else:
        # El producto ya tenia stock: se reemplaza la cantidad y la fecha.
        registro["cantidad"] = cantidad
        registro["ultima_actualizacion"] = fecha

    guardar_stock(registros)

    print(f"Stock actualizado: {producto['nombre']} = {cantidad}")
    print(f"Fecha de actualización: {fecha}")
