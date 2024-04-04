import Pyro4
from resta_um import IJogoRestaUm

class ServidorRestaUm(IJogoRestaUm):
  def __init__(self):
    self.__initJogo()
    self.__initServidor()

  def __initJogo(self):
    self._vencedor = None
    self._tabuleiro = []
    self._turno = 0
    self._lanceFeito = (False, None)
    self._desistencia = False

  def __initServidor(self):
    self._id_atual = 0
    self._clientes = {}
    self._turnoClientes = {}
    self._mensagens = []

  ## Expondo propriedades

  @property
  @Pyro4.expose
  def tabuleiro(self):
    return self._tabuleiro
  @tabuleiro.setter
  @Pyro4.expose
  def tabuleiro(self, nv):
    self._tabuleiro = nv

  @property
  @Pyro4.expose
  def turno(self):
    return self._turno
  @turno.setter
  @Pyro4.expose
  def turno(self, nv):
    self._turno = nv

  @property
  @Pyro4.expose
  def id_atual(self):
    return self._id_atual
  @id_atual.setter
  @Pyro4.expose
  def id_atual(self, nv):
    self._id_atual = nv

  @property
  @Pyro4.expose
  def clientes(self):
    return self._clientes
  @clientes.setter
  @Pyro4.expose
  def clientes(self, nv):
    self._clientes = nv

  @property
  @Pyro4.expose
  def turnoClientes(self):
    return self._turnoClientes
  @turnoClientes.setter
  @Pyro4.expose
  def turnoClientes(self, nv):
    self._turnoClientes = nv

  @property
  @Pyro4.expose
  def mensagens(self):
    return self._mensagens
  @mensagens.setter
  @Pyro4.expose
  def mensagens(self, nv):
    self._mensagens = nv

  @property
  @Pyro4.expose
  def vencedor(self):
    return self._vencedor
  @vencedor.setter
  @Pyro4.expose
  def vencedor(self, nv):
    self._vencedor = nv

  @property
  @Pyro4.expose
  def lanceFeito(self):
    return self._lanceFeito

  @property
  @Pyro4.expose
  def desistencia(self):
    return self._desistencia
  @desistencia.setter
  @Pyro4.expose
  def desistencia(self, nv):
    self._desistencia = nv

  ## Sobrescrevendo os métodos da interface do jogo

  @Pyro4.expose
  def reiniciaTabuleiro(self):
    self._vencedor = None
    self._desistencia = False
    self._turno = 0
    self._tabuleiro = []

    for cliente in self._turnoClientes:
      self._turnoClientes[cliente] = -1

    posicoes = 9
    for i in range(posicoes):
      linha = []
      for j in range(posicoes):
        peca = '*'
        if i == 0 or i == 8 or j == 0 or j == 8:
          peca = ' '
        elif (i < 3 or i > 5) and (j < 3 or j > 5):
          peca = ' '
        if (i == j == 4):
          peca = 'O'
        linha.append(peca)
      self._tabuleiro.append(linha)

  @Pyro4.expose
  def estaNoFim(self):
    if self._desistencia:
      return True, -1

    contagemPecas = 0
    for i in range(9):
      linha = "".join(self._tabuleiro[i])
      contagemPecas += linha.count('*')
      coluna = "".join([lin[i] for lin in self._tabuleiro])
      if (linha.find("**O") != -1) or (linha.find("O**") != -1):
        return False, 0
      if (coluna.find("**O") != -1) or (coluna.find("O**") != -1):
        return False, 0

    for cliente in self._turnoClientes:
      if contagemPecas > 1:
        if self._turnoClientes[cliente] != self._turno:
          self._vencedor = cliente
          break
      else:
        if self._turnoClientes[cliente] == self._turno:
          self._vencedor = cliente
          break

    return True, contagemPecas

