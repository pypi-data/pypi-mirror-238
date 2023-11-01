"""pip install langchain openai pypdf tiktoken faiss-cpu==1.7.4"""

import os
import pickle
import shutil
import tempfile
import uuid
from time import sleep

from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts.prompt import PromptTemplate
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.globals import set_llm_cache   
from langchain.cache import InMemoryCache   

from FuncsForSPO.fpython.functions_for_py import cria_dir_no_dir_de_trabalho_atual

# set cache langchain
set_llm_cache(InMemoryCache())


class Chatbot:

    def __init__(self, vectors, api_key, model_name, temperature, max_tokens, qa_template):
        self.model_name = model_name
        self.temperature = temperature
        self.api_key = api_key
        self.vectors = vectors
        self.max_tokens = max_tokens

        if qa_template is None:
            self.qa_template = """
            Neste cenário, você tem a expertise de um advogado especializado com mais de 10 anos de experiência em análise de andamentos jurídicos. No entanto, ao responder, pense como se estivesse simplificando o conteúdo para alguém de 21 anos sem nenhuma experiência jurídica. Os andamentos serão enviados separados por linha, você deve memorizar os contextos para que nada se perda na sua resposta.

            Aqui um exemplo:


            Distribuído por sorteio
            Audiência inicial por videoconferência cancelada (17/08/2023 13:50 Sala 1 - Principal - 1ª Vara do Trabalho de Jundiaí)
            Conclusos os autos para despacho (genérica) a GUSTAVO TRIANDAFELIDES BALTHAZAR

            você deve interpretar a linha Distribuído por sorteio, se houver outra linha embaixo, você deve interpretar até que todo o contexto esteja pronto para o usuário.

            Outro ponto, você não deve falar na terceira pessoa, "nesse processo" ou "nesse caso". Você deve falar, Olá [nome da pessoa que será fornecido], e dê o resumo do processo

            Caso seja dito para você falar o que aconteceu no ultimo andamento, você deve falar de forma muito amigável, como se fosse para um jovem, e sempre em primeira pessoa, como "na última movimentação do seu processo" ou se for algo positivo (analise com muito cuidado se é algo realmente positivo, por exemplo, um cancelamento de audiência não é positivo), fale "oba! aconteceu algo muito bom! nesse novo andamento" e fale de forma amigavel o que o andamento significa, por exemplo, se a última movimentação foi realização de uma diligência pericial., explique para o usuário o que é de forma muito amigável

            Lembrando que você nunca pode falar na terceira pessoa, por exemplo, "a pessoa está reclamando", fale sempre em primeira pessoa, "você está reclamando sobre..."
            CONTEXTO:
            {context}

            PERGUNTA:
            {question}
            """
        else:
            self.qa_template = qa_template
            
        self.QA_PROMPT = PromptTemplate(template=self.qa_template, input_variables=["context", "question"])

    def conversational_chat(self, query):
        llm = ChatOpenAI(
            model_name=self.model_name, 
            temperature=self.temperature, 
            openai_api_key=self.api_key, 
            max_tokens=self.max_tokens if self.max_tokens else None
        )

        retriever = self.vectors.as_retriever()
        chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever, 
            verbose=True, 
            return_source_documents=True, 
            max_tokens_limit=8191,
            chain_type='stuff',
            combine_docs_chain_kwargs={'prompt': self.QA_PROMPT}
        )
        history = []
        chain_input = {"question": query, "chat_history": history}
        
        if '$(USEHYSTORY)' in query:
            query = query.replace('$(USEHYSTORY)', '').strip()
            result = chain(chain_input)
            history.append((query, result["answer"]))
            return result["answer"]
        
        result = chain(chain_input)
        return result["answer"]


