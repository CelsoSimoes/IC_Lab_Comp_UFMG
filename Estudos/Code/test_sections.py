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
  cs240 = slv.mkConst(stringSort, "cs240/")

  # create the string constans used in the policy
  students = slv.mkString("students")
  tas = slv.mkString("tas")

  getObject = slv.mkString("getObject")

  cs240exam = slv.mkString("Exam.pdf")
  cs240answer = slv.mkString("Answer.pdf")

  # create constraints representing each allow statement
  X0 = slv.mkTerm(kinds.And,
                  p.eqTerm(students),
                  a.eqTerm(getObject),
                  r.eqTerm(cs240.eqTerm(cs240exam)))

  X1 = slv.mkTerm(kinds.And,
                  p.eqTerm(tas),
                  a.eqTerm(getObject),
                  r.eqTerm(cs240.eqTerm(cs240exam)).orTerm(r.eqTerm(cs240.eqTerm(cs240answer))))

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
