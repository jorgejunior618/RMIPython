### imports
from abc import ABC, abstractmethod
import Pyro4

### resta_um.py
class IJogoRestaUm(ABC):
  _tabuleiro: list[list[str]]
  _turno: int
  _id_atual: int
  _clientes: dict[str, int]
  _turnoClientes: dict[str, int]
  _mensagens: list[str]
  _vencedor: str | None
  _lanceFeito: tuple[bool, str]
  _desistencia: bool

  @property
  @abstractmethod
  def tabuleiro(self) -> list[list[str]]:
    pass

  @tabuleiro.setter
  @abstractmethod
  def tabuleiro(self, nv: list[list[str]]):
    pass

  @property
  @abstractmethod
  def turno(self) -> int:
    pass
  @turno.setter
  @abstractmethod
  def turno(self, nv: int):
    pass

  @property
  @abstractmethod
  def id_atual(self) -> int:
    pass
  @id_atual.setter
  @abstractmethod
  def id_atual(self, nv: int):
    pass

  @property
  @abstractmethod
  def clientes(self) -> dict[str, int]:
    pass
  @clientes.setter
  @abstractmethod
  def clientes(self, nv: dict[str, int]):
    pass

  @property
  @abstractmethod
  def turnoClientes(self) -> dict[str, int]:
    pass
  @turnoClientes.setter
  @abstractmethod
  def turnoClientes(self, nv: dict[str, int]):
    pass

  @property
  @abstractmethod
  def mensagens(self) -> list[str]:
    pass
  @mensagens.setter
  @abstractmethod
  def mensagens(self, nv: list[str]):
    pass

  @property
  @abstractmethod
  def vencedor(self) -> str | None:
    pass
  @vencedor.setter
  @abstractmethod
  def vencedor(self, nv: str | None):
    pass

  @property
  @abstractmethod
  def desistencia(self) -> bool:
    pass
  @desistencia.setter
  @abstractmethod
  def desistencia(self, nv: bool):
    pass

  @property
  @abstractmethod
  def lanceFeito(self) -> tuple[bool, str]:
    pass
  @lanceFeito.setter
  @abstractmethod
  def lanceFeito(self, nv: tuple[bool, str]):
    pass

  @abstractmethod
  def reiniciaTabuleiro(self) -> list[list[str]]:
    '''# reiniciaTabuleiro
    Função que retorna um novo tabuleiro de Resta Um

    ## Retorna:
    tabuleiro : list[list[str]]
        objeto que representa um novo tabuleiro com a posição inicial do jogo

    '''
    pass

  @abstractmethod
  def estaNoFim(self) -> tuple[bool, int]:
    '''# estaNoFim

    Função que verifica e retorna se o tabuleiro ainda possui movimentos a serem realizados,
    quantas peças faltaram ser removidas caso não

    ## Retorna:
    out : tuple[ fimDeJogo : bool, contagem : int ]
        onde: [fimDeJogo] indica se há movimentos válidos e [contagem] a quantidade de peças restantes em caso de fimDeJogo[True] e 0 em caso de fimDeJogo[False]
    '''
    pass

  @abstractmethod
  def movimentoValido(self, mover: list[int], retirar: list[int]) -> tuple[bool, list[int]]:
    '''# movimentoValido

    Função que valida se o movimento recebido nos parâmetros é válido e retorna
    o destino da peça que será movida:

    ## Parâmetros:
    mover : list[int]
        indice da peça que será movida de posição
    retirar : list[int]
        indice da peça que será removida do tabuleiro
    tabuleiro : list[list[str]]
        objeto que representa o tabuleiro do jogo atual

    ## Retorna:
    out : tuple[ valido : bool, destino : list[int] ]
        onde: [valido] indica se o movimento recebido pode ser realizado ou não e [destino] é o indice para o qual a peça [mover] deverá ir
    '''
    pass

  @abstractmethod
  def fazMovimento(self, mover: list[int], retirar: list[int], destino: list[int]):
    '''# fazMovimento

    Função recebe o movimento desejado e retorna o tabuleiro com a jogada realizada:

    ## Parâmetros:
    mover : list[int]
        indice da peça que será movida de posição
    retirar : list[int]
        indice da peça que será removida do tabuleiro
    destino : list[int]
        indice de para onde a peça [mover] deverá ir
    tab : list[list[str]]
        objeto que representa o tabuleiro do jogo atual

    ## Retorna:
    tabuleiro : list[list[str]]
        objeto que representa o tabuleiro com a nova posição depois de ser realizaada a jogada
    '''
    pass

  @abstractmethod
  def recebeMovimento(self, movimento: str) -> list[list[int]]:
    '''# recebeMovimento
    Função que recebe o input do usuário e retorna os indices indicados

    ## Retorna:
    mover : list[int]
        indice da peça que será movida de posição
    retirar : list[int]
        indice da peça que será removida do tabuleiro
    '''
    pass

  @abstractmethod
  def desistencia(self, cliente_id: str) -> None:
    '''# desistencia
    Função que registra a desistencia do jogador [cliente_id]
    '''
    pass

  # Métodos referentes as regras de comunicação do servidor

  @abstractmethod
  def registrarCliente(self, cliente: str) -> str:
    '''# registrarCliente
    Função que recebe o cliente e gera um ID único
    '''

  @abstractmethod
  def enviarMensagem(self, cliente_id: str, mensagem: str) -> None:
    '''# enviarMensagem
    Função que recebe e registra no histórico de mensagens
    '''

  @abstractmethod
  def receberMensagens(self, cliente_id: str) -> (list[str] | None):
    '''# receberMensagens
    Função que retorna o histório de mensagens caso não haja novas mensagens retorna None
    '''

  @abstractmethod
  def definirTurno(self, cliente_id: str, turno: int) -> bool:
    '''# definirTurno
    Função que define o turno do cliente [cliente_id] e retorna True, caso o turno seja inválido retorna False
    '''

  @abstractmethod
  def turnosDefinidos(self) -> bool:
    '''# turnosDefinidos
    Função que retorna se o turno dos clientes ja foram devidamente definidos
    '''

  @abstractmethod
  def receberLance(self, cliente_id: str) -> tuple[bool, bool, bool]:
    '''# receberLance
    Função que retorna se um lance foi realizado, se o jogo terminou, e se houve desistencia
    '''

  @abstractmethod
  def enviarLance(self, movimento: str, cliente_id: str) -> bool:
    '''# enviarLance
    Função que registra o lance no jogo e retorna se o mesmo foi realizado com sucesso
    '''

### servidor.py
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

### inicializa_servidor.py
import Pyro4

def inicializaServidor():
  daemon = Pyro4.Daemon()
  ns = Pyro4.locateNS()
  servRestaUm = ServidorRestaUm()

  uri = daemon.register(servRestaUm)
  ns.register("resta_um.servidor", uri)

  print("Servidor do Jogo pronto.")
  daemon.requestLoop()

if __name__ == "__main__":
  inicializaServidor()