# Pipeline de Análise de Resenhas com IA Local

Este projeto implementa um pipeline completo em Python para análise de resenhas de aplicativos,
utilizando um modelo de linguagem local via Ollama (Gemma 3 4B).

## Funcionalidades
- Leitura de resenhas a partir de arquivo `.txt`
- Estruturação e normalização dos dados
- Tradução automática para português
- Classificação de sentimento (Positiva, Negativa, Neutra)
- Tratamento de falhas de saída de LLM (JSON)
- Agregação e contagem dos resultados

## Tecnologias utilizadas
- Python 3
- Ollama
- Modelo Gemma 3 (4B)
- JSON

## Como executar
```bash
python3 main.py
