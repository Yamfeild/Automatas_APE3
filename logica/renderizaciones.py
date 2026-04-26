class AutomataRender:
    def __init__(self, nombre, tipo, estados, alfabeto, estado_inicial, estados_finales, transiciones, ejemplos_aceptados=None, descripcion=None):
        self.nombre = nombre
        self.tipo = tipo
        self.estados = estados
        self.alfabeto = alfabeto
        self.estado_inicial = estado_inicial
        self.estados_finales = set(estados_finales)
        self.transiciones = transiciones
        self.ejemplos_aceptados = ejemplos_aceptados or []
        self.descripcion = descripcion

    def next_states(self, estado, simbolo):
        destino = self.transiciones.get(estado, {}).get(simbolo, [])
        if isinstance(destino, str):
            return [destino]
        return destino

    def simulate_with_steps(self, eventos):
        estados_actuales = {self.estado_inicial}
        pasos = [
            {
                "step": 0,
                "input": "",
                "states": sorted(estados_actuales),
                "accepted": bool(estados_actuales & self.estados_finales),
            }
        ]

        for indice, simbolo in enumerate(eventos, start=1):
            siguientes = set()
            for estado in estados_actuales:
                siguientes.update(self.next_states(estado, simbolo))
            estados_actuales = siguientes
            pasos.append(
                {
                    "step": indice,
                    "input": simbolo,
                    "states": sorted(estados_actuales),
                    "accepted": bool(estados_actuales & self.estados_finales),
                }
            )

        return pasos

    def tabla_transiciones(self):
        tabla = []
        for estado in self.estados:
            fila = {"estado": estado}
            for simbolo in self.alfabeto:
                fila[simbolo] = self.next_states(estado, simbolo)
            tabla.append(fila)
        return tabla

    def to_dict(self):
        data = {
            "nombre": self.nombre,
            "tipo": self.tipo,
            "estados": self.estados,
            "alfabeto": self.alfabeto,
            "estado_inicial": self.estado_inicial,
            "estados_finales": sorted(self.estados_finales),
            "tabla_transiciones": self.tabla_transiciones(),
            "ejemplos_aceptados": self.ejemplos_aceptados,
        }

        if self.descripcion:
            data["descripcion"] = self.descripcion

        return data


# Definiciones de renderizacion para los autómatas del usuario.
dfa_transacciones = AutomataRender(
    nombre="Transacciones",
    tipo="DFA",
    estados=["q0", "q1", "q2", "q3", "qe"],
    alfabeto=["A", "L", "C", "E"],
    estado_inicial="q0",
    estados_finales=["q3"],
    transiciones={
        "q0": {"A": ["q1"], "L": ["qe"], "C": ["qe"], "E": ["qe"]},
        "q1": {"A": ["q1"], "L": ["qe"], "C": ["q2"], "E": ["qe"]},
        "q2": {"A": ["qe"], "L": ["q3"], "C": ["q2"], "E": ["qe"]},
        "q3": {"A": ["q3"], "L": ["q3"], "C": ["q3"], "E": ["q3"]},
        "qe": {"A": ["qe"], "L": ["qe"], "C": ["qe"], "E": ["qe"]},
    },
    ejemplos_aceptados=["A,C,L", "A,C,C,L", "A,A,C,L"],
)

dfa_cerradura = AutomataRender(
    nombre="Cerradura",
    tipo="DFA",
    estados=["q0", "q1", "q2", "q3", "q4"],
    alfabeto=["V", "F"],
    estado_inicial="q0",
    estados_finales=["q4"],
    transiciones={
        "q0": {"V": ["q4"], "F": ["q1"]},
        "q1": {"V": ["q4"], "F": ["q2"]},
        "q2": {"V": ["q4"], "F": ["q3"]},
        "q3": {"V": ["q3"], "F": ["q3"]},
        "q4": {"V": ["q4"], "F": ["q4"]},
    },
    ejemplos_aceptados=["V", "F,V", "F,F,V"],
)

