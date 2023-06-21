
import os
import random
class TerminalSymbol:
    """Class for my terminal symbols"""
    def __init__(self, tsymbol):
        self.tsymbol = tsymbol

    def __eq__(self, other):
        if isinstance(other, TerminalSymbol):
            return self.tsymbol == other.tsymbol
        return False


class VariableSymbol: #etc "LetStatement, PrintStatemnt, are the variables, this is the first thing after
    """Class for my variable symbols"""
    def __init__(self,vsymbol):
        self.vsymbol = vsymbol

class Option: #{LetStatement 1 LET [Variable] [Value]}
    """Class for my options"""
    def __init__(self,weight,symbols):
        self.weight = weight
        self.symbols = symbols

class Rule:
    """Class for my rules"""
    def __init__(self,variable): #give a variable like LetStatement, thne u can add the rest with whatever the rule is
        self.variable = variable
        self.full_options = []

    def append_option(self,option):
        """This will append any options to my full_options list"""
        self.full_options.append(option)
class Grammar:
    """Grammar class for the grammar of the whole file"""
    def __init__(self):
        self.rules = {}

    def append_rules(self, rule):
        """Appends the rules for all the grammar"""
        self.rules[rule.variable] = rule


class file_organizer:
    """File organizer class to do all the yield and return things for my code"""
    def __init__(self,start_var,file_path,num_lines):
        """Initalize all my values that I use while calling my inital grammar class"""
        self.grammar = Grammar()
        self.start_var = start_var
        self.file_path = file_path
        self.rules = []
        self.num_lines = num_lines
        self.final_list_dict = {}
        self.terminal = []
        self.finally_bruh = []
        self.unique_terminals = []
        self.count = 0

    def parse_stuff(self):
        """Function to Parse all my files"""
        directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(directory, self.file_path)
        if os.path.exists(file_path):
            with open(file_path, 'r') as content:
                rule_lines = []
                for each_line in content:
                    each_line = each_line.strip()
                    if each_line == "{":
                        rule_lines = []
                    elif each_line == "}":
                        rule = "\n".join(rule_lines)
                        self.rules.append(rule)
                        rule_lines = []
                    else:
                        rule_lines.append(each_line)
    def get_full_options(self, variable_symbol):
        """Gets all my options from my grammar rules with the variable name"""
        rule = self.grammar.rules.get(variable_symbol.vsymbol)
        if rule:
            return rule.full_options
    def process_each_one(self):
        """Goes through each of the rules"""
        for each_rule in self.rules:
            self.take_parsed_data(each_rule)

    def take_parsed_data(self,each_rule): #self.rules give a full list by each index of everything
        """Takes my data and appends everything to my grammar classes"""
        new_line_split = each_rule.split("\n")
        if len(each_rule) == 0: #the rule is empty for some reason
            return
        else:
            variable = new_line_split[0]
            rule = Rule(variable)
            for each_split in new_line_split[1:]: #grin_sample.txt 4 whv
                split_space = each_split.split(" ")
                weight = split_space[0]
                symbols = split_space[1:]
                option_sym_obj = Option(weight,symbols)
                rule.append_option(option_sym_obj)
                for i in symbols:
                    if i.startswith('[') and i.endswith(']'):
                        variable = i[1:-1]
                        var_sym_object = VariableSymbol(variable)
                        rule.append_option(var_sym_object)
                    else:
                        terminal = i
                        tar_sym_object = TerminalSymbol(terminal)
                        rule.append_option(tar_sym_object)
        self.grammar.append_rules(rule)

    def take_start_var(self):
        """Takes the start variable and uses that for the whole line"""
        for var,rule_obj in self.grammar.rules.items():
            if var == self.start_var:
                yield rule_obj # Want to yield the rule, now we have rule object

    def take_given_rule(self,rule_obj): #first we need to pick out of the rules
        """Main block of code that uses the yield to return the new terminal variable that that rule replaces it with"""
        for new_gen in rule_obj:
            rule_obj = new_gen #grin_sample.txt 4 GrinStatement
        total_weight = 0
        options = rule_obj.full_options #variable and the weight, #gives all the options
        weight_list_and_v_t_list = []
        weight_list = []
        slice_val = []
        total_index = []
        last_index = None
        last_index_bool = False
        final_list = []

        for each_option in options:
            if isinstance(each_option, (VariableSymbol, TerminalSymbol)):
                weight_list_and_v_t_list.append(each_option) #lets say tsym
            elif isinstance(each_option, Option):
                weight_list_and_v_t_list.append(each_option.weight)
                weight_list.append(each_option.weight)
        for i in weight_list:
            total_weight += int(i)
        random_value = random.randint(1, total_weight)
        cumulative_weight = 0
        for index, option in enumerate(weight_list_and_v_t_list):
            if isinstance(option,str):
                total_index.append(index)

        for index, option in enumerate(weight_list_and_v_t_list):
            if isinstance(option, str):  # assuming it's a weight value
                cumulative_weight += int(option)
                slice_val.append(index)
                if random_value <= cumulative_weight:
                    break
        start_val = slice_val[-1]
        for index,i in enumerate(total_index):
            if i == start_val:
                try:
                    last_index = total_index[index+1]
                except IndexError:
                    last_index_bool = True


        if last_index_bool:
            final_list.extend(weight_list_and_v_t_list[start_val:])
        else:
            final_list.extend(weight_list_and_v_t_list[start_val:last_index])
        for index,values in enumerate(final_list):
            self.final_list_dict[index] = values #this is the self we are going to change whenever we change the index
