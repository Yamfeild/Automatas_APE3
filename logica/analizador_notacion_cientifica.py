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