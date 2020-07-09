import pycvc4
from pycvc4 import kinds

if __name__ == "__main__":
  slv = pycvc4.Solver()
  slv.setOption("produce-models", "true")
  slv.setLogic("QF_S")

  stringSort = slv.getStringSort()

  # create symbolic constants representing the policy fields
  p = slv.mkConst(stringSort, "p")
  a = slv.mkConst(stringSort, "a")
  r = slv.mkConst(stringSort, "r")

  # create the string constans used in the policy
  students = slv.mkString("students")
  tas = slv.mkString("tas")

  getObject = slv.mkString("getObject")

  cs240exam = slv.mkString("cs240/Exam.pdf")
  cs240answer = slv.mkString("cs240/Answer.pdf")
  #Question: Can i create one equalite of 3 sections? Like here, instead of r.eqTerm(cs240exam). I could: r.eqTerm(cs240.eqTerm(exam)). Course, cs240 being symbolic also?

  # create constraints representing each allow statement
  X0 = slv.mkTerm(kinds.And,
                  p.eqTerm(students),
                  a.eqTerm(getObject),
                  r.eqTerm(cs240exam))

  X1 = slv.mkTerm(kinds.And,
                  p.eqTerm(tas),
                  a.eqTerm(getObject),
                  r.eqTerm(cs240exam).orTerm(r.eqTerm(cs240answer)))

  # assert to the solver the formula estabilshing that access is granted if X0
  # or X1 is true
  slv.assertFormula(X0.orTerm(X1))

  # while there is a model for the formula, print values of symbolic constants
  modelCount = 0
  while slv.checkSat()._name == "sat":
    modelCount += 1
    print("++++++++++\nModel {}:\n".format(modelCount))
    print("p =", slv.getValue(p))
    print("a =", slv.getValue(a))
    print("r =", slv.getValue(r))
    # block the model found by saying that at least one of the values must be
    # different
    slv.assertFormula(slv.mkTerm(kinds.Or,
                                 p.eqTerm(slv.getValue(p)).notTerm(),
                                 a.eqTerm(slv.getValue(a)).notTerm(),
                                 r.eqTerm(slv.getValue(r)).notTerm()))

#Policy Y:
  #Reseting al the current assertions
  slv.resetAssertions()

  #Creating symbolic constants * and others
  all_p = slv.mkConst(stringSrot, "all_p") #How to represent this? Or we simply dont put on the allow statement?
  all_r = slv.mkConst(stringSort, "all_r")
  allp = slv.mkTerm(kinds.Or, p.eqTerm(students), p.eqTerm(tas))
  allr = slv.mkTerm(kinds.Or, r.eqTerm(cs240exam), r.eqTerm(cs240answer))
  #teachers = slv.mkString("teachers")

  Y0 = slv.mkTerm(kinds.And,
                    p.eqTerm(allp),
                    a.eqTerm(getObject),
                    r.eqTerm(allr))

  Y1 = slv.mkTerm(kinds.And,
                    p.eqTerm(students),
                    a.eqTerm(getObject),
                    r.eqTerm(cs240answer))

  #Asserting that the acess is alowed only when Y0 and (not Y1) is true
  slv.assertFormula(Y0.andTerm(Y1.notTerm()))

  #While theres models, keep couting
  countmodel_y = 0
  while slv.checkSat()._name == "sat":
    countmodel_y += 1
    print("--------------\nModel {}:\n".format(countmodel_y))
    print("p =", slv.getValue(p))
    print("a =", slv.getValue(a))
    print("r =", slv.getValue(r))
    #block the model found by saying that at least one of the values must be
    #different. The .notTerm(), can be used before the Symbolic constant
    slv.assertFormula(slv.mkTerm(kinds.Or,
                                 p.eqTerm(slv.getValue(p)).notTerm(),
                                 a.eqTerm(slv.getValue(a)).notTerm(),
                                 r.eqTerm(slv.getValue(r)).notTerm()))

  #But we know that this is just a representation, cause we dont have "all" the
  #possible principals, and will be more than just a few models that will be true

  slv.resetAssertions()

  #Testing if X0 and X1 is lesser or equal permissive than Y0 and (not)Y1
  X = slv.mkTerm(kinds.Or, X0, X1)
  Y = slv.mkTerm(kinds.And, Y0, Y1.notTerm())

  less_equal = slv.mkTerm(kinds.Implies, X, Y)
  Not_less_equal = slv.mkTerm(kinds.Not, less_equal)
  slv.assertFormula(Not_less_equal)
  print(Not_less_equal)
  print(slv.checkSat())
