from models.cliente import cliente
from gui_resta_um import GuiRestaUm
from gui_define_nome import GuiDefineNome

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