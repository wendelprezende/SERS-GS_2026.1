# SUSTAINABLE MISSION CONTROL - GS 2026.1
# Sistema de monitoramento de sistemas energéticos de missão espacial experimental

from datetime import datetime

historico_missao = []

contador_leituras = 0

# Linha para organizar o terminal visualmente 
def divisoria():
    print("--------------------------------------------")

# Recebe um dicionario de leitura e verifica cada condição crítica do sistema
# Percorre as condições com if/elif e adiciona strings ao array 'alertas'
# Retorna a lista de alertas (pode estar vazia se tudo estiver normal)
# Também retorna uma lista de ações automáticas disparadas pelo sistema
def analise_leitura(leitura):
    alertas = []
    acoes_automaticas = []

    # Condição 1: Temperatura acima de 80 graus indica risco de superaquecimento
    if leitura["temperatura"] > 80:
        alertas.append("ALERTA: Superaquecimento detectado (Temperatura > 80 °C)")

    # Condição 2: Energia abaixo de 20% exige modo de economia imediata
    if leitura["energia"] < 20:
        alertas.append("ALERTA: Nivel critico de energia (< 20%)")
        # Resposta automática disparada pelo sistema diante da condição crítica
        acoes_automaticas.append("AÇÃO AUTOMÁTICA: Modo economia de energia ativado")
        acoes_automaticas.append("AÇÃO AUTOMÁTICA: Sistemas não essenciais suspensos")

    # Condição 3: comunicação igual a 0 significa falha total de sinal
    if leitura["comunicacao"] == 0:
        alertas.append("ALERTA: Falha de comunicação detectada")
        # Resposta automática para falha de comunicação
        acoes_automaticas.append("AÇÃO AUTOMÁTICA: Tentativa de reconexão iniciada")

    # Condição 4: Geração solar abaixo de 50W indica painel comprometido
    if leitura["geracao_solar"] < 50:
        alertas.append("ALERTA: Baixa geração solar (< 50 W) - Painel comprometido")

    # Condição 5: Módulo de energia renovável desativado com bateria abaixo de 50%
    if leitura["modulo_energia"] == 0 and leitura["energia"] < 50:
        alertas.append("ALERTA: Módulo de energia renovável inativo com bateria baixa")
        acoes_automaticas.append("AÇÃO AUTOMÁTICA: Reativação do módulo de energia solicitada")

    return alertas, acoes_automaticas

# Coleta os cinco dados dos sensores via input, valida cada entrada e monta o dicionário de leitura para armazenar no histórico
def inserir_dado():
    global contador_leituras

    divisoria()
    print("INSERIR NOVA LEITURA DE SENSORES")
    divisoria()

    # - Leitura e validação da temperatura
    # ValueError é capturado quando o input não pode virar float
    temperatura = None
    while True:
        entrada = input("Temperatura da nave (°C): ").strip()
        try:
            temperatura = float(entrada)
            break
        except ValueError:
            print("Valor inválido. Digite um número.")

    # - Leitura e validação da energia
    energia = None
    while True:
        entrada = input("Nível de energia (%): ").strip()
        try:
            energia = float(entrada)
            if 0 <= energia <= 100:
                break
            else:
                print("Valor inválido. Digite um número entre 0 e 100.")
        except ValueError:
            print("Valor inválido. Digite um número entre 0 e 100.")

    # - Leitura e validação da comunicação
    # Aceita apenas 0 (falha) ou 1 (operacional)
    comunicacao = None
    while True:
        entrada = input("Status da comunicação (0 = falha / 1 = operacional): ").strip()
        try:
            comunicacao = int(entrada)
            if comunicacao == 0 or comunicacao == 1:
                break
            else:
                print("Valor inválido. Digite 0 ou 1.")
        except ValueError:
            print("Valor inválido. Digite 0 ou 1.")

    # - Leitura e validação da geração solar
    # Representa a potência gerada pelos painéis solares da nave em Watts
    # E a principal fonte de energia renovável do sistema
    geracao_solar = None
    while True:
        entrada = input("Geração solar dos painéis (W): ").strip()
        try:
            geracao_solar = float(entrada)
            if geracao_solar >= 0:
                break
            else:
                print("Valor inválido. Digite um número maior ou igual a zero.")
        except ValueError:
            print("Valor inválido. Digite um número.")

    # - Leitura e validação do módulo de energia renovável
    # 0 = modulo desativado, 1 = modulo ativo
    modulo_energia = None
    while True:
        entrada = input("Módulo de energia renovável (0 = inativo / 1 = ativo): ").strip()
        try:
            modulo_energia = int(entrada)
            if modulo_energia == 0 or modulo_energia == 1:
                break
            else:
                print("Valor inválido. Digite 0 ou 1.")
        except ValueError:
            print("Valor inválido. Digite 0 ou 1.")

    # - Incrementa o contador e captura a data e a hora atual
    contador_leituras += 1
    data_hora = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    # - Analisa as condições críticas e gera alertas e ações automáticas
    alertas, acoes_automaticas = analise_leitura({
        "temperatura": temperatura,
        "energia": energia,
        "comunicacao": comunicacao,
        "geracao_solar": geracao_solar,
        "modulo_energia": modulo_energia
    })

    # - Monta o dicionário de leitura com todos os dados coletados
    nova_leitura = {
        "id": contador_leituras,
        "temperatura": temperatura,
        "energia": energia,
        "comunicacao": comunicacao,
        "geracao_solar": geracao_solar,
        "modulo_energia": modulo_energia,
        "dataHora": data_hora,
        "alertas": alertas,
        "acoes_automaticas": acoes_automaticas
    }

    # Adiciona o dicionário ao final da lista de histórico
    historico_missao.append(nova_leitura)

    divisoria()
    print("Leitura #" + str(nova_leitura["id"]) + " registrada em " + data_hora)

    # Exibe imediatamente os alertas gerados, se houver
    if len(nova_leitura["alertas"]) > 0:
        print("Alertas gerados:")
        for alerta in nova_leitura["alertas"]:
            print(" >> " + alerta)
    else:
        print("Status: Todos os parâmetros dentro do normal.")

    # Exibe as ações automáticas disparadas, se houver
    if len(nova_leitura["acoes_automaticas"]) > 0:
        print("Ações automáticas do sistema:")
        for acao in nova_leitura["acoes_automaticas"]:
            print(" >> " + acao)

    divisoria()


