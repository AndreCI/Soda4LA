from Ctrls.parameter_encoding_controller import ParameterEncodingCtrl
from Models.data_model import Data
from Utils.constants import ENCODING_OPTIONS


class ParameterEncoding():

    """
    Model class for parameters encoding. It enables raw data to be processed into notes. Each track has its own parameter
    encoding objects.
    This can be viewed via a track config view and its subsequent views presented by its buttons.
    """
    def __init__(self, encoded_var):
        #Data
        self.encoded_var=encoded_var
        if(self.encoded_var not in ENCODING_OPTIONS):
            raise NotImplementedError("{} not in encoding options".format(self.encoded_var))
        self.main_var = None

        #Others Models
        self.datas = Data()

        #Ctrl
        self.ctrl = ParameterEncodingCtrl(self)

        #Views
        self.pe_view = None

    def get_variables_instances(self):
        return self.datas.get_variables_instances(self.main_var)