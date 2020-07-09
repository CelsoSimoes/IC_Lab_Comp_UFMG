import pycvc4
from pycvc4 import kinds

if __name__ == "__main__":
    solucionador = pycvc4.Solver()
    olamundo = solucionador.mkConst(solucionador.getBooleanSort(), "Ola Mundo!!!")
    print(olamundo, "e", solucionador.checkEntailed(olamundo))
    print(solucionador.checkSat(olamundo))
