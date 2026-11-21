from productos import registrar_producto
from productos import listar_productos
from productos import mostrar_marcas
from productos import filtrar_por_marca
from productos import filtrar_por_tipo
from productos import filtrar_por_precio
from productos import seleccionar_producto
from stock import menu_stock
from venta import menu_ventas
from reporte import menu_reporte


def opciones(): #Se usa para cargar el menu
    print(r"""
        1. producto
        2. stock
        3. ventas
        4. reporte
        5. salir
    """)


print("""
+----------------------------------+
|           BIENVENIDO             |
+----------------------------------+
""")

while True:
    opciones()

    while True:
        try:
            respuesta = int(input("Ingrese un número: "))
            if 1 <= respuesta <= 5:
                break
            print("Se esperaba un número del 1 al 5.")
        except ValueError:
            print("Se esperaba un número entero.")

    match respuesta:
        case 1:
            while True:
                print(r"""
                    1. Registrar producto
                    2. Buscar productos
                    3. Atras
                """)

                while True:
                    try:
                        respuesta = int(input("Ingrese un número: "))
                        if respuesta in (1, 2, 3):
                            break
                        print("Se esperaba un número del 1 al 3.")
                    except ValueError:
                        print("Se esperaba un número entero.")

                if respuesta == 1:
                    while True:
                        print("Registrar codigo")
                        codigo = input()

                        print("Ingresar nombre del producto")
                        nombre = input()

                        print("Ingresar tipo o pasillo del producto")
                        tipo = input()

                        print("Ingresar marca del producto")
                        marca = input()

                        while True:
                            try:
                                print("Ingresar el precio del producto")
                                precio = float(input())
                                if precio > 0:
                                    break
                                print("El precio debe ser mayor a cero.")
                            except ValueError:
                                print("Se esperaba un precio numérico.")

                        if registrar_producto(codigo, nombre, tipo, marca, precio):
                            print("Producto registrado.")
                        print("1. Registrar otro")
                        print("2. Atras")

                        while True:
                            try:
                                respuesta = int(input())
                                if respuesta in (1, 2):
                                    break
                                print("Se esperaba un 1 o un 2.")
                            except ValueError:
                                print("Se esperaba un número entero.")

                        if respuesta == 2:
                            break

                elif respuesta == 2:
                    while True:
                        listar_productos()
                        print(r"""
                            1. Filtrar por marca
                            2. Filtrar por tipo
                            3. Filtrar por precio
                            4. Atras
                            5. Seleccionar producto
                        """)

                        while True:
                            try:
                                respuesta = int(input("Ingrese un número: "))
                                if respuesta in (1, 2, 3, 4, 5):
                                    break
                                print("Se esperaba un número del 1 al 5.")
                            except ValueError:
                                print("Se esperaba un número entero.")

                        if respuesta == 1:
                            marcas = mostrar_marcas()
                            if marcas:
                                while True:
                                    try:
                                        print("Elegir el número de la marca")
                                        opcion_marca = int(input())
                                        if 1 <= opcion_marca <= len(marcas):
                                            break
                                        print("El número no corresponde a una marca.")
                                    except ValueError:
                                        print("Se esperaba un número entero.")

                                marca = marcas[opcion_marca - 1]
                                filtrar_por_marca(marca)
                            else:
                                print("No hay marcas para mostrar.")
                        elif respuesta == 2:
                            print("Ingresar tipo buscar")
                            tipo = input()
                            filtrar_por_tipo(tipo)
                        elif respuesta == 3:
                            print("""
                                1. Precio más bajo
                                2. Precio más alto
                                3. Atras
                            """)
                            while True:
                                try:
                                    opcion_precio = int(input("Ingrese un número: "))
                                    if opcion_precio in (1, 2, 3):
                                        break
                                    print("Se esperaba un número del 1 al 3.")
                                except ValueError:
                                    print("Se esperaba un número entero.")
                            if opcion_precio in (1, 2):
                                filtrar_por_precio(opcion_precio)
                        elif respuesta == 4:
                            break
                        elif respuesta == 5:
                            seleccionar_producto()

                else:
                    break

        case 2:
            # La tabla, el menu y la actualizacion del stock estan en stock.py
            menu_stock()
        case 3:
            # El carrito, el stock y las ventas se manejan en venta.py
            menu_ventas()
        case 4:
            menu_reporte()
        case 5:
            print("Hasta luego")
            break
