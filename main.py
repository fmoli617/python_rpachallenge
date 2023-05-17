'''
    Aplicação com o objetivo de realizar o desafio que se encontra na página: 'https://www.rpachallenge.com/'.
    
    Algumas informações sobre o desafio/script:

        - CADA LINHA DA TABELA PROPOSTA REPRESENTA UM PREENCHIMENTO DO FORMULARIO;
        - CADA VALOR DA TABELA REPRESENTA UM VALOR A SER PREENCHIDO NO VALOR DO CAMPO DO FORMULARIO;
        - NAO IREI IMPLEMENTAR UMA NOVA TENTATIVA CASO ALGUM CAMPO NAO TENHA SIDO LOCALIZADO, APENAS IREI INFORMAR NO LOG, SEGUINDO
          A IDEIA DE VALIDAR A PORCENTAGEM DE PREENCHIMENTOS CORRETOS ENTREGUE NO FINAL DO PROCESSAMENTO, VISTO QUE OS CAMPOS POSSUEM ALGUM IDENTIFICADOR NAO MUTAVEL
     
'''
__author__ = 'fmoli617'
__version__ = '1.0.0'

# BIBLIOTECAS e FUNCÕES UTILIZADAS
import os
import time
import pandas as pd
from utils.loggers import AppLogger
from selenium import webdriver
from utils.functions import pagina_carregada, preencher_campo, extrair_info_conclusao

# INICIO DE EXECUCAO

# Altera diretório atual para o diretório de execução.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# VARIAVEIS DE APOIO
PATH_XLSX = os.path.join('.\input', 'challenge.xlsx')
PATH_CHROMEDRIVE = os.path.join('.\input', 'chromedriver.exe')
URL_WEBSITE = 'https://www.rpachallenge.com/'
TEMPO_DE_ESPERA_PAGINA_INICIAL = 15
LOCALIZADOR_PAGINA_INICIAL = 'button.waves-effect.col.s12.m12.l12.btn-large.uiColorButton'
DICT_IDENTIFICADOR_WEB = {
    'First Name': '//input[@ng-reflect-name="labelFirstName"]',
    'Last Name ':  '//input[@ng-reflect-name="labelLastName"]',
    'Company Name': '//input[@ng-reflect-name="labelCompanyName"]',
    'Role in Company': '//input[@ng-reflect-name="labelRole"]',
    'Address': '//input[@ng-reflect-name="labelAddress"]',
    'Email': '//input[@ng-reflect-name="labelEmail"]',
    'Phone Number': '//input[@ng-reflect-name="labelPhone"]'   
}

# TRANSFORMANDO OS DADOS DO DATAFRAME
# Gerando dataframe original
df = pd.read_excel(os.path.join(PATH_XLSX),engine='openpyxl',)
# Limpando possivel linhas nulas
TABELA_INPUT = df.dropna()

# Inicia log de execução
log_filename = os.path.basename(__file__).lower().replace('.py', '.log')
logger = AppLogger.setup(log_filename=log_filename)
logger = AppLogger.instance()
logger.info(f'>>>>> START: RPA Challege')
logger.info(f'>\n')

# Abre um novo navagador web.
driver = webdriver.Chrome(executable_path=PATH_CHROMEDRIVE)
# Configura o navegador em tela maximizada.
driver.maximize_window()
# Carregar a URL à ser automatizada.
driver.get(URL_WEBSITE)

# Verifica a condição de se a página foi carregada corretamente
if pagina_carregada(driver, TEMPO_DE_ESPERA_PAGINA_INICIAL, LOCALIZADOR_PAGINA_INICIAL):
    logger.info(f'> Página Carregada! \n')

    # Clica no botão de inicio do desafio.
    start = driver.find_element_by_css_selector(LOCALIZADOR_PAGINA_INICIAL)
    start.click()
    logger.info(f'> Inicío do desafio: \n')
    
    # Percorrer cada linha da tabela.
    for i, linha in TABELA_INPUT .iterrows():
    
        logger.info(f'>PREENCHIMENTO LINHA: {i + 1}')
        
        # Para linha, preencher os campos de acordo com com a coluna.
        for coluna, valor in linha.items():
            
            # Case de formatacao
            if coluna == 'Phone Number':
                #valor = str(valor).replace('.0','')
                valor = str(int(valor))
            
            logger.info(f'>Campo: {coluna}, Valor: {valor}')
             
            # Tentar preeencher o campo.
            if preencher_campo(driver, DICT_IDENTIFICADOR_WEB[coluna], valor):
            
                # Se preencheido, aguardar.
                time.sleep(0.1)
                logger.info(f'>Campo preenchido.')
            
            else:
                # Se nao preechido
                logger.info(f'> Campo não preenchido.')
            
        # Em cada término de preechimento, clicar em "SUMBIT"
        submit = driver.find_element_by_css_selector("input.btn.uiColorButton[type='submit']")
        submit.click()
        logger.info(f'> LINHA: {i + 1} ENVIADA.\n')
    
    logger.info(f'> FIM DO PREENCHIMENTO')
    # Extrair as informações da final da execução
    element_texto_result = elemento_div = driver.find_element_by_xpath("//div[@class='message2']")
    tuple_info = extrair_info_conclusao(element_texto_result.text)
    logger.info(f'\n> RESULTADO: \n> Porcentagem de acerto: {tuple_info[0]}%.\n> Quantidade de campos preenchidos corretamente: {tuple_info[1]}.\n> Tempo gasto {tuple_info[2]} milisegundos')

# Algum erro ao carregar a página inicial    
else:        
    logger.info(f'> ERRO AO CARREGAR A PAGINA INICIAL')
    
driver.quit()
logger.info(f'\n> END: RPA Challege')