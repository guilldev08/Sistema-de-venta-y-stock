import csv
import os
from datetime import datetime

from productos import buscar_por_codigo
from stock import leer_stock, buscar_stock_en_lista, guardar_stock, mostrar_stock

# Archivo con la cabecera de cada venta.
ARCHIVO_VENTAS = "ventas.csv"
COLUMNAS_VENTAS = ["numero_venta", "fecha", "total"]

# Archivo con el detalle de cada venta.
# numero_venta es la clave foranea que apunta a ventas.csv.
ARCHIVO_SUB_VENTAS = "sub_venta.csv"
COLUMNAS_SUB_VENTAS = [
    "numero_venta",
    "codigo",
    "nombre",
    "cantidad",
    "precio_unitario",
    "subtotal",
]


# Muestra el menu del modulo ventas.
def menu_ventas():
    limpiar_pantalla()

    while True:
        print(r"""
            1. Realizar venta
            2. Atras
        """, flush=True)

        opcion = pedir_opcion(1, 2)

        if opcion == 1:
            realizar_venta()
        else:
            break


# Arma el carrito y muestra sus opciones hasta pagar o salir.
def realizar_venta():
    carrito = []

    while True:
        mostrar_carrito(carrito)

        print(r"""
            1. Agregar producto
            2. Quitar producto
            3. Pagar
            4. Atras
        """, flush=True)

        opcion = pedir_opcion(1, 4)

        if opcion == 1:
            agregar_producto(carrito)
        elif opcion == 2:
            quitar_producto(carrito)
        elif opcion == 3:
            if pagar(carrito):
                return
        else:
            if len(carrito) > 0:
                if confirmar("¿Descartar el carrito?"):
                    return
            else:
                return


# Pide un producto y una cantidad, valida el stock y lo agrega al carrito.
def agregar_producto(carrito):
    mostrar_stock()

    while True:
        print("Ingrese el código del producto (Enter para volver)")
        codigo = input().strip()

        if codigo == "":
            return

        producto = buscar_por_codigo(codigo)

        if producto is not None:
            break

        print("No existe un producto con ese código.")

    cantidad = pedir_cantidad_carrito()

    # Si el producto ya esta en el carrito, se suma la cantidad nueva.
    cantidad_en_carrito = 0
    for item in carrito:
        if item["codigo"].lower() == producto["codigo"].lower():
            cantidad_en_carrito = item["cantidad"]
            break

    cantidad_total = cantidad_en_carrito + cantidad
    disponible = cantidad_stock(producto["codigo"])

    # Si el carrito pide mas de lo que hay, se muestra la alerta.
    while cantidad_total > disponible:
        print(f"\nALERTA: querés {cantidad_total} de {producto['nombre']}, pero el stock es {disponible}.")
        print(r"""
            1. Actualizar stock ahora
            2. Actualizar después (dejar en 0)
            3. Cancelar
        """)

        opcion = pedir_opcion(1, 3)

        if opcion == 1:
            nueva_cantidad = pedir_cantidad_stock()
            fecha = fijar_stock(producto["codigo"], nueva_cantidad)
            print(f"Stock actualizado a {nueva_cantidad} ({fecha}).")
            disponible = cantidad_stock(producto["codigo"])
        elif opcion == 2:
            print("Se dejará el stock de este producto en 0 al pagar.")
            break
        else:
            return

    precio = float(producto["precio"])

    if cantidad_en_carrito > 0:
        # El producto ya estaba: se actualiza la cantidad y el subtotal.
        for item in carrito:
            if item["codigo"].lower() == producto["codigo"].lower():
                item["cantidad"] = cantidad_total
                item["subtotal"] = round(precio * cantidad_total, 2)
                break
    else:
        # El producto es nuevo en el carrito.
        carrito.append({
            "codigo": producto["codigo"],
            "nombre": producto["nombre"],
            "cantidad": cantidad,
            "precio_unitario": precio,
            "subtotal": round(precio * cantidad, 2),
        })

    print(f"Producto agregado: {producto['nombre']} x {cantidad}")


