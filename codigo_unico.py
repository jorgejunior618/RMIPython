### imports
from abc import ABC, abstractmethod
import Pyro4
from time import sleep
from threading import Thread
from pygame import mixer

from tkinter import Tk, StringVar, NW, PhotoImage, Canvas, Listbox
from tkinter.font import Font
from tkinter.ttk import Style, Button, Label, Entry
from typing import Callable

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

### cliente.py
uri = "PYRONAME:resta_um.servidor"
cliente: IJogoRestaUm = Pyro4.Proxy(uri)

### gui_define_nome.py
class GuiDefineNome:
  ''' # GuiDefineNome

  Classe que inicializa uma interface grafica, com `TKinter`, para a definição do nome do jogador.

  ## Parâmetros:
    setter : function(nome:str)
        A função que serve para capturar o nome escolhido pelo jogador
    '''
  def __init__(self, setter: Callable):
    '''
    Inicializa a interface grafica do jogo
    '''
    self.setter = setter

    self.criaComponenteJanela()
    self.criaComponenteEstilos()
    self.criaComponenteInsereNome()

  def criaComponenteJanela(self):
    ''' # criaComponenteJanela

    Função de criação de componentes: cria a janela raiz da interface gráfica
    '''
    self.janela = Tk()
    self.janela.iconbitmap("./assets/icone.ico")
    self.janela.title("ANTes que Reste Um - definir nome")
    self.janela.geometry("270x115")
    self.janela.resizable(False, False)

  def criaComponenteEstilos(self):
    ''' # criaComponenteEstilos

    Função de criação de componentes: cria o estilo padrão para os botões e fontes da GUI
    '''
    self.fonteGeral = Font(size=12, family="Trebuchet MS")
    self.fonteErro = Font(size=9, family="Trebuchet MS")

    style = Style()
    style.configure(
      "Estilizado.TButton",
        width=6,
        font=self.fonteGeral
      )

  def criaComponenteInsereNome(self):
    ''' # criaComponenteInsereNome

    Função de criação de componentes: cria a entrada e componentes para
    receber o Nome do jogador
    '''
    self.varNome = StringVar()
    self.varValidadeNome = StringVar()

    Label(self.janela, text="Digite seu nome de usuário:", font=self.fonteGeral).place(x=20, y=20)

    self.inputIP = Entry(self.janela, textvariable=self.varNome, width=16, font=self.fonteGeral)
    self.botConfirmaNome = Button(self.janela, text="Enviar", command=self.recebeNome, style="Estilizado.TButton")
    self.labelNomeValido = Label(self.janela, textvariable=self.varValidadeNome, font=self.fonteErro, foreground="#F03131")
  
    self.inputIP.place(x=20, y=52)
    self.botConfirmaNome.place(x=170, y=50)
    self.labelNomeValido.place(x=20, y=85)

    def bindEnter(kc):
      if kc == 13: # Pressionou enter
        self.recebeNome()
    self.inputIP.bind("<Key>", lambda e: bindEnter(e.keycode))

  def recebeNome(self):
    ''' # recebeNome

    Função que captura o texto digitado na entrada e registra o nome
    '''
    try:
      nome = self.varNome.get().strip()
      print(f"nome: {nome}")
      if self.validarNome(nome):
        self.setter(nome)
        self.janela.destroy()
    except Exception as e:
      print("erro recebeNome:", e)

  def validarNome(self, nome: str) -> bool:
    try:
      if nome.startswith(tuple('1,2,3,4,5,6,7,8,9,0'.split(','))):
        self.varValidadeNome.set("O Nome não pode iniciar com números")
        return False
      if len(nome.split(' ')) > 1:
        self.varValidadeNome.set("O Nome não pode conter espaços")
        return False

      return True
    except Exception as e:
      print("erro validaNome: ", e)
      self.varValidadeNome.set(f"{e}")
      return False

  def iniciaAplicacao(self):
    '''# iniciaAplicacao
    Inicializa a janela da interface gráfica para receber o nome do jogador
    '''
    self.janela.mainloop()

