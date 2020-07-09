import pycvc4
from pycvc4 import kinds

if __name__ == "__main__":

    slv = pycvc4.Solver()
    slv.setOption("produce-models", "true")
    slv.setLogic("QF_S")

    #Definindo os tipos de varaiveis a serem utilizados
    string = slv.getStringSort()
    integer = slv.getIntergerSort()

    data = slv.mkConst(string, "data")
    #Possible equalities of Data:
    EMAIL = slv.mkString("EMAIL")
    CCN = slv.mkString("CCN")
    SSN = slv.mkString("SSN")

    rules = slv.mkConst(string, "rules")
    #Our rules that are also symbolic constants too
    identities = slv.mkConst(string, "identities")
    reads = slv.mkConst(string, "reads")
    updates = slv.mkConst(string, "updates")
    deletes = slv.mkConst(string, "deletes")

    #Definindo as constantes simbolicas
    users = slv.mkConst(string, "users")
    rows = slv.mkConst(string, "rows")

    bob = slv.mkString("bob")
    tom = slv.mkString("tom")
    alex = slv.mkString("alex")
    alice = slv.mkString("alice")
    jeff = slv.mkString("jeff")

    
