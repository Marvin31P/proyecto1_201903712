import xml.etree.ElementTree as ET
import graphviz


class NodoMatriz:
    def __init__(self, valor=None):
        self.valor = valor
        self.siguiente = None  
        self.abajo = None      


class Nodo:
    def __init__(self, nombre=None, filas=0, columnas=0):
        self.nombre = nombre
        self.filas = filas
        self.columnas = columnas
        self.datos = None
        self.siguiente = None


class Matriz:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.primera_fila = None
        self.crear_matriz()

    def crear_matriz(self):
        fila_anterior = None
        for i in range(self.filas):
            nodo_anterior = None
            for j in range(self.columnas):
                nuevo_nodo = NodoMatriz()

                if j == 0:
                    if i == 0:
                        self.primera_fila = nuevo_nodo
                    else:
                        fila_anterior.abajo = nuevo_nodo
                else:
                    nodo_anterior.siguiente = nuevo_nodo

                if i != 0:
                    nodo_arriba = self.obtener_nodo(i-1, j)
                    nodo_arriba.abajo = nuevo_nodo

                nodo_anterior = nuevo_nodo

            fila_anterior = self.obtener_nodo(i, 0)

    def obtener_nodo(self, fila_idx, col_idx):
        if fila_idx < 0 or fila_idx >= self.filas or col_idx < 0 or col_idx >= self.columnas:
            raise IndexError("Fila o columna fuera de rango")

        fila_actual = self.primera_fila
        for _ in range(fila_idx):
            fila_actual = fila_actual.abajo

        nodo_actual = fila_actual
        for _ in range(col_idx):
            nodo_actual = nodo_actual.siguiente

        return nodo_actual

    def set_dato(self, x, y, valor):
        if 1 <= x <= self.filas and 1 <= y <= self.columnas:
            nodo = self.obtener_nodo(x-1, y-1)
            nodo.valor = valor
        else:
            raise IndexError("Coordenadas fuera de rango")

    def get_dato(self, x, y):
        if 1 <= x <= self.filas and 1 <= y <= self.columnas:
            nodo = self.obtener_nodo(x-1, y-1)
            return nodo.valor
        return None
class ListaCircular:
    def __init__(self):
        self.primero = None

    def agregar_matriz(self, nombre, filas, columnas):
        nuevo_nodo = Nodo(nombre, filas, columnas)
        nuevo_nodo.datos = Matriz(filas, columnas)

        if self.primero is None:
            self.primero = nuevo_nodo
            self.primero.siguiente = self.primero
        else:
            actual = self.primero
            while actual.siguiente != self.primero:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
            nuevo_nodo.siguiente = self.primero

    def buscar_matriz(self, nombre):
        if self.primero is None:
            return None
        actual = self.primero
        while True:
            if actual.nombre == nombre:
                return actual
            actual = actual.siguiente
            if actual == self.primero:
                break
        return None

    def procesar_matriz(self, matriz):
        patrones = []
        frecuencias = []

        for i in range(matriz.filas):
            patron = ""
            for j in range(matriz.columnas):
                valor = matriz.get_dato(i+1, j+1)
                patron += '1' if valor > 0 else '0'

            encontrado = False
            for idx in range(len(patrones)):
                if patrones[idx] == patron:
                    frecuencias[idx] += 1
                    grupo = idx + 1
                    encontrado = True
                    break

            if not encontrado:
                patrones.append(patron)
                frecuencias.append(1)
                grupo = len(patrones)

            if len(frecuencias) < grupo:
                frecuencias.append(0)

            for j in range(matriz.columnas):
                if matriz.get_dato(grupo, j+1) is None:
                    matriz.set_dato(grupo, j+1, 0)
                matriz.set_dato(grupo, j+1, matriz.get_dato(grupo, j+1) + matriz.get_dato(i+1, j+1))

        nueva_matriz = Matriz(matriz.filas, matriz.columnas)
        for i in range(matriz.filas):
            for j in range(matriz.columnas):
                nueva_matriz.set_dato(i+1, j+1, matriz.get_dato(i+1, j+1))

        return nueva_matriz, frecuencias

    def generar_grafica(self, nombre):
        matriz_nodo = self.buscar_matriz(nombre)
        if not matriz_nodo:
            print("Matriz no encontrada.")
            return
        
        dot = graphviz.Digraph(comment=matriz_nodo.nombre)
        dot.node('A', f'Matriz {matriz_nodo.nombre}\n{matriz_nodo.filas}x{matriz_nodo.columnas}')
        
        for i in range(matriz_nodo.filas):
            for j in range(matriz_nodo.columnas):
                valor = matriz_nodo.datos.get_dato(i+1, j+1)
                dot.node(f'{i}{j}', str(valor))
                dot.edge('A', f'{i}{j}')
        
        dot.render(f'{matriz_nodo.nombre}.gv', view=True)


