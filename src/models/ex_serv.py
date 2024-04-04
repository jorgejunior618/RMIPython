import Pyro4

@Pyro4.expose
class ChatServidor:
    def __init__(self):
        self.id_atual = 0
        self.clientes: dict[str, int] = {}
        self.mensagens = []

    def registrar_cliente(self, cliente):
        if (len(self.clientes.keys()) == 2):
            return "limite de clientes atingido"
        id_cli = f"{self.id_atual}__{cliente}"
        self.clientes[id_cli] = 0
        self.id_atual = 1
        print("Novo cliente registrado:", self.clientes)
        return id_cli

    def enviar_mensagem(self, cli, msg):
        mensagen = f"[{cli}]: {msg}"
        self.mensagens.append(mensagen)

        for c in self.clientes:
            if c != cli:
                self.clientes[c] = 0

        if len(self.mensagens) > 20:
            self.mensagens.pop(0)

    def receber_mensagens(self, cli):
        if self.clientes[cli] == 0:
            self.clientes[cli] = 1
            return self.mensagens

daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()

# Criando uma única instância do servidor
servidor = ChatServidor()

# Registrando o servidor com o daemon
uri = daemon.register(servidor)
ns.register("chat.servidor", uri)

print("Servidor de chat pronto.", uri)
daemon.requestLoop()