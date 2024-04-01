import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import time, sleep
from openpyxl import Workbook
import PySimpleGUI as sg
import re
import sys
import csv
import os

def dividir_string_em_quatro_partes(texto):
    # Calcular o tamanho de cada parte
    tamanho_total = len(texto)
    tamanho_parte = tamanho_total // 4

    # Calcular os índices de divisão
    inicio_1, inicio_2, inicio_3 = 0, tamanho_parte, 2 * tamanho_parte
    fim_1, fim_2, fim_3 = tamanho_parte, 2 * tamanho_parte, 3 * tamanho_parte

    # Dividir a string em quatro partes
    parte_1 = texto[inicio_1:fim_1]
    parte_2 = texto[inicio_2:fim_2]
    parte_3 = texto[inicio_3:fim_3]
    parte_4 = texto[fim_3:]

    return parte_1, parte_2, parte_3, parte_4

def atualizar_barra_carregamento(indice, total_numeros, horas_restantes, minutos_restantes, segundos_restantes, progress_bar, porcentagem_text):
    
    taxa_progresso = indice / total_numeros

    progress_bar.update_bar(indice, total_numeros)

    porcentagem_text.update(f'{int(taxa_progresso * 100)}% | Faltam {int(total_numeros - indice)} contatos | Tempo Restante Estimado: {int(horas_restantes)}h {int(minutos_restantes)}m {int(segundos_restantes)}s')

