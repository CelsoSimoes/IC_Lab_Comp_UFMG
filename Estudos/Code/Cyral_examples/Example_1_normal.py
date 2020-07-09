import pycvc4
from pycvc4 import kinds

if __name__ == "__main__":

    slv = pycvc4.Solver()
    slv.setOption("produce-models", "true")
    slv.setLogic("QF_S")

    #Definindo os tipos de varaiveis a serem utilizados
    string = slv.getStringSort()
    integer = slv.getIntegerSort()

    #data = slv.mkConst(string, "data")
    #Possible equalities of Data:
    data_EMAIL = slv.mkString("/EMAIL")
    data_CCN = slv.mkString("/CCN")
    data_SSN = slv.mkString("/SSN")

    rules = slv.mkConst(string, "rules")

    #Our rules that are also symbolic constants too
    identities_users = slv.mkConst(string, "identities_users")
    reads_data = slv.mkConst(string, "reads_data")
    reads_rows = slv.mkConst(integer, "reads_rows")
    updates_data = slv.mkConst(string, "updates_data")
    updates_rows = slv.mkConst(integer, "updates_rows")
    deletes_data = slv.mkConst(string, "deletes_data")
    deletes_rows = slv.mkConst(integer, "deletes_rows")

    #Defining last Symbolic Constants
    #users = slv.mkConst(string, "users")
    #rows = slv.mkConst(integer, "rows")
    #Defining Concrete Constants
    bob = slv.mkString("bob")
    alice = slv.mkString("alice")

    #any_data = slv.mkTerm(kinds.Or, data_EMAIL, data_CCN, data_SSN)
    infinit_rows = slv.mkTerm(kinds.Geq, reads_rows, slv.mkReal(0))
    #Creating constraints that represents each allow statment
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

    Constraint_1 = X0.orTerm(X1)

    #Check sat
    slv.assertFormula(Constraint_1)
    print("CVC4 reports:", Constraint_1, "is", slv.checkSat())

    count_models = 0
    while slv.checkSat()._name == "sat":
        count_models += 1
        print("-----------------\nModel {}:\n".format(count_models))
        print("ID-\n     User: ", slv.getValue(identities_users))
        print("Reads-\n     Data: ", slv.getValue(reads_data))
        print("Reads-\n     Rows: ", slv.getValue(reads_rows))
        print("Updtates-\n     Data: ", slv.getValue(updates_data))
        print("Updtates-\n     Rows: ", slv.getValue(updates_rows))

        slv.assertFormula(slv.mkTerm(kinds.Or,
                                    identities_users.eqTerm(slv.getValue(identities_users)).notTerm(),
                                    reads_data.eqTerm(slv.getValue(reads_data)).notTerm()))
