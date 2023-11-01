import logging
from lxml import etree

from pyjt import ElementNotFoundError

from tools import assert_raises


def dump(helloworld):
    for line in helloworld.dump().splitlines():
        logging.error(line)


def test_miss(helloworld, java, javax):
    xpath = "//JLabel[contains(@text, 'XName')]"
    assert_raises(ElementNotFoundError, lambda: helloworld.find_by_xpath(xpath))


def test_empty_textfield(helloworld, java, javax):
    helloworld.find_by_xpath("//JTextField[@name='tf1']").fill("")
    dump(helloworld)
    assert helloworld.find_by_xpath("//JTextField[@text='']")


def test_empty_namefield(helloworld, java, javax):
    assert helloworld.find_by_xpath("//JTextField[@name='']")


def test_simple_xpath(helloworld, java, javax):
    xpath = "//JLabel[contains(@text, 'Name')]"
    label = helloworld.find_by_xpath(xpath)
    assert label.getText() == "Name:"
    xpath = "//JLabel[contains(@text, 'Name')]"
    label = helloworld.find_by_xpath(xpath)
    assert label.getText() == "Name:"


def test_advanced_xpath(helloworld, java, javax):
    xpath = "//Container[//JLabel[contains(@text, 'Name')]]/JTextField"
    logging.warning(etree.tostring(helloworld.etree()))
    tf = helloworld.find_by_xpath(xpath)
    tf.fill("xpath")
    xpath = "//Container[//JLabel[contains(@text, 'Name')]]/JTextField[@text='xpath']"
    tf = helloworld.find_by_xpath(xpath)
    assert tf is not None
