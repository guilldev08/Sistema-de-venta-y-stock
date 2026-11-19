import csv
import os

ARCHIVO = "productos.csv"
COLUMNAS = ["codigo", "nombre", "tipo", "marca", "precio"]


def menu_productos():
    print("""
        1. Registrar producto
        2. Buscar productos
        3. Atras
    """, flush=True)


def crear_archivo_si_no_existe():
    # Si el archivo no existe o esta vacio, se crea con el nombre de las columnas.
    if not os.path.exists(ARCHIVO) or os.path.getsize(ARCHIVO) == 0:
        with open(ARCHIVO, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(COLUMNAS)


def leer_productos():
    # Devuelve una lista de diccionarios, por ejemplo:
    # {"codigo": "P001", "nombre": "Leche entera 1L", "tipo": "Lacteos", ...}
    crear_archivo_si_no_existe()
    productos = []

    with open(ARCHIVO, "r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for producto in lector:
            productos.append(producto)

    return productos


def guardar_productos(productos):
    # Se usa para reescribir el archivo completo (editar o eliminar).
    with open(ARCHIVO, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
        escritor.writeheader()
        escritor.writerows(productos)


def imprimir_tabla(productos):
    print("-" * 82)
    print(f"{'CODIGO':<10} {'NOMBRE':<22} {'TIPO':<20} {'MARCA':<15} {'PRECIO':>10}")
    print("-" * 82)

    for producto in productos:
        print(
            f"{producto['codigo']:<10} "
            f"{producto['nombre']:<22} "
            f"{producto['tipo']:<20} "
            f"{producto['marca']:<15} "
            f"{producto['precio']:>10}"
        )

    print("-" * 82)


def existe_codigo(codigo):
    for producto in leer_productos():
        if producto["codigo"].lower() == codigo.lower():
            return True

    return False


def buscar_por_codigo(codigo):
    for producto in leer_productos():
        if producto["codigo"].lower() == codigo.lower():
            return producto

    return None


def registrar_producto(codigo, nombre, tipo, marca, precio):
    codigo = codigo.strip()
    nombre = nombre.strip()
    tipo = tipo.strip()
    marca = marca.strip()

    if codigo == "" or nombre == "":
        print("El codigo y el nombre no pueden estar vacios.")
        return False

    if existe_codigo(codigo):
        print("Ya existe un producto con ese codigo.")
        return False

    # Si el precio es entero se guarda sin decimales (1450 en vez de 1450.0).
    precio = float(precio)
    if precio % 1 == 0:
        precio = int(precio)

    with open(ARCHIVO, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([codigo, nombre, tipo, marca, precio])

    return True


def listar_productos():
    productos = leer_productos()

    if not productos:
        print("No hay productos registrados.")
        return

    imprimir_tabla(productos)


def mostrar_marcas():
    marcas = set()

    for producto in leer_productos():
        if producto["marca"].strip() != "":
            marcas.add(producto["marca"])

    marcas_ordenadas = sorted(marcas)

    print("\n--- MARCAS DISPONIBLES ---")

    if not marcas_ordenadas:
        print("No hay marcas para mostrar.")
        return []

    for i in range(len(marcas_ordenadas)):
        print(f"{i + 1}. {marcas_ordenadas[i]}")

    # Devuelve la lista para que menu.py pueda buscar la marca elegida.
    return marcas_ordenadas


def filtrar_por_marca(marca_busqueda):
    encontrados = []

    for producto in leer_productos():
        if producto["marca"].lower() == marca_busqueda.lower():
            encontrados.append(producto)

    if encontrados:
        imprimir_tabla(encontrados)
    else:
        print("No se encontraron productos de esa marca.")


def filtrar_por_tipo(tipo_busqueda):
    tipo_busqueda = tipo_busqueda.strip()

    if tipo_busqueda == "":
        print("Debe ingresar un tipo para buscar.")
        return

    encontrados = []

    for producto in leer_productos():
        # "in" permite buscar una parte del tipo, por ejemplo "bebida".
        if tipo_busqueda.lower() in producto["tipo"].lower():
            encontrados.append(producto)

    if encontrados:
        imprimir_tabla(encontrados)
    else:
        print("No se encontraron productos de ese tipo.")


def filtrar_por_precio(opcion):
    productos = leer_productos()

    if not productos:
        print("No hay productos registrados.")
        return

    elegido = productos[0]

    for producto in productos:
        if opcion == 1:
            # Opcion 1: precio mas bajo.
            if float(producto["precio"]) < float(elegido["precio"]):
                elegido = producto
        else:
            # Opcion 2: precio mas alto.
            if float(producto["precio"]) > float(elegido["precio"]):
                elegido = producto

    if opcion == 1:
        print("\nProducto de menor precio:")
    else:
        print("\nProducto de mayor precio:")

    imprimir_tabla([elegido])


def pedir_numero(mensaje, minimo, maximo):
    while True:
        try:
            numero = int(input(mensaje))
            if minimo <= numero <= maximo:
                return numero
            print(f"Se esperaba un numero del {minimo} al {maximo}.")
        except ValueError:
            print("Se esperaba un numero entero.")


def pedir_precio():
    while True:
        try:
            precio = float(input("Ingresar el nuevo precio: "))
            if precio <= 0:
                print("El precio debe ser mayor a cero.")
                continue
            return precio
        except ValueError:
            print("Se esperaba un precio numerico.")


def editar_producto(codigo):
    productos = leer_productos()
    producto = None

    for p in productos:
        if p["codigo"].lower() == codigo.lower():
            producto = p
            break

    if producto is None:
        print("No existe un producto con ese codigo.")
        return None

    while True:
        print(f"""
            Producto: {producto['codigo']} - {producto['nombre']}
            1. Editar codigo
            2. Editar nombre
            3. Editar tipo
            4. Editar marca
            5. Editar precio
            6. Atras
        """)

        opcion = pedir_numero("Ingrese un numero: ", 1, 6)

        if opcion == 6:
            break

        if opcion == 1:
            print("Ingresar nuevo codigo")
            nuevo_codigo = input().strip()

            if nuevo_codigo == "":
                print("El codigo no puede estar vacio.")
                continue

            # No se permite usar el codigo de otro producto.
            if nuevo_codigo.lower() != producto["codigo"].lower() and existe_codigo(nuevo_codigo):
                print("Ya existe otro producto con ese codigo.")
                continue

            producto["codigo"] = nuevo_codigo

        elif opcion == 2:
            print("Ingresar nuevo nombre")
            nuevo_nombre = input().strip()

            if nuevo_nombre == "":
                print("El nombre no puede estar vacio.")
                continue

            producto["nombre"] = nuevo_nombre

        elif opcion == 3:
            print("Ingresar nuevo tipo o pasillo")
            producto["tipo"] = input().strip()

        elif opcion == 4:
            print("Ingresar nueva marca")
            producto["marca"] = input().strip()

        elif opcion == 5:
            precio = pedir_precio()

            # Si el precio es entero se guarda sin decimales.
            if precio % 1 == 0:
                precio = int(precio)

            producto["precio"] = precio

        # Cada cambio se guarda en el archivo.
        guardar_productos(productos)
        print("Producto actualizado.")

    return producto


def eliminar_producto(codigo):
    productos = leer_productos()
    productos_restantes = []
    eliminado = False

    for producto in productos:
        if producto["codigo"].lower() == codigo.lower():
            eliminado = True
        else:
            productos_restantes.append(producto)

    if not eliminado:
        print("No existe un producto con ese codigo.")
        return False

    guardar_productos(productos_restantes)
    print("Producto eliminado.")
    return True


def seleccionar_producto():
    if not leer_productos():
        print("No hay productos registrados.")
        return

    # Se pide el codigo hasta que exista o hasta que el usuario presione Enter.
    while True:
        print("Ingrese el codigo del producto (Enter para volver)")
        codigo = input().strip()

        if codigo == "":
            return

        producto = buscar_por_codigo(codigo)

        if producto is not None:
            break

        print("No existe un producto con ese codigo.")

    imprimir_tabla([producto])

    while True:
        print("""
            1. Editar
            2. Eliminar
            3. Atras
        """)

        opcion = pedir_numero("Ingrese un numero: ", 1, 3)

        if opcion == 1:
            producto = editar_producto(producto["codigo"])

            if producto is None:
                return

            imprimir_tabla([producto])

        elif opcion == 2:
            print("Seguro que desea eliminar el producto? (s/n)")
            confirmacion = input().strip().lower()

            while confirmacion != "s" and confirmacion != "n":
                print("Ingrese s o n")
                confirmacion = input().strip().lower()

            if confirmacion == "s":
                eliminar_producto(producto["codigo"])
                return

        else:
            return