class Embedder:
    PATH = "embeddings"

    def __init__(self, api_key):
        self.api_key = api_key
        self.createEmbeddingsDir()

    def createEmbeddingsDir(self):
        if not os.path.exists(self.PATH):
            os.mkdir(self.PATH)

    def storeDocEmbeds(self, file, original_filename):
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt", encoding="utf-8") as tmp_file:
            tmp_file.write(file)
            tmp_file_path = tmp_file.name

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=20000,
            chunk_overlap=250,
            length_function=len,
            separators=["\n\n", "\n", r"\n\n", r"\n" " ", ""]
        )

        loader = TextLoader(file_path=tmp_file_path, autodetect_encoding=True)
        data = loader.load_and_split(text_splitter)

        embeddings = OpenAIEmbeddings(
            openai_api_key=self.api_key, 
            chunk_size=20000, 
            max_retries=6, 
            embedding_ctx_length=8191
        )

        vectors = FAISS.from_documents(data, embeddings)
        os.remove(tmp_file_path)

        with open(f"{self.PATH}/{os.path.basename(original_filename)}.pkl", "wb") as f:
            pickle.dump(vectors, f)

    def getDocEmbeds(self, file, original_filename):
        if not os.path.isfile(f"{self.PATH}/{os.path.basename(original_filename)}.pkl"):
            self.storeDocEmbeds(file, os.path.basename(original_filename))

        with open(f"{self.PATH}/{os.path.basename(original_filename)}.pkl", "rb") as f:
            vectors = pickle.load(f)

        return vectors


def chatpdf(prompts:dict, text:str, api_key:str, model:str="gpt-3.5-turbo-16k", temperature:float=0.8, max_tokens:int|None=None, sleep_per_request:int|float=0, qa_template:str|None=None):
    """Uma classe Chatbot e funções relacionadas para realizar consultas em documentos usando o modelo OpenAI e FAISS para busca semântica.

    O `Chatbot` é inicializado com vetores de documento, chave da API e outros parâmetros e pode responder a consultas baseadas nos documentos.
    A `Embedder` é usada para criar e recuperar embeddings de documentos. A função `chatpdf` configura o chatbot, processa os prompts 
    e retorna as respostas.

    Use:
        >>> chatbot = Chatbot(vetores, 'sua_chave_api', model_name='gpt-3.5-turbo')
        >>> resposta = chatbot.conversational_chat('Qual é o significado da vida?')

    Classes:
        Chatbot: Realiza consultas em documentos e retorna as respostas geradas pelo modelo.
        Embedder: Cria e recupera embeddings de documentos.

    Função:
        chatpdf(prompts, text, api_key, model='gpt-3.5-turbo', temperature=0.8, max_tokens=None, sleep_per_request=0):
            Processa um conjunto de prompts e retorna as respostas do chatbot.

    Args (para a classe Chatbot):
        vectors (FAISS): Os vetores FAISS criados a partir dos documentos.
        api_key (str): A chave da API para acessar o modelo OpenAI.
        model_name (str, optional): O nome do modelo a ser utilizado. Padrão é 'gpt-3.5-turbo'.
        temperature (float, optional): A temperatura para controlar a aleatoriedade das respostas do modelo. Padrão é 0.7.
        max_tokens (int, optional): O número máximo de tokens nas respostas do modelo. Padrão é None.
        qa_template (str, optional): O template para formatação das perguntas e respostas. Padrão é None.

    Args (para a função chatpdf):
        prompts (dict): Dicionário de prompts para os quais as respostas são desejadas.
        text (str): O texto do documento a ser consultado.
        api_key (str): A chave da API para acessar o modelo OpenAI.
        model (str, optional): O nome do modelo a ser utilizado. Padrão é 'gpt-3.5-turbo'.
        temperature (float, optional): A temperatura para controlar a aleatoriedade das respostas do modelo. Padrão é 0.8.
        max_tokens (int, optional): O número máximo de tokens nas respostas do modelo. Padrão é None.
        sleep_per_request (int, optional): O tempo de espera entre cada solicitação ao modelo OpenAI. Padrão é 0.
        qa_template (str, optional): O template para formatação das perguntas e respostas. Padrão é None.

        Exemplo de qa_template:
        meu_qa_template = '''
        Olá! 👋 Eu estou aqui para ajudar você a entender o andamento do seu processo de forma simples e clara.

        CONTEXTO:
        {context}

        PERGUNTA:
        {question}
        '''

    Retorna:
        dict: Um dicionário contendo as respostas do chatbot para cada prompt fornecido.

    Exceções:
        As exceções são levantadas dependendo das falhas na criação de embeddings, consulta ao modelo OpenAI ou outros erros inesperados.
    """
    shutil.rmtree('embeddings', ignore_errors=True)

    cria_dir_no_dir_de_trabalho_atual('tempdir')

    uploaded_file = os.path.abspath(f'tempdir/{str(uuid.uuid4())}.txt')
    with open(uploaded_file, 'w+', encoding='utf-8') as f:
        f.write(text)

    def setup_chatbot(uploaded_file):
        embeds = Embedder(api_key=api_key)
        with open(uploaded_file, encoding='utf-8') as f:
            file = f.read()
        
        vectors = embeds.getDocEmbeds(file, uploaded_file)
        return vectors

    chatbot = Chatbot(
        vectors=setup_chatbot(uploaded_file), 
        model_name=model, 
        temperature=temperature, 
        api_key=api_key, 
        max_tokens=max_tokens,
        qa_template=qa_template
    )

    prompts_list = [prompt for _, prompt in prompts.items()]
    return_list = []

    for query in prompts_list:
        answer = chatbot.conversational_chat(query)
        return_list.append(answer)
        sleep(sleep_per_request)

    return {k: v for k, v in zip(prompts.keys(), return_list)}


