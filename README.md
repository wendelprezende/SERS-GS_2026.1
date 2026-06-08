  SUSTAINABLE MISSION CONTROL - GS 2026.1
  Missão Espacial Experimental

1. DESCRIÇÃO DO PROJETO
-----------------------
  O Sustainable Mission Control é um sistema de monitoramento operacional desenvolvido em Python para acompanhar em tempo real os sistemas energéticos de uma missão espacial experimental.
  
   O sistema recebe dados simulados de sensores da nave, analisa as condições criticas, gera alertas automáticos e registra ações de resposta do sistema diante de situações de risco. O histórico completo de leituras fica armazenado em memória durante toda a sessão.

   A solução aplica diretamente conceitos de energias renováveis e sustentabilidade ao monitorar a geração solar dos painéis fotovoltaicos da nave e o status do módulo de captação de energia renovável, os quais são elementos centrais para a autossuficiência energética de missões de longa duração.

2. CONCEITOS APLICADOS — ENERGIAS RENOVÁVEIS
--------------------------------------------
   Em missões espaciais reais, a energia elétrica é gerada quase que exclusivamente por painéis solares fotovoltaicos. Esses painéis convertem a radiação solar diretamente em corrente elétrica, carregando as baterias da nave e alimentando seus sistemas.

O princípio central é o de potência (P), em Watts:

  P = V x I

   Quanto maior a potência gerada pelos painéis, mais energia (Watt/hora) fica disponível para a operação da nave. Quando a geração cai abaixo do mínimo necessário, o sistema precisa acionar um modo de economia para preservar a bateria que resta.

   O módulo de energia renovável representa o conjunto de circuitos responsáveis por captar, regular e distribuir essa energia solar para os demais sistemas da nave. Se esse módulo for desativado com a bateria abaixo de 50%, a nave perde sua principal fonte sustentável de energia, o que seria a situação crítica que o sistema detecta e sinaliza automaticamente.

3. FUNCIONALIDADES DO SISTEMA
-----------------------------
O sistema oferece cinco funções acessíveis pelo menu:

  1. Inserir dados dos sensores
     Coleta cinco leituras do usuário, valida cada entrada e registra um novo dicionário no histórico da missão.

  2. Visualizar status atual
     Exibe os dados da leitura mais recente, incluindo todos os alertas e ações automáticas associados a leitura.

  3. Executar análise
     Percorre todo o histórico e exibe médias, totais, relatório de sustentabilidade e leitura mais crítica.

  4. Histórico de leituras
     Lista todas as leituras registradas na sessão, da mais antiga para a mais recente.

  5. Encerrar sistema
     Finaliza o programa.

4. DADOS MONITORADOS POR LEITURA
--------------------------------
Cada leitura armazena os seguintes campos:

  - id
  - temperatura (em °C)
  - energia (em %)
  - comunicacao (0 ou 1)
  - geracao_solar (potência gerada em Watts)
  - modulo_energia (0 = inativo / 1 = ativo)
  - dataHora (dateTime)
  - alertas
  - acoes_automaticas (disparadas pelo sistema)

5. LÓGICA DE ALERTAS E AÇÕES AUTOMÁTICAS
----------------------------------------
A função analise_leitura() avalia cinco condições:

  Condição | Alerta gerado
  ------------------------
  Temperatura > 80°C | Superaquecimento detectado
  Energia < 20% | Nível crítico de energia
  Comunicacao = 0 | Falha de comunicacao
  Geracao solar < 50W | Painel comprometido
  Modulo inativo + Energia < 50% | Módulo renovável crítico

Ações automáticas disparadas:

  - Energia < 20% -> Modo economia ativado
                     Sistemas não essenciais suspensos
  - Comunicação = 0 -> Tentativa de reconexão iniciada
  - Módulo inativo
    + Energia < 50% -> Reativação do módulo solicitada

   Alertas e ações são armazenados como listas dentro do dicionário de cada leitura, permitindo recuperá-los depois na análise e no histórico.

