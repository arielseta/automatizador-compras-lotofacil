import logging
import sys
from io import BufferedReader, TextIOWrapper
from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Configuração básica
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
nav: WebDriver
dezenas_xpath: dict[str, str]
# Alterar para False se desejar fechar o navegador automaticamente
debug_mode: bool = True


def clicar_elemento(nav: WebDriver, xpathcode: str, tentativas: int = 3) -> bool:
    for tentativa in range(tentativas):
        if esperar_elemento(nav, xpathcode):
            try:
                nav.find_element(By.XPATH, xpathcode).click()
                logging.info(f'Elemento {xpathcode} clicado.')
                return True
            except Exception as e:
                logging.warning(f"Tentativa {tentativa+1} falhou: {e}")
        sleep(1)
    logging.critical(f"Falha ao clicar no elemento {xpathcode} após {tentativas} tentativas.")
    return False


def esperar_elemento(browser: WebDriver, xpathcode: str, timeout: int = 10) -> bool:
    try:
        WebDriverWait(browser, timeout).until(EC.element_to_be_clickable((By.XPATH, xpathcode)))
        return True
    except TimeoutException:
        logging.warning(f"Elemento {xpathcode} não encontrado após {timeout} segundos.")
        return False


def preencher_campo(nav: WebDriver, xpathcode: str, valor: str):
    if esperar_elemento(nav, xpathcode):
        nav.find_element(By.XPATH, xpathcode).send_keys(valor)
        logging.info(f'{valor} preenchido no elemento {xpathcode}.')
        return True
    logging.critical(f"Elemento {xpathcode} não encontrado!")
    return False


def encerrar_navegador(nav: WebDriver):
    if not debug_mode:
        logging.info("Encerrando navegador.")
        nav.quit()
    sys.exit()


def login(nav: WebDriver):
    try:
        # Clica no elemento 'btnLogin'
        clicar_elemento(nav, '//*[@id="btnLogin"]')
        # Preenche o elemento 'username' com o CPF
        preencher_campo(nav, '//*[@id="username"]', USERNAME)
        # Clica no elemento 'button-submit'
        clicar_elemento(nav, '//*[@id="button-submit"]')
        # Clica no elemento 'button[1]' (Receber código)
        clicar_elemento(nav, '//*[@id="form-login"]/div[2]/button[1]')
    except Exception as e:
        logging.critical(f"Erro durante o login: {e}")
        encerrar_navegador(nav)


def efetuar_apostas(nav: WebDriver, linha: str):
    for dezena in linha.strip().split('-'):
        xpath = dezenas_xpath.get(dezena)
        if xpath and esperar_elemento(nav, xpath):
            clicar_elemento(nav, xpath)
        else:
            logging.error(f'Dezena |{dezena}| não encontrada ou elemento não clicável.')


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
    logging.critical('Não foi encontrado os parâmetros no arquivo credenciais.txt')
    sys.exit()
else:
    logging.info('Credenciais carregadas.')

# Verifica existencia do arquivo de jogos.
if not Path.exists(ARQUIVO_JOGOS):
    logging.critical('Arquivo "jogos.txt" não foi encontrado!')
    sys.exit()
else:
    logging.info('Arquivo "jogos.txt" localizado!')

# Valida a composição das apostas.
with open(ARQUIVO_JOGOS, 'r', encoding='utf8') as arquivo:
    for index, linha in enumerate(arquivo):
        dezenas = linha.strip().split('-')
        if len(dezenas) not in range(15, 21):
            logging.critical(f'Aposta mal formatada na linha {index + 1}: {linha}')
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
if not clicar_elemento(nav, '//*[@id="botaosim"]'):
    encerrar_navegador(nav)

# Clica no elemento 'adopt-reject-all-button'
if esperar_elemento(nav, '//*[@id="adopt-reject-all-button"]'):
    sleep(0.5)
    clicar_elemento(nav, '//*[@id="adopt-reject-all-button"]')

# Efetua processo de login no site.
login(nav)

# Clica no elemento 'codigo' para setar o focus do input do teclado.
if not clicar_elemento(nav, '//*[@id="codigo"]'):
    encerrar_navegador(nav)

nav.minimize_window()
codigo_validacao = input("Digite o código de validação e pressione Enter para continuar...")
if len(codigo_validacao.strip()) == 6:
    if not preencher_campo(nav, '//*[@id="codigo"]', codigo_validacao):
        encerrar_navegador(nav)
else:
    logging.critical('Código de validação inválido.')
    encerrar_navegador(nav)
nav.maximize_window()

# Clica no elemento 'button[1]' (Enviar)
if not clicar_elemento(nav, '//*[@id="form-login"]/div[3]/button[1]'):
    encerrar_navegador(nav)

# Preenche o elemento 'password' com a senha
if not preencher_campo(nav, '//*[@id="password"]', SENHA):
    encerrar_navegador(nav)

# Clica no elemento 'button' (Enviar)
if not clicar_elemento(nav, '//*[@id="template-section"]/form[1]/div/button'):
    encerrar_navegador(nav)

# Clica no elemento 'button' (Entrar)
if not clicar_elemento(nav, '/html/body/div[3]/div/ul[3]/li/a/figure/h3'):
    encerrar_navegador(nav)

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
        ActionChains(nav).scroll_to_element(
            nav.find_element(By.XPATH, '/html/body/div[2]/header/div[4]/div[1]/div/a')
        ).perform()
        logging.info('Rolagem na pagina.')

        # Clica no elemento 'a' (Aposte já)
        if not clicar_elemento(nav, '/html/body/div[2]/header/div[4]/div[1]/div/a'):
            encerrar_navegador(nav)

        # Efetua as apostas da linha.
        sleep(0.5)
        efetuar_apostas(nav, linha)

        # Clica no elemento 'colocarnocarrinho' (Colocar no carrinho)
        if not clicar_elemento(nav, '//*[@id="colocarnocarrinho"]'):
            encerrar_navegador(nav)
logging.info('Apostas efetuadas com sucesso!')
encerrar_navegador(nav)
