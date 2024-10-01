import sys
from io import BufferedReader, TextIOWrapper
from pathlib import Path
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Configuração básica
logging.basicConfig(
    level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s'
)

# Compatível com versao_sistema_apostador 2.98.19.10

# Variaveis
ARQUIVO_JOGOS: Path
ARQUIVO_CREDENCIAIS: Path
ARQUIVO_JOGOS = Path(__file__).parent / 'jogos.txt'
ARQUIVO_CREDENCIAIS = Path(__file__).parent / 'credenciais.txt'
USERNAME: str = ''
SENHA: str = ''
linha: str = ''
dezena: str = ''
arquivo: TextIOWrapper
buffer_arquivo: BufferedReader
dezenas_xpath: dict[str, str]


def esperar_elemento(browser, xpathcode: str) -> bool:
    """[Espera até que certo elemento WebElent seja criado no browser]

    Args:
        xpathcode (str): [Código xpath do elemento]
    """
    # Classe de espera
    from selenium.webdriver.support.ui import WebDriverWait
    # Classe de condição
    from selenium.webdriver.support import expected_conditions as EC

    # WebDriverWait(browser, segs).util(condição) ->  Espera por alguns
    # segundos até que uma condição seja comprida, por padrão essa condição
    # é verificada a cada 500 milisegundos até que o tempo segs expire;
    # EC.presence_of_element_located(localizador) -> Verifica se um elemento
    # já existe retorna um bool. O localizador (locator) é uma tupla
    # (By.XPATH, CÓDIGO exPATH)
    try:
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpathcode))
        )
        return True
    except TimeoutException:
        return False


# Verifica existencia do arquivo de credenciais.
if not Path.exists(ARQUIVO_CREDENCIAIS):
    logging.critical('Arquivo "credenciais.txt" não foi encontrado!')
    sys.exit()
else:
    logging.info('Arquivo "credenciais.txt" localizado!')

# Carrega as credenciais do arquivo.
with open(ARQUIVO_CREDENCIAIS, 'r', encoding='utf8') as arquivo:
    for linha in arquivo:
        if linha.strip().find('username') == 0:
            USERNAME = (linha.strip().split('='))[1]
        if linha.strip().find('senha') == 0:
            SENHA = (linha.strip().split('='))[1]

# Valida as credenciais.
if USERNAME == '' or SENHA == '':
    logging.critical(
        'Não foi encontrado os parâmetros no arquivo credenciais.txt'
    )
    sys.exit()
else:
    logging.info('Credenciais carregadas.')

# Verifica existencia do arquivo de jogos.
if not Path.exists(ARQUIVO_JOGOS):
    logging.critical('Arquivo "jogos.txt" não foi encontrado!')
    sys.exit()
else:
    logging.info('Arquivo "jogos.txt" localizado!')

with open(ARQUIVO_JOGOS, 'r', encoding='utf8') as arquivo:
    for linha in arquivo:
        if '-' not in linha:
            logging.critical(f'Aposta mal formatada: {linha}')
            sys.exit()

# Valida se o arquivo está em UTF8
with open(ARQUIVO_JOGOS, 'rb') as buffer_arquivo:
    bom: bytes = buffer_arquivo.read(3)
    if bom == b"\xef\xbb\xbf":
        logging.critical('Arquivo "jogos.txt" não está no formato UTF8!')
        sys.exit()

# Cria o componente para o navegador Chrome.
nav = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Abre o navegador em tela maximizada.
nav.implicitly_wait(3)
nav.maximize_window()
nav.get("https://www.loteriasonline.caixa.gov.br/silce-web/#/lotofacil")
logging.info('Navegador aberto.')

# Clica no elemento 'botaosim'
try:
    esperar_elemento(nav, '//*[@id="botaosim"]')
    nav.find_element(By.XPATH, '//*[@id="botaosim"]').click()
    logging.info('Sim clicado.')
    sleep(0.5)
except Exception as e:
    logging.critical(f"Erro ao clicar em 'Sim': {e}")
    nav.quit()

# Clica no elemento 'adopt-reject-all-button'
try:
    if nav.find_element(By.XPATH, '//*[@id="adopt-reject-all-button"]'):
        esperar_elemento(nav, '//*[@id="adopt-reject-all-button"]')
        nav.find_element(
            By.XPATH, '//*[@id="adopt-reject-all-button"]'
        ).click()
except Exception:
    ...

# Clica no elemento 'btnLogin'
try:
    esperar_elemento(nav, '//*[@id="btnLogin"]')
    nav.find_element(By.XPATH, '//*[@id="btnLogin"]').click()
    logging.info('Acessar clicado.')
except Exception as e:
    logging.critical(f"Erro ao clicar em 'Acessar': {e}")
    nav.quit()

# Preenche o elemento 'username' com o CPF
try:
    esperar_elemento(nav, '//*[@id="username"]')
    nav.find_element(By.XPATH, '//*[@id="username"]').send_keys(USERNAME)
    logging.info('username preenchido.')
except Exception as e:
    logging.critical(f"Erro ao preencher CPF: {e}")
    nav.quit()

# Clica no elemento 'button-submit'
try:
    esperar_elemento(nav, '//*[@id="button-submit"]')
    nav.find_element(By.XPATH, '//*[@id="button-submit"]').click()
    logging.info('Proximo clicado.')
except Exception as e:
    logging.critical(f"Erro ao clicar em 'Próximo': {e}")
    nav.quit()

