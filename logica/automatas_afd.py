#Ejercicio1
def transaciones_bancarias(cadena):
   Alfabeto = ["A", "L", "C", "E"]
   estado_inicial = "q0"
   estado_final = "q3"
   estado_siguiente = estado_inicial
   cadena_aceptada = False

   if not all(letra in Alfabeto for letra in cadena):
        print("La cadena contiene símbolos no válidos. Solo se permiten 'A', 'L', 'C' y 'E'.")
        return False

   for letra in cadena:
    if estado_siguiente == "q0" and letra == "A" :
       estado_siguiente = "q1"
       print(f"Pasando de estado {estado_inicial} a {estado_siguiente} con entrada '{letra}'")
    elif estado_siguiente == "q0" and (letra == "L" or letra == "C" or letra == "E") :
      estado_siguiente = "qe"
      print(f"Pasando de estado {estado_inicial} a {estado_siguiente} con entrada '{letra}'")

    if estado_siguiente == "q1":
        if letra == "C":
            estado_siguiente = "q2"
            print(f"Pasando de estado {estado_inicial} a {estado_siguiente} con entrada '{letra}'")
        elif letra == "L" or letra == "E":
            estado_siguiente = "qe"
            print(f"Pasando de estado {estado_inicial} a {estado_siguiente} con entrada '{letra}'")
        elif letra == "A":
            estado_siguiente = "q1"
            print(f"Pasando de estado {estado_inicial} a {estado_siguiente} con entrada '{letra}'")

    if estado_siguiente == "q2":
        if letra == "L":
            estado_siguiente = "q3"
            print(f"Pasando de estado {estado_inicial} a {estado_siguiente} con entrada '{letra}'")
        elif  letra == "E" or letra == "A":
            estado_siguiente = "qe"
            print(f"Pasando de estado {estado_inicial} a {estado_siguiente} con entrada '{letra}'")
        elif letra == "C":
            estado_siguiente = "q2"
            print(f"Pasando de estado {estado_inicial} a {estado_siguiente} con entrada '{letra}'")

    
    if estado_siguiente == estado_final:       
        cadena_aceptada = True
    
   return cadena_aceptada



#Ejercicio2

def cerradura(cadena):
   Alfabeto = ["V", "F"]
   estado_inicial = "q0"
   estado_final = "q4"
   estado_siguiente = estado_inicial
   cadena_aceptada = False

   if not all(letra in Alfabeto for letra in cadena):
      print("La cadena contiene símbolos no válidos. Solo se permiten 'V' y 'F'.")
      return False

   for letra in cadena:
     if estado_siguiente == "q0" and letra == "V":
        estado_siguiente = "q4"
        print(f"Pasando de estado {estado_inicial} a {estado_siguiente} con entrada '{letra}'" , "Cerradura abierta")
        cadena_aceptada = True
        
     elif estado_siguiente == "q0" and letra == "F":
        estado_siguiente = "q1"
        print(f"Pasando de estado {estado_inicial} a {estado_siguiente} con entrada '{letra}'" , "Primer intento fallido")

     if estado_siguiente == "q1":
        if letra == "V":
            estado_siguiente = "q4"
            print(f"Pasando de estado {estado_inicial} a {estado_siguiente} con entrada '{letra}'" , "Cerradura abierta")
            cadena_aceptada = True

        elif letra == "F":
            estado_siguiente = "q2"
            print(f"Pasando de estado {estado_inicial} a {estado_siguiente} con entrada '{letra}'" , "Segundo intento fallido, el siguiente es el último intento")

        if estado_siguiente == "q2":
            if letra == "V":
                estado_siguiente = "q4"
                print(f"Pasando de estado {estado_inicial} a {estado_siguiente} con entrada '{letra}'" , "Cerradura abierta")
                cadena_aceptada = True

            elif letra == "F":
                estado_siguiente = "q3"
                print(f"Pasando de estado {estado_inicial} a {estado_siguiente} con entrada '{letra}'" , "Tercer intento fallido, cerradura bloqueada")
   return cadena_aceptada







#Ejercicio3

def analizador_notacion_cientifica(cadena):
    # Definición clásica del alfabeto de dígitos
    digitos = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    estado_actual = "q0"
    estado_final = "q4"
    
    for simbolo in cadena:
        estado_anterior = estado_actual
        
        # 1. Transiciones desde q0 (Estado Inicial)
        if estado_actual == "q0":
            if simbolo in ["+", "-"]:
                estado_actual = "q1"
            elif simbolo == ".":
                estado_actual = "q2"
            else: return False

        # 2. Transiciones desde q1 (Signo leído)
        elif estado_actual == "q1":
            if simbolo == ".":
                estado_actual = "q2"
            elif simbolo in digitos: 
                estado_actual = "q4"
            else: return False

        # 3. Transiciones desde q2 (Punto leído)
        elif estado_actual == "q2":
            if simbolo in digitos: 
                estado_actual = "q4"
            else: return False

        # 4. Transiciones desde q3 (Exponente 'e' leído)
        elif estado_actual == "q3":
            if simbolo in ["+", "-"]:
                estado_actual = "q1"
            elif simbolo in digitos: 
                estado_actual = "q4"
            else: return False

        # 5. Transiciones desde q4 (Estado Final / Dígitos)
        elif estado_actual == "q4":
            if simbolo in digitos:    
                estado_actual = "q4"
            elif simbolo == ".":
                estado_actual = "q2"
            elif simbolo == "e":
                estado_actual = "q3"
            else: return False

        print(f"Pasando de {estado_anterior} a {estado_actual} con entrada '{simbolo}'")
            
    return estado_actual == estado_final





