from FuncsForSPO.fpython.functions_for_py import *
from FuncsForSPO.fpdf.pdfutils.pdfutils import split_pdf
from tqdm import tqdm
from PIL import Image
import numpy as np
import fitz, uuid, os, gdown, pytesseract, cv2, base64

def faz_ocr_em_pdf_offline(path_pdf: str, export_from_file_txt: str=False) -> str:
    """Converte pdf(s) em texto com pypdf
        
    ## Atenção, só funciona corretamente em PDF's que o texto é selecionável!
    
    Use:
        ...
    
    Args:
        path_pdf (str): caminho do pdf
        export_from_file_txt (bool | str): passar um caminho de arquivo txt para o texto sair

    Returns:
        str: texto do PDF
    """
    
    text = []
    from pypdf import PdfReader

    reader = PdfReader(path_pdf)
    pages = reader.pages
    for page in pages:
        text.append(page.extract_text())
    else:
        text = transforma_lista_em_string(text)
        
        if export_from_file_txt:
            with open('extraction_pdf.txt', 'w', encoding='utf-8') as f:
                f.write(text)
        return text

def ocr_tesseract(pdf, dpi=300, file_output=uuid.uuid4(), return_text=True, config_tesseract='', limit_pages=None, lang='por', improve_image=True, use_threshold=True):
    """Executa OCR em um arquivo PDF usando Tesseract e retorna o texto extraído ou o caminho para o arquivo de texto.

    Esta função realiza o OCR em um arquivo PDF usando Tesseract. Se necessário, ela baixará e extrairá os binários 
    do Tesseract. O PDF é convertido em imagens antes de realizar o OCR. O texto extraído é salvo em um arquivo, e 
    o conteúdo desse arquivo ou o seu caminho podem ser retornados.

    Use:
        >>> ocr_tesseract('meu_documento.pdf', dpi=300, return_text=True, lang='por')
        Retorna o texto extraído do arquivo 'meu_documento.pdf'.

    Args:
        pdf (str): O caminho para o arquivo PDF no qual o OCR será realizado.
        dpi (int, optional): A resolução DPI para converter páginas PDF em imagens. Padrão é 300.
        file_output (str, optional): O nome do arquivo de saída onde o texto OCR será salvo. Padrão é um UUID gerado.
        return_text (bool, optional): Se True, retorna o texto extraído; se False, retorna o caminho para o arquivo de texto. 
            Padrão é True.
        config_tesseract (str, optional): Configurações adicionais para o Tesseract. Padrão é uma string vazia.
        limit_pages (int, optional): Limita o número de páginas do PDF a serem processadas. Se None, todas as páginas serão processadas. 
            Padrão é None.
        lang (str, optional): O código de idioma usado pelo Tesseract para o OCR. Padrão é 'por' (português).

    Returns:
        str: Se `return_text` for True, retorna o texto extraído; se False, retorna o caminho para o arquivo de texto.

    Raises:
        Exception: Se ocorrer um erro durante o processamento, o OCR ou a escrita do arquivo.
    """
    path_exit = arquivo_com_caminho_absoluto('temp_tess', 'Tesseract-OCR.zip')
    path_tesseract_extract = arquivo_com_caminho_absoluto('bin', 'Tesseract-OCR')
    path_tesseract = arquivo_com_caminho_absoluto(('bin', 'Tesseract-OCR'), 'tesseract.exe')

    def corrigir_orientacao(image): # By GPT
        # Converte a imagem para escala de cinza
        gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

        # Usa o Pytesseract para detectar a orientação do texto
        osd = pytesseract.image_to_osd(gray, output_type=pytesseract.Output.DICT)
        angle = osd['rotate']

        # Rotaciona a imagem para corrigir a orientação do texto
        if angle != 0:
            center = tuple(np.array(image.size) / 2)
            rot_img = image.rotate(angle, center=center)
            return rot_img
        return image
    
    def melhorar_imagem(image):
        # Converte para escala de cinza
        gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

        # Aplica um filtro de suavização (por exemplo, filtro Gaussiano)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        # Equaliza o histograma para realçar o preto
        gray = cv2.equalizeHist(gray)

        # Aplica thresholding adaptativo (opcional)
        improved = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        return Image.fromarray(improved)
    
    def aplicar_threshold(image, threshold=128):
        """
        Converte a imagem para escala de cinza e aplica thresholding.

        Args:
        - image (PIL.Image): A imagem original.
        - threshold (int): O valor de threshold. Pixels com valor acima deste serão brancos, abaixo serão pretos.

        Retorna:
        - PIL.Image: A imagem binarizada.
        """

        # Converte para escala de cinza
        gray = image.convert('L')

        # Aplica thresholding
        binary = gray.point(lambda p: p > threshold and 255)

        return binary
    

    if not os.path.exists(path_tesseract):
        faz_log('Baixando binários do Tesseract, aguarde...')
        cria_dir_no_dir_de_trabalho_atual('temp_tess')
        cria_dir_no_dir_de_trabalho_atual('bin')
        gdown.download('https://drive.google.com/uc?id=1yX6I7906rzo3YHK5eTmdDOY4FulpQKJ-', path_exit, quiet=True)
        sleep(1)
        with zipfile.ZipFile(path_exit, 'r') as zip_ref:
            # Obtém o nome da pasta interna dentro do arquivo ZIP
            zip_info = zip_ref.infolist()[0]
            folder_name = zip_info.filename.split("/")[0]

            # Extrai o conteúdo da pasta interna para a pasta de destino
            for file_info in zip_ref.infolist():
                if file_info.filename.startswith(f"{folder_name}/"):
                    file_info.filename = file_info.filename.replace(f"{folder_name}/", "", 1)
                    zip_ref.extract(file_info, path_tesseract_extract)
        deleta_diretorio('temp_tess')
    pytesseract.pytesseract.tesseract_cmd = path_tesseract

    with fitz.open(pdf) as pdf_fitz:
        cria_dir_no_dir_de_trabalho_atual('pages')
        limpa_diretorio('pages')
        faz_log(f'Convertendo PDF para páginas...')
        number_of_pages = len(pdf_fitz) if limit_pages is None else min(limit_pages, len(pdf_fitz))
        with tqdm(total=number_of_pages, desc='EXTRACT PAGES') as bar:
            for i, page in enumerate(pdf_fitz):
                if i >= number_of_pages:
                    break
                page = pdf_fitz.load_page(i)
                mat = fitz.Matrix(dpi/72, dpi/72)  # Matriz de transformação usando DPI
                pix = page.get_pixmap(matrix=mat)
                image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                image = corrigir_orientacao(image)
                
                if improve_image:
                    image = melhorar_imagem(image)
                
                if use_threshold:
                    image = aplicar_threshold(image, threshold=128)

                image.save(f'pages/{i}.png')
                bar.update(1)
        

        files = arquivos_com_caminho_absoluto_do_arquivo('pages')
        with tqdm(total=len(files), desc='OCR') as bar:
            for i, image in enumerate(files):
                text = pytesseract.image_to_string(image, config=config_tesseract, lang=lang)
                with open(arquivo_com_caminho_absoluto('tempdir', f'{file_output}.txt'), 'a', encoding='utf-8') as f:
                    f.write(text)
                bar.update(1)
            else:
                limpa_diretorio('pages')
                if return_text:
                    text_all = ''
                    with open(arquivo_com_caminho_absoluto('tempdir', f'{file_output}.txt'), 'r', encoding='utf-8') as f:
                        text_all = f.read()
                    os.remove(arquivo_com_caminho_absoluto('tempdir', f'{file_output}.txt'))
                    return text_all
                else:
                    return os.path.abspath(arquivo_com_caminho_absoluto('tempdir', f'{file_output}.txt'))
                
                
                
                
