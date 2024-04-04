import Pyro4
from threading import Thread
from time import sleep

class ChatCliente:
    def __init__(self, nome):
        self.nome = nome

    def set_servidor(self, servidor):
        self.servidor = servidor

    def set_id(self, id):
        self.id = id

    def registrar(self):
        self.set_id(self.servidor.registrar_cliente(self.nome))

    def receber_mensagem(self):
        while True:
            mensagens = self.servidor.receber_mensagens(self.id)
            for msg in mensagens or []:
                if len(msg) > 0:
                    print(f"\n{msg}")
            sleep(0.2)

    def enviar_mensagem(self, mensagem):
        self.servidor.enviar_mensagem(self.id, mensagem)

nome_cliente = input("Digite seu nome: ")
servidor_uri = "PYRONAME:chat.servidor"

cliente = ChatCliente(nome_cliente)
with Pyro4.Daemon() as daemon:
    # Registrar cliente com um nome personalizado
    servidor = Pyro4.Proxy(servidor_uri)

    cliente.set_servidor(servidor)
    cliente.registrar()

    thread_chat = Thread(target=cliente.receber_mensagem, daemon=True)
    thread_chat.start()
    while True:
        mensagem = input("Digite sua mensagem (ou 'sair' para sair): ")
        if mensagem.lower() == "sair":
            break
        cliente.enviar_mensagem(mensagem)
