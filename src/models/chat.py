from abc import ABC, abstractmethod
class IChat(ABC):
  @abstractmethod
  def registrar_cliente(self, cliente):
    '''# registrar_cliente
    Função que retorna um novo tabuleiro de Resta Um

    ## Retorna:
    tabuleiro : list[list[str]]
        objeto que representa um novo tabuleiro com a posição inicial do jogo

    '''
    pass

  @abstractmethod
  def enviar_mensagem(self, cli, msg):
    '''# enviar_mensagem

    Função que verifica e retorna se o tabuleiro ainda possui movimentos a serem realizados,
    quantas peças faltaram ser removidas caso não

    ## Retorna:
    out : tuple[ fimDeJogo : bool, contagem : int ]
        onde: [fimDeJogo] indica se há movimentos válidos e [contagem] a quantidade de peças restantes em caso de fimDeJogo[True] e 0 em caso de fimDeJogo[False]
    '''
    pass

  @abstractmethod
  def receber_mensagens(self, cli):
    '''# receber_mensagens

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
