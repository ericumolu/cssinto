#!/usr/local/bin/python3.1

from cssinto import Css

css = Css()
css.read('css_file.css')
css.add_block()

print (css.show_block())
print (css.get_block(3).show_selector())
print (css.get_block(3).show_body())

