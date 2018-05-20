
import unittest

from ..code.Singleton import Singleton, SingletonArgs



class test_singletons(unittest.TestCase):


    def test_simple_singleton_like(self):
        class A(object, metaclass=SingletonArgs):
            FOO = 'bar'
        assert A() is A()


    def test_simple_singleton(self):
        class A(object, metaclass=Singleton):
            FOO = 'bar'
        assert A() is A()


    def test_simple_singleton_args(self):
        class B(object, metaclass=SingletonArgs):
            def __init__(self, key):
                self.key = key
        assert B('key1') is B('key1')
        assert B('key1') is not B('key2')


    def test_complex_singleton_args(self):
        class C(object, metaclass=SingletonArgs):
            def __init__(self, key=None):
                self.key = key
        assert C() is C()
        assert C() is C(None)
        assert C(None) is C(key=None)
        assert C() is C(key=None)
        assert C() is not C('key')
        assert C('key') is C('key')
        assert C('key') is C(key='key')
        assert C('key1') is not C(key='key2')
        assert C(key='key1') is not C(key='key2')


    def test_different_singleton(self):
        class D(object, metaclass=SingletonArgs):
            def __init__(self):
                pass

        class E(object, metaclass=SingletonArgs):
            def __init__(self):
                pass
        assert D() is not E()
