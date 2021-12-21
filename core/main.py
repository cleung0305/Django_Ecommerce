# class MathClass():
#     def __init__(self, *num):
#         self.num = num
#     def __repr__(self):
#         return 'MathClass(*{!r})'.format(self.num)
#     def __add__(self, other):
#         return MathClass(*(x + y for x , y in zip(self.num, other.num)))
#     def __len__(self):
#         return len(self.num)


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


#---------------------------=------------------------------------

# class BaseMeta(type):
#     def __new__(cls, name, bases, body):
#         print(f"BaseMeta.__new__      :       {cls}         {name}       {bases}       {body}")
#         if not 'bar' in body:
#             raise TypeError("Bad user!")
#         return super().__new__(cls, name, bases, body)

# class Base(metaclass=BaseMeta):
#     def foo(self):
#         return self.bar()
#     def bar(self):
#         return 'bar'

# class Derived(Base):
#     def foo(self):
#         return 'foo'
#     def bar(self):
#         return 'bar'

# class MyClass(metaclass=BaseMeta):
#     def too(self):
#         return 'too'
#     def bar(self):
#         return 'bar'


#--------------------------------------------------------------

# from time import time
# def timer(func):
#     def wrapper(*args, **kwargs):
#         before = time()
#         result = func(*args, **kwargs)
#         after = time()
#         print('time: ', after - before)
#         return result
#     return wrapper

# n = 5
# def nTimes(func):
#     def wrapper(*args, **kwargs):
#         for _ in range(n):
#             rv = func(*args, **kwargs)
#         return rv
#     return wrapper

# @nTimes
# @timer
# def add(x, y, a, s, v):
#     print('hi')
#     return x+y+a+s+v

# print(add(3,6,2,1,4))

# from time import sleep
# def compute():
#     for i in range(10):
#         sleep(0.5)
#         yield i
        
# for i in compute():
#     print(i)


#--------------------------------------------------------------

# import time
# import requests
# from bs4 import BeautifulSoup

# url = ('https://www.coinbase.com/price/ethereum')
# r = requests.get(url)

# time.sleep(10)
# web_content = BeautifulSoup(r.text, 'html5lib')
# price = web_content.find('span', {"class" : 'AssetChartAmount__Number-sc-1b4douf-1 fQDZTy'})

# print(web_content)


#--------------------------------------------------------------

#-----getting price from coinbase-----
# import time
# from bs4 import BeautifulSoup
# from selenium  import webdriver

# try:
#     driver = webdriver.Chrome()
#     driver.get('https://www.coinbase.com/price/bitcoin')

#     for _ in range(30):
#         driver.refresh()
#         time.sleep(3)
#         soup = BeautifulSoup(driver.page_source,"html5lib")
#         item = soup.find('span', {'class' : 'AssetChartAmount__Number-sc-1b4douf-1 fQDZTy'}).text
#         print(item)
#         time.sleep(7)
#     driver.quit()
# except AttributeError:
#     print("Use find() you dumb! Please try again!")
#     driver.quit()

# import pandas as pd
# import plotly.express as px

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_apple_stock.csv')
# print(df.head())
# fig = px.line(df, x = 'AAPL_x', y = 'AAPL_y', title='Apple Share Price Over Time (2014)')
# fig.show()


#--------------------------------------------------------------

# import psycopg2

# with psycopg2.connect(
#     host='database-20220727.cukgv6q3mgp8.us-east-1.rds.amazonaws.com',
#     user="postgres",
#     password="loklok123",
#     port="5432"
# ) as conn:
#     print("connected")
#     with conn.cursor() as cur:
#         cur.execute("select version()")
#         data = cur.fetchone()
#         print(data)

#--------------------------------------------------------------

# from abc import abstractmethod, ABC
# from overloading import overload
# from functools import singledispatchmethod
# from datetime import date, datetime, time

# class A(ABC):
#     @abstractmethod
#     def absA(self):
#         print("This is abstract method.")


