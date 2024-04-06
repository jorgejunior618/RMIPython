import Pyro4
from models.resta_um import IJogoRestaUm

uri = "PYRONAME:resta_um.servidor"
cliente: IJogoRestaUm = Pyro4.Proxy(uri)