6. EXPLICAÇÃO DO CÓDIGO 
-----------------------
ESTRUTURA DE DADOS PRINCIPAL
  historico_missao = []

  Lista Python que armazena todos os dicionários de leitura.
  Cada chamada a inserir_dado() adiciona um novo elemento ao final da lista via .append(). A ordem é sempre da leitura mais antiga para a mais recente.

  contador_leituras = 0

  Variável global incrementada a cada inserção. Gera o ID único de cada leitura. É declarada global dentro de inserir_dado() para que a função possa modificá-la.

----

FUNÇÃO divisoria()
  Imprime uma linha de hífens. Usada para separar visualmente as seções de saída no terminal.

----

FUNÇÃO analise_leitura(leitura)
  Recebe um dicionário com os cinco sensores.
  Cria dois arrays vazios: alertas e acoes_automaticas.
  Percorre cinco condições com estruturas if independentes (não elif, pois múltiplos alertas podem ser gerados ao mesmo tempo). Para cada condição verdadeira, adiciona uma string ao array correspondente.
  Retorna os dois arrays ao final.

----

FUNÇÃO inserir_dado()
  Usa loops while True para garantir que cada campo seja validado antes de avancar. Quando o valor digitado é inválido, o loop recomeça e pede nova entrada.
  O try/except ValueError captura entradas que não podem ser convertidas para float ou int.

  Após coletar os cinco valores, chama analise_leitura() e monta o dicionário nova_leitura com todos os dados, incluindo os alertas já gerados. Esse dicionário é adicionado ao historico_missao com .append().

  Por fim, exibe na tela os alertas e ações gerados.

----

FUNÇÃO visualizar_status()
  Verifica se historico_missao está vazia.
  Se sim, informa que não há leituras e retorna.
  Se não, acessa historico_missao[-1], o último elemento da lista, ou seja, a leitura mais recente, e exibe todos os seus campos formatados.

----

FUNÇÃO exec_analise()
  Percorre historico_missao com for i in range(len(...)) acumulando soma de temperatura, energia e geração solar. Conta o total de alertas, ações e leituras com módulo ativo. Ao final calcula as médias com round(..., 2).

  Exibe também o RELATÓRIO DE SUSTENTABILIDADE:
  - Média de geração solar
  - Percentual de leituras com módulo ativo
  - Classificação de eficiência: Boa / Regular / Crítica

  Identifica a leitura mais crítica comparando o tamanho da lista de alertas de cada leitura com max_alertas.

----

FUNÇÃO mostrar_historico()
  Usa enumerate(historico_missao) para percorrer a lista obtendo ao mesmo tempo o índice e o dicionário de cada leitura. 
  Exibe os dados em ordem cronológica (do mais antigo ao mais recente, pois a lista cresce pelo final).

----

FUNÇÃO mostrar_menu()
  Loop while True com if/elif para cada opção numérica.
  Chama a função correspondente a cada escolha válida.
  A opção 5 chama sys.exit(0), encerrando o processo.
  Opções inválidas exibem mensagem de erro sem quebrar o loop, retornando ao menu automaticamente.

----

PONTO DE ENTRADA
  O bloco if __name__ == "__main__" garante que o código só executa quando o arquivo é rodado diretamente, exibindo o cabeçalho e chamando mostrar_menu().

7. COMO EXECUTAR
----------------
Pré-requisito: Python 3 instalado.

No terminal, dentro da pasta do projeto:

  python gs_sers.py

8. EXEMPLO DE USO
-----------------
Ao iniciar o sistema, o menu principal será exibido.
Escolha a opção 1 para inserir uma leitura:

  Temperatura da nave (°C): 85
  Nível de energia (%): 15
  Status da comunicação (0/1): 1
  Geração solar dos painéis (W): 30
  Módulo de energia renovável (0/1): 0

Saída esperada:

  >> ALERTA: Superaquecimento detectado (Temperatura > 80°C)
  >> ALERTA: Nível crítico de energia (< 20%)
  >> ALERTA: Baixa geração solar (< 50 W) - Painel comprometido
  >> ALERTA: Módulo de energia renovável inativo com bateria baixa
  >> AÇÃO AUTOMÁTICA: Modo economia de energia ativado
  >> AÇÃO AUTOMÁTICA: Sistemas não essenciais suspensos
  >> AÇÃO AUTOMÁTICA: Reativação do módulo de energia solicitada
