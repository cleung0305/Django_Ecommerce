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

# class BaseMeta(type):
#     def __new__(cls, name, bases, body):
#         print("BaseMeta.__new__", cls, name, bases, body)
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