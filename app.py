from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>¡Hola, Flask!</h1><p>Tu entorno básico está funcionando.</p>"

if __name__ == '__main__':
    app.run(debug=True)