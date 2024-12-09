from textx import metamodel_from_file
import psutil
import gpustat
import time
import platform

# Load the model from the grammar and input program
lumen_mm = metamodel_from_file('lumen.tx')
lumen_model = lumen_mm.model_from_file('program.lmn')

class Lumen:
    def __init__(self):
        self.varmap = {}

    def interpret(self, model):
        for c in model.statements:
            # Handle different types of statements
            if c.__class__.__name__ == "PrintStatement":
                self.handle_print(c)
            elif c.__class__.__name__ == "Initialization":
                self.handle_initialization(c)
            elif c.__class__.__name__ == "VariableAssignment":
                self.handle_variable_assignment(c)
            elif c.__class__.__name__ == "IfStatement":
                self.handle_if(c)
            elif c.__class__.__name__ == "WhileLoop":
                self.handle_while(c)
            elif c.__class__.__name__ == "ForLoop":
                self.handle_for(c)
            elif c.__class__.__name__ == "ArrayDeclaration":
                self.handle_array_declaration(c)
            elif c.__class__.__name__ == "ArrayAssignment":
                self.handle_array_assignment(c)
            elif c.__class__.__name__ == "ArrayAccess":
                self.handle_array_access(c)
            elif c.__class__.__name__ == "ArrayElementAssignment":
                self.handle_array_assignment(c)
            elif c == "NETWORK.live()":
                self.handle_network_usage()

    def handle_print(self, command):
        # Print command, supporting variables, arrays, and expressions
        expr = command.expression
        print(self.evaluate_expression(expr))

    def handle_initialization(self, command):
        var_name = command.varName
        value = self.evaluate_expression(command.value)
        if var_name in self.varmap: # Raise Error if already initialized
            raise Exception("Variable is already defined")
        elif isinstance(value, int):
            self.varmap[var_name] = value
        elif isinstance(value, str):
            if value.startswith("["):
                self.varmap[var_name] = list(map(int, value[1:-1].split(",")))
            else:
                self.varmap[var_name] = eval(value)

    def handle_variable_assignment(self, command):
        var_name = command.varName
        value = command.value

        if var_name not in self.varmap:
            raise Exception("Variable is not defined")

        if isinstance(value, int):
            self.varmap[var_name] = value
        elif isinstance(value, str):
            self.varmap[var_name] = self.evaluate_expression(value)
        elif value.__class__.__name__ == "LumenFunctionCall":
            self.varmap[var_name] = self.lumen_function_call(value)

    def handle_array_declaration(self, command):
        array_name = command.varName
        elements = command.elements
        if array_name in self.varmap:
            raise Exception("Variable already defined")
        self.varmap[array_name] = [self.evaluate_expression(x) for x in elements]

    def handle_array_assignment(self, command):
        array_name = command.varName
        elements = command.elements

        if array_name in self.varmap:
            self.varmap[array_name] = [self.evaluate_expression(x) for x in elements]
        else:
            raise Exception("Array is not defined")

    def handle_array_element_assignment(self, command):
        command.expression
        value = command.value
        array_name = value.varName
        index = self.evaluate_expression(value.index)
        array = self.varmap.get(array_name, [])

        if isinstance(array, list) and 0 <= index < len(array):
            self.varmap[var_name] = array[index]
        else:
            raise ValueError(f"Invalid array access: {array_name}[{index}]")

    def handle_array_access(self, command):
        array_name = command.varName
        index = self.evaluate_expression(command.index)

        if array_name not in self.varmap:
            raise Exception("Array is not defined")

        array_length = len(self.varmap[array_name])

        if index >= array_length or index <= -1:
            raise Exception("Index out of bounds error")

        return self.varmap[array_name][index]

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

    def lumen_function_call(self, command):
        system = command.system
        methodName = command.methodName

        if system == "CPU":
            cpu_info ={
                "name": platform.processor(),
                "count": psutil.cpu_count(logical=True),  # Logical cores
                "phys_cores": psutil.cpu_count(logical=False),  # Physical cores
                "freq": psutil.cpu_freq().current,  # Current frequency in MHz
                "usage": psutil.cpu_percent(interval=1),  # CPU usage percentage
                "usage_per_core": psutil.cpu_percent(interval=1, percpu=True),  # Usage per core
            }

            if methodName == "info":
                return cpu_info
            elif methodName not in cpu_info:
                raise Exception("CPU method does not exist")
            return cpu_info[methodName]

        elif system == "MEMORY":
            memory = psutil.virtual_memory()
            memory_info = {
                "total": round(memory.total / (1024 ** 3), 2),  # Total memory in gb
                "available": round(memory.available / (1024 ** 3), 2),
                "usage": memory.percent
            }

            if methodName == "info":
                return memory_info
            elif methodName not in memory_info:
                raise Exception("Memory method does not exist")
            return memory_info[methodName]

        elif system == "NETWORK":
            net_io = psutil.net_io_counters()

            network_info = {
                "sent": net_io.bytes_sent / (1024 ** 2),
                "recv": net_io.bytes_recv / (10024 ** 2)
            }

            if methodName == "info":
                return network_info
            elif methodName not in network_info:
                raise Exception("Network method does not exist")
            else:
                return network_info[methodName]

        elif system == "GPU":
            gpu_info = {
                "name": [],
                "usage": [],
                "total": [],
                "temp": []
            }
            gpu_stats = gpustat.new_query().gpus
            for gpu in gpu_stats:
                gpu_info['name'].append(gpu['name'])
                gpu_info['usage'].append(gpu['utilization.gpu'])
                gpu_info['total'].append(gpu['memory.total'] / 1024)
                gpu_info['temp'].append(gpu['temperature.gpu'])

            if methodName == "info":
                return gpu_info
            elif methodName not in gpu_info:
                raise Exception("GPU method does not exist")
            else:
                if not command.index:
                    return gpu_info[methodName]
                else:
                    return gpu_info[methodName][self.evaluate_expression(command.index)]

    def evaluate_expression(self, expr):
        evaluated_expr = self.evaluate_term(expr)
        try:
            # Safely evaluate the resulting expression
            return eval(evaluated_expr, {"__builtins__": None}, self.varmap)
        except Exception as e:
            raise ValueError(f"Error evaluating expression '{evaluated_expr}': {e}")

    def evaluate_condition(self, condition):
        # Evaluate conditions in If, While, and For statements
        left = self.evaluate_expression(condition.left)
        right = self.evaluate_expression(condition.right)

        if condition.logOp:
            if condition.logOp == "&&":
                return self.evaluate_condition(left) and self.evaluate_condition(right)
            elif condtion.logOp == "||":
                return self.evaluate_condition(left) or self.evaluate_condition(right)
        return self.evaluate_operation(condition)

    def evaluate_term(self, term):
        if isinstance(term, int):
            return term
        elif isinstance(term, str):
            if term in self.varmap:
                return str(self.varmap[term])
            else:
                raise ValueError(f"Undefined variable '{term}' encountered in term.")
        elif term.__class__.__name__ == "ArrayAccess":
            # Evaluate array access and return the value
            return self.handle_array_access(term)
        elif term.__class__.__name__ == "ArrayLength":
            var_name = term.varName
            return len(self.varmap[var_name])
        elif term.__class__.__name__ == "LumenFunctionCall":
            return self.lumen_function_call(term)
        elif hasattr(term, 'left') and hasattr(term, 'op') and hasattr(term, 'right'):
            # Build the expression string recursively
            left_value = self.evaluate_term(term.left)
            right_values = [self.evaluate_term(r) for r in term.right]
            operators = term.op

            # Combine left value, operators, and right values
            expression = str(left_value)
            for op, rv in zip(operators, right_values):
                expression += f" {op} {rv}"
            return expression
        else:
            return term

    def evaluate_operation(self, condition):
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

    def format_bytes(self, bytes_val):
        if bytes_val < 1024:
            return f"{bytes_val} B"
        elif bytes_val < 1024 ** 2:
            return f"{bytes_val / 1024:.2f} KB"
        elif bytes_val < 1024 ** 3:
            return f"{bytes_val / (1024 ** 2):.2f} MB"
        else:
            return f"{bytes_val / (1024 ** 3):.2f} GB"

    def handle_network_usage(self):
        interval = 2
        print("Tracking network usage. Press Ctrl+C to stop.\n")
        print(f"{'Time':<15} {'Upload Speed':<20} {'Download Speed':<20}")
        print("-" * 60)

        # Get initial stats
        prev_net_io = psutil.net_io_counters()
        prev_sent = prev_net_io.bytes_sent
        prev_recv = prev_net_io.bytes_recv

        try:
            while True:
                time.sleep(interval)

                # Get current stats
                net_io = psutil.net_io_counters()
                curr_sent = net_io.bytes_sent
                curr_recv = net_io.bytes_recv

                # Calculate speed
                upload_speed = (curr_sent - prev_sent) / interval
                download_speed = (curr_recv - prev_recv) / interval

                # Update previous stats
                prev_sent, prev_recv = curr_sent, curr_recv

                # Print results
                print(
                    f"{time.strftime('%H:%M:%S'):>15} "
                    f"{self.format_bytes(upload_speed):<20} "
                    f"{self.format_bytes(download_speed):<20}"
                )

        except KeyboardInterrupt:
            print("\nTracking stopped.")




# Interpret the program
lumen = Lumen()
lumen.interpret(lumen_model)


