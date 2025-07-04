from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from pathlib import Path

class Bot_ODS():
     
    def baixa_arquivos(self, IP):
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
    
    def verifica_arquivos(self, IP):
        pasta = Path.home() / "Downloads"
        arquivo = pasta / "Base_de_Dados_IDSC-BR_2024.xlsx"

        if arquivo.exists():
            print("✅ Arquivo encontrado:", arquivo)
            return True
        else:
            print("⬇️  Arquivo não encontrado, iniciando download...")
            baixa_arquivos(IP)
            return True
    
    
    