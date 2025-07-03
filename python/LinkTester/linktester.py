import os
import requests
import urllib3
from msal import ConfidentialClientApplication
from dotenv import load_dotenv

# Ignora apenas o warning visual do SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Carrega variáveis de ambiente do arquivo config.env
dotenv_path = os.path.join(os.path.dirname(__file__), "config.env")
load_dotenv(dotenv_path)

CLIENT_ID = os.getenv("CLIENT_ID")
print("CLIENT_ID:", CLIENT_ID)
TENANT_ID = os.getenv("TENANT_ID")
print("TENANT_ID:", TENANT_ID)
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
print("CLIENT_SECRET:", CLIENT_SECRET[:5] + "..." if CLIENT_SECRET else "None")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/.default"]
REMITENTE = "importadados@elian.com.br"
DESTINATARIO = "importa_ad@elian.com.br"

# Descobre o caminho da pasta atual onde o script está rodando
caminho_base = os.path.dirname(os.path.abspath(__file__))

# Função para ler URLs de um arquivo .txt na mesma pasta do script
def ler_urls_do_arquivo(nome_arquivo):
    caminho_arquivo = os.path.join(caminho_base, nome_arquivo)
    with open(caminho_arquivo, "r") as arquivo:
        urls = [linha.strip() for linha in arquivo if linha.strip()]
    return urls

# Função para testar URLs e gerar relatório
def testar_urls(lista_urls):
    urls_ok = []
    urls_erro = []
    urls_falha = []

    for url in lista_urls:
        try:
            resposta = requests.get(url, timeout=5, verify=False)
            if resposta.status_code == 200:
                urls_ok.append(url)
            else:
                urls_erro.append(f"{url} - Status {resposta.status_code}")
        except requests.exceptions.RequestException as e:
            urls_falha.append(f"{url} - Erro: {e}")

    # Começa com o resumo
    corpo_email = f"URLs testadas: {len(lista_urls)}\n"
    corpo_email += f"✔️ OK: {len(urls_ok)} | ⚠️ Erro: {len(urls_erro)} | ❌ Falha: {len(urls_falha)}\n"

    # Depois lista os resultados
    corpo_email += "\n\n✅ URLs que responderam OK:\n"
    corpo_email += "\n".join(f"   - {url}" for url in urls_ok) or "   (nenhuma)"

    corpo_email += "\n\n⚠️ URLs que responderam com erro (status diferente de 200):\n"
    corpo_email += "\n".join(f"   - {url}" for url in urls_erro) or "   (nenhuma)"

    corpo_email += "\n\n❌ URLs que não responderam ou deram falha:\n"
    corpo_email += "\n".join(f"   - {url}" for url in urls_falha) or "   (nenhuma)"

    return corpo_email


# Função para enviar e-mail via Microsoft Graph API
def enviar_email(corpo):
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )
    token_response = app.acquire_token_for_client(scopes=SCOPE)
    access_token = token_response.get("access_token")

    if not access_token:
        print("Erro ao obter token de acesso.")
        return

    email_msg = {
        "message": {
            "subject": "Relatório de Teste de URLs",
            "body": {
                "contentType": "Text",
                "content": corpo
            },
            "toRecipients": [
                {"emailAddress": {"address": DESTINATARIO}}
            ]
        },
        "saveToSentItems": "true"
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        f"https://graph.microsoft.com/v1.0/users/{REMITENTE}/sendMail",
        headers=headers,
        json=email_msg
    )

    if response.status_code == 202:
        print("✅ E-mail enviado com sucesso.")
    else:
        print(f"❌ Falha ao enviar e-mail. Código: {response.status_code}")
        print(response.text)

from datetime import datetime

def salvar_log(texto):
    pasta_logs = os.path.join(caminho_base, "Logs")
    os.makedirs(pasta_logs, exist_ok=True)

    data_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"log_{data_str}.txt"
    caminho_log = os.path.join(pasta_logs, nome_arquivo)

    with open(caminho_log, "w", encoding="utf-8") as log:
        log.write(texto)

    print(f"📁 Log salvo em: {caminho_log}")


# Execução principal
if __name__ == "__main__":
    urls = ler_urls_do_arquivo("urls.txt")
    relatorio = testar_urls(urls)
    enviar_email(relatorio)
    salvar_log(relatorio)