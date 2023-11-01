import os
import sys
from winotify import Notification, audio
from time import sleep

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller 

        SE QUISER ADICIONAR ALGO NO ROBÔ BASTA USAR ESSA FUNÇÃO PARA ADICIONAR O CAMINHO PARA O EXECUTÁVEL COLOCAR
    """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def notificacao_windows_erro(app_id: str = 'Erro ocorrido', title: str = 'Erro ocorrido', msg: str = 'Ocorreu um erro no programa!', duration: str = 'long', icon='', launch='', actions_msg: str = 'Erro', actions_launch='', actions_msg2: str|bool=False, actions_launch2: str|bool=False, sound=audio.LoopingAlarm4, loop_sound: bool = False, path_log_dir=None):
    """Mostra uma notificação no canto inferior direito no Windows
    ### Funciona bem no Windows 11

    Args:
        app_id (str, optional): Id da notificação, geralmente o mesmo que o title. Defaults to 'Erro ocorrido'.
        title (str, optional): O título que aparecerá na notificação. Defaults to 'Erro ocorrido'.
        msg (str, optional): A mensagem que aparecerá na notificação. Defaults to 'Ocorreu um erro no programa!'.
        duration (str, optional): A duração da apresentação da notificação. Defaults to 'long'.
        icon (str, optional): Um ícone pode ser adicionado na notificação. Defaults to ''.
        launch (str, optional): Inicia um link ao clicar na notificação. Defaults to ''.
        actions_msg (str, optional): Mensagem no botão para ocorrer uma ação. Defaults to 'Erro'.
        actions_launch (str, optional): Ação do botão ao ser clicado, geralmente um link. Defaults to ''.
        sound (audio, optional): Som ao executar a notificação. Defaults to audio.LoopingCall2.
        loop_sound (bool, optional): Executa o som da notificação em loop. Defaults to False.
        path_log_dir (str|none, optional): Caminho do log. Defaults to None.
    """
    if isinstance(path_log_dir, str):
        os.system(f'explorer.exe {path_log_dir}')

    toast = Notification(app_id=app_id, title=title, msg=msg,
                         icon=resource_path(icon), duration=duration, launch=launch)
    toast.add_actions(label=actions_msg, launch=actions_launch)
    if isinstance(actions_launch2, str) and isinstance(actions_msg2, str):
        toast.add_actions(label=actions_msg2, launch=actions_launch2)
    toast.set_audio(sound=sound, loop=loop_sound)
    sleep(.3)
    toast.show()


def notificacao_windows_finalizado(app_id: str = 'Finalizado', title: str = 'Finalizado', msg: str = 'O programa finalizou as execuções!', duration: str = 'long', icon='', launch='', actions_msg: str = '', actions_launch='', actions_msg2: str|bool = False, actions_launch2: str|bool = False, sound=audio.LoopingAlarm3, loop_sound: bool = True, path_log_dir=None):
    """Mostra uma notificação no canto inferior direito no Windows
    ### Funciona bem no Windows 11

    # exemplo de launch -> launch=r'file:///C:/Users/user/mydata/mydir
    # exemplo de launch -> launch=r'file:///C:/Users/user/mydata/mydir/myfile.txt

    Args:
        app_id (str, optional): Id da notificação, geralmente o mesmo que o title. Defaults to 'Finalizado'.
        title (str, optional): O título que aparecerá na notificação. Defaults to 'Finalizado'.
        msg (str, optional): A mensagem que aparecerá na notificação. Defaults to 'O programa finalizou as execuções!'.
        duration (str, optional): A duração da apresentação da notificação. Defaults to 'long'.
        icon (str, optional): Um ícone pode ser adicionado na notificação. Defaults to ''.
        launch (str, optional): Inicia um link ao clicar na notificação. Defaults to ''.
        actions_msg (str, optional): Mensagem no botão para ocorrer uma ação. Defaults to 'Finalizado'.
        actions_launch (str, optional): Ação do botão ao ser clicado, geralmente um link. Defaults to ''.
        sound (audio, optional): Som ao executar a notificação. Defaults to audio.LoopingCall2.
        loop_sound (bool, optional): Executa o som da notificação em loop. Defaults to False.
        path_log_dir (str|none, optional): Caminho do log. Defaults to None.
    """

    if isinstance(path_log_dir, str):
        os.system(f'explorer.exe {path_log_dir}')

    toast = Notification(app_id=app_id, title=title, msg=msg,
                         icon=resource_path(icon), duration=duration, launch=launch)
    if actions_msg != '':
        toast.add_actions(label=actions_msg, launch=actions_launch)
        if isinstance(actions_launch2, str) and isinstance(actions_msg2, str):
            toast.add_actions(label=actions_msg2, launch=actions_launch2)
    toast.set_audio(sound=sound, loop=loop_sound)
    sleep(.3)
    toast.show()