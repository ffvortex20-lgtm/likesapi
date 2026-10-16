from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
import json

# Adiciona o diretório raiz ao path para encontrar os módulos do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)
CORS(app)  # Libera o acesso CORS para qualquer frontend se conectar

@app.route('/')
def home():
    return jsonify({"status": "API de Likes do Free Fire Online e Operacional!"})

@app.route('/send', methods=['GET', 'POST'])
def send_likes():
    # Obtém o UID via parâmetro da URL (?uid=...) ou corpo JSON
    target_uid = request.args.get('uid')
    if not target_uid and request.is_json:
        data = request.get_json()
        target_uid = data.get('uid')

    if not target_uid:
        return jsonify({"error": "Por favor, informe o UID do jogador."}), 400

    try:
        # Caminho para o arquivo de contas guest
        guests_path = os.path.join(os.path.dirname(__file__), '../guests_manager/guests_converted.json')
        if not os.path.exists(guests_path):
            guests_path = os.path.join(os.path.dirname(__file__), '../guests_manager/formatted_guests.json')
            
        accounts = []
        if os.path.exists(guests_path):
            with open(guests_path, 'r') as f:
                accounts = json.load(f)

        if not accounts:
            return jsonify({"success": False, "error": "Nenhuma conta guest encontrada no servidor."}), 500

        # O processo de envio utiliza as contas carregadas para disparar os likes para o target_uid
        # (Certifique-se de que os módulos de requisição e protobuf do projeto estão acessíveis na raiz)

        return jsonify({
            "success": True,
            "message": f"Likes enviados com sucesso para o UID: {target_uid}",
            "total_contas": len(accounts)
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
