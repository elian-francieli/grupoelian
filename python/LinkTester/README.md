README - LinkTester

## Descrição

   Este utilitário executável (linktester.exe) foi desenvolvido para testar a disponibilidade de uma lista de URLs e enviar um relatório por e-mail com os resultados. Ele é ideal para monitoramento periódico de links internos ou externos, e pode ser agendado para execução automática em servidores Windows.

## ⚙️ Arquivos utilizados

1. config.env
   - Contém as credenciais de autenticação para envio de e-mail via Microsoft Graph API.
   - Variáveis esperadas:
     CLIENT_ID, TENANT_ID, CLIENT_SECRET

2. urls.txt
   - Lista de URLs a serem testadas.
   - Cada linha deve conter uma URL válida.

3. Logs/
   - Pasta onde são salvos os relatórios de execução.
   - Cada log é salvo com data e hora no nome do arquivo (ex: log_2025-07-03_14-30-00.txt).

## 🪄 Funcionamento

- O executável lê as URLs do arquivo urls.txt.
- Para cada URL, ele realiza uma requisição HTTP e classifica como:
  - ✔️ OK (resposta 200)
  - ⚠️ Erro (resposta diferente de 200)
  - ❌ Falha (timeout, conexão recusada, etc.)
- Um resumo e a lista de resultados são enviados por e-mail no corpo da mensagem.
- O mesmo conteúdo é salvo em um arquivo de log na pasta Logs.

## 🖥️ Como agendar no Windows Server

1. Copie os arquivos para uma pasta no servidor (ex: C:\Scripts\LinkTester).
2. Crie uma tarefa no Agendador de Tarefas do Windows:
   - Ação: Iniciar um programa
   - Programa/script: C:\Scripts\LinkTester\linktester.exe
   - Marque:
     - ✅ Executar se o usuário estiver conectado ou não
     - ✅ Executar com privilégios mais altos

## 🛠️ Desenvolvimento

Este projeto foi desenvolvido em **Python** utilizando o **Visual Studio Code (VSCode)**.  
Os arquivos-fonte estão disponíveis no repositório GitHub vinculado ao e-mail corporativo:  
**francieli.p@elian.com.br**