import pycvc4
from pycvc4 import kinds

if __name__ == "__main__":

    #This program print the models Allowed by the constraints of Example 1

    #These three, are standard lines:
    #Especifiyng the name we will use to call the solver commands
    slv = pycvc4.Solver()
    #Necessary line to enable the production of models
    slv.setOption("produce-models", "true")
    #Defining logic
    slv.setLogic("QF_S")

    #Defining the types of variables that we will use
    string = slv.getStringSort()
    integer = slv.getIntegerSort()

    #Concrete string constants. Represents the data:
    data_EMAIL = slv.mkString("EMAIL")
    data_CCN = slv.mkString("CCN")
    data_SSN = slv.mkString("SSN")

    #Variables, that represents each Rule segment of this example.
    identities_users = slv.mkConst(string, "identities_users")
    reads_data = slv.mkConst(string, "reads_data")
    reads_rows = slv.mkConst(integer, "reads_rows")
    updates_data = slv.mkConst(string, "updates_data")
    updates_rows = slv.mkConst(integer, "updates_rows")

    #Defining Concrete Constants, that represents the Users bob and alice
    bob = slv.mkString("bob")
    alice = slv.mkString("alice")

    #Constant that i could use to represent a infinite number of rows
    infinit_rows = slv.mkTerm(kinds.Geq, reads_rows, slv.mkReal(0))

    #Creating constraints that represents each allow statment
    #In this example i dont use Regexes or StringPrefix. Just specify each term
    X0 = slv.mkTerm(kinds.And,
                        identities_users.eqTerm(bob),
                        reads_data.eqTerm(data_EMAIL).orTerm(reads_data.eqTerm(data_CCN).orTerm(reads_data.eqTerm(data_SSN))),
                        infinit_rows)

    X1 = slv.mkTerm(kinds.And,
                        identities_users.eqTerm(alice),
                        reads_data.eqTerm(data_EMAIL).orTerm(reads_data.eqTerm(data_CCN)),
                        reads_rows.eqTerm(slv.mkReal(1)),
                        updates_data.eqTerm(data_EMAIL),
                        updates_rows.eqTerm(slv.mkReal(1)))

    #Combining the constraints, saying that acces is granted if X0 or X1 is true
    Constraint_1 = X0.orTerm(X1)

    #Asserting the formula to the solver and Check the Satisfiability.
    slv.assertFormula(Constraint_1)
    print("CVC4 reports:", Constraint_1, "is", slv.checkSat())

    #Counter
    count_models = 0

    #Printing "all" the possible models allowed by the constraint, while the
    #formula is "Sat".
    while slv.checkSat()._name == "sat":
        count_models += 1
        print("-----------------\nModel {}:\n".format(count_models))
        print("ID-\n     User: ", slv.getValue(identities_users))
        print("Reads-\n     Data: ", slv.getValue(reads_data))
        print("     Rows: ", slv.getValue(reads_rows))
        print("Updtates-\n     Data: ", slv.getValue(updates_data))
        print("     Rows: ", slv.getValue(updates_rows))

        # Block the model found by saying that at least one of the values must
        # be different
        slv.assertFormula(slv.mkTerm(kinds.Or,
                                    identities_users.eqTerm(slv.getValue(identities_users)).notTerm(),
                                    reads_data.eqTerm(slv.getValue(reads_data)).notTerm()))
