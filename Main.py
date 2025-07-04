from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pathlib import Path
import pandas as pd
import time
import os
import matplotlib.pyplot as plt

def baixa_arquivos():
    # Inicia o navegador
    navegador = webdriver.Chrome()
    navegador.get('https://idsc.cidadessustentaveis.org.br')

    # Clica no botão de download (ícone SVG)
    navegador.find_element(By.CSS_SELECTOR, "svg.DownloadButton__StyledSvgIcon-bf6n0i-0.HEpJY").click()

    # Muda para a nova aba
    abas = navegador.window_handles
    navegador.switch_to.window(abas[1])

    wait = WebDriverWait(navegador, 20)

    # Abre o formulário de download
    wait.until(EC.element_to_be_clickable((By.ID, "btn_agenda"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "cidade")))

    # Seleciona a cidade
    option = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//mat-option//span[contains(text(), 'Santa Cruz do Sul - Rio Grande do Sul - Brasil')]"
    )))
    option.click()

    # Preenche os campos do formulário
    actions = webdriver.ActionChains(navegador)
    actions.send_keys(Keys.TAB).send_keys("lucasemgarth@gmail.com").send_keys(Keys.TAB)
    time.sleep(0.5)
    actions.send_keys("Leonardo André Muller").send_keys(Keys.TAB)
    time.sleep(0.5)
    actions.send_keys("Unisc").perform()

    time.sleep(3)

    # Clica no botão Confirmar
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Confirmar']]"))).click()

    # Aguarda o download
    time.sleep(10)

# Caminho portátil para a pasta Downloads do usuário
pasta = Path.home() / "Downloads"
arquivo = pasta / "Base_de_Dados_IDSC-BR_2024.xlsx"

if arquivo.exists():
    print("✅ Arquivo encontrado:", arquivo)
else:
    print("⬇️  Arquivo não encontrado, iniciando download...")
    baixa_arquivos()

def filtrar_ods(cidades_rs, numero_ods):

    municipio = 'MUNICIPIO'
    coluna_score = f'Goal {numero_ods} Score'
    colunas_ods = cidades_rs.filter(like=f'SDG{numero_ods}_').columns
    
    if coluna_score not in cidades_rs.columns:
        print(f"Aviso: Coluna '{coluna_score}' não encontrada.")
        return pd.DataFrame()
    
    return cidades_rs[[municipio, coluna_score] + list(colunas_ods)]

def main():
    nome_arquivo = 'Base_de_Dados_IDSC-BR_2024.xlsx'
    
    df = pd.read_excel(nome_arquivo, sheet_name='IDSC-BR 2024')
    livro_df = pd.read_excel(nome_arquivo, sheet_name='Livro de Códigos')

    cidades_rs = df.loc[df['SIGLA_UF'] == 'RS'].copy()
    cidades_rs.reset_index(drop=True, inplace=True)

    for i in range(1, 18):
        coluna_para_remover = f'ODS{i}_reg'
        if coluna_para_remover in cidades_rs.columns:
            cidades_rs.drop(columns=coluna_para_remover, inplace=True)

    cidades_rs['MUNICIPIO'] = cidades_rs['MUNICIPIO'].str.strip()

    try:
        numero_ods = int(input('Digite o número da ODS (1-17): '))
        if not 1 <= numero_ods <= 17:
            print("Número da ODS deve estar entre 1 e 17")
            return
    except ValueError:
        print("Por favor, digite um número válido.")
        return

    ods_escolhida = filtrar_ods(cidades_rs, numero_ods)
    
    ods_escolhida = ods_escolhida.sort_values(by=f'Goal {numero_ods} Score', ascending=False).reset_index(drop=True)

    if not ods_escolhida.empty:
        print(f"\nDados da ODS {numero_ods}:")
        print(ods_escolhida.head(10))
        print(ods_escolhida.tail(10))
        
        santa_cruz = ods_escolhida[ods_escolhida['MUNICIPIO'] == 'Santa Cruz do Sul']
        if not santa_cruz.empty:
            print(f"\nDados da ODS {numero_ods} para Santa Cruz do Sul:")
            print(santa_cruz)
    else:
        print(f"Não foram encontrados dados para a ODS {numero_ods}") 

    ods_grafico = ods_escolhida.head(10)
    tail_grafico = ods_escolhida.tail(10)
    ods_grafico = pd.concat([ods_grafico, tail_grafico], ignore_index=True)

    existe = 'Santa Cruz do Sul' in ods_grafico.values

    if existe is False:    
        ods_grafico = pd.concat([ods_grafico, santa_cruz], ignore_index=True)
    
    ods_grafico = ods_grafico.sort_values(by=f'Goal {numero_ods} Score', ascending=False)
    
    ods_grafico.plot(x='MUNICIPIO', y=[f'Goal {numero_ods} Score'], kind='bar', figsize=(10, 6), color=['#1f77b4', '#ff7f0e'])

    plt.title('Pontuação da ODS')
    plt.ylabel('Puntuação')
    plt.xlabel('Cidade')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()
    #time.sleep(5)
    #plt.close()

    municipios = ods_escolhida['MUNICIPIO']
    colunas = ods_escolhida.filter(like='Normalizado')
    normalizados = pd.concat([municipios, colunas], axis=1)

    coluna_normalizados = normalizados.columns.tolist()
    tamanho_normalizados = len(normalizados)
    i=1

    while i < tamanho_normalizados:
        titulo = coluna_normalizados[i]

        normalizados = normalizados.sort_values(by=titulo, ascending=False)  

        head_normalizados = normalizados.head(10)
        tail_normalizados = normalizados.tail(10)
        normalizados_grafico = pd.concat([head_normalizados, tail_normalizados], ignore_index=True)

        santa_cruz_normalizados = normalizados[normalizados['MUNICIPIO'] == 'Santa Cruz do Sul']
        
        existe_normalizados = 'Santa Cruz do Sul' in normalizados_grafico.values

        if existe_normalizados is False:    
           normalizados_grafico = pd.concat([normalizados_grafico, santa_cruz_normalizados], ignore_index=False)

        normalizados_grafico = normalizados_grafico.sort_values(by=titulo, ascending=False) 

        normalizados_grafico.plot(x='MUNICIPIO', y=titulo, kind='bar', figsize=(10, 6), color=['#1f77b4', '#ff7f0e'])

        plt.title('Pontuação do índice')
        plt.ylabel('Puntuação')
        plt.xlabel('Cidade')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend(loc='upper right')
        plt.tight_layout()
        plt.show()
        i+=1
        
    livro_codigos = livro_df[livro_df['ODS'] == numero_ods]

    #with pd.ExcelWriter("DataFrame da ODS.xlsx") as writer:
        #livro_codigos.to_excel(writer, sheet_name= "Livro Códigos.xlsx", index=False)
        #ods_escolhida.to_excel(writer, sheet_name=f"ODS_{numero_ods}_IDSC-BR_2024.xlsx", index=False)

main()