def generar_grafica_matriz(nombre, matriz, n, m):
    dot = graphviz.Digraph(comment=nombre)
    dot.node('A', f'Matriz {nombre}\n{n}x{m}')

    for i in range(n):
        for j in range(m):
            valor = matriz.get_dato(i+1, j+1)
            dot.node(f'{i}{j}', str(valor))
            dot.edge('A', f'{i}{j}')
    
    dot.render(f'{nombre}_reducida.gv', view=True)


def cargar_archivo(ruta, lista):
    try:
        tree = ET.parse(ruta)
        root = tree.getroot()

        for matriz_xml in root.findall('matriz'):
            nombre = matriz_xml.get('nombre')
            n = int(matriz_xml.get('n'))
            m = int(matriz_xml.get('m'))

            lista.agregar_matriz(nombre, n, m)
            nodo_matriz = lista.buscar_matriz(nombre)

            for dato in matriz_xml.findall('dato'):
                x = int(dato.get('x'))
                y = int(dato.get('y'))
                valor = int(dato.text)
                nodo_matriz.datos.set_dato(x, y, valor)

    except ET.ParseError:
        print("Error al parsear el archivo XML.")
    except FileNotFoundError:
        print(f"El archivo {ruta} no fue encontrado.")
    except Exception as e:
        print(f"Se produjo un error: {e}")

def escribir_archivo_salida(nombre, nueva_matriz, frecuencias):
    root = ET.Element("matrices")
    matriz_xml = ET.SubElement(root, "matriz", nombre=f"{nombre}_Salida", n=str(nueva_matriz.filas), m=str(nueva_matriz.columnas), g=str(len(frecuencias)))

    for i in range(nueva_matriz.filas):
        for j in range(nueva_matriz.columnas):
            valor = nueva_matriz.get_dato(i+1, j+1)
            ET.SubElement(matriz_xml, "dato", x=str(i+1), y=str(j+1)).text = str(valor)

    for i, frecuencia in enumerate(frecuencias):
        ET.SubElement(matriz_xml, "frecuencia", g=str(i+1)).text = str(frecuencia)

    tree = ET.ElementTree(root)
    tree.write(f"{nombre}_Salida.xml")



def mostrar_menu():
    print("Menú principal:")
    print("1. Cargar archivo")
    print("2. Procesar archivo")
    print("3. Escribir archivo salida")
    print("4. Mostrar datos del estudiante")
    print("5. Generar gráfica")
    print("6. Salida")

def main():
    
    lista = ListaCircular()
    nueva_matriz = None
    frecuencias = []

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            ruta = input("Ingrese la ruta del archivo XML: ")
            cargar_archivo(ruta, lista)
        elif opcion == "2":
            nombre = input("Ingrese el nombre de la matriz a procesar: ")
            nodo_matriz = lista.buscar_matriz(nombre)
            if nodo_matriz:
                nueva_matriz, frecuencias = lista.procesar_matriz(nodo_matriz.datos)
            else:
                print("Matriz no encontrada.")
        elif opcion == "3":
            if nueva_matriz:
                nombre = input("Ingrese el nombre para el archivo de salida: ")
                escribir_archivo_salida(nombre, nueva_matriz, frecuencias)
            else:
                print("No hay una matriz procesada.")
        elif opcion == "4":
            print("Datos del estudiante: ")
            print("Carné: 201903712")
            print("Nombre: Marvin Pérez")
            print("Curso: introduccion a la programacion y computacion 2")
            print("Carrera: Ingeniería en Sistemas")
            print("Semestre: 4to")
            
        elif opcion == "5":

            nombre = input("Ingrese el nombre de la matriz a graficar: ")
            lista.generar_grafica(nombre)
            
        elif opcion == "6":
            break
        else:
            print("Opción no válida. Intente de nuevo.")
if __name__ == "__main__":
    main()          