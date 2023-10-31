from FuncsForSPO.fgpt.__fgpt import *

def gpt(prompt, headless=True):
    """
    Runs a GPTBot with the given prompt and returns the generated text.
    
    :param prompt: A string representing the prompt to generate text from.
    :type prompt: str
    :param headless: A boolean flag indicating whether to run the bot in headless mode. Defaults to False.
    :type headless: bool
    :return: A string representing the generated text.
    :rtype: str
    """
    if isinstance(prompt, str):
        prompt = re.sub(r'[\n\t\r\f\v\\]', '', prompt)
        app = GPTBot(prompt, headless)
        return app.run().replace("GPT_RESPOSTA", '').strip()
    else:
        prompt_to_gpt = {}
        for chave, valor in prompt.items():
            prompt_to_gpt[chave] = re.sub(r'[\n\t\r\f\v\\]', '', valor)
        app = GPTBot(prompt_to_gpt, headless)
        return app.run()
        


def cria_diretorios_para_novo_projeto_python(with_draft=False, create_base_dir:bool=True, packages:str='FuncsForSPO'):
    """# ATENÇÃO, UTILIZAR SOMENTE UMA VEZ NO MOMENTO DA CRIAÇÃO DO NOVO PROJETO!
    
    create_base_dir: cria o diretorio para o user colocar a base
    packages: instala pacotes necessários
    
    with_draft deve ser como nesse exemplo:
        # 1. importe from src.base.base import * no app.py
        # 2. crie um bot com o uso abaixo que entre nesse site: https://www.pythonanywhere.com/login/
        # 3. envie o usuário que virá no arquivo config.json em BOT USUARIO nesse seletor: #id_auth-username
        # 4. envie também a senha que virá no arquivo config.json em BOT SENHA nesse seletor: #id_auth-password
        # 5. e clique em login nesse seletor: #id_next
        # 6. espere 5 segundos
        
        o resultado esperado no arquivo app.py é:
        
        >>> from src.base.base import *
        >>> class RobotClass(Bot):
        >>>    def __init__(self) -> None:
        >>>        self.configs = read_json(CONFIG_PATH)
        >>>        self.HEADLESS = self.configs['BOT']['HEADLESS']
        >>>        self.DOWNLOAD_FILES = False
        >>>        super().__init__(self.HEADLESS, self.DOWNLOAD_FILES)
        >>>        
        >>>    def run(self):
        >>>        self.DRIVER.get("https://www.pythonanywhere.com/login/")
        >>>        username = self.configs['BOT']['USUARIO']
        >>>        password = self.configs['BOT']['SENHA']
        >>>        self.WDW10.until(EC.presence_of_element_located((By.ID, 'id_auth-username')))
        >>>        self.DRIVER.find_element_by_id('id_auth-username').send_keys(username)
        >>>        self.DRIVER.find_element_by_id('id_auth-password').send_keys(password)
        >>>        self.DRIVER.find_element_by_id('id_next').click()
        >>>        time.sleep(5) # Espera 5 segundos antes de encerrar a execução.
    """
    faz_log('Criando pasta e arquivo de logs com esse log...')
    # cria diretório src
    cria_dir_no_dir_de_trabalho_atual('src')
    APP_PATH = arquivo_com_caminho_absoluto(['src', 'app'], 'app.py')
    BASE_PATH = arquivo_com_caminho_absoluto(['src', 'base'], 'base.py')
    DATABASE_PATH = arquivo_com_caminho_absoluto(['src', 'database'], 'database.py')
    EXCEPTIONS_PATH = arquivo_com_caminho_absoluto(['src', 'exceptions'], 'exceptioins.py')
    CONFIG_PATH = arquivo_com_caminho_absoluto(['bin'], 'config.json')
    UTILS_PATH = arquivo_com_caminho_absoluto(['src', 'utils'], 'utils.py')
    TESTS_PATH = arquivo_com_caminho_absoluto(['src', 'tests'], 'tests.py')
    # cria subdiretorios do src

    if not isinstance(with_draft, str):
        # CRIA ARQUIVO PYTHON EM SRC\\APP
        with open(APP_PATH, 'w', encoding='utf-8') as f:
            f.write("""from src.base.base import *
class RobotClass(Bot):
    def __init__(self) -> None:
        self.configs = read_json(CONFIG_PATH)
        self.HEADLESS = self.configs['BOT']['HEADLESS']
        self.DOWNLOAD_FILES = False
        super().__init__(self.HEADLESS, self.DOWNLOAD_FILES)

    def run(self):
        self.DRIVER.get("https://google.com.br")  # aqui já está usando selenium dando get
    """)
    else:
        print('Criando arquivo com draft... É MUITO IMPORTANTE VOCÊ VER SE FICOU BOM COMO O GPT ESCREVEU O CÓDIGO!\nEscreve apenas no arquivo app.py, se precisar colocar dados do usuário no Json, adiicone manualmente')
        # CRIA ARQUIVO PYTHON EM SRC\\APP
        from FuncsForSPO.utils.utils import GPT_WITH_DRAFT_PROMPT
        response_gpt = gpt(GPT_WITH_DRAFT_PROMPT.replace('DRAFT_USER', with_draft))
        with open(APP_PATH, 'w', encoding='utf-8') as f:
            f.write(f"""from src.base.base import *
class RobotClass(Bot):
    def __init__(self) -> None:
        self.configs = read_json(CONFIG_PATH)
        self.HEADLESS = self.configs['BOT']['HEADLESS']
        self.DOWNLOAD_FILES = False
        super().__init__(self.HEADLESS, self.DOWNLOAD_FILES)
        
    {response_gpt}
""")

    # CRIA ARQUIVO PYTHON EM base
    with open(BASE_PATH, 'w', encoding='utf-8') as f:
        f.write("""from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *
from webdriver_manager.chrome import ChromeDriverManager
from FuncsForSPO.fpython.functions_for_py import *
from FuncsForSPO.fselenium.functions_selenium import *
from FuncsForSPO.fwinotify.fwinotify import *
from FuncsForSPO.fregex.functions_re import *
import pandas as pd
import json
import os

# -- GLOBAL -- #
URL_SUPORTE = f'https://api.whatsapp.com/send?phone=5511985640273'
CONFIG_PATH = arquivo_com_caminho_absoluto('bin', 'config.json')
BASE = os.path.abspath('base')
DOWNLOAD_DIR =  cria_dir_no_dir_de_trabalho_atual(dir='downloads', print_value=False, criar_diretorio=True)
limpa_diretorio(DOWNLOAD_DIR)
# -- GLOBAL -- #

class Bot:    
    def __init__(self, headless, download_files) -> None:
        # --- CHROME OPTIONS --- #
        self._options = ChromeOptions()
        
        if download_files:
            # --- PATH BASE DIR --- #
            self._SETTINGS_SAVE_AS_PDF = {
                        "recentDestinations": [
                            {
                                "id": "Save as PDF",
                                "origin": "local",
                                "account": ""
                            }
                        ],
                        "selectedDestinationId": "Save as PDF",
                        "version": 2,
                    }


            self._PROFILE = {'printing.print_preview_sticky_settings.appState': json.dumps(self._SETTINGS_SAVE_AS_PDF),
                    "savefile.default_directory":  f"{DOWNLOAD_DIR}",
                    "download.default_directory":  f"{DOWNLOAD_DIR}",
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "profile.managed_default_content_settings.images": 2,
                    "safebrowsing.enabled": True}
                
            self._options.add_experimental_option('prefs', self._PROFILE)
        
        if headless == True:
            self._options.add_argument('--headless')
            
        self._options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
        self._options.add_experimental_option('useAutomationExtension', False)
        self.user_agent = cria_user_agent()
        self._options.add_argument(f"--user-agent=self.user_agent")
        self._options.add_argument("--disable-web-security")
        self._options.add_argument("--allow-running-insecure-content")
        self._options.add_argument("--disable-extensions")
        self._options.add_argument("--start-maximized")
        self._options.add_argument("--no-sandbox")
        self._options.add_argument("--disable-setuid-sandbox")
        self._options.add_argument("--disable-infobars")
        self._options.add_argument("--disable-webgl")
        self._options.add_argument("--disable-popup-blocking")
        self._options.add_argument('--disable-gpu')
        self._options.add_argument('--disable-software-rasterizer')
        self._options.add_argument('--no-proxy-server')
        self._options.add_argument("--proxy-server='direct://'")
        self._options.add_argument('--proxy-bypass-list=*')
        self._options.add_argument('--disable-dev-shm-usage')
        self._options.add_argument('--block-new-web-contents')
        self._options.add_argument('--incognito')
        self._options.add_argument('–disable-notifications')
        self._options.add_argument("--window-size=1920,1080")
        self._options.add_argument('--kiosk-printing')

        
        self.__service = Service(ChromeDriverManager().install())
        
        # create DRIVER
        self.DRIVER = Chrome(service=self.__service, options=self._options)
        
        def enable_download_in_headless_chrome(driver, download_dir):
            '''
            Esse código adiciona suporte ao navegador Chrome sem interface gráfica (headless) no Selenium WebDriver para permitir o download automático de arquivos em um diretório especificado.

            Mais especificamente, o código adiciona um comando ausente "send_command" ao executor de comando do driver e, em seguida, executa um comando "Page.setDownloadBehavior" para permitir o download automático de arquivos no diretório especificado.

            O primeiro passo é necessário porque o suporte para o comando "send_command" não está incluído no Selenium WebDriver por padrão. O segundo passo usa o comando "Page.setDownloadBehavior" do Chrome DevTools Protocol para permitir o download automático de arquivos em um diretório especificado.

            Em resumo, o código adiciona suporte para o download automático de arquivos em um diretório especificado no Chrome sem interface gráfica usando o Selenium WebDriver.
            '''
            driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

            params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
            command_result = driver.execute("send_command", params)
        enable_download_in_headless_chrome(self.DRIVER, DOWNLOAD_DIR)
        
        
        self.WDW3 = WebDriverWait(self.DRIVER, timeout=3)
        self.WDW5 = WebDriverWait(self.DRIVER, timeout=5)
        self.WDW7 = WebDriverWait(self.DRIVER, timeout=7)
        self.WDW10 = WebDriverWait(self.DRIVER, timeout=10)
        self.WDW30 = WebDriverWait(self.DRIVER, timeout=30)
        self.WDW = self.WDW7

        self.DRIVER.maximize_window()
        return self.DRIVER
""")
    
    # CRIA ARQUIVO PYTHON EM database
    with open(DATABASE_PATH, 'w', encoding='utf-8') as f:
        f.write("""from FuncsForSPO.fpython.functions_for_py import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

engine = create_engine('sqlite:///database.db', pool_size=15, max_overflow=20)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class TABLE(Base):
    __tablename__ = 'table'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String)
    nome = Column(String)
    
Base.metadata.create_all(engine)  # cria a tabela no banco de dados

    
class DBManager:
    def __init__(self):
        # Inicializa uma nova sessão com o banco de dados.
        
        self.session = Session()

    def create_item(self, status, name):
        # Cria um novo registro na tabela.

        new_item = TABLE(status=status, name=name)
        self.session.add(new_item)
        self.session.commit()

    def get_item(self, id):
        # Retorna o registro com o ID fornecido
        return self.session.query(TABLE).filter_by(id=id).first()
    

    def delete_item(self, id):
        # Exclui o registro com o ID fornecido da tabela

        delete_item_from_db = self.get_item(id)
        self.session.delete(delete_item_from_db)
        self.session.commit()
        
    def delete_all(self):
        # Exclui todos os registros da tabela.

        self.session.query(TABLE).delete()
        self.session.commit()

    def get_item(self, id):
        # Retorna o registro com o ID fornecido da tabela. Se nenhum registro for encontrado, retorna None.
        return self.session.query(TABLE).filter_by(id=id).first()
    

    def get_column_status(self):
        # Retorna o registro de status com o ID fornecido da tabela. Se nenhum registro for encontrado, retorna None.
        return self.session.query(TABLE.status).all()
    
    

""")
    
    # CRIA ARQUIVO PYTHON EM exceptions
    with open(EXCEPTIONS_PATH, 'w', encoding='utf-8') as f:
        f.write("""from FuncsForSPO.fexceptions.exceptions import *
""")
    
    # cria arquivo json
    with open(CONFIG_PATH, 'w', encoding='utf-8') as fjson:
        fjson.write("""{
    "BOT": {
        "USER": "USER",
        "PASSWORD": "PASSWORD",
        "HEADLESS": true
        }
}""")
        
    # cria arquivo utils
    with open(UTILS_PATH, 'w', encoding='utf-8') as fjson:
        fjson.write("""""")

    # cria arquivo de tests
    with open(TESTS_PATH, 'w', encoding='utf-8') as fjson:
        fjson.write("""from FuncsForSPO.fpdf.focr.orc import *
from FuncsForSPO.fpdf.fcompress.compress import *
from FuncsForSPO.fpdf.fimgpdf.img_to_pdf import *
from FuncsForSPO.fpysimplegui.functions_for_sg import *
from FuncsForSPO.fpython.functions_for_py import *
from FuncsForSPO.fregex.functions_re import *
from FuncsForSPO.fselenium.functions_selenium import *
import sys
import os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

# SEMPRE COLOQUE O QUE A FUNÇÃO TEM QUE FAZER EXPLICITAMENTE
""")

    # cria diretório base
    if create_base_dir:
        cria_dir_no_dir_de_trabalho_atual('base')

    # cria ambiente virtual
    # if os.path.exists('venv'):
    #     print('Ambiente Virtual "venv" já criado')
    #     print('Baixando pacotes')
    #     os.system(f'.\\venv\\Scripts\\pip.exe install {packages}')
    #     pass
    # else:
    print('Criando Ambiente Virtual')
    os.system('python -m venv venv')
    print('Criado!')
    print('Baixando pacotes')
    os.system(f'.\\venv\Scripts\\pip.exe install {packages}')
    