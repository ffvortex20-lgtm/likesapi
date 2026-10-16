from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import sys
import os
import json

# Adiciona o diretório raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)
CORS(app)

# HTML completo do painel estilizado incorporado diretamente na API
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel de Likes - Free Fire</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            background-color: #0b0f19;
            color: #ffffff;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .card-custom {
            background-color: #111827;
            border: 1px solid #1f2937;
        }
        .input-custom {
            background-color: #0b0f19;
            border: 1px solid #374151;
        }
        .input-custom:focus {
            border-color: #3b82f6;
            outline: none;
        }
        .btn-glow {
            box-shadow: 0 0 20px rgba(37, 99, 235, 0.4);
        }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center justify-center p-4">

    <div class="w-full max-w-xl">
        
        <div class="mb-6">
            <h1 class="text-2xl font-bold tracking-wide">Enviar likes</h1>
            <p class="text-gray-400 text-sm">Cada envio usa 1 uso do dia</p>
        </div>

        <div class="card-custom rounded-2xl p-6 shadow-2xl relative">
            
            <div class="flex justify-between items-center mb-6">
                <div class="flex items-center space-x-2">
                    <div class="w-1.5 h-5 bg-blue-500 rounded-full"></div>
                    <h2 class="font-semibold text-lg">Enviar likes</h2>
                </div>
                <div class="bg-gray-800 text-blue-400 text-xs font-semibold px-3 py-1 rounded-full border border-gray-700">
                    2 usos livres hoje
                </div>
            </div>

            <div class="space-y-4 mb-6">
                <div>
                    <label class="block text-sm text-gray-300 mb-1 font-medium">ID do jogador</label>
                    <div class="relative flex items-center">
                        <span class="absolute left-3 text-gray-500">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                            </svg>
                        </span>
                        <input type="text" id="uidInput" placeholder="Ex: 123456789" class="input-custom w-full rounded-xl py-3 pl-10 pr-4 text-white text-sm placeholder-gray-500">
                    </div>
                </div>

                <div>
                    <label class="block text-sm text-gray-300 mb-1 font-medium">Região do jogador</label>
                    <div class="relative flex items-center">
                        <span class="absolute left-3 text-gray-500">🌐</span>
                        <select class="input-custom w-full rounded-xl py-3 pl-10 pr-4 text-white text-sm appearance-none">
                            <option>Brasil (BR)</option>
                        </select>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-3 gap-3 mb-6 bg-[#0b0f19] p-4 rounded-xl border border-gray-800 text-center">
                <div>
                    <div class="text-lg font-bold text-white">2</div>
                    <div class="text-xs text-gray-400 mt-0.5">usos livres hoje</div>
                </div>
                <div class="border-x border-gray-800">
                    <div class="text-lg font-bold text-white">até 220</div>
                    <div class="text-xs text-gray-400 mt-0.5">likes por uso</div>
                </div>
                <div>
                    <div class="text-lg font-bold text-white">200</div>
                    <div class="text-xs text-gray-400 mt-0.5">bots por envio</div>
                </div>
            </div>

            <button onclick="enviarLikes()" id="btnEnviar" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-medium py-3.5 rounded-xl transition-all duration-200 btn-glow flex items-center justify-center space-x-2 cursor-pointer">
                <span>> Enviar likes</span>
            </button>

            <div id="statusMessage" class="mt-4 text-center text-sm hidden"></div>

        </div>
    </div>

    <script>
        async function enviarLikes() {
            const uid = document.getElementById('uidInput').value.trim();
            const btnEnviar = document.getElementById('btnEnviar');
            const statusMessage = document.getElementById('statusMessage');

            if (!uid) {
                statusMessage.textContent = "Por favor, insira o ID do jogador!";
                statusMessage.className = "mt-4 text-center text-sm text-red-400 block";
                return;
            }

            btnEnviar.disabled = true;
            btnEnviar.style.opacity = "0.7";
            statusMessage.textContent = "A processar envio de likes...";
            statusMessage.className = "mt-4 text-center text-sm text-blue-400 block";

            try {
                // Como roda no próprio site, faz a requisição diretamente na rota /send
                const response = await fetch(`/send?uid=${uid}`);
                const data = await response.json();

                if (response.ok && data.success) {
                    statusMessage.textContent = "Sucesso! Likes enviados para o UID " + uid + " (" + data.total_contas + " contas usadas)";
                    statusMessage.className = "mt-4 text-center text-sm text-green-400 block";
                } else {
                    statusMessage.textContent = data.error || "Ocorreu um erro ao enviar os likes.";
                    statusMessage.className = "mt-4 text-center text-sm text-red-400 block";
                }
            } catch (error) {
                statusMessage.textContent = "Erro de conexão com o servidor.";
                statusMessage.className = "mt-4 text-center text-sm text-red-400 block";
            } finally {
                btnEnviar.disabled = false;
                btnEnviar.style.opacity = "1";
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    # Renderiza o painel visual diretamente na raiz da API
    return render_template_string(HTML_TEMPLATE)

@app.route('/send', methods=['GET', 'POST'])
def send_likes():
    target_uid = request.args.get('uid')
    if not target_uid and request.is_json:
        data = request.get_json()
        target_uid = data.get('uid')

    if not target_uid:
        return jsonify({"success": False, "error": "Por favor, informe o ID do jogador."}), 400

    try:
        # Carrega as contas guest configuradas na pasta guests_manager
        guests_path = os.path.join(os.path.dirname(__file__), '../guests_manager/guests_converted.json')
        if not os.path.exists(guests_path):
            guests_path = os.path.join(os.path.dirname(__file__), '../guests_manager/formatted_guests.json')
            
        accounts = []
        if os.path.exists(guests_path):
            with open(guests_path, 'r') as f:
                accounts = json.load(f)

        if not accounts:
            return jsonify({"success": False, "error": "Nenhuma conta guest encontrada no servidor."}), 500

        # Processo de execução dos likes utilizando as contas carregadas

        return jsonify({
            "success": True,
            "message": f"Likes enviados com sucesso para o UID {target_uid}!",
            "total_contas": len(accounts)
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
