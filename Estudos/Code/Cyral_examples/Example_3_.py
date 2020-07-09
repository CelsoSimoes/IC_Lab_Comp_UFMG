import pycvc4
from pycvc4 import kinds

if __name__ == "__main__":

    #This program print the models Allowed by the constraints of Example 3

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

    #We were thinking ways to represent that all the possible datas can be
    # accessed. Solutions are: Using StringPrefixes or Regular Expressions.
    #In this example i use Regex to specify what are the possible datas and, with
    # this, print the models
    #But in the test, believe that we can use StringPrefixes instead.

    #Converting the strings into Regex(Regular expressions)
    EMAIL_regex = slv.mkTerm(kinds.StringToRegexp, EMAIL)
    CNN_regex = slv.mkTerm(kinds.StringToRegexp, CCN)
    SSN_regex = slv.mkTerm(kinds.StringToRegexp, SSN)

    #Combining the strings in one Regex
    uniao = slv.mkTerm(kinds.RegexpUnion, EMAIL_regex, CNN_regex, SSN_regex)

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

    #Combining the constraints, saying thar access is granted if X0 or X1 is true
    Constraint = slv.mkTerm(kinds.Or, X0, X1)

    #Asserting to the solver the formula
    slv.assertFormula(Constraint)

    #Checkingif the Constraint is Satisfiable
    print("CVC4 reports:", Constraint, "is", slv.checkSat())

    #Counter and the constant that i use to compara in the if Statment
    count_models = 0
    empty_string = slv.mkString("")

    #Printing "all" the possible models allowed by the constraint, while the
    #formula is "Sat". Since "any" means infinite for the rows number, we will
    #not print "all" the models
    while slv.checkSat()._name == "sat":
        count_models += 1
        print("-----------------\nModel {}:\n".format(count_models))
        print("ID-\n     User: ", slv.getValue(identities_users))
        print("\nReads-\n     Data: ", slv.getValue(reads_data))
        print("     Rows: ", slv.getValue(reads_rows))
        print("\nUpdtates-\n     Data: ", slv.getValue(updates_data))
        print("     Rows: ", slv.getValue(updates_rows))

        #If the value os deletes_data variable is not empty, we will print it
        if not (slv.getValue(deletes_data) == empty_string):
            print("\nDeletes-\n     Data:", slv.getValue(deletes_data))
            print("     Rows: ", slv.getValue(deletes_rows))

        #The "getValue" gets the actual value of the variavle, where the formula
        #is "sat". The "notTerm" prevents the value of appearing again

        # Block the model found by saying that at least one of the values, of
        #those that have 2 or more possible values,must be different
        #(The if else condition it's used to prevent us from "exclude" one empty
        # value and ended uo in an infinite loop)
        if not (slv.getValue(deletes_data) == empty_string):
            slv.assertFormula(slv.mkTerm(kinds.Or,
                                    identities_users.eqTerm(slv.getValue(identities_users)).notTerm(),
                                    reads_data.eqTerm(slv.getValue(reads_data)).notTerm(),
                                    deletes_data.eqTerm(slv.getValue(deletes_data)).notTerm())
                              )
        else:
            slv.assertFormula(slv.mkTerm(kinds.Or,
                                    identities_users.eqTerm(slv.getValue(identities_users)).notTerm(),
                                    reads_data.eqTerm(slv.getValue(reads_data)).notTerm())
                              )
