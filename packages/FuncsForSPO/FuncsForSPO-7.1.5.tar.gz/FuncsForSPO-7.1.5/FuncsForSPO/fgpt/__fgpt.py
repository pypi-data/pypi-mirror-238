from FuncsForSPO.fgpt.base import *

class GPTBot(BotMain):
    def __init__(self, prompt, headless):
        self.PROMPT = prompt
        self.HEADLESS = headless
        super().__init__(headless)
        
    def run(self):
        self.DRIVER.get('https://chat.chatgptdemo.net/')
        if isinstance(self.PROMPT, str):
            espera_elemento_e_envia_send_keys(self.WDW, 'coloque no final "GPT_RESPOSTA" '+self.PROMPT, (By.CSS_SELECTOR, '#input-chat'))
            espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, 'div.send-button'))
            tentativas = 20
            while tentativas != 0:
                text = espera_e_retorna_elemento_text(self.WDW, (By.CSS_SELECTOR, 'pre[class="chat-content chat-response"]'))
                if 'GPT_RESPOSTA' in text:
                    return text
                else:
                    sleep(1)
                    tentativas -= 1
            else:
                return text
        if isinstance(self.PROMPT, dict):
            response = {}
            for chave, valor in self.PROMPT.items():
                faz_log(f'Fazendo pergunta {chave}: {valor}')
                espera_elemento_e_envia_send_keys(self.WDW, 'Adicione "GPT_RESPOSTA" apenas no final da sua resposta! '+valor, (By.CSS_SELECTOR, '#input-chat'))
                espera_elemento_disponivel_e_clica(self.WDW, (By.CSS_SELECTOR, 'div.send-button'))
                tentativas = 20
                while tentativas != 0:
                    try:
                        text = espera_e_retorna_lista_de_elementos(self.WDW, (By.CSS_SELECTOR, 'pre[class="chat-content chat-response"]'))[-1].text
                    except:
                        sleep(1)
                        tentativas -= 1
                    if 'GPT_RESPOSTA' in text:
                        response[chave] = text
                        break
                    else:
                        sleep(1)
                        tentativas -= 1
                else:
                    response[chave] = text
            else:
                return response
