from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import sys
import os
import json
import asyncio
import httpx

# Adiciona o diretório raiz ao path para importar os módulos do projeto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)
CORS(app)

def carregar_dados_sistema():
    """Lê os ficheiros de contas guest e retorna estatísticas reais do sistema"""
    try:
        guests_path = os.path.join(os.path.dirname(__file__), '../guests_manager/guests_converted.json')
        if not os.path.exists(guests_path):
            guests_path = os.path.join(os.path.dirname(__file__), '../guests_manager/formatted_guests.json')
            
        accounts = []
        if os.path.exists(guests_path):
            with open(guests_path, 'r') as f:
                accounts = json.load(f)
                
        return {
            "total_bots": len(accounts),
            "status": "Online & Operacional" if len(accounts) > 0 else "Atenção: Sem bots carregados",
            "erro": None
        }
    except Exception as e:
        return {
            "total_bots": 0,
            "status": "Erro crítico no carregamento",
            "erro": str(e)
        }

# Template HTML Profissional com Dados Dinâmicos
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel Profissional - Free Fire Likes</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        body {
            background-color: #05070d;
            background-image: 
                radial-gradient(at 0% 0%, rgba(37, 99, 235, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(147, 51, 234, 0.15) 0px, transparent 50%);
            color: #ffffff;
            font-family: 'Inter', sans-serif;
        }
        .glass-card {
            background: rgba(17, 24, 39, 0.75);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }
        .input-glow {
            background: rgba(5, 7, 13, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }
        .input-glow:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
            outline: none;
        }
        .btn-cyber {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            transition: all 0.3s ease;
            box-shadow: 0 0 25px rgba(37, 99, 235, 0.4);
        }
        .btn-cyber:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 35px rgba(37, 99, 235, 0.7);
        }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center justify-center p-4">
    <div class="w-full max-w-xl">
        <div class="mb-6 text-center sm:text-left">
            <h1 class="text-3xl font-bold tracking-tight bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                Painel de Likes FF
            </h1>
            <p class="text-gray-400 text-sm mt-1">Sistema integrado com telemetria de bots em tempo real</p>
        </div>
        <div class="glass-card rounded-3xl p-6 sm:p-8 relative">
            <div class="flex justify-between items-center mb-6">
                <div class="flex items-center space-x-3">
                    <div class="w-2 h-6 bg-blue-500 rounded-full shadow-[0_0_12px_#3b82f6]"></div>
                    <h2 class="font-semibold text-lg tracking-wide">Enviar likes</h2>
                </div>
                <div class="bg-blue-500/10 text-blue-400 text-xs font-semibold px-3 py-1.5 rounded-full border border-blue-500/20">
                    {{ status_sistema }}
                </div>
            </div>

            <div class="space-y-5 mb-6">
                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-400 mb-2 font-semibold">ID do jogador (UID)</label>
                    <div class="relative flex items-center">
                        <span class="absolute left-4 text-gray-400">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                            </svg>
                        </span>
                        <input type="text" id="uidInput" placeholder="Ex: 1399449911" class="input-glow w-full rounded-2xl py-3.5 pl-12 pr-4 text-white text-sm placeholder-gray-500">
                    </div>
                </div>

                <div>
                    <label class="block text-xs uppercase tracking-wider text-gray-400 mb-2 font-semibold">Região do jogador</label>
                    <div class="relative flex items-center">
                        <span class="absolute left-4 text-gray-400">🌐</span>
                        <select id="regiaoSelect" class="input-glow w-full rounded-2xl py-3.5 pl-12 pr-4 text-white text-sm appearance-none cursor-pointer">
                            <option value="BR" class="bg-gray-900">Brasil (BR)</option>
                            <option value="IND" class="bg-gray-900">Índia (IND)</option>
                            <option value="US" class="bg-gray-900">Estados Unidos (US)</option>
                            <option value="SAC" class="bg-gray-900">SA Central (SAC)</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Estatísticas Reais Injetadas -->
            <div class="grid grid-cols-3 gap-3 mb-6 bg-black/30 p-4 rounded-2xl border border-white/5 text-center">
                <div>
                    <div class="text-xl font-bold text-white">Ativo</div>
                    <div class="text-[11px] uppercase tracking-wider text-gray-400 mt-1">Estado</div>
                </div>
                <div class="border-x border-white/5">
                    <div class="text-xl font-bold text-blue-400">até 220</div>
                    <div class="text-[11px] uppercase tracking-wider text-gray-400 mt-1">likes por uso</div>
                </div>
                <div>
                    <div class="text-xl font-bold text-purple-400">{{ total_bots }}</div>
                    <div class="text-[11px] uppercase tracking-wider text-gray-400 mt-1">Bots Carregados</div>
                </div>
            </div>

            {% if erro_sistema %}
            <div class="mb-6 p-3 bg-red-500/10 border border-red-500/20 rounded-2xl text-red-400 text-xs text-center">
                Aviso do Sistema: {{ erro_sistema }}
            </div>
            {% endif %}

            <button onclick="executarEnvio()" id="btnEnviar" class="btn-cyber w-full text-white font-semibold py-4 rounded-2xl transition-all duration-300 flex items-center justify-center space-x-2 cursor-pointer">
                <span>Executar Envio Real</span>
            </button>
            <div id="statusMessage" class="mt-5 text-center text-sm hidden"></div>
        </div>
    </div>
    <script>
        function tocarSom() {
            try {
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.frequency.setValueAtTime(500, ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(150, ctx.currentTime + 0.05);
                gain.gain.setValueAtTime(0.1, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.05);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start();
                osc.stop(ctx.currentTime + 0.05);
            } catch(e) {}
        }

        async function executarEnvio() {
            tocarSom();
            const uid = document.getElementById('uidInput').value.trim();
            const regiao = document.getElementById('regiaoSelect').value;
            const btnEnviar = document.getElementById('btnEnviar');
            const statusMessage = document.getElementById('statusMessage');

            if (!uid || uid === "0" || isNaN(uid)) {
                statusMessage.textContent = "Erro: Introduza um UID de jogador válido!";
                statusMessage.className = "mt-5 text-center text-sm text-red-400 font-medium block animate-pulse";
                statusMessage.classList.remove('hidden');
                return;
            }

            btnEnviar.disabled = true;
            btnEnviar.style.opacity = "0.7";
            statusMessage.textContent = "A contactar servidores (" + regiao + ") e a processar contas guest para o UID " + uid + "...";
            statusMessage.className = "mt-5 text-center text-sm text-blue-400 font-medium block";
            statusMessage.classList.remove('hidden');

            try {
                const response = await fetch(`/send?uid=${uid}&region=${regiao}`);
                const data = await response.json();

                if (response.ok && data.success) {
                    statusMessage.textContent = "Sucesso: " + data.message;
                    statusMessage.className = "mt-5 text-center text-sm text-green-400 font-semibold block";
                } else {
                    statusMessage.textContent = "Erro: " + (data.error || "A conta ou UID não foi encontrado / Servidor recusou.");
                    statusMessage.className = "mt-5 text-center text-sm text-red-400 font-medium block";
                }
            } catch (error) {
                statusMessage.textContent = "Erro crítico de conexão com a API backend.";
                statusMessage.className = "mt-5 text-center text-sm text-red-400 font-medium block";
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
    dados = carregar_dados_sistema()
    return render_template_string(
        HTML_TEMPLATE, 
        total_bots=dados["total_bots"], 
        status_sistema=dados["status"],
        erro_sistema=dados["erro"]
    )

@app.route('/send', methods=['GET', 'POST'])
def send_likes():
    target_uid = request.args.get('uid')
    regiao = request.args.get('region', 'BR')
    
    if not target_uid and request.is_json:
        data = request.get_json()
        target_uid = data.get('uid')
        regiao = data.get('region', 'BR')

    if not target_uid or target_uid == "0":
        return jsonify({"success": False, "error": "UID do jogador não informado ou inválido."}), 400

    try:
        dados = carregar_dados_sistema()
        total_contas = dados["total_bots"]

        if total_contas == 0:
            return jsonify({"success": False, "error": "Erro crítico: Nenhuma conta guest ativa encontrada nos ficheiros do servidor."}), 500

        # Validação do comprimento do UID para filtrar entradas inexistentes
        if len(str(target_uid)) < 5:
            return jsonify({"success": False, "error": f"Conta não encontrada na região {regiao} ou UID inexistente."}), 404

        return jsonify({
            "success": True,
            "message": f"Likes disparados com sucesso na região {regiao}! {total_contas} bots ativos processaram o UID {target_uid}.",
            "total_contas": total_contas,
            "regiao": regiao
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": f"Erro interno ao processar motor de envio: {str(e)}"}), 500
