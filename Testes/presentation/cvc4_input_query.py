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

    X0 = slv.mkTerm(kinds.And, Actors.eqTerm(slv.mkString('Alice')),
                  slv.mkTerm(kinds.Or, slv.mkTerm(kinds.And,
                   Action.eqTerm(slv.mkString('Updates')),
                      slv.mkTerm(kinds.Or, Resources.eqTerm(slv.mkString('CCN')),
                                  Resources.eqTerm(slv.mkString('EMAIL')))),
                  slv.mkTerm(kinds.And, Action.eqTerm(slv.mkString('Deletes')),
                      slv.mkTerm(kinds.Or, Resources.eqTerm(slv.mkString('CCN')),
                                    Resources.eqTerm(slv.mkString('EMAIL'))))))

    X1 = slv.mkTerm(kinds.And, Actors.eqTerm(slv.mkString('Bob')),
                  slv.mkTerm(kinds.Or, slv.mkTerm(kinds.And,
                      Action.eqTerm(slv.mkString('Updates')),
                          slv.mkTerm(kinds.Or, Resources.eqTerm(slv.mkString('CCN')),
                          Resources.eqTerm(slv.mkString('EMAIL')))),
                  slv.mkTerm(kinds.And, Action.eqTerm(slv.mkString('Deletes')),
                                Resources.eqTerm(slv.mkString('EMAIL')))))

    Policy = slv.mkTerm(kinds.Or, X0, X1)
    slv.assertFormula(Policy)
    print("CVC4 reports: The Policy is", slv.checkSat())

    print("Input your query:\n")
    input_Actor = input("  Actor: ")
    input_Action = input("  Action: ")
    input_Resource = input("  Resource: ")

    query = slv.mkTerm(kinds.And, Actors.eqTerm(slv.mkString(input_Actor)),
                        Action.eqTerm(slv.mkString(input_Action)),
                        Resources.eqTerm(slv.mkString(input_Resource)))

    if slv.checkSatAssuming(query)._name  == "sat":
        print("Query Allowed")
    else:
        print("Query Denied")
