from fractions import Fraction

def reverse(fraction: Fraction) -> Fraction:
  return Fraction(fraction.denominator, fraction.numerator)

def indexMaxPositive(values: list[Fraction]) -> int:
  response: int = 0
  for i in range(0, len(values), 1):
    if values[i] > values[response] and values[i] > 0:
      response = i
  return response

class Value:
  def __init__(self, name, value) -> None:
    self.name = name
    self.value = value

class SimplexRow:
  def __init__(self, numero: int, variables: list[str], values: list[Fraction], sign: str, equal: Fraction, nFunctions: int) -> None:
    self.numero: int = numero
    self.variables: list(str) = variables
    self.nVariables = len(self.variables)
    self.values: list(Fraction) = values
    self.sign: str = sign
    self.equal: Fraction = equal
    self.addVariable(nFunctions)
  
  def addVariable(self, nFunctions: int) -> None:
    i: int = 1
    while i <= nFunctions:
      self.variables.append("S" + str(i))
      if i == self.numero:
        if self.sign == "=":
          self.values.append(0)
        if self.sign == ">=":
          self.values.append(-1)
        if self.sign == "<=":
          self.values.append(1)
      else:
        self.values.append(0)
      i += 1

  def fractionRatio(self, index: int) -> None:
    return reverse(self.values[index])
  
  def multiply(self, fraction: Fraction) -> None:
    for i in range(0, len(self.values), 1):
      self.values[i] *= fraction
    self.equal *= fraction

  def simplify(self, index: int) -> None:
    ratio = self.fractionRatio(index)
    self.multiply(ratio)
  
  def ratio(self, index: int, simplex) -> Fraction:
    return simplex.values[index] / self.values[index]
  
  def calcul(self, fraction: Fraction, simplex) -> None:
    for i in range(0, len(self.values), 1):
      simplex.values[i] -= (self.values[i] * fraction)
    simplex.equal -= (self.equal * fraction)

  def __str__(self) -> str:
    response: str = ""
    for i in range(0, len(self.variables), 1):
      response += str(self.values[i]) + "" + str(self.variables[i]) + " "
    response += str(self.sign) + " " + str(self.equal)
    return response


class Simplex:
  def __init__(self, objectiveFunction: SimplexRow, functions: list[SimplexRow]) -> None:
    self.objectiveFunction = objectiveFunction
    self.functions = functions
    
  def isMaxResolved(self) -> bool:
    for item in self.objectiveFunction.values:
      if item > 0:
        return False
    return True

  def isMinResolved(self) -> bool:
    for item in self.objectiveFunction.values:
      if item < 0:
        return False
    return True
  
  def ratios(self, index: int):
    response = []
    for i in self.functions:
      if i.values[index] != 0:
        response.append(i.equal / i.values[index])
      else:
        response.append(-1)
    return response
  
  def pivotIndexMax(self, index: int):
    response = 0
    ratios = self.ratios(index)
    for i in range (0, len(ratios), 1):
      if self.functions[i].values[index] > 0:
        if ratios[response] > ratios[i] or ratios[response] < 0:
          response = i
    return response
  
  def initBasis(self):
    response = []
    for i in range(0, len(self.functions), 1):
      response.append("S" + str(i + 1))
    return response
  
  def variables(self):
    return self.functions[0].variables + self.initBasis()

  def max(self):
    basis = self.initBasis()
    variables = self.variables()
    while (not self.isMaxResolved()):
      # print("itteration")
      index = indexMaxPositive(self.objectiveFunction.values)
      pivotIndex = self.pivotIndexMax(index)
      # print(index)
      # print(pivotIndex)
      # print(self)
      self.functions[pivotIndex].simplify(index)
      pivot = self.functions[pivotIndex]
      ratioObjective = pivot.ratio(index, self.objectiveFunction)
      pivot.calcul(ratioObjective, self.objectiveFunction)
      basis[pivotIndex] = variables[index]
      for i in range(0, len(self.functions), 1):
        if i != pivotIndex:
          ratioFunction = pivot.ratio(index, self.functions[i])
          pivot.calcul(ratioFunction, self.functions[i])
    response = []
    for i in range(0, len(basis), 1):
      response.append(Value(basis[i], self.functions[i].equal))
    response.append(Value("F", -self.objectiveFunction.equal))
    return response

  def transpose(self):
    inequations = []
    i = 0
    while i < self.objectiveFunction.nVariables:
      variables = []
      for h in self.functions:
        variables.append("y" + str(h.numero))
      values = []
      for func in self.functions:
        values.append(func.values[i])
      sign = "<="
      simplexRoe = SimplexRow(i + 1, variables, values, sign, self.objectiveFunction.values[i], self.objectiveFunction.nVariables)
      inequations.append(simplexRoe)
      i += 1
    variables = []
    values = []
    for h in self.functions:
      variables.append("y" + str(h.numero))
      values.append(h.equal)
    newObjectiveFUnction = SimplexRow(0, variables, values, "=", Fraction(0), self.objectiveFunction.nVariables)
    return Simplex(newObjectiveFUnction, inequations)
  
  def min(self):
    transponse = self.transpose()
    response = transponse.max()
    print(transponse)
    return response
  
  def __str__(self) -> str:
    response = ""
    for function in self.functions:
      response += function.__str__() + "\n"
    response += self.objectiveFunction.__str__() + "\n"
    return response


# simplex = Simplex(
#   SimplexRow(0, ["x", "y"], [Fraction(30, 1), Fraction(50, 1)], "=", Fraction(0, 1), 3),
#   [
#     SimplexRow(1, ["x", "y"], [Fraction(3, 1), Fraction(2, 1)], "<=", Fraction(1800, 1), 3),
#     SimplexRow(2, ["x", "y"], [Fraction(1, 1), Fraction(0, 1)], "<=", Fraction(400, 1), 3),
#     SimplexRow(3, ["x", "y"], [Fraction(0, 1), Fraction(1, 1)], "<=", Fraction(600, 1), 3),
#   ]
# )

# simplex.max()
# print(simplex)
simplex = Simplex(
  SimplexRow(0, ["x1", "x2"], [Fraction(40), Fraction(50)], "=", Fraction(0), 3),
  [
    SimplexRow(1, ["x1", "x2"], [Fraction(1), Fraction(2)], "<=", Fraction(700), 3),
    SimplexRow(2, ["x1", "x2"], [Fraction(2), Fraction(1)], "<=", Fraction(800), 3),
    SimplexRow(3, ["x1", "x2"], [Fraction(0), Fraction(1)], "<=", Fraction(225), 3)
  ]
)
# transponse = simplex.transpose()
print("Matrice de base")
print(simplex)

print("solutions")
response = simplex.max()
for item in response:
  print(item.name + " " + str(item.value))
print("")
# print("transpose")
# print(simplex.transpose())
print("Solution")
print(simplex)