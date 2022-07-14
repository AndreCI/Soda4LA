from Ctrls.parameter_encoding_controller import ParameterEncodingCtrl
from Models.data_model import Data
from Utils.constants import ENCODING_OPTIONS
from Utils.filter_module import FilterModule


class ParameterEncoding():

    """
    Model class for parameters encoding. It enables raw data to be processed into notes. Each track has its own parameter
    encoding objects.
    This can be viewed via a track config view and its subsequent views presented by its buttons.
    """
    def __init__(self, encoded_var : str):
        #Data
        self.encoded_var=encoded_var #a variable of a note
        if(self.encoded_var not in ENCODING_OPTIONS):
            raise NotImplementedError("{} not in encoding options".format(self.encoded_var))
        self.filter = FilterModule() #Filter module applied to mainVar
        self.handpicked = True #if true, uses handpickedEncoding to compute a parameter for a note, if not it uses functionEncoding
        self.handpickEncoding = {} #Dictionnary containing information to transform a row into a paramter for a note

        self.functionEncoding = {} #Dictionnary containing information to transform a row into a paramter for a note


        #Others Models
        self.datas = Data()

        #Ctrl
        self.ctrl = ParameterEncodingCtrl(self)

        #Views
        self.peView = None

    def set_main_var(self, variable : str):
        self.filter.assign_variable(variable)


    def assign_function_encoding(self, function : str, min_val : int, max_val : int):
        """
        Assign a function with parameter as encoding, according to user preference
        :param function: type of encoding to use, such as linear or log
        :param min_val: lower bound of selected function
        :param max_val: upper bound of selected function
        """
        self.functionEncoding["function"] = function
        self.functionEncoding["min"] = min_val
        self.functionEncoding["max"] = max_val


    def assign_handpicked_encoding(self, variables : [], values : []):
        """
        Assign values to variable, accordingly to user preference.
        :param variables: a list of all possible instances of a variable
        :param values: a list of value linked to the variable
        """
        if(len(variables) != len(values)):
            raise ValueError()
        for var, val in zip(variables, values):
            self.handpickEncoding[var] = val

    def get_variables_instances(self):
        #TODO should be somewhere else?
        return self.datas.get_variables_instances(self.filter.variable)