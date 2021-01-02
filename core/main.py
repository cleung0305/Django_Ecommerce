class MathClass():
    def __init__(self, *num):
        self.num = num
    def __repr__(self):
        return 'MathClass(*{!r})'.format(self.num)
    def __add__(self, other):
        return MathClass(*(x + y for x , y in zip(self.num, other.num)))
    def __len__(self):
        return len(self.num)


# x1 = MathClass(3, 8, 2)
# x2 = MathClass(4, 10, 1)
# x3 = MathClass(5, 12, 5)

# print(x1.__repr__())
# print(x1 + x2 + x3)
# print(x1.__module__)

# a = 1
# b = 10
# print(a.__lt__(b))
# print(len(x1))

class BaseMeta(type):
    def __new__(cls, name, bases, body):
        print("BaseMeta.__new__", cls, name, bases, body)
        if not 'bar' in body:
            raise TypeError("Bad user!")
        return super().__new__(cls, name, bases, body)

class Base(metaclass=BaseMeta):
    def foo(self):
        return self.bar()
    def bar(self):
        return 'bar'

class Derived(Base):
    def foo(self):
        return 'foo'
    def bar(self):
        return 'bar'

class MyClass(metaclass=BaseMeta):
    def too(self):
        return 'too'
    def bar(self):
        return 'bar'


from time import time
def timer(func):
    def wrapper(*args, **kwargs):
        before = time()
        result = func(*args, **kwargs)
        after = time()
        print('time: ', after - before)
        return result
    return wrapper

n = 2
def nTimes(func):
    def wrapper(*args, **kwargs):
        for _ in range(n):
            rv = func(*args, **kwargs)
        return rv
    return wrapper

@nTimes
@timer
def add(x, y, a, s, v):
    print('hi')
    return x + y + s+v+a

print(add(3,6,2,1,4))