### gui_resta_um.py
class GuiRestaUm:
  ''' # RestaUmInterface

  Classe que inicializa uma interface grafica, com `TKinter`, para o jogo Resta Um.

  ## Parâmetros:
    cli_tabuleiro : IJogoRestaUm
        O cliente socket ja inicializado que será utilizado para a conexão multiplayer
    '''
  jogada = ""
  pecaDestacada = -1
  meuTurno = -1
  prontoPJogar = False
  turnoVar: StringVar = None
  labelInfoTurno: Label = None
  tagFimJogo = None
  img_tabuleiro = None
  img_peca = None
  img_vazio = None
  img_peca_high = None
  fim_jogo = None
  dictImgs = {}

  def __init__(self, cli: IJogoRestaUm, cliente_id: str):
    '''
    Inicializa a interface grafica do jogo

    ## Parâmetros:
    cli_tabuleiro : IJogoRestaUm
        O cliente socket ja inicializado que será utilizado para a conexão multiplayer
    '''
    self.meuID: str = cliente_id
    self.cliRMI: IJogoRestaUm = cli
    self.desistiu = False
    self.cliRMI.reiniciaTabuleiro()
    self.criaComponenteJanela()
    mixer.init()

    GuiRestaUm.fonteText = Font(size=11, family="Trebuchet MS")
    GuiRestaUm.turnoVar = StringVar()
    GuiRestaUm.labelInfoTurno = Label(self.janela, textvariable=GuiRestaUm.turnoVar)
    GuiRestaUm.img_tabuleiro = PhotoImage(file="assets/tabuleiro.png")
    GuiRestaUm.img_peca = PhotoImage(file="assets/peca.png")
    GuiRestaUm.img_vazio = PhotoImage(file="assets/vazio.png")
    GuiRestaUm.img_peca_high = PhotoImage(file="assets/peca_highlight.png")
    GuiRestaUm.fim_jogo = PhotoImage(file="assets/fim_jogo.png")

    GuiRestaUm.dictImgs['peca'] = GuiRestaUm.img_peca.name[-1]
    GuiRestaUm.dictImgs['vazio'] = GuiRestaUm.img_vazio.name[-1]
    GuiRestaUm.dictImgs['destacada'] = GuiRestaUm.img_peca_high.name[-1]
    
    self.criaComponenteTabuleiro()
    self.criaComponenteEstilos()
    self.criaComponentePecas()
    self.criaComponenteTurnos()
    
    self.mensagens: list[str] = []
    self.minhaMensagem = StringVar()
    self.criaComponenteChat()

  @staticmethod
  def reproduzSom(efeito: str):
    ''' ## reproduzSom(efeito)

    Reproduz um efeito sonoro referente ao movimento/ação do jogo

    ## Parâmetro:
    efeito : str
        A ação realizada, gatilho para o efeito sonoro
    '''
    efeitos = {
      'derrota': 'derrota_1',
      'vitoria': 'vitoria_1',
      'movimento': 'movimento_1',
      'mov_erro': 'mov_erro_2',
    }
    arq = f"assets/{efeitos[efeito]}.mp3"
    if mixer.music.get_busy():
      mixer.music.queue(arq)
    else:
      mixer.music.load(arq)

    mixer.music.set_volume(0.7)
    mixer.music.play()

  @staticmethod
  def selecionaPeca(
    x: int,
    y: int,
    tag: int,
    clente_id: str,
    cRMI: IJogoRestaUm
  ) -> tuple[bool, int, bool]:
    ''' # selecionaPeca

    Função que gerencia o clique do usuário nas peças segundo a seguinte lógica:
    - Se nenhuma peça estiver selecionada, seleciona a clicada
    - Se uma peça estiver selecionada eseja um movimento válido, realiza o movimento
    - Se uma peça estiver selecionada e o movimento inválido, seleciona a nova peça

    ## Parâmetros:
    x : int
        indice da linha da peça

    y : int
        indice da coluna da peça

    tag : int
        identificador do componente da peça

    ct : IJogoRestaUm
        cli do RMI de Jogo

    ## Retorno:
    r : tuple[reposicionar: bool , rmDst: int , movErrado: bool]
        reposicionar: indica se o tabuleiro tem que ser re-renderizado

        removeDestaque: indica o idnetificador que deve ser removido o destaque

        movErrado: indica se o som de movimento errado deve ser reproduzido
    '''
    posicaoJogada = ["","a", "b", "c", "d", "e", "f", "g",""]
    pecaSelecionada = f"{posicaoJogada[x]}{y}"
    removerDestaque = GuiRestaUm.pecaDestacada

    if (removerDestaque == tag):
      GuiRestaUm.jogada = ""
      GuiRestaUm.pecaDestacada = -1
      return False, tag, False
    GuiRestaUm.pecaDestacada = tag

    if len(GuiRestaUm.jogada) == 0:
      GuiRestaUm.jogada = f"{pecaSelecionada}"
      return False, removerDestaque, False

    GuiRestaUm.jogada = f"{GuiRestaUm.jogada} {pecaSelecionada}"
    minhaVez = not cRMI.enviarLance(GuiRestaUm.jogada, clente_id)

    if minhaVez:
      GuiRestaUm.pecaDestacada = tag
      GuiRestaUm.jogada = pecaSelecionada
      return False, removerDestaque, True

    GuiRestaUm.jogada = ""
    GuiRestaUm.pecaDestacada = -1
    return True, removerDestaque, False

  def criaComponenteJanela(self):
    ''' # criaComponenteJanela

    Função de criação de componentes: cria a janela raiz da interface gráfica
    '''
    self.janela = Tk()
    self.janela.iconbitmap("./assets/icone.ico")
    self.janela.title("ANTes que Reste Um")
    self.janela.geometry("800x500")
    self.janela.resizable(False, False)

  def criaComponenteEstilos(self):
    ''' # criaComponenteEstilos

    Função de criação de componentes: cria o estilo padrão para os botões da GUI
    '''
    style = Style()
    style.configure(
      "Estilizado.TButton",
        width=6,
        font=GuiRestaUm.fonteText
      )

  def criaComponenteTabuleiro(self):
    ''' # criaComponenteTabuleiro

    Função de criação de componentes: cria o canvas que receberá o tabuleiro e peças e posiciona as peças
    '''
    self.canvas = Canvas(self.janela, width=500, height=500)
    self.canvas.place(x=0, y=0)
    self.canvas.create_image(0,0, anchor=NW, image=GuiRestaUm.img_tabuleiro)

  def criaComponenteTurnos(self, texto: str = "Escolha seu turno"):
    ''' # criaComponenteTurnos

    Função de criação de componentes: cria as labels e botões utilizados para decisão de turnos
    '''
    # fonteText = Font(size=11, family="Trebuchet MS")
    GuiRestaUm.botaoT1 = Button(self.janela, text="1º", command=lambda t=0: self._setTurno(t), style="Estilizado.TButton")
    GuiRestaUm.botaoT2 = Button(self.janela, text="2º", command=lambda t=1: self._setTurno(t), style="Estilizado.TButton")
    GuiRestaUm.labelDecTurno = Label(self.janela, text=texto, font=GuiRestaUm.fonteText)
    
    GuiRestaUm.botaoT1.place(x=520, y=45)
    GuiRestaUm.botaoT2.place(x=590, y=45)
    GuiRestaUm.labelDecTurno.place(x=520, y=15)

  def criaComponentePecas(self):
    ''' # criaComponentePecas

    Função de criação de componentes: cria e posiciona as peças no tabuleiro
    '''
    self.tagPecas = []
    posicoesTabuleiro = self.cliRMI.tabuleiro

    for i in range(1, 8):
      linha = []
      for j in range(1, 8):
        lin = 90 + ((i-1) * 40) + ((i-1) * 5)
        col = 35 + ((j-1) * 50) + ((j-1) * 10)
        tagItem = -1
        if posicoesTabuleiro[i][j] == '*':
          tagItem = self.canvas.create_image(col, lin, anchor=NW, image=GuiRestaUm.img_peca)
        if posicoesTabuleiro[i][j] == 'O':
          tagItem = self.canvas.create_image(col, lin, anchor=NW, image=GuiRestaUm.img_vazio)
        self.canvas.tag_bind(
          tagItem,
          "<Button-1>",
          lambda e, x=i, y=j, id=tagItem: self.fazJogada(x, y, id)
        )
        linha.append(tagItem)
      self.tagPecas.append(linha[:])

  def criaComponenteChat(self):
    ''' # criaComponenteChat

    Função de criação de componentes: cria a entrada e componentes do chat do jogo
    '''
    fonteChat = Font(size=11, family="Comic Sans MS")
    GuiRestaUm.variavelMensagens = StringVar(value=self.mensagens)

    GuiRestaUm.lboxMensagens = Listbox(
      self.janela,
      listvariable=GuiRestaUm.variavelMensagens,
      height=12,
      width=29,
      font=fonteChat,
      foreground="#7C3509"
    )
    GuiRestaUm.inputChat = Entry(
      self.janela,
      textvariable=self.minhaMensagem,
      width=20,
      font=fonteChat
    )
    GuiRestaUm.botaoEnviarChat = Button(
      self.janela,
      text="Enviar",
      command=self.chatEnviaMensagem,
      width=8,
      style="Estilizado.TButton"
    )

    GuiRestaUm.lboxMensagens.place(x=520, y=190)
    GuiRestaUm.inputChat.place(x=520, y=460)
    GuiRestaUm.botaoEnviarChat.place(x=715, y=457)

    def enviaMsgEnter(kc):
      if kc == 13: # Pressionou enter
        self.chatEnviaMensagem()
    GuiRestaUm.inputChat.bind("<Key>", lambda e: enviaMsgEnter(e.keycode))

  def reproduzFimDeJogo(self):
    ''' # reproduzFimDeJogo

    Função que cria a thread que  de animação do componente da placa de fim de jogo
    '''
    if GuiRestaUm.tagFimJogo == None:
      GuiRestaUm.tagFimJogo = self.canvas.create_image(75,-330, anchor=NW, image=GuiRestaUm.fim_jogo)
    def desce():
      cont = 0
      for i in range(104):
        alturaAtual = i*3.2 - 330
        balancoAtual = 0
        if GuiRestaUm.meuTurno == -1:
          self.canvas.moveto(GuiRestaUm.tagFimJogo, 75, -330)
          break
        if cont < 20:
          balancoAtual = 0 - cont*2
        elif cont < 56:
          balancoAtual = cont*2 - 78
        elif cont < 82:
          balancoAtual = 144 - cont*2
        elif cont < 98:
          balancoAtual = cont*2 - 180
        else:
          balancoAtual = 210 - cont*2

        self.canvas.moveto(GuiRestaUm.tagFimJogo, 35 + balancoAtual, alturaAtual)
        cont += 1

        sleep(0.025)

    thread_placa = Thread(target=desce, daemon=True)
    thread_placa.start()

  def fazJogada(self, x: int, y: int, tag: int):
    ''' # fazJogada

    Função para ser utilizada no clique das peças do jogo, ativada apenas no turno do jogador,
    identifica a posição selecionada e envia para a função `selecionaPeca` para realizar as funções
    gráficas

    ## Parâmetros:
    x : int
        indice da linha da peça

    y : int
        indice da coluna da peça

    tag : int
        identificador do componente da peça

    ct : IJogoRestaUm
        cli do socket de Jogo

    '''
    if self.cliRMI.turno == GuiRestaUm.meuTurno and GuiRestaUm.prontoPJogar:
      pecaID = self.canvas.itemcget(tag, 'image')[-1]
      if pecaID != GuiRestaUm.dictImgs['vazio']:
        reposicionar, rmDst, movErrado = GuiRestaUm.selecionaPeca(x, y, tag, self.meuID, self.cliRMI)
        if GuiRestaUm.pecaDestacada != -1:
          self.canvas.itemconfigure(tag, image=GuiRestaUm.img_peca_high)
        if rmDst != -1:
          self.canvas.itemconfigure(rmDst, image=GuiRestaUm.img_peca)

        if reposicionar:
          GuiRestaUm.reproduzSom('movimento')
          self.reposicionaPecas()
        if movErrado:
          GuiRestaUm.reproduzSom('mov_erro')

  def recebeJogadaAdversario(self):
    ''' # recebeJogadaAdversario

    Função para ser inicializada por execução de Threads que controla o recebimento de lances do adversário
    e para quando é dado o sinal de fim de jogo
    '''
    while True:
      try:
        sleep(0.5)
        recebeu, fim, desi = self.cliRMI.receberLance(self.meuID)
        if recebeu:
          GuiRestaUm.reproduzSom('movimento')
          self.reposicionaPecas()
        elif fim:
          if desi and not self.desistiu:
            self.checaFimDeJogo()
          break
      except:
        print("[Movimento]: nenhuma resposta obtida")

  def setTurnoAdversario(self):
    ''' # setTurnoAdversario

    Função para ser inicializada por execução de Threads que controla o recebimento da decisão
    de turno feita pelo adversário

    Aguarda até receber a mensagem e até o usuário local realizar a sua decisão, e caso as
    respostas entrem em conflito, reposiciona os componentes de decisão de turno
    '''
    while True:
      try:
        while GuiRestaUm.meuTurno == -1:
          sleep(0.5)
        while not self.cliRMI.turnosDefinidos():
          sleep(0.5)

        GuiRestaUm.prontoPJogar = True
        if GuiRestaUm.meuTurno == 0:
          GuiRestaUm.turnoVar.set("Você inicia a partida")
        elif GuiRestaUm.meuTurno == 1:
          GuiRestaUm.turnoVar.set("Seu adversario iniciará a partida")
        thread_jogo = Thread(target=self.recebeJogadaAdversario, daemon=True)
        thread_jogo.start()
        break
      except:
        print("[Turno]: nenhuma resposta obtida")

  def _setTurno(self, t: int):
    ''' # _setTurno

    Função dos botões de decisão de turno que define o desejo do usuário local de iniciar ou não a partida
    e envia para o adversário para verificação

    ## Parâmetro
    
    t : int (0 or 1)
        0 se o usuario local quiser iniciar a partida, ou 1 caso contrário
    '''
    GuiRestaUm.meuTurno = t
    if (self.cliRMI.definirTurno(self.meuID, t)):
      GuiRestaUm.botaoT1.destroy()
      GuiRestaUm.botaoT2.destroy()
      GuiRestaUm.labelDecTurno.destroy()

      GuiRestaUm.turnoVar.set("Aguardando resposta do seu adversário")
      GuiRestaUm.labelInfoTurno = Label(self.janela, textvariable=GuiRestaUm.turnoVar, font=GuiRestaUm.fonteText)
      GuiRestaUm.labelInfoTurno.place(x=520, y=15)
      GuiRestaUm.botaoDesistencia = Button(self.janela, text="Desistir", command=self._desistir, style="Estilizado.TButton", width=11)
      GuiRestaUm.botaoDesistencia.place(x=520, y=45)
    else:
      GuiRestaUm.meuTurno = -1
      GuiRestaUm.labelDecTurno.config(text=f"Seu adversário decidiu por este turno")

  def _desistir(self):
    self.desistiu = True
    self.cliRMI.desistencia(self.meuID)
    self.checaFimDeJogo()

  def reposicionaPecas(self):
    ''' # reposicionaPecas

    Função para realizar a re-renderização da posição das peças no tabuleiro
    '''
    posicoesTabuleiro = self.cliRMI.tabuleiro
    for i in range(1, 8):
      for j in range(1, 8):
        if posicoesTabuleiro[i][j] == '*':
          self.canvas.itemconfigure(self.tagPecas[i-1][j-1], image=GuiRestaUm.img_peca)
        if posicoesTabuleiro[i][j] == 'O':
          self.canvas.itemconfigure(self.tagPecas[i-1][j-1], image=GuiRestaUm.img_vazio)
    if GuiRestaUm.meuTurno == self.cliRMI.turno:
      GuiRestaUm.turnoVar.set("Sua vez")
    else:
      GuiRestaUm.turnoVar.set("Vez do adversário")

    self.checaFimDeJogo()

  def checaFimDeJogo(self):
    ''' # checaFimDeJogo

    Função que verifica se o jogo finalizou, se restou apenas uma peça, e se o usuário
    local venceu ou perdeu a partida

    Em caso de termino da partida, mostra o resultado em tela, inicia a animação de
    fim de jogo e adiciona a opção de jogar novamente
    '''
    terminou, contPecas = self.cliRMI.estaNoFim()

    if terminou:
      GuiRestaUm.turnoVar.set("")
      GuiRestaUm.botaoDesistencia.destroy()
      self.reproduzFimDeJogo()
      GuiRestaUm.prontoPJogar = False
      vencedor = self.cliRMI.vencedor == self.meuID

      fonteResultado = Font(size=18, weight="bold")
      if vencedor:
        if contPecas == -1:
          GuiRestaUm.labelInfoResultado = Label(self.janela,text="Parabéns, você venceu!\nSeu adversario desistiu!",font=fonteResultado)
        elif contPecas == 1:
          GuiRestaUm.labelInfoResultado = Label(self.janela,text="Parabéns, você venceu!\n         Restou Um!",font=fonteResultado)
        else:
          GuiRestaUm.labelInfoResultado = Label(self.janela,text=f"Fim de movimentos\n     Você venceu!\n      Restaram {contPecas}",font=fonteResultado)
        self.reproduzSom("vitoria")
      else:
        if contPecas == -1:
          GuiRestaUm.labelInfoResultado = Label(self.janela,text="Você desistiu :(",font=fonteResultado)
        elif contPecas == 1:
          GuiRestaUm.labelInfoResultado = Label(self.janela,text="Você perdeu :(\n   Restou Um  ",font=fonteResultado)
        else:
          GuiRestaUm.labelInfoResultado = Label(self.janela,text=f"Fim de movimentos\n    Você perdeu :(  \n      Restaram {contPecas}",font=fonteResultado)
        self.reproduzSom("derrota")

      GuiRestaUm.labelInfoResultado.place(x=650, y=65, anchor="center")
      GuiRestaUm.botaoResetaJogo = Button(
        self.janela,
        text="Novo Jogo",
        command=self.resetaJogo,
        style="Estilizado.TButton",
        width=10
      )
      GuiRestaUm.botaoResetaJogo.place(x=650, y=150, anchor="center")

  def resetaJogo(self):
    ''' # resetaJogo

    Função que limpa os componentes de resultado do jogo finalizado, reinicia a
    Thread de escolha de turnos, interrompe a Thread de animação de Fim de Jogo,
    reposiciona e renderiza as peças do tabuleiro e chama a função `criaComponenteTurnos`
    '''
    thread_turno = Thread(target=self.setTurnoAdversario, daemon=True)
    thread_turno.start()

    GuiRestaUm.meuTurno = -1

    self.cliRMI.reiniciaTabuleiro()
    self.reposicionaPecas()
    GuiRestaUm.turnoVar.set("")
    GuiRestaUm.labelInfoResultado.destroy()
    GuiRestaUm.botaoResetaJogo.destroy()
    GuiRestaUm.botaoDesistencia.destroy()
    self.canvas.moveto(GuiRestaUm.tagFimJogo, 75, -330)

    self.criaComponenteTurnos()
  
  def atualizarMensagens(self, mensgs: list[str]):
    ''' # atualizarMensagens

    Função que recebe uma nova mensagem registrada e a renderiza no componente
    da conversa do chat

    ## Parâmetros:
    
    identificador : str
        Identifica se a mensagem é do usuário local ou do adversário
    msg : str
        O texto da mensagem a ser exibida
    '''
    self.mensagens = mensgs
    qtdMsg = len(self.mensagens)
    lm = list(reversed(self.mensagens))
    mensagens: list[str] = []
    for i in range(11, -1, -1):
      if qtdMsg > i:
        mensg = lm[i].replace(self.meuID, "Você")
        mensg = mensg.replace("0__", "")
        mensg = mensg.replace("1__", "")
        mensagens.append(mensg)
      else :
        mensagens.append("")
    GuiRestaUm.variavelMensagens.set(mensagens)
    if qtdMsg > 12:
      qtdMsg = 12
    for i in range(11, 11-qtdMsg, -1):
      if mensagens[i].startswith("Voc"):
        GuiRestaUm.lboxMensagens.itemconfigure(i, background='#F0F0FF')
      else:
        GuiRestaUm.lboxMensagens.itemconfigure(i, background='#FFF')

  def chatRecebeMensagem(self):
    ''' # chatRecebeMensagem

    Função para ser inicializada por execução de Threads que controla o recebimento de
    mensagens do chat entre os usuários
    '''
    while True:
      try:
        msgs = self.cliRMI.receberMensagens(self.meuID)
        if msgs != None:
          self.atualizarMensagens(msgs)
        sleep(0.25)
      except:
        print("[Rec. msg]: nenhuma resposta obtida")

  def chatEnviaMensagem(self):
    ''' # chatEnviaMensagem

    Função que captura o texto digitado pelo usuário e envia para o adversário
    '''
    try:
      msg = self.minhaMensagem.get()
      if len(msg) > 0:
        self.minhaMensagem.set("")
        self.cliRMI.enviarMensagem(self.meuID, msg)
        self.mensagens.append(f"{self.meuID}: {msg}")
        self.atualizarMensagens(self.mensagens)
    except:
      print("[Env. Msg.]: nenhuma resposta obtida")

  def iniciaAplicacao(self):
    '''# iniciaAplicacao
    Inicia as Threads de recebimento de decisão de turnos do Jogo e de
    recebimento de mensagens do chat, e inicializa a interface gráfica
    '''
    # Criando a thread que recebe a escolha do turno do adversário via Socket
    thread_turno = Thread(target=self.setTurnoAdversario, daemon=True)
    thread_turno.start()

    # Criando a thread que recebe as mensagens do adversário via Socket
    thread_chat = Thread(target=self.chatRecebeMensagem, daemon=True)
    thread_chat.start()

    self.janela.mainloop()

### index.py
class Jogador:
  def __init__(self):
    self.nome: str = None

  def defineNome(self, nome: str):
    self.nome = nome

def mainApp():
  # Inicializando o socket do cliente do jogador
  print("Se tento criar um executavel sem esse console,")
  print("o arquivo é acusado como virus")
  print(";-;")

  jogador = Jogador()
  try:
    defineNome = GuiDefineNome(jogador.defineNome)
    defineNome.iniciaAplicacao()
  except Exception as e:
    print("erro defineNome:", e)

  if jogador.nome == None: return

  cli_id = cliente.registrarCliente(jogador.nome)
  # Inicializando o objeto que instanciará o jogo
  try:
    meuJogo = GuiRestaUm(cliente, cliente_id=cli_id)
  except Exception as e:
    print("erro meuJogo:", e)

  # Inicializando a aplicação grafica do jogo
  meuJogo.iniciaAplicacao()

if __name__ == "__main__":
  mainApp()