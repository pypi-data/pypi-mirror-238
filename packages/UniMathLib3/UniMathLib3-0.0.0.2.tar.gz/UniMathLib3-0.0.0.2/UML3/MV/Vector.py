from typing import Iterable
from .MV_error import VectorDimensionMismatchError, VectorLengthMismatchError, VectorOutOfRangeError, VectorError

class Vector():

    def __init__(self, data:list[int|float]) -> None: 
        self.vector = data

    def __setitem__(self, key, value:int | float):
        self.vector[key] = value
    
    def __getitem__(self, key):
        try:
            return self.vector[key]
        except:
            raise VectorOutOfRangeError(key,len(self))
    
    def __iter__(self):
        return iter(self.vector)
    
    def __len__(self):
         return len(self.vector)
    
    def __str__(self):
        if not self.vector:
            return "[\n]"
        result = "[\n"
        for element in self.vector:
            result += f" [{element}]\n"
        result += "]"
        return result

    def __add__(self, other:'Vector') -> 'Vector':
        if len(self) == len(other):
            return Vector([self_el + other_el for self_el, other_el in zip(self,other)])
        else:
            raise VectorLengthMismatchError()

    def extend(self, iterable:Iterable[int | float]):
        self.vector.extend(iterable)
    
    def append(self, item:int|float):
        self.vector.append(item)

    def clear(self):
        self.vector.clear()

    @property
    def sort(self):
        if len(self) <= 1:
                return self
        stack = [(0, len(self) - 1)]  
        while stack:
                left, right = stack.pop()
                pivot_index = self._partition(left, right)
                if pivot_index - 1 > left:
                    stack.append((left, pivot_index - 1))
                if pivot_index + 1 < right:
                    stack.append((pivot_index + 1, right))
        return self
    
    def _partition(self, left, right):
        pivot = self[right]
        i = left - 1
        for j in range(left, right):
            if self[j] <= pivot:
                i += 1
                self[i], self[j] = self[j], self[i]
        self[i + 1], self[right] = self[right], self[i + 1]
        return i + 1







