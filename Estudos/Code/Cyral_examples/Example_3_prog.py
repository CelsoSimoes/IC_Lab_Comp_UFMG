import pycvc4
from pycvc4 import kinds

if __name__ == "__main__":

    #This program just simula what should verify, by receiving the user inputs
    #and telling if the input corresponds to a model allowed by the constraint.
    #This is the same code of Example_3.py untill the AssertFormula,
    #I choose to maintain the coments

    slv = pycvc4.Solver()
    slv.setOption("produce-models", "true")
    slv.setLogic("QF_S")

    #Defining the types of variables that we will use
    string = slv.getStringSort()
    integer = slv.getIntegerSort()

    #Concrete string constants. Represents the data:
    EMAIL = slv.mkString("EMAIL")
    CCN = slv.mkString("CCN")
    SSN = slv.mkString("SSN")

    #We were thinking ways to represent that all the possible datas can be accessed;
    #Solutions are: Using StringPrefixes or Regular Expressions.
    #In this case i use Regex to specify what are the possible datas and, with this, print the models
    #But in the test, believe that we can use StringPrefixes instead.

    #Converting the strings into Regex(Regular expressions)
    EMAIL_regex = slv.mkTerm(kinds.StringToRegexp, EMAIL)
    CCN_regex = slv.mkTerm(kinds.StringToRegexp, CCN)
    SSN_regex = slv.mkTerm(kinds.StringToRegexp, SSN)

    #Combining the strings in one Regex
    uniao = slv.mkTerm(kinds.RegexpUnion, EMAIL_regex, CCN_regex, SSN_regex)

    #Variables, that represents each Rule segment of this example.
    identities_users = slv.mkConst(string, "identities_users")
    reads_data = slv.mkConst(string, "reads_data")
    reads_rows = slv.mkConst(integer, "reads_rows")
    updates_data = slv.mkConst(string, "updates_data")
    updates_rows = slv.mkConst(integer, "updates_rows")
    deletes_data = slv.mkConst(string, "deletes_data")
    deletes_rows = slv.mkConst(integer, "deletes_rows")

    #Defining Concrete Constants, that represents the Users in this example
    bob = slv.mkString("bob")
    alice = slv.mkString("alice")
    tom = slv.mkString("tom")
    alex = slv.mkString("alex")
    jeff = slv.mkString("jeff")

    #Building the constraints that represents the allow statments; most important part.
    X0 = slv.mkTerm(kinds.And,
                            slv.mkTerm(kinds.Or, identities_users.eqTerm(bob), identities_users.eqTerm(tom), identities_users.eqTerm(alex)),
                            slv.mkTerm(kinds.StringInRegexp, reads_data, uniao),
                            slv.mkTerm(kinds.Geq, reads_rows, slv.mkReal(1)),
                            updates_data.eqTerm(CCN),
                            updates_rows.eqTerm(slv.mkReal(1)),
                            slv.mkTerm(kinds.StringInRegexp, deletes_data, uniao),
                            deletes_rows.eqTerm(slv.mkReal(1))
                    )

    X1 = slv.mkTerm(kinds.And,
                              identities_users.eqTerm(alice).orTerm(identities_users.eqTerm(jeff)),
                              reads_data.eqTerm(EMAIL).orTerm(reads_data.eqTerm(CCN)),
                              reads_rows.eqTerm(slv.mkReal(1)),
                              updates_data.eqTerm(EMAIL),
                              updates_rows.eqTerm(slv.mkReal(1))
                    )

    #Asserting to the solver the formula, estabilshing that access is granted if X0 or X1 is true
    slv.assertFormula(X0.orTerm(X1))

    #Different part of the code.
    #Getting Users inputs, to determine if access is granted or deny.
    print("Test model, to see if you have the proper access.\n")
    input_user = input("User: ")
    print("Reads:\n")

    #To get access you will need to put exactly inputs
    #Example:
    #   user: "bob"
    #   data: "EMAIL";"CCN";"EMAIL" for each "Data"
    #   rows: "1";"1"; "1" for each "Rows"
    input_reads_data = input("  Data: ")
    input_reads_rows = int(input("  Rows: "))
    print("Updates:\n")
    input_updates_data = input("  Data: ")
    input_updates_rows = int(input("  Rows: "))
    print("Deletes:\n")
    input_deletes_data = input("  Data: ")
    input_deletes_rows = int(input("  Rows: "))

    #Converting, from python inputs to CVC4 string constants:
    test_user = slv.mkString(input_user)
    test_reads_data = slv.mkString(input_reads_data)
    test_reads_rows = slv.mkReal(input_reads_rows)
    test_updates_data = slv.mkString(input_updates_data)
    test_updates_rows = slv.mkReal(input_updates_rows)
    test_deletes_data = slv.mkString(input_deletes_data)
    test_deletes_rows = slv.mkReal(input_deletes_rows)

    #Asserting the equalities
    slv.assertFormula(slv.mkTerm(kinds.And,
                                    identities_users.eqTerm(test_user),
                                    reads_data.eqTerm(test_reads_data),
                                    reads_rows.eqTerm(test_reads_rows),
                                    updates_data.eqTerm(test_updates_data),
                                    updates_rows.eqTerm(test_updates_rows),
                                    deletes_data.eqTerm(test_deletes_data),
                                    deletes_rows.eqTerm(test_deletes_rows)
                                )
                        )

    #Check your inputs satisfiability, if is "sat" you have access.
    print("\nYou model is: ", slv.checkSat())

    print("-----------------\nModel:\n")
    print("Identitie-\n     User: ", input_user)
    print("Reads-\n     Data: ", input_reads_data)
    print("     Rows: ", input_reads_rows)
    print("Updtates-\n     Data: ", input_updates_data)
    print("     Rows: ", input_updates_rows)
    print("Deletes-\n     Data:", input_deletes_data)
    print("     Rows: ", input_deletes_rows)

    print("\nIs: ")
    if slv.checkSat()._name == "sat":
        print(" Allowed")
    else:
        print(" Denied")
