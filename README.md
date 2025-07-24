# Chatbot

Chatbot para Dividir Conta de Luz com WhatsApp e Python

Este é um projeto pessoal criado para automatizar uma tarefa real do meu dia a dia: *dividir a conta de energia* entre duas pessoas , com base nas leituras individuais dos nossos medidores.

O que esse chatbot faz

✅ Recebe o valor total da fatura de energia  
✅ Pergunta as leituras anteriores e atuais dos dois medidores  
✅ Calcula o consumo de cada um  
✅ Aplica a fórmula para dividir o valor proporcionalmente  
✅ Retorna quanto cada um deve pagar


Tecnologias utilizadas

- Python 🐍  
- Flask 💻  
- Twilio API (para WhatsApp)  
- Ngrok (para testes locais)


## 📲 Como testar o projeto

> Requisitos: Python instalado + Conta gratuita na Twilio + Ngrok

```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio
pip install -r requirements.txt
python bot.py