# Espera por 3s para Escolher o email ou telefone para receber o código
# de validação.
# Caso não selecionar ele irá para o selecionado por padrao.
logging.info('Aguardando seleção para receber o código de validação.')
sleep(3)

# Clica no elemento 'button[1]' (Receber código)
try:
    esperar_elemento(nav, '//*[@id="form-login"]/div[2]/button[1]')
    nav.find_element(
        By.XPATH, '//*[@id="form-login"]/div[2]/button[1]'
    ).click()
    logging.info('Receber código clicado.')
except Exception as e:
    logging.critical(f"Erro ao clicar em 'Receber código': {e}")
    nav.quit()

# Clica no elemento 'codigo' para setar o focus do input do teclado.
esperar_elemento(nav, '//*[@id="codigo"]')
nav.find_element(By.XPATH, '//*[@id="codigo"]').click()
logging.info('Focus no código.')

# Espera por 20s para você digitar o código de validação recebido.
logging.info('Aguardando digitar código de validação.')
sleep(20)

# Clica no elemento 'button[1]' (Enviar)
try:
    esperar_elemento(nav, '//*[@id="form-login"]/div[3]/button[1]')
    nav.find_element(
        By.XPATH, '//*[@id="form-login"]/div[3]/button[1]'
    ).click()
    logging.info('Enviar clicado.')
except Exception as e:
    logging.critical(f"Erro ao clicar em 'Enviar': {e}")
    nav.quit()

# Preenche o elemento 'password' com a senha
try:
    esperar_elemento(nav, '//*[@id="password"]')
    nav.find_element(By.XPATH, '//*[@id="password"]').send_keys(SENHA)
    logging.info('password preenchido.')
except Exception as e:
    logging.critical(f"Erro ao preencher 'password': {e}")
    nav.quit()

# Clica no elemento 'button' (Enviar)
try:
    esperar_elemento(nav, '//*[@id="template-section"]/form[1]/div/button')
    nav.find_element(
        By.XPATH, '//*[@id="template-section"]/form[1]/div/button').click()
    sleep(2)
    logging.info('Enviar clicado.')
except Exception as e:
    logging.critical(f"Erro ao clicar em 'Enviar': {e}")
    nav.quit()

# Clica no elemento 'button' (Entrar)
try:
    esperar_elemento(nav, '/html/body/div[3]/div/ul[3]/li/a/figure/h3')
    nav.find_element(
        By.XPATH, '/html/body/div[3]/div/ul[3]/li/a/figure/h3').click()
    logging.info('Entrar clicado.')
except Exception as e:
    logging.critical(f"Erro ao clicar em 'Entrar': {e}")
    nav.quit()

dezenas_xpath = {
    '01': '//*[@id="n01"]',
    '02': '//*[@id="n02"]',
    '03': '//*[@id="n03"]',
    '04': '//*[@id="n04"]',
    '05': '//*[@id="n05"]',
    '06': '//*[@id="n06"]',
    '07': '//*[@id="n07"]',
    '08': '//*[@id="n08"]',
    '09': '//*[@id="n09"]',
    '10': '//*[@id="n10"]',
    '11': '//*[@id="n11"]',
    '12': '//*[@id="n12"]',
    '13': '//*[@id="n13"]',
    '14': '//*[@id="n14"]',
    '15': '//*[@id="n15"]',
    '16': '//*[@id="n16"]',
    '17': '//*[@id="n17"]',
    '18': '//*[@id="n18"]',
    '19': '//*[@id="n19"]',
    '20': '//*[@id="n20"]',
    '21': '//*[@id="n21"]',
    '22': '//*[@id="n22"]',
    '23': '//*[@id="n23"]',
    '24': '//*[@id="n24"]',
    '25': '//*[@id="n25"]'
}

# Abre o arquivo.csv que contem as apostas
with open(ARQUIVO_JOGOS, 'r', encoding='utf8') as arquivo:
    for linha in arquivo:
        # Rola pagina para encaixar a exibição
        ActionChains(nav).scroll_to_element(nav.find_element(
            By.XPATH, '/html/body/div[2]/header/div[4]/div[1]/div/a')
            ).perform()
        logging.info('Rolagem na pagina.')
        sleep(0.5)
        # Clica no elemento 'a' (Aposte já)
        try:
            esperar_elemento(
                nav, '/html/body/div[2]/header/div[4]/div[1]/div/a'
            )
            nav.find_element(
                By.XPATH, '/html/body/div[2]/header/div[4]/div[1]/div/a'
            ).click()
            logging.info('Aposte já clicado.')
            sleep(0.5)
        except Exception as e:
            logging.critical(f"Erro ao clicar em 'Aposte já': {e}")
            nav.quit()
        for dezena in linha.strip().split('-'):
            xpath = dezenas_xpath.get(dezena)
            if xpath:
                try:
                    nav.find_element(By.XPATH, xpath).click()
                    logging.info(f'Dezena {dezena} clicado.')
                except Exception as e:
                    logging.critical(f"Erro ao clicar {dezena}: {e}")
                    nav.quit()
            else:
                logging.error(f'Dezena |{dezena}| nao encontrada.')
        # Clica no elemento 'colocarnocarrinho' (Colocar no carrinho)
        try:
            nav.find_element(By.XPATH, '//*[@id="colocarnocarrinho"]').click()
            logging.info('Colocar no carrinho clicado.')
            sleep(0.5)
        except Exception as e:
            logging.critical(f"Erro ao clicar em 'Colocar no carrinho': {e}")
            nav.quit()
logging.info('Apostas efetuadas com sucesso!')