# Quita del carrito toda la linea de un producto.
def quitar_producto(carrito):
    if not carrito:
        print("El carrito está vacío.")
        return

    mostrar_carrito(carrito)
    print("Ingrese el código del producto a quitar (Enter para volver)")
    codigo = input().strip()

    if codigo == "":
        return

    for item in carrito:
        if item["codigo"].lower() == codigo.lower():
            carrito.remove(item)
            print(f"Producto quitado: {item['nombre']}")
            return

    print("Ese producto no está en el carrito.")


# Confirma la venta, descuenta stock y guarda la cabecera y el detalle.
def pagar(carrito):
    if not carrito:
        print("El carrito está vacío. Agregá un producto antes de pagar.")
        return False

    mostrar_carrito(carrito)
    total = calcular_total(carrito)

    if not confirmar(f"¿Confirmar la venta por ${total:.2f}?"):
        return False

    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    registros = leer_stock()

    # Se descuenta el stock de cada producto del carrito.
    for item in carrito:
        registro = buscar_stock_en_lista(registros, item["codigo"])

        if registro is None:
            disponible = 0
        else:
            disponible = int(registro["cantidad"])

        if item["cantidad"] > disponible:
            print(
                f"ALERTA: {item['nombre']}: pediste {item['cantidad']} "
                f"y hay {disponible}. Se deja el stock en 0."
            )
            nueva_cantidad = 0
        else:
            nueva_cantidad = disponible - item["cantidad"]

        if registro is None:
            registros.append({
                "codigo": item["codigo"],
                "cantidad": nueva_cantidad,
                "ultima_actualizacion": fecha,
            })
        else:
            registro["cantidad"] = nueva_cantidad
            registro["ultima_actualizacion"] = fecha

    guardar_stock(registros)

    # Se guarda la venta y despues su detalle.
    numero_venta = nuevo_numero_venta()
    agregar_venta(numero_venta, fecha, total)

    for item in carrito:
        agregar_sub_venta(
            numero_venta,
            item["codigo"],
            item["nombre"],
            item["cantidad"],
            item["precio_unitario"],
            item["subtotal"],
        )

    mostrar_ticket(numero_venta, fecha, carrito)
    carrito.clear()
    return True


# Muestra el carrito con sus subtotales y el total.
def mostrar_carrito(carrito):
    print("\n--- CARRITO ---")

    if not carrito:
        print("El carrito está vacío.")
        print("TOTAL: $0.00")
        return

    imprimir_items(carrito)
    total = calcular_total(carrito)
    print(f"TOTAL: ${total:.2f}")


# Muestra el ticket de una venta ya confirmada.
def mostrar_ticket(numero_venta, fecha, carrito):
    print("\n" + "=" * 78)
    print(f"VENTA N° {numero_venta}")
    print(f"Fecha: {fecha}")
    print("=" * 78)

    imprimir_items(carrito)

    total = calcular_total(carrito)
    print(f"TOTAL: ${total:.2f}")
    print("=" * 78)


# Imprime la tabla de productos del carrito.
def imprimir_items(carrito):
    print("-" * 78)
    print(
        f"{'CODIGO':<10} {'NOMBRE':<22} {'CANTIDAD':>10} "
        f"{'PRECIO':>12} {'SUBTOTAL':>12}"
    )
    print("-" * 78)

    for item in carrito:
        print(
            f"{item['codigo']:<10} "
            f"{item['nombre']:<22} "
            f"{item['cantidad']:>10} "
            f"{float(item['precio_unitario']):>12.2f} "
            f"{float(item['subtotal']):>12.2f}"
        )

    print("-" * 78)


# Suma los subtotales del carrito.
def calcular_total(carrito):
    total = 0

    for item in carrito:
        total = total + float(item["subtotal"])

    return total


