from productos import menu_productos
from stock import menu_stock
from venta import menu_ventas
from reporte import menu_reporte


def opciones():
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
        menu_productos()
    case 2:
        menu_stock()
    case 3:
        menu_ventas()
    case 4:
        menu_reporte()
    case 5:
        print("hasta luego")