# Exibe os dados da última leitura registrada (elemento mais recente da lista)
def visualizar_status():
    divisoria()
    print("STATUS ATUAL DA MISSÃO")
    divisoria()

    # Verifica se há pelo menos uma leitura no histórico
    if len(historico_missao) == 0:
        print("Nenhuma leitura registrada ainda.")
        divisoria()
        return

    # Acessa o último elemento da lista (leitura mais recente)
    ultima = historico_missao[-1]

    print("Leitura ID    : #" + str(ultima["id"]))
    print("Data/Hora     : " + ultima["dataHora"])
    print("Temperatura   : " + str(ultima["temperatura"]) + " C")
    print("Energia       : " + str(ultima["energia"]) + "%")

    if ultima["comunicacao"] == 1:
        comunicacao_str = "Operacional"
    else:
        comunicacao_str = "FALHA"
    print("Comunicação   : " + comunicacao_str)

    # Exibe dados do sistema de energia renovável
    print("Geração Solar : " + str(ultima["geracao_solar"]) + " W")

    if ultima["modulo_energia"] == 1:
        modulo_str = "Ativo"
    else:
        modulo_str = "INATIVO"
    print("Módulo Energia: " + modulo_str)

    # Exibe alertas ou confirmação de normalidade
    if len(ultima["alertas"]) > 0:
        print("Alertas:")
        for a in ultima["alertas"]:
            print(" >> " + a)
    else:
        print("Alertas: Nenhum - Sistema normal")

    # Exibe ações automáticas registradas para essa leitura
    if len(ultima["acoes_automaticas"]) > 0:
        print("Ações automáticas registradas:")
        for acao in ultima["acoes_automaticas"]:
            print(" >> " + acao)

    divisoria()


