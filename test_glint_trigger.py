# test_glint_trigger.py - A test file to demonstrate Spiral Linter glints

def greet(name):
    print(f"Hello, {name}")    
    # Trailing whitespace on purpose:     
    
class Test:
    def __init__(self):
        self.x=1  # Missing spaces around operator
        
    def method(self):
        pass
        
# Missing two blank lines before this function
def another_function():
    unused_var = 42  # Unused variable
    return True
