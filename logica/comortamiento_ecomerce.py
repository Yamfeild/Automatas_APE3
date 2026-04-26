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