# Percorre todas as leituras e gera relatório com estatísticas acumuladas
def exec_analise():
    divisoria()
    print("ANÁLISE COMPLETA DO HISTÓRICO")
    divisoria()

    if len(historico_missao) == 0:
        print("Nenhuma leitura para analisar.")
        divisoria()
        return

    # Variáveis para calcular médias
    soma_temp = 0
    soma_energia = 0
    soma_solar = 0
    total_alertas = 0
    total_acoes = 0

    # Variáveis para identificar a leitura mais crítica
    leitura_critica = None
    max_alertas = 0

    # Contador de leituras com módulo de energia ativo
    leituras_modulo_ativo = 0

    # Percorre cada leitura da lista e acumula os valores
    for i in range(len(historico_missao)):
        leitura = historico_missao[i]

        soma_temp += leitura["temperatura"]
        soma_energia += leitura["energia"]
        soma_solar += leitura["geracao_solar"]
        total_alertas += len(leitura["alertas"])
        total_acoes += len(leitura["acoes_automaticas"])

        # Conta quantas leituras tinham o módulo de energia renovável ativo
        if leitura["modulo_energia"] == 1:
            leituras_modulo_ativo += 1

        # Verifica se essa leitura tem mais alertas que o máximo registrado
        if len(leitura["alertas"]) > max_alertas:
            max_alertas = len(leitura["alertas"])
            leitura_critica = leitura

    total_leituras = len(historico_missao)

    # Calcula as médias 
    media_temp = round(soma_temp / total_leituras, 2)
    media_energia = round(soma_energia / total_leituras, 2)
    media_solar = round(soma_solar / total_leituras, 2)

    # Calcula o percentual de leituras com módulo ativo
    percentual_modulo_ativo = round((leituras_modulo_ativo / total_leituras) * 100, 2)

    print("Total de leituras      : " + str(total_leituras))
    print("Média de temperatura   : " + str(media_temp) + " C")
    print("Média de energia       : " + str(media_energia) + "%")
    print("Total de alertas       : " + str(total_alertas))
    print("Total de ações autom.  : " + str(total_acoes))

    # Relatório de energia renovável
    divisoria()
    print("RELATÓRIO DE SUSTENTABILIDADE")
    divisoria()
    print("Média de geração solar : " + str(media_solar) + " W")
    print("Leituras c/ módulo ativo: " + str(leituras_modulo_ativo) + " de " + str(total_leituras) + " (" + str(percentual_modulo_ativo) + "%)")

    # Avalia o nivel de aproveitamento da energia solar
    if media_solar >= 100:
        print("Eficiência energética  : Boa - Geração solar satisfatória")
    elif media_solar >= 50:
        print("Eficiência energética  : Regular - Geração solar abaixo do ideal")
    else:
        print("Eficiência energética  : Crítica - Geração solar insuficiente")

    divisoria()

    # Exibe a leitura mais crítica, se houver pelo menos um alerta
    if leitura_critica is not None and max_alertas > 0:
        print("Leitura mais crítica: #" + str(leitura_critica["id"]) + " (" + str(max_alertas) + " alerta(s))")
        for a in leitura_critica["alertas"]:
            print(" >> " + a)
        if len(leitura_critica["acoes_automaticas"]) > 0:
            print("Ações automáticas tomadas:")
            for acao in leitura_critica["acoes_automaticas"]:
                print(" >> " + acao)
    else:
        print("Nenhum alerta em todo o histórico.")

    divisoria()


# Exibe todas as leituras registradas na lista historico_missao
def mostrar_historico():
    divisoria()
    print("HISTÓRICO COMPLETO DE LEITURAS")
    divisoria()

    if len(historico_missao) == 0:
        print("Nenhuma leitura registrada.")
        divisoria()
        return

    for indice, leitura in enumerate(historico_missao):
        print("[" + str(indice + 1) + "] ID #" + str(leitura["id"]) + " - " + leitura["dataHora"])

        if leitura["comunicacao"] == 1:
            comunicacao_str = "OK"
        else:
            comunicacao_str = "FALHA"

        if leitura["modulo_energia"] == 1:
            modulo_str = "Ativo"
        else:
            modulo_str = "Inativo"

        print("    Temp: " + str(leitura["temperatura"]) + " C | Energia: " + str(leitura["energia"]) + "% | Comunicacao: " + comunicacao_str)
        print("    Solar: " + str(leitura["geracao_solar"]) + " W | Módulo de energia: " + modulo_str)

        if len(leitura["alertas"]) > 0:
            for a in leitura["alertas"]:
                print("    >> " + a)
            if len(leitura["acoes_automaticas"]) > 0:
                for acao in leitura["acoes_automaticas"]:
                    print("    >> " + acao)
        else:
            print("    Status: Normal")

    divisoria()


# Exibe as opções do menu, lê a escolha do usuário e chama a função correspondente
# O loop while True mantém o sistema rodando até que o usuário decida encerrar com a opção 5
def mostrar_menu():
    import sys

    # Loop
    while True:
        print("- MENU PRINCIPAL -")
        divisoria()
        print("1. Inserir dados dos sensores")
        print("2. Visualizar status atual")
        print("3. Executar análise")
        print("4. Histórico de leituras")
        print("5. Encerrar sistema")
        divisoria()

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            inserir_dado()

        elif opcao == "2":
            visualizar_status()

        elif opcao == "3":
            exec_analise()

        elif opcao == "4":
            mostrar_historico()

        elif opcao == "5":
            divisoria()
            print("Sistema encerrado.")
            divisoria()
            sys.exit(0)

        else:
            print("Opção inválida. Digite um número de 1 a 5.")


# Ponto de entrada do programa
if __name__ == "__main__":
    print("SUSTAINABLE MISSION CONTROL - GS 2026.1")
    print("Missão Espacial Experimental")
    mostrar_menu()
