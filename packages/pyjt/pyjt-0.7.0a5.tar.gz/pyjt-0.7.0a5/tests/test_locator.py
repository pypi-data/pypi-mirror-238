from pyjt import Locator, ElementNotFoundError

from tools import assert_raises

import logging


def test_locator_has_fail(helloworld, java, javax):
    loc = Locator(role=java.awt.Container).contains(role=javax.swing.JLabel, text="Namex:")
    assert_raises(ElementNotFoundError, lambda: helloworld.locate(loc))


def test_locator_has(helloworld, java, javax):
    loc = Locator(role=java.awt.Container).has(role=javax.swing.JLabel, text="Name:")
    tf3 = helloworld.locate(loc)
    logging.warning(tf3)
    assert tf3 is not None
    assert tf3.find(javax.swing.JTextField).getText() == "textfield3"

    loc = Locator(role=java.awt.Container).has(role=javax.swing.JLabel, text="Email:")
    tf4 = helloworld.locate(loc)
    logging.warning(tf3)
    assert tf4 is not None
    tf = tf4.find(javax.swing.JTextField)
    assert tf.getText() == "textfield4"
    tf.fill("john@smith.com")
    assert tf.getText() == "john@smith.com"

    loc = Locator(role=java.awt.Container).has(role=javax.swing.JLabel, text="Email:").has(text="john@smith.com")
    match = helloworld.locate(loc)
    assert match is not None
