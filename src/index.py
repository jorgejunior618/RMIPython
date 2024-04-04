from models.cliente import cliente
from gui_resta_um import GuiRestaUm

def mainApp():
  # Inicializando o socket do cliente do jogador
  print("Se tento criar um executavel sem esse console,")
  print("o arquivo é acusado como virus")
  print(";-;")

  cli_id = cliente.registrarCliente("jorge")
  # Inicializando o objeto que instanciará o jogo
  try:
    meuJogo = GuiRestaUm(cliente, cliente_id=cli_id)
  except Exception as e:
    print(e)

  # Inicializando a aplicação grafica do jogo
  meuJogo.iniciaAplicacao()

if __name__ == "__main__":
  mainApp()