def ocr_google_vision(pdf, api_key, dpi=300, file_output=uuid.uuid4(), return_text=True, limit_pages=None):
    def detect_text(files_png: list[str], api_key) -> str:
        """Recupera o texto das imagens

        Args:
            files_png (list[str]): Lista de imagens do pdf

        Raises:
            Exception: != de 200 a response

        Returns:
            str: O texto do PDF
        """
        url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
        requests_json = []
        result = ''
        contador = len(files_png)
        while contador != 0:  # enquanto existir imagens...
            faz_log(f'Recuperando 16 imagens de {contador} imagens | Se tiver 16 de fato, senão pega o resto')
            files_png_temp = files_png[:16]
            for filepath in files_png_temp:  # faz uma lista de requests para o post
                with open(filepath, mode='rb') as file:
                    bytes_content = file.read()
                    requests_json.append(
                        {
                            "image": {
                                "content": base64.b64encode(bytes_content).decode("utf-8")
                            },
                            "features": [{"type": "TEXT_DETECTION"}]
                        }
                    )
            else:
                for i in files_png_temp:
                    files_png.remove(i)
                    

                r = requests.post(url=url, json={"requests": requests_json})
                requests_json = []  # limpa para os proximos 10
                if r.status_code == 200:
                    # faz_log(r.text)
                    r_json = r.json()
                    for resp in r_json['responses']:
                        try:
                            result = result + str(resp['textAnnotations'][0]['description']).strip()
                        except Exception as e:
                            faz_log(repr(e))
                            raise Exception(repr(e))
                    else:
                        contador = len(files_png)
                else:
                    raise Exception(r.json()['error']['message'])

        return remover_acentos(result.lower().strip())
    
    with fitz.open(pdf) as pdf_fitz:
        cria_dir_no_dir_de_trabalho_atual('pages')
        limpa_diretorio('pages')
        faz_log(f'Convertendo PDF para páginas...')
        number_of_pages = len(pdf_fitz) if limit_pages is None else min(limit_pages, len(pdf_fitz))
        with tqdm(total=number_of_pages, desc='EXTRACT PAGES') as bar:
            for i, page in enumerate(pdf_fitz):
                if i >= number_of_pages:
                    break
                page = pdf_fitz.load_page(i)
                mat = fitz.Matrix(dpi/72, dpi/72)  # Matriz de transformação usando DPI
                pix = page.get_pixmap(matrix=mat)
                image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                image.save(f'pages/{i}.png')
                bar.update(1)
        
    faz_log('Enviando para Google Vision...')
    files = list(arquivos_com_caminho_absoluto_do_arquivo('pages'))
    text_ocr = detect_text(files, api_key)
    limpa_diretorio('pages')
    if return_text:
        return text_ocr
    else:
        file_path = arquivo_com_caminho_absoluto('tempdir', f'{file_output}.txt')
        with open(file_path, 'w') as f:
            text_ocr.write(f)
        return file_path
    
    
    