dfa_notacion_cientifica = AutomataRender(
    nombre="Notacion cientifica",
    tipo="DFA",
    estados=["q0", "q1", "q2", "q3", "q4"],
    alfabeto=["+", "-", ".", "e", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    estado_inicial="q0",
    estados_finales=["q4"],
    transiciones={
        "q0": {
            "+": ["q1"], "-": ["q1"], ".": ["q2"], "e": [],
            "0": ["q4"], "1": ["q4"], "2": ["q4"], "3": ["q4"], "4": ["q4"], "5": ["q4"], "6": ["q4"], "7": ["q4"], "8": ["q4"], "9": ["q4"],
        },
        "q1": {
            "+": [], "-": [], ".": ["q2"], "e": [],
            "0": ["q4"], "1": ["q4"], "2": ["q4"], "3": ["q4"], "4": ["q4"],
            "5": ["q4"], "6": ["q4"], "7": ["q4"], "8": ["q4"], "9": ["q4"],
        },
        "q2": {
            "+": [], "-": [], ".": [], "e": [],
            "0": ["q4"], "1": ["q4"], "2": ["q4"], "3": ["q4"], "4": ["q4"],
            "5": ["q4"], "6": ["q4"], "7": ["q4"], "8": ["q4"], "9": ["q4"],
        },
        "q3": {
            "+": ["q1"], "-": ["q1"], ".": [], "e": [],
            "0": ["q4"], "1": ["q4"], "2": ["q4"], "3": ["q4"], "4": ["q4"],
            "5": ["q4"], "6": ["q4"], "7": ["q4"], "8": ["q4"], "9": ["q4"],
        },
        "q4": {
            "+": [], "-": [], ".": ["q2"], "e": ["q3"],
            "0": ["q4"], "1": ["q4"], "2": ["q4"], "3": ["q4"], "4": ["q4"],
            "5": ["q4"], "6": ["q4"], "7": ["q4"], "8": ["q4"], "9": ["q4"],
        },
    },
    ejemplos_aceptados=[".5", "+.3", "1e2", "-2.7e3"],
)

nfa_telemetria = AutomataRender(
    nombre="Telemetria",
    tipo="NFA",
    estados=["q0", "q1", "q2"],
    alfabeto=["HDR", "H", "T", "CRC"],
    estado_inicial="q0",
    estados_finales=["q2"],
    transiciones={
        "q0": {"HDR": ["q1"]},
        "q1": {"H": ["q1"], "T": ["q1"], "CRC": ["q1", "q2"]},
        "q2": {},
    },
    ejemplos_aceptados=["HDR,CRC", "HDR,H,CRC", "HDR,T,H,CRC", "HDR,H,T,CRC"],
)

nfa_ecommerce = AutomataRender(
    nombre="Ecommerce",
    tipo="NFA",
    estados=["q0", "q1", "q2", "q3"],
    alfabeto=["H", "S", "C"],
    estado_inicial="q0",
    estados_finales=["q3"],
    transiciones={
        "q0": {"H": ["q1"]},
        "q1": {"S": ["q2"]},
        "q2": {"S": ["q2"], "C": ["q3"]},
        "q3": {},
    },
    ejemplos_aceptados=["H,S,C", "H,S,S,C", "H,S,S,S,C"],
)

nfa_deteccion_ataque = AutomataRender(
    nombre="Deteccion de ataque",
    tipo="NFA",
    estados=["q0", "q1", "q2"],
    alfabeto=["S", "A", "R"],
    estado_inicial="q0",
    estados_finales=["q2"],
    transiciones={
        "q0": {"S": ["q1"]},
        "q1": {"A": ["q1"], "R": ["q2"]},
        "q2": {},
    },
    ejemplos_aceptados=["S,R", "S,A,R", "S,A,A,R"],
)
