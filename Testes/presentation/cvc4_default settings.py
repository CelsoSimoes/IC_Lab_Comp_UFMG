import pycvc4
from pycvc4 import kinds

if __name__ == "__main__":

    #This program print the models allowed by the constraints of our Legalease
    # file

    #Standard lines
    slv = pycvc4.Solver()
    slv.setOption("produce-models", "true")
    slv.setOption("output-lang", "smt2.6")
    slv.setLogic("QF_S")

    #Defining the types of variables that we will use
    string = slv.getStringSort()
    integer = slv.getIntegerSort()

    #Defining our variables
    Actors = slv.mkConst(string, 'Actors')
    Action = slv.mkConst(string, 'Action')
    Resources = slv.mkConst(string, 'Resources')
    Rows = slv.mkConst(integer, 'Rows')