def ocr_tesseract_v2(pdf, dpi=300, file_output=uuid.uuid4(), return_text=True, config_tesseract='', limit_pages=None, lang='por', timeout=120):
    path_exit = arquivo_com_caminho_absoluto('temp_tess', 'Tesseract-OCR.zip')
    path_tesseract_extract = arquivo_com_caminho_absoluto('bin', 'Tesseract-OCR')
    path_tesseract = arquivo_com_caminho_absoluto(('bin', 'Tesseract-OCR'), 'tesseract.exe')

    if not os.path.exists(path_tesseract):
        faz_log('Baixando binários do Tesseract, aguarde...')
        cria_dir_no_dir_de_trabalho_atual('temp_tess')
        cria_dir_no_dir_de_trabalho_atual('bin')
        gdown.download('https://drive.google.com/uc?id=1yX6I7906rzo3YHK5eTmdDOY4FulpQKJ-', path_exit, quiet=True)
        sleep(1)
        with zipfile.ZipFile(path_exit, 'r') as zip_ref:
            # Obtém o nome da pasta interna dentro do arquivo ZIP
            zip_info = zip_ref.infolist()[0]
            folder_name = zip_info.filename.split("/")[0]

            # Extrai o conteúdo da pasta interna para a pasta de destino
            for file_info in zip_ref.infolist():
                if file_info.filename.startswith(f"{folder_name}/"):
                    file_info.filename = file_info.filename.replace(f"{folder_name}/", "", 1)
                    zip_ref.extract(file_info, path_tesseract_extract)
        deleta_diretorio('temp_tess')
    pytesseract.pytesseract.tesseract_cmd = path_tesseract

    with fitz.open(pdf) as pdf_fitz:
        cria_dir_no_dir_de_trabalho_atual('pages')
        limpa_diretorio('pages')
        faz_log(f'Convertendo PDF para páginas...')
        number_of_pages = len(pdf_fitz) if limit_pages is None else min(limit_pages, len(pdf_fitz))
        with tqdm(total=number_of_pages, desc='EXTRACT PAGES') as bar:
            for i, page in enumerate(pdf_fitz):
                if i >= number_of_pages:
                    break
                page = pdf_fitz.load_page(i)
                mat = fitz.Matrix(dpi/72, dpi/72)  # Matriz de transformação usando DPI
                pix = page.get_pixmap(matrix=mat)
                pix.save(arquivo_com_caminho_absoluto('pages', f'{i}.png'))
                bar.update(1)
        

        files = arquivos_com_caminho_absoluto_do_arquivo('pages')
        with tqdm(total=len(files), desc='OCR') as bar:
            for i, image in enumerate(files):
                try:
                    text = pytesseract.image_to_string(image, config=config_tesseract, lang=lang, timeout=timeout)
                except Exception as e:
                    return False
                with open(arquivo_com_caminho_absoluto('tempdir', f'{file_output}.txt'), 'a', encoding='utf-8') as f:
                    f.write(text)
                bar.update(1)
            else:
                limpa_diretorio('pages')
                if return_text:
                    text_all = ''
                    with open(arquivo_com_caminho_absoluto('tempdir', f'{file_output}.txt'), 'r', encoding='utf-8') as f:
                        text_all = f.read()
                    os.remove(arquivo_com_caminho_absoluto('tempdir', f'{file_output}.txt'))
                    return text_all
                else:
                    return os.path.abspath(arquivo_com_caminho_absoluto('tempdir', f'{file_output}.txt'))