# class B(A):
#     @singledispatchmethod
#     def absA(self, x: int):
#         print(f'{x = } is an int.')

#     @absA.register
#     def absAOverloaded(self, x: str):
#         print(f'{x = } is a string.')
        
#     @absA.register
#     def absAOverloaded(self, x: date):
#         print(f"{x.day}-{x.month}-{x.year}")

# class C(A):
#     @singledispatchmethod
#     def absA(self, x: int):
#         print(f"{x = } is an integer")

#     @absA.register
#     def absAOverloaded(self, x: str):
#         print(f'{x = } is a string.')

# c = C()
# c.absA('hello')
# c.absA(123)

#--------------------------------------------------------------

# class Sample():
#     def __init__(self):
#         self.a = 1
#         self._b = 2
#         self.__c = 3
#     def display(self):
#         print(f"{self.a = } , {self._b = } , {self.__c = }")

# class Sample2(Sample):
#     def __init__(self):
#         super().__init__()

# s = Sample()
# s.display()
# print(dir(s))

# s2 = Sample2()
# s2.display()
# print(dir(s2))

#--------------------------------------------------------------


# def foo(a, *args):
#   for _ in args:
#     print(f"{_}")

# l, *rest, b= [1,2,3,4]
# foo('yo', "lok", 26,"hi", *rest)

# for x, y, z in [(1, 2, 3), (3, 4, 5)]:
#     print(f'x={x}, y={y}')


#---------------------------=------------------------------------


# import math

# def solution(A):
#     # write your code in Python 3.6
#     result = min(flip1(A), noflip1(A))
#     return result
    


# def flip1(A):
#     result = 0
#     if A[0] == 1: A[0] = 0
#     elif A[0] == 0: A[0] = 1
#     result += 1
#     prev = A[0]
#     for num in A[1:]:
#         if num == prev:
#             if num == 1: num = 0
#             elif num == 0: num = 1
#             result += 1
#         prev = num
#     return result

# def noflip1(A):
#     result = 0
#     prev = A[0]
#     for num in A[1:]:
#         if num == prev:
#             if num == 1: num = 0
#             elif num == 0: num = 1
#             result += 1
#         prev = num
#     return result
# A = [1,0,1,0,1,1]
# B = A
# print(flip1(A.copy()))
# print(noflip1(A.copy()))


#---------------------------=------------------------------------

#Component !!

# from abc import ABC, abstractmethod
# from dataclasses import dataclass
# from typing import Optional

# @dataclass
# class Contract(ABC):
#     @abstractmethod
#     def get_payment(self) -> float:
#         #compute the payment to employee under this contract.
#         pass


# @dataclass
# class HourlyContract(Contract):
#     pay_rate: float
#     hour: int = 0
#     employer_cost: float = 1000

#     def get_payment(self) -> float:
#         return self.hour * self.pay_rate + self.employer_cost

# @dataclass
# class FreelanceContract(Contract):
#     pay_rate: float
#     hour: int = 0


# @dataclass
# class Commission(ABC):

#     @abstractmethod
#     def get_payment(self) -> float:
#         #Commissions to be paid out
#         pass


# @dataclass
# class ContractCommission(Commission):
#     commission: float = 100
#     contract_landed: int = 0

#     def get_payment(self) -> float:
#         return self.commission * self.contract_landed

# @dataclass
# class Employee():
#     name: str
#     id: int
#     contract: Contract
#     commission: Optional[Contract] = None

#     def compute_pay(self) -> float:
#         pay = self.contract.get_payment()
#         if self.commission is not None:
#             pay += self.commission.get_payment()
#         return pay

# lok_contract = HourlyContract(pay_rate=80, hour=50, employer_cost=10)
# lok_commission = ContractCommission(contract_landed=8)
# lok = Employee(name='lok', id=1, contract=lok_contract, commission=lok_commission)

# print(lok.contract.get_payment())
# print(lok.commission.get_payment())
# print(f"{lok.name} is paid for {lok.compute_pay()}")

#---------------------------=------------------------------------