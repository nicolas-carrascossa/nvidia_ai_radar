import firecrawl
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
app = firecrawl.FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))
cliente = Groq(api_key=os.getenv("GROQ_API_KEY"))

resultados = app.search("startup inteligencia artificial Brasil site:startups.com.br")

for r in resultados.web[:3]:
    print(f"Acessando: {r.url}")
    try:
        conteudo = app.scrape_url(r.url)
        print(conteudo.markdown[5000])
        resposta = cliente.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "Você extrai informações de startups. Responda apenas em JSON válido, sem texto extra."
                },
                {
                    "role": "user", 
                    "content": f"""Extraia as seguintes informações do texto abaixo:
                      - setor (ex: fintech, healthtech, edtech)
                      - produto (o que a empresa faz em uma frase)
                      - tecnologias_ia (lista de tecnologias de IA mencionadas)
                      - sinal_de_ia (true ou false)

                      Texto:
                      {conteudo.markdown[:500]}"""
                }
            ]
          )

        print(resposta.choices[0].message.content)
    except Exception as e:
        print(f"Falhou: {e}")
    print("---")