# Devuelve la cantidad de stock de un producto. Si no tiene registro, es 0.
def cantidad_stock(codigo):
    registros = leer_stock()
    registro = buscar_stock_en_lista(registros, codigo)

    if registro is None:
        return 0

    return int(registro["cantidad"])


# Fija el stock de un producto y guarda la fecha de actualizacion.
def fijar_stock(codigo, cantidad):
    registros = leer_stock()
    registro = buscar_stock_en_lista(registros, codigo)
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    if registro is None:
        registros.append({
            "codigo": codigo,
            "cantidad": cantidad,
            "ultima_actualizacion": fecha,
        })
    else:
        registro["cantidad"] = cantidad
        registro["ultima_actualizacion"] = fecha

    guardar_stock(registros)
    return fecha


# Crea ventas.csv y sub_venta.csv con sus encabezados si no existen.
def crear_archivos_si_no_existen():
    if not os.path.exists(ARCHIVO_VENTAS) or os.path.getsize(ARCHIVO_VENTAS) == 0:
        with open(ARCHIVO_VENTAS, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(COLUMNAS_VENTAS)

    if not os.path.exists(ARCHIVO_SUB_VENTAS) or os.path.getsize(ARCHIVO_SUB_VENTAS) == 0:
        with open(ARCHIVO_SUB_VENTAS, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(COLUMNAS_SUB_VENTAS)


# Devuelve una lista con todas las ventas de ventas.csv.
def leer_ventas():
    crear_archivos_si_no_existen()
    ventas = []

    with open(ARCHIVO_VENTAS, "r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for venta in lector:
            ventas.append(venta)

    return ventas


# Devuelve una lista con todo el detalle de sub_venta.csv.
def leer_sub_ventas():
    crear_archivos_si_no_existen()
    sub_ventas = []

    with open(ARCHIVO_SUB_VENTAS, "r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for sub_venta in lector:
            sub_ventas.append(sub_venta)

    return sub_ventas


# Calcula el proximo numero de venta.
def nuevo_numero_venta():
    ventas = leer_ventas()
    mayor = 0

    for venta in ventas:
        numero = int(venta["numero_venta"])
        if numero > mayor:
            mayor = numero

    return mayor + 1


# Agrega una fila a ventas.csv.
def agregar_venta(numero_venta, fecha, total):
    crear_archivos_si_no_existen()

    with open(ARCHIVO_VENTAS, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([numero_venta, fecha, f"{total:.2f}"])


# Agrega una fila a sub_venta.csv.
def agregar_sub_venta(numero_venta, codigo, nombre, cantidad, precio_unitario, subtotal):
    crear_archivos_si_no_existen()

    with open(ARCHIVO_SUB_VENTAS, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([
            numero_venta,
            codigo,
            nombre,
            cantidad,
            f"{float(precio_unitario):.2f}",
            f"{float(subtotal):.2f}",
        ])


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


# Pide una cantidad entera mayor a cero para el carrito.
def pedir_cantidad_carrito():
    while True:
        try:
            cantidad = int(input("Ingresar la cantidad: "))
            if cantidad > 0:
                return cantidad
            print("La cantidad debe ser mayor a cero.")
        except ValueError:
            print("Se esperaba un número entero.")


# Pide una cantidad entera mayor o igual a cero para el stock real.
def pedir_cantidad_stock():
    while True:
        try:
            cantidad = int(input("Ingresar la cantidad real en stock: "))
            if cantidad >= 0:
                return cantidad
            print("La cantidad no puede ser negativa.")
        except ValueError:
            print("Se esperaba un número entero.")


# Pregunta con 1 o 2 y devuelve True si la respuesta es 1 (Si).
def confirmar(mensaje):
    print(mensaje)
    print("1. Si")
    print("2. No")
    opcion = pedir_opcion(1, 2)

    return opcion == 1
