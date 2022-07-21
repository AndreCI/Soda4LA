from Ctrls.parameter_encoding_controller import ParameterEncodingCtrl
from Models.data_model import Data
from Utils.constants import ENCODING_OPTIONS
from Utils.filter_module import FilterModule


class ParameterEncoding:

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
        self.filter = FilterModule() #Filter module applied to column
        self.handpicked = True # What is this??
        self.handpickEncoding = {}

        #Others Models
        self.datas = Data.getInstance()
        self.filter.column = self.datas.get_variables()[0]

        #Ctrl
        self.ctrl = ParameterEncodingCtrl(self)

        #Views
        self.peView = None

    def set_main_var(self, variable : str):
        self.filter.column = variable

    def get_parameter(self, row):
        """
        Compute and return a value for the parameter selected for this model, based on the filter selected by the user
        and the encoding.
        :param row: Pandas Dataframe,
            a row containing data to transform into a parameter
        :return: int,
            a value between 0 and 128 used as a parameter for a note
        """
        return int(self.handpickEncoding[row[self.filter.column]])

    def assign_encoding(self, variables : [], values : []):
        """
        Assign values to variable, accordingly to user preference.
        :param variables: list,
            a list of all possible instances of a variable
        :param values: list,
            a list linked to the variable, used to compute a notes parameter
        """
        if(len(variables) != len(values)):
            raise ValueError()
        for var, val in zip(variables, values):
            self.handpickEncoding[var] = val


    def get_variables_instances(self):
        return self.datas.get_variables_instances(self.filter.column)