#we have a full list of from the start_variable, which sentence structure to go off of

        for index, value_check in enumerate(final_list): #this is the index of the final list or what we are going to come back to
            if isinstance(value_check, VariableSymbol):#checks if any are a variable symbol,
                u_t = self.turn_var_into_term(value_check, index)
                self.final_list_dict[index] = u_t
                self.finally_bruh = self.get_terminal_objects(self.final_list_dict)
                self.terminal = []
                self.unique_terminals = []
            if isinstance(value_check,TerminalSymbol):
                self.finally_bruh = self.get_terminal_objects(self.final_list_dict) #fix this here, test for tmrw
                self.count += 1

        symbols_to_print = []
        for symbol in self.finally_bruh:
            symbols_to_print.append(symbol)

        print(" ".join(symbols_to_print),end="")

    def turn_var_into_term(self, var_symbol,index):
        """Code that turns a variable symbol into a terminal symbol randomly and recursively """
        full_options = self.get_full_options(var_symbol)
        if not full_options:
            return
        total_weight = 0
        weight_list = []
        terminal_options = []
        variable_options = []

        for option in full_options:
            if isinstance(option, TerminalSymbol):
                terminal_options.append(option)
            elif isinstance(option, VariableSymbol):
                variable_options.append(option)
            elif isinstance(option, Option):
                weight_list.append(option.weight)

        for weight in weight_list:
            total_weight += int(weight)

        random_value = random.randint(1, total_weight)
        cumulative_weight = 0
        selected_option = None

        for option in full_options:
            if isinstance(option, Option):
                cumulative_weight += int(option.weight)
                if random_value <= cumulative_weight:
                    selected_option = option
                    break
        values = [] #This values list will give us the terminal and variables from the GIVEN variable at the start
        selected_option_index = full_options.index(selected_option)
        for i in range(selected_option_index, len(full_options)):
            if i != selected_option_index and isinstance(full_options[i], Option):
                break
            values.append(full_options[i])

        for symbol_t_or_v in values:
            if isinstance(symbol_t_or_v, VariableSymbol):
                self.turn_var_into_term(symbol_t_or_v,index) #THIS IS WHERE RECURSION HAPPENS, I give that same varible now with the SAME index to the function until it is all terminals
            elif isinstance(symbol_t_or_v, TerminalSymbol):
                self.terminal.append(symbol_t_or_v)
                self.count += 1

        for terminal in self.terminal:
            if terminal not in self.unique_terminals:
                self.unique_terminals.append(terminal)
                break
        return self.unique_terminals

    def printing_my_stuff(self):
        """Yields from the start var to get the random sentence it starts with"""
        yield from self.take_start_var()

    def get_terminal_objects(self, data):
        """Gets my full terminal objects and returns the values"""
        terminal_objects = []
        if isinstance(data, dict):
            for value in data.values():
                if isinstance(value, list):
                    for item in value:
                        terminal_objects.extend(self.get_terminal_objects(item))
                elif isinstance(value, TerminalSymbol):
                    terminal_objects.append(value.tsymbol)
        elif isinstance(data, TerminalSymbol):
            terminal_objects.append(data.tsymbol)

        return terminal_objects





