import requests

# Função para ler URLs de um arquivo .txt
def ler_urls_do_arquivo(caminho_arquivo):
    with open(caminho_arquivo, "r") as arquivo:
        urls = [linha.strip() for linha in arquivo if linha.strip()]
    return urls

# Função para salvar lista em um arquivo .txt
def salvar_em_arquivo(lista, nome_arquivo):
    with open(nome_arquivo, "w") as f:
        for item in lista:
            f.write(f"{item}\n")

# Função para testar URLs e exibir resultados organizados
def testar_urls(lista_urls):
    urls_ok = []
    urls_erro = []
    urls_falha = []

    for url in lista_urls:
        try:
            resposta = requests.get(url, timeout=5)
            if resposta.status_code == 200:
                urls_ok.append(url)
            else:
                urls_erro.append(f"{url} - Status {resposta.status_code}")
        except requests.exceptions.RequestException as e:
            urls_falha.append(f"{url} - Erro: {e}")

    # Exibe resultados organizados
    print("\n✅ URLs que responderam OK:")
    for url in urls_ok:
        print(f"   - {url}")

    print("\n⚠️ URLs que responderam com erro (status diferente de 200):")
    for url in urls_erro:
        print(f"   - {url}")

    print("\n❌ URLs que não responderam ou deram falha:")
    for url in urls_falha:
        print(f"   - {url}")

    # Resumo
    print(f"\nResumo Final:")
    print(f"Total testadas: {len(lista_urls)}")
    print(f"✔️ OK: {len(urls_ok)} | ⚠️ Erro: {len(urls_erro)} | ❌ Falha: {len(urls_falha)}")

    # Salvando em arquivos
    salvar_em_arquivo(urls_ok, "urls_ok.txt")
    salvar_em_arquivo(urls_erro, "urls_erro.txt")
    salvar_em_arquivo(urls_falha, "urls_falha.txt")

    print("\nResultados salvos em arquivos: urls_ok.txt, urls_erro.txt, urls_falha.txt")

# Caminho do arquivo de URLs
caminho_arquivo = "urls.txt"

# Leitura e execução
urls = ler_urls_do_arquivo(caminho_arquivo)
testar_urls(urls)