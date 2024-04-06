import Pyro4
import Pyro4.naming
from models.servidor import ServidorRestaUm

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