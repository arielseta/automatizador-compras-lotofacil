import sys
from io import BufferedReader, TextIOWrapper
from pathlib import Path
from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

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


def esperar_elemento(browser, xpathcode: str) -> None:
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
    WebDriverWait(browser, 10).until(EC.presence_of_element_located(
        (By.XPATH, xpathcode))
    )


# Verifica existencia do arquivo de credenciais.
if not Path.exists(ARQUIVO_CREDENCIAIS):
    print('Arquivo "credenciais.txt" não foi encontrado!')
    sys.exit()
else:
    print('Arquivo "credenciais.txt" localizado!')

# Carrega as credenciais do arquivo.
with open(ARQUIVO_CREDENCIAIS, 'r', encoding='utf8') as arquivo:
    for linha in arquivo:
        if linha.strip().find('username') == 0:
            USERNAME = (linha.strip().split('='))[1]
        if linha.strip().find('senha') == 0:
            SENHA = (linha.strip().split('='))[1]

# Valida as credenciais.
if USERNAME == '' or SENHA == '':
    print('Não foi encontrado os parâmetros no arquivo credenciais.txt')
    sys.exit()
else:
    print('Credenciais carregadas.')

# Verifica existencia do arquivo de jogos.
if not Path.exists(ARQUIVO_JOGOS):
    print('Arquivo "jogos.txt" não foi encontrado!')
    sys.exit()
else:
    print('Arquivo "jogos.txt" localizado!')

# Valida se o arquivo está em UTF8
with open(ARQUIVO_JOGOS, 'rb') as buffer_arquivo:
    bom: bytes = buffer_arquivo.read(3)
    if bom == b"\xef\xbb\xbf":
        print('Arquivo "jogos.txt" não está no formato UTF8!')
        sys.exit()

# Cria o componente para o navegador Chrome.
service: Service = Service(ChromeDriverManager().install())
nav: WebDriver = webdriver.Chrome(service=service)

# Abre o navegador em tela maximizada.
nav.implicitly_wait(3)
nav.maximize_window()
nav.get("https://www.loteriasonline.caixa.gov.br/silce-web/#/lotofacil")
print('Navegador aberto.')

# Clica no elemento 'botaosim'
esperar_elemento(nav, '//*[@id="botaosim"]')
nav.find_element(By.XPATH, '//*[@id="botaosim"]').click()
print('Sim clicado.')
sleep(0.5)

if nav.find_element(By.XPATH, '//*[@id="adopt-reject-all-button"]'):
    esperar_elemento(nav, '//*[@id="adopt-reject-all-button"]')
    nav.find_element(By.XPATH, '//*[@id="adopt-reject-all-button"]').click()

# Clica no elemento 'btnLogin'
esperar_elemento(nav, '//*[@id="btnLogin"]')
nav.find_element(By.XPATH, '//*[@id="btnLogin"]').click()
print('Acessar clicado.')

# Preenche o elemento 'username' com o CPF
esperar_elemento(nav, '//*[@id="username"]')
nav.find_element(By.XPATH, '//*[@id="username"]').send_keys(USERNAME)
print('username preenchido.')

# Clica no elemento 'button-submit'
esperar_elemento(nav, '//*[@id="button-submit"]')
nav.find_element(By.XPATH, '//*[@id="button-submit"]').click()
print('Proximo clicado.')

# Espera por 3s para Escolher o email ou telefone para receber o código
# de validação.
# Caso não selecionar ele irá para o selecionado por padrao.
print('aguardando selecao para receber o codigo validacao.')
sleep(3)

# Clica no elemento 'button[1]' (Receber código)
esperar_elemento(nav, '//*[@id="form-login"]/div[2]/button[1]')
nav.find_element(By.XPATH, '//*[@id="form-login"]/div[2]/button[1]').click()
print('Receber codigo clicado.')

# Clica no elemento 'codigo' para setar o focus do input do teclado.
esperar_elemento(nav, '//*[@id="codigo"]')
nav.find_element(By.XPATH, '//*[@id="codigo"]').click()
print('focus no codigo.')

# Espera por 20s para você digitar o código de validação recebido.
print('aguardando codigo de validacao.')
sleep(20)

# Clica no elemento 'button[1]' (Enviar)
esperar_elemento(nav, '//*[@id="form-login"]/div[3]/button[1]')
nav.find_element(By.XPATH, '//*[@id="form-login"]/div[3]/button[1]').click()
print('Enviar clicado.')

# Preenche o elemento 'password' com a senha
esperar_elemento(nav, '//*[@id="password"]')
nav.find_element(By.XPATH, '//*[@id="password"]').send_keys(SENHA)

# Clica no elemento 'button' (Enviar)
esperar_elemento(nav, '//*[@id="template-section"]/form[1]/div/button')
nav.find_element(
    By.XPATH, '//*[@id="template-section"]/form[1]/div/button').click()
sleep(2)

# Clica no elemento 'button' (Entrar)
esperar_elemento(nav, '/html/body/div[3]/div/ul[3]/li/a/figure/h3')
nav.find_element(
    By.XPATH, '/html/body/div[3]/div/ul[3]/li/a/figure/h3').click()
