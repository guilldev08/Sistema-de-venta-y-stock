import os

from venta import leer_ventas, leer_sub_ventas

# Los reportes no tienen archivos propios:
# leen ventas.csv y sub_venta.csv a traves de venta.py.


# Muestra el menu de reportes.
def menu_reporte():
    limpiar_pantalla()

    while True:
        print(r"""
            1. Consultar ventas realizadas
            2. Consultar ganancias
            3. Consultar productos vendidos
            4. Atras
        """, flush=True)

        opcion = pedir_opcion(1, 4)

        if opcion == 1:
            menu_ventas_realizadas()
        elif opcion == 2:
            menu_ganancias()
        elif opcion == 3:
            menu_productos_vendidos()
        else:
            break


# Submenu para consultar las ventas realizadas.
def menu_ventas_realizadas():
    while True:
        print(r"""
            1. Por día
            2. Por mes
            3. Por año
            4. Buscar detalles de una venta
            5. Atras
        """, flush=True)

        opcion = pedir_opcion(1, 5)

        if opcion == 1:
            reporte_ventas("dia")
        elif opcion == 2:
            reporte_ventas("mes")
        elif opcion == 3:
            reporte_ventas("ano")
        elif opcion == 4:
            detalles_venta()
        else:
            break


# Submenu para consultar las ganancias.
def menu_ganancias():
    while True:
        print(r"""
            1. Por día
            2. Por mes
            3. Por año
            4. Atras
        """, flush=True)

        opcion = pedir_opcion(1, 4)

        if opcion == 1:
            reporte_ganancias("dia")
        elif opcion == 2:
            reporte_ganancias("mes")
        elif opcion == 3:
            reporte_ganancias("ano")
        else:
            break


# Submenu para consultar los productos vendidos.
def menu_productos_vendidos():
    while True:
        print(r"""
            1. Ordenar por mayor ventas
            2. Ordenar por nombre
            3. Atras
        """, flush=True)

        opcion = pedir_opcion(1, 3)

        if opcion == 1:
            reporte_productos_vendidos(1)
        elif opcion == 2:
            reporte_productos_vendidos(2)
        else:
            break


# Muestra la cantidad de ventas y el total recaudado por dia, mes o año.
def reporte_ventas(tipo):
    resumen = agrupar_ventas(tipo)

    if not resumen:
        print("No hay ventas registradas.")
        return

    print(f"\n--- VENTAS POR {nombre_periodo(tipo)} ---")
    print("-" * 52)
    print(f"{'PERIODO':<14} {'VENTAS':>10} {'TOTAL ($)':>16}")
    print("-" * 52)

    total_ventas = 0
    total_recaudado = 0.0

    for clave in sorted(resumen.keys()):
        grupo = resumen[clave]
        print(f"{grupo['texto']:<14} {grupo['cantidad']:>10} {grupo['total']:>16.2f}")
        total_ventas = total_ventas + grupo["cantidad"]
        total_recaudado = total_recaudado + grupo["total"]

    print("-" * 52)
    print(f"TOTAL DE VENTAS: {total_ventas}")
    print(f"TOTAL RECAUDADO: ${total_recaudado:.2f}")


# Muestra el total vendido por dia, mes o año.
def reporte_ganancias(tipo):
    resumen = agrupar_ventas(tipo)

    if not resumen:
        print("No hay ganancias registradas.")
        return

    print(f"\n--- GANANCIAS POR {nombre_periodo(tipo)} ---")
    print("-" * 44)
    print(f"{'PERIODO':<14} {'TOTAL ($)':>16}")
    print("-" * 44)

    total_general = 0.0

    for clave in sorted(resumen.keys()):
        grupo = resumen[clave]
        print(f"{grupo['texto']:<14} {grupo['total']:>16.2f}")
        total_general = total_general + grupo["total"]

    print("-" * 44)
    print(f"TOTAL GENERAL: ${total_general:.2f}")


# Junta las ventas de ventas.csv por dia, mes o año.
def agrupar_ventas(tipo):
    ventas = leer_ventas()
    resumen = {}

    for venta in ventas:
        clave, texto = obtener_periodo(venta["fecha"], tipo)

        if clave not in resumen:
            resumen[clave] = {
                "texto": texto,
                "cantidad": 0,
                "total": 0.0,
            }

        resumen[clave]["cantidad"] = resumen[clave]["cantidad"] + 1
        resumen[clave]["total"] = resumen[clave]["total"] + float(venta["total"])

    return resumen


# Devuelve una clave para ordenar y un texto para mostrar.
def obtener_periodo(fecha, tipo):
    # fecha tiene el formato "20/11/2026 16:39".
    fecha_sola = fecha.split(" ")[0]
    partes = fecha_sola.split("/")

    dia = partes[0]
    mes = partes[1]
    ano = partes[2]

    if tipo == "dia":
        return f"{ano}/{mes}/{dia}", f"{dia}/{mes}/{ano}"
    elif tipo == "mes":
        return f"{ano}/{mes}", f"{mes}/{ano}"
    else:
        return ano, ano


