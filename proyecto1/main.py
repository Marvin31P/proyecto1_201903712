
# Clase NodoMatriz para los elementos de la matriz
class NodoMatriz:
    def __init__(self, valor=None):
        self.valor = valor
        self.siguiente = None  # Apunta al siguiente nodo en la fila
        self.abajo = None      # Apunta al siguiente nodo en la columna

# Clase Nodo para la lista circular de matrices
class Nodo:
    def __init__(self, nombre=None, filas=0, columnas=0):
        self.nombre = nombre
        self.filas = filas
        self.columnas = columnas
        self.datos = None
        self.siguiente = None

# Clase Matriz usando nodos enlazados
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


def mostrar_menu():
    print("Menú principal:")
    print("1. Cargar archivo")
    print("2. Procesar archivo")
    print("3. Escribir archivo salida")
    print("4. Mostrar datos del estudiante")
    print("5. Generar gráfica")
    print("6. Salida")

def main():
    


    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            ruta = input("Ingrese la ruta del archivo XML: ")
            
        elif opcion == "2":
            print("")
        elif opcion == "3":
           print(" ")
        elif opcion == "4":
            print("Datos del estudiante: ")
            print("Carné: 201903712")
            print("Nombre: Marvin Pérez")
            print("Curso: introduccion a la programacion y computacion 2")
            print("Carrera: Ingeniería en Sistemas")
            print("Semestre: 4to")
            
        elif opcion == "5":
            print("Función de generar gráfica pendiente de implementación.")
        elif opcion == "6":
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()          