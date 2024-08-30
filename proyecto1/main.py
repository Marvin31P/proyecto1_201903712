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