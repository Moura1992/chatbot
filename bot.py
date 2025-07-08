from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
usuarios = {}

@app.route("/bot", methods=["POST"])
def bot():
    numero = request.form['From']
    mensagem = request.form['Body'].strip().lower()
    resp = MessagingResponse()

    if numero not in usuarios:
        usuarios[numero] = {"estado": "esperando_comando", "dados": {}}

    estado = usuarios[numero]["estado"]
    dados = usuarios[numero]["dados"]

    if estado == "esperando_comando":
        if "dividir a conta" in mensagem:
            resp.message("Vamos dividir a conta de luz! Qual o valor total da conta (em R$)?")
            usuarios[numero]["estado"] = "valor_total"
        else:
            resp.message("Digite 'dividir a conta' para iniciar o cálculo.")

    elif estado == "valor_total":
        try:
            dados["valor_total"] = float(mensagem.replace(",", "."))
            resp.message("Qual a leitura anterior do seu medidor (Cidinha)?")
            usuarios[numero]["estado"] = "cidinha_inicio"
        except:
            resp.message("Por favor, envie um valor numérico válido (ex: 253.60).")

    elif estado == "cidinha_inicio":
        dados["cidinha_inicio"] = int(mensagem)
        resp.message("Qual a leitura atual do seu medidor (Cidinha)?")
        usuarios[numero]["estado"] = "cidinha_fim"

    elif estado == "cidinha_fim":
        dados["cidinha_fim"] = int(mensagem)
        resp.message("Qual a leitura anterior do medidor do Fabinho?")
        usuarios[numero]["estado"] = "fabinho_inicio"

    elif estado == "fabinho_inicio":
        dados["fabinho_inicio"] = int(mensagem)
        resp.message("Qual a leitura atual do medidor do Fabinho?")
        usuarios[numero]["estado"] = "fabinho_fim"

    elif estado == "fabinho_fim":
        dados["fabinho_fim"] = int(mensagem)
        resultado = calcular_conta(dados)
        resp.message(resultado)
        usuarios[numero]["estado"] = "esperando_comando"

    return str(resp)

def calcular_conta(dados):
    consumo_cidinha = dados["cidinha_fim"] - dados["cidinha_inicio"]
    consumo_fabinho = dados["fabinho_fim"] - dados["fabinho_inicio"]
    consumo_total = consumo_cidinha + consumo_fabinho

    if consumo_total == 0:
        return "Erro: O consumo total é zero. Verifique as leituras."

    valor_unitario = dados["valor_total"] / consumo_total
    valor_cidinha = round(valor_unitario * consumo_cidinha, 2)
    valor_fabinho = round(valor_unitario * consumo_fabinho, 2)
    valor_unitario = round(valor_unitario, 2)

    return (f"Consumo de Cidinha: {consumo_cidinha} kWh\n"
            f"Consumo de Fabinho: {consumo_fabinho} kWh\n"
            f"Total de {consumo_total} kWh consumidos\n"
            f"Valor por kWh: R$ {valor_unitario}\n"
            f"Cidinha deve pagar: R$ {valor_cidinha}\n"
            f"Fabinho deve pagar: R$ {valor_fabinho}")

if __name__ == "__main__":
    app.run(debug=True)
