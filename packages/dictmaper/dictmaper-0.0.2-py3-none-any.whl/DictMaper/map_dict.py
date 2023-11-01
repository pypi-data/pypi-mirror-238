import ast
from utils import format_numbers, format_str, recursive_get

class MapDict:

    def __init__(self,
                 output: dict,
                 context: dict,
                 vars: dict,
                 default="-",
                 complex_dict_mapping=False
                 ) -> None:

        self.output = output
        self.context = context
        self.vars = vars
        self.default = default
        self.complex_dict_mapping = complex_dict_mapping

    def process(self) -> dict:
        if self.complex_dict_mapping:
            self.result = self.complex_process()
        else:
            self.result =  self.simple_process()
        return self.result

    def simple_process(self):
        self.map_init_vars()
        self.process_data()
        return self.result
    
    def complex_process(self):
        self.map_init_vars_complex()
        self.result = self.replace_vars(self.output, self.vars)
        return self.result

    def map_init_vars(self) -> dict:
        for key, value in self.vars.items():
            data = recursive_get(self.context, value, default=self.default)
            if isinstance(data, (int, float)):
                data = '{:,.0f}'.format(data).replace(',', '.')
            self.vars[key] = data
        return self.vars

    def process_data(self):
        data_to_map_str = str(self.output)
        for key, val in self.vars.items():
            data_to_map_str = data_to_map_str.replace(
                "{" + key + "}", str(val))
        self.result = ast.literal_eval(data_to_map_str)

    def map_init_vars_complex(self) -> dict:
        for key, value in self.vars.items():
            if isinstance(value, list):
                for item in value:
                    new_value_key = [{} for _ in range(len(self.context[key]))]
                    for index, dict_context in enumerate(self.context[key]):
                        for var_name, var_path in item.items():
                            data = recursive_get(dict_context, var_path, default=self.default)
                            data = format_numbers(data)
                            new_value_key[index][var_name] = data

                    self.vars[key] = new_value_key
            else:
                data = recursive_get(self.context, value, default=self.default)
                data = format_numbers(data)
                self.vars[key] = data
        return self.vars
    
    def replace_vars(self, output, vars, key_list=''):
        if isinstance(output, dict):
            new_output = {}
            for key, value in output.items():
                new_key = key

                if isinstance(value, list):
                    new_value = self.replace_vars(value, vars, key)
                else:
                    new_value = self.replace_vars(value, vars)

                # I replace the key if it is enclosed in braces and matches a key in vars
                if isinstance(key, str) and key.startswith('{') and key.endswith('}'):
                    found_value = self.find_and_return_value(vars, key[1:-1])

                    if not found_value:
                        continue

                    new_key = found_value

                new_output[new_key] = new_value

            return new_output
        elif isinstance(output, list):
            if key_list in vars:
                for _ in range(len(vars[key_list])-1): 
                    output.append(output[0])
            return [self.replace_vars(item, vars) for item in output]
        else:
            # I replace the value if it is enclosed in braces and matches a key in vars
            if isinstance(output, str) and output.startswith('{') and output.endswith('}'):
                found_value = self.find_and_return_value(vars, output[1:-1])

                if not found_value:
                    return output

                return found_value
            else:
                return output
    
    def find_and_return_value(self, dict_values, key):
        new_value = None
        if key in dict_values:
            new_value = dict_values[key]
            del dict_values[key]

            return format_str(new_value)

        for value in dict_values.values():
            if isinstance(value, list):
                for element in value:
                    if isinstance(element, dict):
                        resultado = self.find_and_return_value(element, key)
                        if resultado:
                            return resultado
            elif isinstance(value, dict):
                resultado = self.find_and_return_value(value, key)
                if resultado:
                    return resultado

        return False
    