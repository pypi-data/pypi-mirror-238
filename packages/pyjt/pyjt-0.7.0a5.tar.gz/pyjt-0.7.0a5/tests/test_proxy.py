from pyjt import Fixture, Proxy


def test_proxy(helloworld, javax):
    tf1 = helloworld.find(javax.swing.JTextField)
    assert isinstance(tf1, Fixture)
    assert isinstance(tf1.control, Proxy)


def test_isinstance(helloworld, javax):
    tf1 = helloworld.find(javax.swing.JTextField)
    assert tf1.isinstance(javax.swing.JTextField)


def test_object(helloworld, javax):
    tf1 = helloworld.find(javax.swing.JTextField)
    assert isinstance(tf1.object, javax.swing.JTextField)