# Devuelve el nombre del periodo para los titulos.
def nombre_periodo(tipo):
    if tipo == "dia":
        return "DIA"
    elif tipo == "mes":
        return "MES"
    else:
        return "AÑO"


# Muestra el detalle de una venta elegida por su numero.
def detalles_venta():
    ventas = leer_ventas()

    if not ventas:
        print("No hay ventas registradas.")
        return

    print("\n--- VENTAS REGISTRADAS ---")
    print("-" * 52)
    print(f"{'N° VENTA':<10} {'FECHA':<20} {'TOTAL ($)':>14}")
    print("-" * 52)

    for venta in ventas:
        print(
            f"{venta['numero_venta']:<10} "
            f"{venta['fecha']:<20} "
            f"{float(venta['total']):>14.2f}"
        )

    print("-" * 52)

    while True:
        print("Ingrese el número de venta (Enter para volver)")
        respuesta = input().strip()

        if respuesta == "":
            return

        try:
            numero = int(respuesta)
        except ValueError:
            print("Se esperaba un número entero.")
            continue

        venta_encontrada = None
        for venta in ventas:
            if int(venta["numero_venta"]) == numero:
                venta_encontrada = venta
                break

        if venta_encontrada is not None:
            break

        print("No existe una venta con ese número.")

    mostrar_detalle_venta(venta_encontrada)


# Muestra la cabecera y los productos de una venta.
def mostrar_detalle_venta(venta):
    detalles = leer_sub_ventas()

    print(f"\n===== VENTA N° {venta['numero_venta']} =====")
    print(f"Fecha: {venta['fecha']}")
    print(f"Total: ${float(venta['total']):.2f}")
    print("-" * 78)
    print(
        f"{'CODIGO':<10} {'NOMBRE':<22} {'CANTIDAD':>10} "
        f"{'PRECIO':>12} {'SUBTOTAL':>12}"
    )
    print("-" * 78)

    for detalle in detalles:
        if detalle["numero_venta"] == venta["numero_venta"]:
            print(
                f"{detalle['codigo']:<10} "
                f"{detalle['nombre']:<22} "
                f"{detalle['cantidad']:>10} "
                f"{float(detalle['precio_unitario']):>12.2f} "
                f"{float(detalle['subtotal']):>12.2f}"
            )

    print("-" * 78)


# Muestra los productos vendidos ordenados por cantidad o por nombre.
def reporte_productos_vendidos(orden):
    resumen = agrupar_productos()

    if not resumen:
        print("No hay productos vendidos.")
        return

    productos = list(resumen.values())

    if orden == 1:
        productos.sort(key=obtener_cantidad_vendida, reverse=True)
        titulo = "PRODUCTOS ORDENADOS POR MAYOR VENTA"
    else:
        productos.sort(key=obtener_nombre_producto)
        titulo = "PRODUCTOS ORDENADOS POR NOMBRE"

    print(f"\n--- {titulo} ---")
    print("-" * 70)
    print(
        f"{'CODIGO':<10} {'NOMBRE':<24} {'CANTIDAD':>10} {'TOTAL ($)':>14}"
    )
    print("-" * 70)

    total_unidades = 0
    total_recaudado = 0.0

    for producto in productos:
        print(
            f"{producto['codigo']:<10} "
            f"{producto['nombre']:<24} "
            f"{producto['cantidad']:>10} "
            f"{producto['total']:>14.2f}"
        )
        total_unidades = total_unidades + producto["cantidad"]
        total_recaudado = total_recaudado + producto["total"]

    print("-" * 70)
    print(f"TOTAL DE UNIDADES VENDIDAS: {total_unidades}")
    print(f"TOTAL RECAUDADO: ${total_recaudado:.2f}")


# Junta el detalle de sub_venta.csv por codigo de producto.
def agrupar_productos():
    detalles = leer_sub_ventas()
    resumen = {}

    for detalle in detalles:
        codigo = detalle["codigo"]

        if codigo not in resumen:
            resumen[codigo] = {
                "codigo": codigo,
                "nombre": detalle["nombre"],
                "cantidad": 0,
                "total": 0.0,
            }

        resumen[codigo]["cantidad"] = resumen[codigo]["cantidad"] + int(detalle["cantidad"])
        resumen[codigo]["total"] = resumen[codigo]["total"] + float(detalle["subtotal"])

    return resumen


# Devuelve la cantidad vendida de un producto para ordenar.
def obtener_cantidad_vendida(producto):
    return producto["cantidad"]


# Devuelve el nombre en minusculas para ordenar alfabeticamente.
def obtener_nombre_producto(producto):
    return producto["nombre"].lower()


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
