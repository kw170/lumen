from textx import metamodel_from_file
# import psutil

# Load the model from the grammar and input program
lumen_mm = metamodel_from_file('lumen.tx')
lumen_model = lumen_mm.model_from_file('program.lmn')

class Lumen:
    def __init__(self):
        self.varmap = {}


    def __str__(self):
        return f"Robot position is {self.x}, {self.y}."

    def interpret(self, model):
        # model is an instance of Program
        for c in model.statements:
            # Handle different types of statements
            if c.__class__.__name__ == "PrintStatement":
                self.handle_print(c)
            elif c.__class__.__name__ == "Initialization":
                self.handle_initialization(c)
            elif c.__class__.__name__ == "Assignment":
                self.handle_assignment(c)
            elif c.__class__.__name__ == "IfStatement":
                self.handle_if(c)
            elif c.__class__.__name__ == "WhileLoop":
                self.handle_while(c)
            elif c.__class__.__name__ == "ForLoop":
                self.handle_for(c)
            elif c.__class__.__name__ == "ArrayDeclaration":
                self.handle_array_declaration(c)
            elif c.__class__.__name__ == "ArrayAccess":
                self.handle_array_access(c)

    def handle_print(self, command):
        # Print command, supporting variables, arrays, and expressions
        expr = command.expression

        if isinstance(expr, str):
            expr = self.evaluate_expression(expr)
            print(expr)  # Direct string
        elif isinstance(expr, int):
            print(expr)  # Direct integer
        elif isinstance(expr, str) and expr.startswith("["):  # Assuming array
            arr = self.varmap.get(expr, [])
            print(arr)
        else:  # Handle variables
            print(self.varmap.get(expr, "Undefined"))

    def handle_initialization(self, command):
        var_name = command.varName
        value = command.value

        if var_name in self.varmap: # Raise Error if already initialized
            raise Exception("Variable is already defined")

        self.varmap[var_name] = value
        if isinstance(value, int):
        	self.varmap[var_name] = value
        elif isinstance(value, str):
            if value.startswith("["):
                self.varmap[var_name] = list(map(int, value[1:-1].split(",")))
            else:
                self.varmap[var_name] = eval(value)

    def handle_assignment(self, command):
        # Handle variable assignment
        var_name = command.varName
        value = command.value
        if isinstance(value, int):  # Direct integer assignment
            self.varmap[var_name] = value
        elif isinstance(value, str):  # Handle variable or expression assignment
            self.varmap[var_name] = self.evaluate_expression(value)

    def handle_array_declaration(self, command):
        array_name = command.varName
        elements = command.elements
        if array_name in self.varmap:
            raise Exception("Variable already defined")
        self.varmap[array_name] = [self.evaluate_expression(x) for x in elements]

    # def handle_array_assignment(self, command):

    # def handle_array_access(self, command):


    def handle_if(self, command):
        condition = command.condition
        if self.evaluate_condition(condition):
            self.interpret(command)

    def handle_while(self, command):
        condition = command.condition
        while self.evaluate_condition(condition):
            self.interpret(command)


    def handle_for(self, command):
        loopVar = command.loopVar
        range_start = command.rangeStart
        range_end = command.rangeEnd

        for i in range(range_start, range_end):
            self.varmap[loopVar] = i
            self.interpret(command)

    def evaluate_expression(self, expr):
        # Evaluate simple expressions, including arithmetic operations
        if isinstance(expr, int):
            return expr
        elif isinstance(expr, str):
            # Handle arithmetic expressions
            if any(op in expr for op in "+-*/%"):
                try:
                    # Safely evaluate the arithmetic expression
                    return eval(expr, {"__builtins__": None}, self.varmap)
                except Exception as e:
                    raise Exception(f"Error evaluating expression '{expr}': {e}")
            elif expr.startswith("["):
                # Handle array expressions
                return self.varmap.get(expr, [])
            else:
                # Handle variable lookups
                return self.varmap.get(expr, None)                 #come back to this
        return 0

    def evaluate_condition(self, condition):
        # Evaluate conditions in If, While, and For statements
        left = self.evaluate_expression(condition.left)
        right = self.evaluate_expression(condition.right)
        if condition.comp == "==":
            return left == right
        elif condition.comp == "!=":
            return left != right
        elif condition.comp == "<":
            return left < right
        elif condition.comp == "<=":
            return left <= right
        elif condition.comp == ">":
            return left > right
        elif condition.comp == ">=":
            return left >= right
        return False




# Interpret the program
lumen = Lumen()
lumen.interpret(lumen_model)

# ArrayAccess:
#   varName=ID '[' index=Expression ']'
# ;

# FunctionCall:
#   'CPU.' methodName=ID '(' ')'
# ;