def chatpdf2(prompts: dict, text: str, api_key: str, model: str = "gpt-3.5-turbo-16k", temperature: float = 0.8, max_tokens: int | None = None, sleep_per_request: int | float = 0, qa_template: str | None = None):
    """Perform semantic search on text documents using OpenAI model and FAISS."""
    
    import os
    import pickle
    import shutil
    import tempfile
    import uuid
    from langchain.chat_models import ChatOpenAI
    from langchain.chains import ConversationalRetrievalChain
    from langchain.prompts.prompt import PromptTemplate
    from langchain.vectorstores.faiss import FAISS
    from langchain.embeddings.openai import OpenAIEmbeddings
    from langchain.document_loaders import TextLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.globals import set_llm_cache   
    from langchain.cache import InMemoryCache   

    from FuncsForSPO.fpython.functions_for_py import cria_dir_no_dir_de_trabalho_atual

    # set cache langchain
    set_llm_cache(InMemoryCache())

    # Use given qa_template or default
    if qa_template is None:
        qa_template = """Neste cenário, você tem a expertise de um advogado especializado com mais de 10 anos de experiência em análise de andamentos jurídicos. Lembrando que você nunca pode falar na terceira pessoa, por exemplo, "a pessoa está reclamando", fale sempre em primeira pessoa, "você está reclamando sobre..."
CONTEXTO:
{context}

PERGUNTA:
{question}"""

    QA_PROMPT = PromptTemplate(template=qa_template, input_variables=["context", "question"])
    
    # Setup embeds
    PATH = "embeddings"
    if not os.path.exists(PATH):
        os.mkdir(PATH)
    
    # Create embeddings for text and store/retrieve them
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt", encoding="utf-8") as tmp_file:
        tmp_file.write(text)
        tmp_file_path = tmp_file.name

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=27000,
        chunk_overlap=5000,
        length_function=len,
        separators=["\n\n", "\n", r"\n\n", r"\n" " ", "\r", ""]
    )
    loader = TextLoader(file_path=tmp_file_path, autodetect_encoding=True)
    data = loader.load_and_split(text_splitter)
    embeddings = OpenAIEmbeddings(
            openai_api_key=api_key, 
            chunk_size=27000, 
            max_retries=6, 
            embedding_ctx_length=8191
        )
    vectors = FAISS.from_documents(data, embeddings)
    os.remove(tmp_file_path)
    
    # Setup chatbot with vectors
    llm = ChatOpenAI(
        model_name=model, 
        temperature=temperature, 
        openai_api_key=api_key, 
        max_tokens=max_tokens
    )

    retriever = vectors.as_retriever()
    chain = ConversationalRetrievalChain.from_llm(llm=llm,
            retriever=retriever, 
            verbose=True, 
            return_source_documents=True, 
            max_tokens_limit=8191,
            chain_type='stuff',
            combine_docs_chain_kwargs={'prompt': QA_PROMPT}
            )
    
    results = {}
    for key, prompt in prompts.items():
        chain_input = {"question": prompt, "chat_history": []}
        result = chain(chain_input)
        results[key] = result["answer"]

    shutil.rmtree('embeddings', ignore_errors=True)
    return results