# Funções relacionadas aos movimentos e validadações do jogo
  @Pyro4.expose
  def movimentoValido(self, mover, retirar):
    moverLinha, moverColuna = mover
    retirarLinha, retirarColuna = retirar

    # Verificando se as posições estão dentro do tabuleiro
    if moverLinha > 7 or moverColuna > 7 or retirarLinha > 7 or retirarColuna > 7 or moverLinha < 1 or moverColuna < 1 or retirarLinha < 1 or retirarColuna < 1:
      return False, []

    # Verificando se as posições selecionadas são peças
    if self._tabuleiro[moverLinha][moverColuna] != '*':
      return False, []
    if self._tabuleiro[retirarLinha][retirarColuna] != '*':
      return False, []

    # Caso o movimento seja Horizontal
    if moverLinha == retirarLinha:
      if moverColuna == retirarColuna or abs(moverColuna - retirarColuna) != 1: # Caso as peças selecionadas sejam identicas
        return False, []
      # Caso seja um movimento da esquerda para a direita (->)
      if moverColuna < retirarColuna:
        if self._tabuleiro[retirarLinha][retirarColuna+1] != 'O':
          return False, []
        return True, [retirarLinha,retirarColuna+1]
      # Caso seja um movimento da direita para a esquerda (<-)
      else:
        if self._tabuleiro[retirarLinha][retirarColuna-1] != 'O':
          return False, []
        return True, [retirarLinha,retirarColuna-1]

    # Caso o movimento seja Vertical
    elif moverColuna == retirarColuna:
      if moverLinha == retirarLinha or abs(moverLinha - retirarLinha) != 1: # Caso as peças selecionadas sejam identicas
        return False, []
      # Caso seja um movimento de cima para baixo (\/)
      if moverLinha < retirarLinha:
        if self._tabuleiro[retirarLinha+1][retirarColuna] != 'O':
          return False, []
        return True, [retirarLinha+1,retirarColuna]
      # Caso seja um movimento de baixo para cima (/\)
      else:
        if self._tabuleiro[retirarLinha-1][retirarColuna] != 'O':
          return False, []
        return True, [retirarLinha-1,retirarColuna]
    # Caso as peças não estajam juntas
    else:
      return False, []

  @Pyro4.expose
  def fazMovimento(self, mover, retirar, destino):
    tab = []
    for i in range(9):
      linha = []
      for j in range(9):
        linha.append(self._tabuleiro[i][j])
      tab.append(linha)

    tab[mover[0]][mover[1]], tab[retirar[0]][retirar[1]], tab[destino[0]][destino[1]] = 'O','O' ,'*'

    self._turno = 1 - self._turno
    self._tabuleiro = tab

  @Pyro4.expose
  def recebeMovimento(self, movimento):
    indiceLinha = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7}
    mover, retirar = movimento.split(' ')

    mover = [*mover]
    mover[0] = indiceLinha[mover[0]]
    mover[1] = int(mover[1])

    retirar = [*retirar]
    retirar[0] = indiceLinha[retirar[0]]
    retirar[1] = int(retirar[1])
    return mover, retirar

  @Pyro4.expose
  def desistencia(self, cliente_id):
    self._desistencia = True
    for cliente in self._clientes:
      if cliente != cliente_id:
        self._vencedor = cliente

  @Pyro4.expose
  def registrarCliente(self, cliente):
    if (len(self._clientes.keys()) == 2):
      return "limite de clientes atingido"

    cliente_id = f"{self._id_atual}__{cliente}"
    self._clientes[cliente_id] = 0
    self._turnoClientes[cliente_id] = -1
    self.id_atual = 1
    print("Novo cliente registrado:", self._clientes)
    return cliente_id

  @Pyro4.expose
  def enviarMensagem(self, cliente_id, mensagem):
    mensagen = f"{cliente_id}: {mensagem}"
    self._mensagens.append(mensagen)

    for c in self._clientes:
      if c != cliente_id:
        self._clientes[c] = 0
    
    if len(self._mensagens) > 20:
      self._mensagens.pop(0)

  @Pyro4.expose
  def receberMensagens(self, cliente_id):
    if self._clientes[cliente_id] == 0:
      self._clientes[cliente_id] = 1
      return self._mensagens
    return None

  @Pyro4.expose
  def definirTurno(self, cliente_id, turno):
    for cliente in self._clientes:
      if cliente != cliente_id and self._turnoClientes[cliente] == turno:
        return False

    self._turnoClientes[cliente_id] = turno
    return True

  @Pyro4.expose
  def turnosDefinidos(self):
    for cliente in self._clientes:
      if self._turnoClientes[cliente] == -1:
        return False
    return True

  @Pyro4.expose
  def receberLance(self, cliente_id):
    fim, _ = self.estaNoFim()
    lanceFeito, cliID = self._lanceFeito
    lanceFeito = lanceFeito and cliID != None and cliID != cliente_id
    if lanceFeito:
      self._lanceFeito = (False, None)
    return lanceFeito, fim, self._desistencia

  @Pyro4.expose
  def enviarLance(self, movimento, cliente_id):
    mover, retirar = self.recebeMovimento(movimento)
    valido, destino = self.movimentoValido(mover, retirar)

    if not valido:
      return False

    self.fazMovimento(mover, retirar, destino)
    self._lanceFeito = (True, cliente_id)
    return True

daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
servRestaUm = ServidorRestaUm()

uri = daemon.register(servRestaUm)
ns.register("resta_um.servidor", uri)

print("Servidor do Jogo pronto.")
daemon.requestLoop()
