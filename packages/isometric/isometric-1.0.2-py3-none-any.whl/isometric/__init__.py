import math as _math

_y = .75 ** .5
class _Empty:
    pass
class Vector(tuple):
    @classmethod
    def _num(cls, obj, /):
        ans = int(obj)
        if ans == obj:
            return ans
        else:
            raise ValueError
    @classmethod
    def from_polar(cls, *, orientation, distance):
        return cls(distance, distance).rotate(steps=orientation)
    def _dot(self, other):
        # other is a Vector
        pA, qA = self
        pB, qB = other
        ans = 0
        ans -= pA * qB
        ans -= qA * pB
        ans /= 2
        ans += pA * pB
        ans += qA * qB
        return ans        
    def _scale(self, factor):
        # factor cannot be implicitely converted into two values
        # this is needed to prevent an infinite loop
        return type(self)((x * factor) for x in self)
    def rotate(self, steps):
        if not self:
            return self
        steps = self._num(steps) % 6
        ans = self
        if steps < 3:
            p, q = self
        else:
            p, q = -self
            steps -= 3
        if steps == 0:
            return type(self)(p, q)
        if steps == 1:
            return type(self)(q, q - p)
        if steps == 2:
            return type(self)(q - p, -p)
    def flip_horizontally(self):
        return -self.flip_vertically()
    def flip_vertically(self):
        return self[::-1]
    def x(self):
        return sum(self) / 2
    def y(self):
        return _y * (self[0] - self[1])
    def distance(self):
        if self[0] == self[1]:
            return abs(self[0])
        if self[0] == 0:
            return abs(self[1])
        if self[1] == 0:
            return abs(self[0])
        return abs(self)
    def orientation(self):
        if not self:
            return float('nan')
        vector = self
        ans = 0
        while not (vector[0] >= vector[1] > 0):
            vector = vector.rotate(-1)
            ans += 1
        if vector[0] != vector[1]:
            ans += _math.atan(vector.y() / vector.x()) * 3 / _math.pi
        return ans
    def __new__(cls, p=_Empty, q=_Empty, /):
        if q is not _Empty:
            pass
        elif p is _Empty:
            p = q = 0
        elif p == 0:
            p = q = 0
        else:
            p, q = p
        p = cls._num(p)
        q = cls._num(q)
        return tuple.__new__(cls, (p, q))
    def __repr__(self):
        return f"{__name__}.Vector.{tuple(self)}"
    def __getitem__(self, key):
        ans = tuple(self)[key]
        if type(ans) is tuple:
            return type(self)(ans)
        return ans
    def __add__(self, other):
        pA, qA = self
        pB, qB = type(self)(other)
        return type(self)(pA + pB, qA + qB)
    def __radd__(self, other):
        return self.__add__(other)
    def __sub__(self, other):
        return self + (-other)
    def __rsub__(self, other):
        return other + (-self)
    def __mul__(self, other):
        try:
            p, q = other # here zero is not interpreted as a vector 
            other = type(self)(p, q)
        except:
            return self._scale(other)
        else:
            return self._dot(other) # other is now a vector
    def __rmul__(self, other):
        return self.__mul__(other)
    def __truediv__(self, other):
        p, q = self
        return type(self)(p / other, q / other)
    def __pow__(self, other):
        other = self._num(other)
        if other < 0:
            raise ValueError
        ans = 1
        for n in range(other):
            ans *= self
        return ans
    def __neg__(self):
        return type(self)((-x) for x in self)
    def __abs__(self):
        return self.__mul__(self) ** .5
    def __hash__(self):
        return tuple(self).__hash__()
    def __eq__(self, other):
        other = type(self)(other)
        return tuple(self) == tuple(other)
    def __ne__(self, other):
        return not self.__eq__(other)
    def __bool__(self):
        return tuple(self) != (0, 0)
    def __int__(self):
        return int(self.__float__())
    def __float__(self):
        if self.__bool__():
            return float('nan')
        else:
            return 0.0
    def __str__(self):
        return self.__repr__()

