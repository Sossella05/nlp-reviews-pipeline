import json
import time
from ollama import chat


# ===============================
# 1. Ler arquivo TXT
# ===============================
def carregar_resenhas(caminho_arquivo):
    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    return [linha.strip() for linha in linhas if linha.strip()]


# ===============================
# 2. Parsear linhas
# ===============================
def parsear_resenhas(lista_linhas):
    resenhas = []

    for linha in lista_linhas:
        partes = linha.split("$")

        if len(partes) != 3:
            continue

        resenhas.append({
            "id": partes[0],
            "usuario": partes[1],
            "resenha_original": partes[2]
        })

    return resenhas


# ===============================
# 3. Chamada à IA local
# ===============================
def analisar_com_ia(usuario, resenha):
    prompt = f"""
Você receberá uma resenha de aplicativo.

Retorne EXCLUSIVAMENTE um JSON válido, sem markdown, sem texto extra, no formato:

{{
  "usuario": "{usuario}",
  "resenha_original": "{resenha}",
  "resenha_pt": "<tradução para português>",
  "avaliacao": "Positiva" | "Negativa" | "Neutra"
}}
"""

    response = chat(
        model="gemma3:4b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]


# ===============================
# 4. Limpeza de JSON
# ===============================
def limpar_json(texto):
    texto = texto.strip()

    if texto.startswith("```"):
        texto = texto.replace("```json", "")
        texto = texto.replace("```", "")
        texto = texto.strip()

    return texto


# ===============================
# 5. Processar TODAS as resenhas
# ===============================
def processar_resenhas(resenhas):
    resultados = []

    for idx, item in enumerate(resenhas, start=1):
        print(f"Processando {idx}/{len(resenhas)}...")

        try:
            resposta_ia = analisar_com_ia(
                item["usuario"],
                item["resenha_original"]
            )

            resposta_limpa = limpar_json(resposta_ia)
            resposta_dict = json.loads(resposta_limpa)

            resultados.append(resposta_dict)

        except Exception as erro:
            print("Erro ao processar resenha:", erro)
            continue

        time.sleep(0.5)  # evita sobrecarga do modelo local

    return resultados


# ===============================
# 6. Função final do desafio
# ===============================
def analisar_resultados(lista, separador=" | "):
    contagem = {
        "Positiva": 0,
        "Negativa": 0,
        "Neutra": 0
    }

    textos = []

    for item in lista:
        avaliacao = item.get("avaliacao", "Neutra")
        contagem[avaliacao] += 1

        textos.append(f'{item["usuario"]}: {item["resenha_pt"]}')

    texto_concatenado = separador.join(textos)

    return contagem, texto_concatenado


# ===============================
# EXECUÇÃO
# ===============================
resenhas_brutas = carregar_resenhas("Resenhas_App_ChatGPT.txt")
resenhas_parseadas = parsear_resenhas(resenhas_brutas)

resultados_ia = processar_resenhas(resenhas_parseadas)

contagem, texto_final = analisar_resultados(resultados_ia)

print("\n=== CONTAGEM DE AVALIAÇÕES ===")
print(contagem)

print("\n=== TEXTO CONCATENADO (500 primeiros caracteres) ===")
print(texto_final[:500])
