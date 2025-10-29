import requests
import json
import time
import telebot
import os

# ===============================
# CONFIGURAÇÕES
# ===============================
TOKEN = os.environ.get("TOKEN")  # Coloque seu token no Railway como variável de ambiente
bot = telebot.TeleBot(TOKEN)

# API gratuita para buscar jogos (exemplo: TheSportsDB)
API_URL = "https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={data}&l=English%20Premier%20League"

def buscar_jogos(data):
    try:
        url = API_URL.format(data=data)
        r = requests.get(url)
        dados = r.json()
        jogos = dados.get("events", [])
        lista = []
        if not jogos:
            return ["Nenhum jogo encontrado para esta data."]
        for j in jogos:
            partida = f"{j['strEvent']} - {j['dateEvent']} às {j['strTime']}"
            lista.append(partida)
        return lista
    except Exception as e:
        return [f"Erro ao buscar jogos: {e}"]

# ===============================
# COMANDOS DO BOT
# ===============================
@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "⚽ Olá! Sou o seu Bot de Análise de Futebol.\nDigite /jogos para ver os jogos do dia.")

@bot.message_handler(commands=['jogos'])
def jogos(msg):
    data = time.strftime("%Y-%m-%d")
    bot.reply_to(msg, f"Buscando jogos de {data}...")
    jogos = buscar_jogos(data)
    resposta = "\n".join(jogos[:10])
    bot.send_message(msg.chat.id, f"📅 Jogos principais de hoje:\n\n{resposta}")

bot.polling()
