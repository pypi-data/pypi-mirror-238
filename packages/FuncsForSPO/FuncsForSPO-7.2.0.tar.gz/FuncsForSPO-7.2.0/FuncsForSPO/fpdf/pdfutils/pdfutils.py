from PyPDF2 import PdfReader, PdfWriter 
from FuncsForSPO.fpython.functions_for_py import *

def extract_pages(original_pdf_path, new_pdf_path, num_pages):
    """
    Extracts a specified number of pages from a given PDF file and creates a new PDF file.
    
    :param original_pdf_path: A string representing the path to the original PDF file.
    :param new_pdf_path: A string representing the path to the new PDF file.
    :param num_pages: An integer representing the number of pages to extract.
    
    :return: None
    
    This function uses the PdfReader class to read the original PDF file, and the PdfWriter class to create a new PDF file
    with the specified number of pages. If the number of pages to extract is greater than the total number of pages in
    the original PDF file, it extracts all the available pages.

    Exemple:
        >>> extract_pages('input.pdf', 'output.pdf', 10)
    """
    pdf = PdfReader(original_pdf_path)
    total_pages = len(pdf.pages)

    num_pages_to_extract = min(num_pages, total_pages)

    writer = PdfWriter()
    for page_num in range(num_pages_to_extract):
        writer.add_page(pdf.pages[page_num])

    with open(new_pdf_path, "wb") as new_pdf:
        writer.write(new_pdf)
        

def split_pdf(input_path, output_dir='output_split', interval=30):
    """
    Splits a PDF file into multiple files with a specified page interval.

    :param input_path: The path to the input PDF file.
    :type input_path: str
    :param output_dir: The directory where the output PDF files will be saved. Defaults to 'output_split'.
    :type output_dir: str, optional
    :param interval: The number of pages in each output PDF file. Defaults to 30.
    :type interval: int, optional
    """
    
    # Cria o diretório de saída, se não existir
    cria_dir_no_dir_de_trabalho_atual(output_dir)
    limpa_diretorio(output_dir)

    # Abre o arquivo PDF de entrada
    with open(input_path, 'rb') as file:
        pdf = PdfReader(file)
        total_pages = len(pdf.pages)

        # Divide o PDF em intervalos de tamanho 'interval'
        for start in range(0, total_pages, interval):
            end = min(start + interval, total_pages)

            # Cria um novo arquivo PDF para cada intervalo
            output_pdf = PdfWriter()
            pages = pdf.pages[start:end]
            for page in pages:
                output_pdf.add_page(page)

            # Define o nome do arquivo de saída
            output_path = os.path.join(output_dir, f'output_{start + 1}-{end}.pdf')

            # Salva o arquivo PDF de saída
            with open(output_path, 'wb') as output_file:
                output_pdf.write(output_file)

        # Verifica se há páginas restantes
        if end < total_pages:
            # Cria um PDF com as páginas restantes
            output_pdf = PdfWriter()
            output_pdf.addPages(pdf.pages[end:])

            # Define o nome do arquivo de saída
            output_path = os.path.join(output_dir, f'output_{end + 1}-{total_pages}.pdf')

            # Salva o arquivo PDF de saída
            with open(output_path, 'wb') as output_file:
                output_pdf.write(output_file)
                
    return arquivos_com_caminho_absoluto_do_arquivo(output_dir)