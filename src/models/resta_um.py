from abc import ABC, abstractmethod

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