print('Entrar clicado.')

# Clica no elemento 'a' (Aposte já)
esperar_elemento(nav, '/html/body/div[2]/header/div[4]/div[1]/div/a')
nav.find_element(
    By.XPATH, '/html/body/div[2]/header/div[4]/div[1]/div/a').click()
print('Aposte já clicado.')
sleep(0.5)

# Abre o arquivo.csv que contem as apostas
with open(ARQUIVO_JOGOS, 'r', encoding='utf8') as arquivo:
    for linha in arquivo:
        for dezena in linha.strip().split('-'):
            if dezena == '01':
                nav.find_element(By.XPATH, '//*[@id="n01"]').click()
                print('Dezena 01 clicado.')
            elif dezena == '02':
                nav.find_element(By.XPATH, '//*[@id="n02"]').click()
                print('Dezena 02 clicado.')
            elif dezena == '03':
                nav.find_element(By.XPATH, '//*[@id="n03"]').click()
                print('Dezena 03 clicado.')
            elif dezena == '04':
                nav.find_element(By.XPATH, '//*[@id="n04"]').click()
                print('Dezena 04 clicado.')
            elif dezena == '05':
                nav.find_element(By.XPATH, '//*[@id="n05"]').click()
                print('Dezena 05 clicado.')
            elif dezena == '06':
                nav.find_element(By.XPATH, '//*[@id="n06"]').click()
                print('Dezena 06 clicado.')
            elif dezena == '07':
                nav.find_element(By.XPATH, '//*[@id="n07"]').click()
                print('Dezena 07 clicado.')
            elif dezena == '08':
                nav.find_element(By.XPATH, '//*[@id="n08"]').click()
                print('Dezena 08 clicado.')
            elif dezena == '09':
                nav.find_element(By.XPATH, '//*[@id="n09"]').click()
                print('Dezena 09 clicado.')
            elif dezena == '10':
                nav.find_element(By.XPATH, '//*[@id="n10"]').click()
                print('Dezena 10 clicado.')
            elif dezena == '11':
                nav.find_element(By.XPATH, '//*[@id="n11"]').click()
                print('Dezena 11 clicado.')
            elif dezena == '12':
                nav.find_element(By.XPATH, '//*[@id="n12"]').click()
                print('Dezena 12 clicado.')
            elif dezena == '13':
                nav.find_element(By.XPATH, '//*[@id="n13"]').click()
                print('Dezena 13 clicado.')
            elif dezena == '14':
                nav.find_element(By.XPATH, '//*[@id="n14"]').click()
                print('Dezena 14 clicado.')
            elif dezena == '15':
                nav.find_element(By.XPATH, '//*[@id="n15"]').click()
                print('Dezena 15 clicado.')
            elif dezena == '16':
                nav.find_element(By.XPATH, '//*[@id="n16"]').click()
                print('Dezena 16 clicado.')
            elif dezena == '17':
                nav.find_element(By.XPATH, '//*[@id="n17"]').click()
                print('Dezena 17 clicado.')
            elif dezena == '18':
                nav.find_element(By.XPATH, '//*[@id="n18"]').click()
                print('Dezena 18 clicado.')
            elif dezena == '19':
                nav.find_element(By.XPATH, '//*[@id="n19"]').click()
                print('Dezena 19 clicado.')
            elif dezena == '20':
                nav.find_element(By.XPATH, '//*[@id="n20"]').click()
                print('Dezena 20 clicado.')
            elif dezena == '21':
                nav.find_element(By.XPATH, '//*[@id="n21"]').click()
                print('Dezena 21 clicado.')
            elif dezena == '22':
                nav.find_element(By.XPATH, '//*[@id="n22"]').click()
                print('Dezena 22 clicado.')
            elif dezena == '23':
                nav.find_element(By.XPATH, '//*[@id="n23"]').click()
                print('Dezena 23 clicado.')
            elif dezena == '24':
                nav.find_element(By.XPATH, '//*[@id="n24"]').click()
                print('Dezena 24 clicado.')
            elif dezena == '25':
                nav.find_element(By.XPATH, '//*[@id="n25"]').click()
                print('Dezena 25 clicado.')
            else:
                print(f'Dezena |{dezena}| nao encontrada. ')
        # Clica no elemento 'colocarnocarrinho' (Colocar no carrinho)
        nav.find_element(By.XPATH, '//*[@id="colocarnocarrinho"]').click()
        print('Colocar no carrinho clicado.')
        sleep(0.5)
        # Rola pagina para encaixar a exibição
        ActionChains(nav).scroll_to_element(nav.find_element(
            By.XPATH, '/html/body/div[2]/header/div[4]/div[1]/div/a')
            ).perform()
        print('Rolagem na pagina.')
        sleep(0.5)
        # Clica no elemento 'a' (Aposte já)
        nav.find_element(
            By.XPATH, '/html/body/div[2]/header/div[4]/div[1]/div/a').click()
        print('Aposte já clicado.')
        sleep(0.5)
print('Apostas efetuadas com sucesso!')
