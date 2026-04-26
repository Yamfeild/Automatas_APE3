#Ejercicio1

def telemetria_nfa(encabezado):
    #Σ={HDR[, Lectura de sensores de humedad[H],Lectura de sensores de temperatura[T] CRC}
    Alfabeto = ["HDR", "H", "T", "CRC"]
    estado_inicial = "q0"
    estado_final = "q2"
    estado_siguiente = estado_inicial
    cadena_aceptada = False

    if not all(parametro in Alfabeto for parametro in encabezado):
        print("El encabezado contiene parametros no válidos. Solo se permiten 'HDR', 'H', 'T' y 'CRC'.")
        return False

    for letra in encabezado:
        if estado_siguiente == "q0" and letra == "HDR":
            estado_siguiente = "q1"
            print(f"Pasando de estado {estado_inicial} a {estado_siguiente} con entrada '{letra}'")
        
        elif estado_siguiente == "q1" and (letra == "H" or letra == "T"):
            estado_siguiente = "q1"
            print(f"Pasando de estado {estado_inicial} a {estado_siguiente} con entrada '{letra}'")
        
        elif estado_siguiente == "q1" and letra == "CRC":
            estado_siguiente = "q2"
            print(f"Pasando de estado {estado_inicial} a {estado_siguiente} con entrada '{letra}'")
        


        if estado_siguiente == estado_final:
            cadena_aceptada = True

    return cadena_aceptada





#Ejercicio2
def analizador_ecommerce(secuencia):
    # H=HOME, S=SEARCH, C=CART
    alfabeto = ["H", "S", "C"]
    estado_actual = "q0"
    
    if not all(s in alfabeto for s in secuencia):
        return False
        
    for simbolo in secuencia:
        if estado_actual == "q0":
            if simbolo == "H":
                estado_actual = "q1"
            else:
                return False
            
        elif estado_actual == "q1":
            if simbolo == "S":
                estado_actual = "q2"
            else:
                return False
            
        elif estado_actual == "q2":
            if simbolo == "S":
                estado_actual = "q2"
            elif simbolo == "C":
                estado_actual = "q3"
            else:
                return False
                
        elif estado_actual == "q3":
            return False
            
    return estado_actual == "q3"








#Ejercicio3
def deteccion_ataque(secuencia):
    # S=SYN, A=ACK, R=RST
    alfabeto = ["S", "A", "R"]
    estado_actual = "q0"
    
    # Validación de símbolos [cite: 365]
    if not all(s in alfabeto for s in secuencia):
        return False
        
    for simbolo in secuencia:
        if estado_actual == "q0":
            if simbolo == "S":
                estado_actual = "q1"
            else:
                return False 
        
        elif estado_actual == "q1":
            if simbolo == "A":
                estado_actual = "q1" 
            elif simbolo == "R":
                estado_actual = "q2" 
            else:
                return False 
        
        elif estado_actual == "q2":
            return False 
            
    return estado_actual == "q2"

