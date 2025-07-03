import os
import requests
import urllib3
import sys
from msal import ConfidentialClientApplication
from dotenv import load_dotenv
from datetime import datetime

# Ignora apenas o warning visual do SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define o caminho base corretamente, mesmo quando empacotado com PyInstaller
if getattr(sys, 'frozen', False):
    caminho_base = os.path.dirname(sys.executable)
else:
    caminho_base = os.path.dirname(os.path.abspath(__file__))

print(f"Caminho base detectado: {caminho_base}")

# Carrega o arquivo config.env a partir do caminho base
dotenv_path = os.path.join(caminho_base, "config.env")
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

# Função para ler URLs de um arquivo .txt na mesma pasta do executável
def ler_urls_do_arquivo(nome_arquivo):
    caminho_arquivo = os.path.join(caminho_base, nome_arquivo)
    with open(caminho_arquivo, "r") as arquivo:
        urls = [linha.strip() for linha in arquivo if linha.strip()]
    return urls

# Função para testar URLs e gerar relatório com debug
def testar_urls(lista_urls):
    urls_ok = []
    urls_erro = []
    urls_falha = []

    for url in lista_urls:
        print(f"Testando: {url}")  # Mostra cada URL sendo testada

        try:
            resposta = requests.get(url, timeout=2, verify=False)
            if resposta.status_code == 200:
                print(f"✅ {url} respondeu OK.")
                urls_ok.append(url)
            else:
                print(f"⚠️ {url} respondeu com status {resposta.status_code}.")
                urls_erro.append(f"{url} - Status {resposta.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {url} falhou: {e}")
            urls_falha.append(f"{url} - Erro: {e}")

    print("✅ Testes concluídos. Montando relatório...")

    corpo_email = f"URLs testadas: {len(lista_urls)}\n"
    corpo_email += f"✔️ OK: {len(urls_ok)} | ⚠️ Erro: {len(urls_erro)} | ❌ Falha: {len(urls_falha)}\n"

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
        print("❌ Erro ao obter token de acesso.")
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
        json=email_msg,
        timeout=10
    )

    if response.status_code == 202:
        print("✅ E-mail enviado com sucesso.")
    else:
        print(f"❌ Falha ao enviar e-mail. Código: {response.status_code}")
        print(response.text)

# Função para salvar log em arquivo
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
    print("Lendo arquivo de URLs...")
    urls = ler_urls_do_arquivo("urls.txt")
    print(f"{len(urls)} URLs encontradas.")
    print(urls)

    print("Testando URLs e montando relatório...")
    relatorio = testar_urls(urls)
    print("Relatório montado.")

    print("Enviando e-mail com o relatório...")
    enviar_email(relatorio)
    
    print("Salvando o log...")
    salvar_log(relatorio)
    print("✅ Processo concluído.")