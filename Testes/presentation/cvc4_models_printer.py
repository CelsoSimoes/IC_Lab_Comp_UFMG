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

    #Counter
    count_models = 0

    #Here we print all the models/querys allowedby the policy.
    while slv.checkSat()._name == "sat":
        count_models += 1
        print("-----------------\nModel {}:\n".format(count_models))
        print("ID-\n     Actor: ", slv.getValue(Actors))
        print("     Action: ", slv.getValue(Action))
        print("     Resource: ", slv.getValue(Resources))

        slv.assertFormula(slv.mkTerm(kinds.Or,
                        Actors.eqTerm(slv.getValue(Actors)).notTerm(),
                        Action.eqTerm(slv.getValue(Action)).notTerm(),
                        Resources.eqTerm(slv.getValue(Resources)).notTerm())
                  )
