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