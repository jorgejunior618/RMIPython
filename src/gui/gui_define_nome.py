from tkinter import Tk, StringVar
from tkinter.font import Font
from tkinter.ttk import Style, Button, Label, Entry
from typing import Callable

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
