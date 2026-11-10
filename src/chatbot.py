
import json
import urllib.request
import urllib.error

API_URL = "http://127.0.0.1:8080/v1/chat/completions"

SYSTEM_PROMPT = """
Você é o GeoETR Brasil, um chatbot especializado em elementos
terras raras (ETR), com foco no contexto brasileiro.

Seu público é técnico e acadêmico, incluindo pesquisadores,
estudantes de graduação e pós-graduação e profissionais
do setor mineral e ambiental.

Suas áreas de conhecimento incluem:
- Geologia, mineralogia e geoquímica dos ETR;
- Ocorrências, depósitos e projetos de ETR no Brasil;
- Exploração mineral, lavra e beneficiamento;
- Processamento e separação dos elementos;
- Aplicações tecnológicas e mercado de ETR;
- Aspectos ambientais, rejeitos e recuperação de áreas.

DIRETRIZES:
1. Utilize linguagem técnico-científica, clara e objetiva.
2. Explique conceitos complexos quando necessário.
3. Diferencie fatos comprovados, hipóteses e incertezas.
4. Não invente dados, estatísticas ou referências bibliográficas.
5. Quando não souber uma informação, declare essa limitação.
6. Priorize o contexto brasileiro, sem ignorar a literatura
   e os avanços científicos internacionais.
7. Organize respostas extensas em tópicos quando apropriado.
"""

historico = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

print("\n===================================")
print("          GeoETR Brasil")
print(" Chatbot sobre Elementos Terras Raras")
print("===================================")
print("Digite 'sair' para encerrar.\n")

while True:
    pergunta = input("Você: ").strip()

    if pergunta.lower() == "sair":
        print("\nEncerrando o GeoETR Brasil.")
        break

    if not pergunta:
        continue

    historico.append({
        "role": "user",
        "content": pergunta
    })

    dados = {
        "messages": historico,
        "temperature": 0.3,
        "max_tokens": 800
    }

    requisicao = urllib.request.Request(
        API_URL,
        data=json.dumps(dados).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(requisicao) as resposta:
            resultado = json.loads(resposta.read().decode("utf-8"))

        mensagem = resultado["choices"][0]["message"]
        resposta_bot = mensagem.get("content", "")

        if not resposta_bot:
            resposta_bot = "Não foi possível gerar uma resposta textual."

        print(f"\nGeoETR Brasil: {resposta_bot}\n")

        historico.append({
            "role": "assistant",
            "content": resposta_bot
        })

    except urllib.error.URLError as erro:
        print(f"\nErro de conexão com o servidor: {erro}\n")

    except Exception as erro:
        print(f"\nErro durante a geração da resposta: {erro}\n")