def criar_grupo(progress_bar, porcentagem_text):

    navegador = webdriver.Chrome()
    navegador.get("https://web.whatsapp.com/")

    while len(navegador.find_elements(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas')) < 1:
        pass

    while len(navegador.find_elements(By.ID, 'side')) < 1:
        pass

    # Obter números do arquivo CSV
    numeros_do_csv = ler_numeros_csv()
    sleep(5)
    try:

        # Criando grupo
        criar_grupo = navegador.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/header/div[2]/div/span/div[5]/div')
        sleep(1)
        criar_grupo.click()

        # Novo grupo
        novo_grupo = navegador.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/header/div[2]/div/span/div[5]/span/div/ul/li[1]/div')
        sleep(1)
        novo_grupo.click()
        sleep(5)

        total_numeros = len(numeros_do_csv)
        tempo_inicial = time()

        # Acessando o campo de pesquisa
        sleep(5)
        campo_pesquisa1 = navegador.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div/div[1]/div/div/div[2]/input')
        sleep(10)
        for indice, numero in enumerate(numeros_do_csv, start=1):

            # Calcular o tempo decorrido
            tempo_decorrido = time() - tempo_inicial

            # Calcular a taxa de progresso
            taxa_progresso = indice / total_numeros

            # Calcular o tempo restante estimado
            tempo_restante_estimado = (tempo_decorrido / taxa_progresso) - tempo_decorrido

            # Formatar e imprimir o tempo restante estimado
            minutos_restantes, segundos_restantes = divmod(int(tempo_restante_estimado), 60)
            horas_restantes, minutos_restantes = divmod(minutos_restantes, 60)
            atualizar_barra_carregamento(indice, total_numeros, horas_restantes, minutos_restantes, segundos_restantes, progress_bar, porcentagem_text)

            parte1, parte2, parte3, parte4 = dividir_string_em_quatro_partes(str(numero))

            # Escrevendo o numero do telefone
            campo_pesquisa1.send_keys(parte1)
            sleep(0.05)
            campo_pesquisa1.send_keys(parte2)
            sleep(0.04)
            campo_pesquisa1.send_keys(parte3)
            sleep(0.05)
            campo_pesquisa1.send_keys(parte4)

            for i in range(12):
                try:
                    adicionar_numero = campo_pesquisa1.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div/div[2]/div[2]/div[2]')
                    adicionar_numero.click()
                    break
                except Exception:
                    sleep(0.3)
                    pass

            campo_pesquisa1.clear()
                


        avancar_grupo = navegador.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div/span/div')
        avancar_grupo.click()
        sleep(2.5)


        # Finaliza criação do grupo
        input("\nPressione ENTER para Continuar")
        finish_grpup = navegador.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[1]/span/div/span/div/div/span/div/div')
        finish_grpup.click()    

    except Exception as er:
        sg.popup_error(f"Error: {er}")           

def capturar_dados(grupo_nome, nome_contato):

    navegador = webdriver.Chrome()
    navegador.get("https://web.whatsapp.com/")

    while len(navegador.find_elements(By.XPATH, '//*[@id="app"]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas')) < 1:
        pass

    while len(navegador.find_elements(By.ID, 'side')) < 1:
        pass

    # Encontrar o elemento de pesquisa
    pesquisa_element = navegador.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/button/div[2]/span')   
    if pesquisa_element:
        pesquisa_element.click()
    else:
        print("Search button not found")


    try:
        # Acessando o campo de pesquisa
        campo_pesquisa = navegador.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div[1]/p')
        campo_pesquisa.clear()
        sleep(5)

        # Escrevendo o nome do grupo
        # Lista de grupos
        campo_pesquisa.send_keys(grupo_nome)
        sleep(2)

        # Clicando no grupo
        entrar_grupo = campo_pesquisa.find_element(By.XPATH, '//*[@id="pane-side"]/div[1]/div/div[contains(.,"Conversas")]/div[1]/div/div/div/div[2]')
        sleep(3)
        entrar_grupo.click()
                
        # Extrair números
        sleep(1.5)
        extrair_num_element = navegador.find_element(By.XPATH, '//*[@id="main"]/header/div[2]/div[2]/span')
        sleep(1.5)
        extrair_num = extrair_num_element.text.strip()
                
        # Dividir a string do número de telefone
        telefones = [telefone.strip() for telefone in extrair_num.split(',')]

        # Filtrar apenas linhas que contêm números de telefone
        telefones = [telefone for telefone in telefones if is_phone_number(telefone)]

        # Salvar no arquivo CSV
        with open("output.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["First Name", "Mobile Phone"])
            for telefone in telefones:
                writer.writerow([nome_contato, telefone])
    except Exception as e:
        print(f"Error: {e}")  

def remover_numero_csv(numero):

    with open("output.csv", 'r', newline='') as file:
        leitor_csv = csv.reader(file)
        linhas = list(leitor_csv)

    with open("output.csv", 'w', newline='') as file:
        escritor_csv = csv.writer(file)
        removido = False  # Flag para indicar se o número foi removido
        for linha in linhas:
            if linha and linha[1] == numero:
                removido = True
                continue  # Ignora a linha que contém o número a ser removido
            escritor_csv.writerow(linha)

        if removido:
            sg.popup(f"Número {numero} removido com sucesso!")
        else:
            sg.popup(f"Número {numero} não encontrado no CSV.")

def ler_numeros_csv():
    numeros = []
    with open("output.csv", 'r') as file:
        leitor_csv = csv.reader(file)
        for linha in leitor_csv:
            if linha:
                numeros.append(linha[1])  # Assumindo que os números estão na coluna B (índice 1)
    return numeros

def is_phone_number(line):
    return re.match(r'^[\d\s\+\-\(\)]+$', line) is not None

def main():
    layout = [
        [sg.Text("Nome dos Contatos:"), sg.Input(key='nome_contato')],
        [sg.Text("Nome do Grupo:"), sg.Input(key='grupo_nome')],
        [sg.Button("Capturar Dados")],
        [sg.Text('')],
        [sg.Text("Remover Número:"), sg.Input(key='numero')],
        [sg.Button("Remover Número")],
        [sg.Text('')],
        [sg.Button("Criar Grupo")],
        [sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS-', visible=False)],
        [sg.Text('0%', size=(80, 1), key='-PERCENTAGE-')],
    ]

    window = sg.Window("Clona Grupo Wpp", layout)

    while True:
        event, values = window.read(timeout=100)

        if event == sg.WIN_CLOSED:
            break

        if event == "Capturar Dados":
            grupo_nome = values['grupo_nome']
            nome_contato = values['nome_contato']

            try:
                capturar_dados(grupo_nome, nome_contato)

            except Exception as e:
                sg.popup_error(f"Erro ao capturar dados: {e}")

        elif event == "Remover Número":
            numero = values['numero']

            try:
                remover_numero_csv(numero)

            except Exception as e:
                sg.popup_error(f"Erro ao remover número: {e}")

        elif event == "Criar Grupo":
            try:
                # Exibir barra de carregamento
                window['-PROGRESS-'].update(visible=True)

                criar_grupo(window['-PROGRESS-'], window['-PERCENTAGE-'])

                # Esconder barra de carregamento após a conclusão
                window['-PROGRESS-'].update(visible=False)
                window['-PERCENTAGE-'].update('0%')

            except Exception as e:
                sg.popup_error(f"Erro ao criar grupo: {e}")

    window.close()

if __name__ == "__main__":
    main()