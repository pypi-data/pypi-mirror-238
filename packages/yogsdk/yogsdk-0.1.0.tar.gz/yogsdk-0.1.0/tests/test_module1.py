# test_module1.py

from yogsdk.module1 import MyClass

def test_my_method():
    obj = MyClass("World")
    assert obj.my_method() == "Hello, World!"