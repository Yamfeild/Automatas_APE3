from flask import Flask, request, jsonify, render_template
from logica.renderizaciones import (
    dfa_transacciones,
    dfa_cerradura,
    dfa_notacion_cientifica,
    nfa_telemetria,
    nfa_ecommerce,
    nfa_deteccion_ataque,
)

app = Flask(__name__)

AUTOMATAS = {
    "transacciones": dfa_transacciones,
    "cerradura": dfa_cerradura,
    "notacion_cientifica": dfa_notacion_cientifica,
    "telemetria": nfa_telemetria,
    "ecommerce": nfa_ecommerce,
    "deteccion_ataque": nfa_deteccion_ataque,
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/automatas", methods=["GET"])
def listar_automatas():
    return jsonify({clave: automata.to_dict() for clave, automata in AUTOMATAS.items()})


@app.route("/simular/<nombre>", methods=["POST"])
def simular(nombre):
    data = request.json or {}
    eventos = [str(token).strip() for token in data.get("eventos", []) if str(token).strip()]

    automata = AUTOMATAS.get(nombre)
    if automata is None:
        return jsonify({"error": "No existe"}), 404

    steps = automata.simulate_with_steps(eventos)
    estado_final = steps[-1]["states"] if steps else []
    aceptada = bool(set(estado_final) & automata.estados_finales)

    return jsonify({
        "automata": nombre,
        "cadena": eventos,
        "aceptada": aceptada,
        "steps": steps,
        "definicion": automata.to_dict(),
    })


if __name__ == "__main__":
    app.run(debug=True)