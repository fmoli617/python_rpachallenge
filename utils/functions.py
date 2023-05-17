import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def extrair_info_conclusao (texto: str) -> tuple:
    """
    Funcao para ser executada ao termino dos inputs afim de buscar do texto informações a serem inputadas, retornando uma tupla com 3 informaçòes,
    A - Porcentagem de acerto;
    B - Campos preenchidos com sucesso;
    C - Tempo em milisegundos.
    
    :param texto: string a ser avaliada
    :returns: tuple com as informações descritas acima
    """  
    
    """ 
    Um pouco sobre a expressão regular utilizada
    
    """
    expressao = r"is\s+(\S+)%.*\(\s*(\S+)\s*out.*in\s+(\S+)\s*milliseconds"
    resultado = re.search(expressao , texto)
    
    if resultado:
        
        return resultado.group(1), resultado.group(2), resultado.group(3)
    
    else:
        return None

def pagina_carregada(driver, tempo_espera: int, localizador_elemento: str) -> bool:
    """
    Funcao para ser executada sempre que a pagina for carregada, tem como objetivo verificar se o objeto explicitado foi carregado. Caso seja encontrado, 
    retorna true, se nao retorna false.
    
    :param driver: driver selenium web configurado inicialmente
    :param tempo_espera: float que representa o tempo máximo de espera
    :param localizador_elemento: string com o localizador necessário para identificar o elemento.
    :returns: boleano que valida se página foi carregada ou não.
    """
    try:
        WebDriverWait(driver, tempo_espera).until(EC.visibility_of_element_located((By.CSS_SELECTOR, localizador_elemento)))
        return True
        
    except Exception:
        return False 

def preencher_campo(driver, localizador:str, info: str) -> bool:
    """
    Funcao para ser executada em cada preechimento de campo de um input do desafio retorna TRUE se inputado corretamente, e se nao retorna FALSE.
    
    :param driver: driver selenium web configurado inicialmente.
    :param chave_loc: string do localizador
    :param info: valor a ser preenchido no campo
    :returns: boleano que valida se página foi carregada ou não.
    """    
    try:
        element = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, localizador)))
        element.send_keys(info)
        return True
    
    except Exception:
        return False 
