import typing as t

class Conditional(t.Protocol):
    def evaluate(**kwargs) -> bool:
        ...
    
    def operators(self) -> t.List[str]:
        ...


class NumericalComparisonConditional(Conditional):
    def __init__(self, op: str, sentinel: float):
        self._operator = op
        self._sentinel = sentinel

    def operators(self) -> t.List[str]:
        return ["lt", "gt", "eq", "lte", "gte"]

    def evaluate(self, input) -> bool:
        if self._operator == "lt":
            output = input < self._sentinel
            log = f"Numerical({input} < {self._sentinel} == {output})"
        elif self._operator == "gt": 
            output = input > self._sentinel
            log = f"Numerical({input} > {self._sentinel} == {output})"
        elif self._operator == "gte":
            output = input >= self._sentinel
            log = f"Numerical({input} >= {self._sentinel} == {output})"
        elif self._operator == "lte":
            output = input <= self._sentinel
            log = f"Numerical({input} <= {self._sentinel} == {output})"
        else:
            output = input == self._sentinel
            log = f"Numerical({input} = {self._sentinel} == {output})"
        
        print(f'{log} {"succeeds" if output else "fails"}')
        return output


class OrComparisonConditional(Conditional):
    def __init__(self, c_lhs: Conditional, c_rhs: Conditional):
        self._lhs = c_lhs
        self._rhs = c_rhs

    def operators(self) -> t.List[str]:
        return []

    def evaluate(self, input) -> bool:
        if self._lhs.evaluate(input=input) or self._rhs.evaluate(input=input):
            print("Or compound comparison succeeds")
            return True
        
        print("Or compound comparison fails")
        return False


class Unconditional(Conditional):
    def __init__(self):
        ...
    
    def evaluate(self, input) -> bool:
        print("Unconditional comparison succeeds")
        return True
    
    def operators(self) -> t.List[str]:
        return []
