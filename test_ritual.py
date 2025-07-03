def test_function():
    # Missing docstring
    print('hello')
    # Intentional trailing whitespace:    
    return 1+1  # No spaces around operator

class TestClass:
    def __init__(self):
        self.value = 42
    
    def get_value(self):
        # Inconsistent return
        if self.value > 0:
            return self.value
        # Missing explicit return

# Line too long - this line is intentionally made longer than 79 characters to trigger the E501 error in flake8
print('This is a very long line that exceeds the maximum line length of 79 characters and should trigger a linter warning')

# Unused import (simulated since we can't actually import in this test)
# import os
# import sys
