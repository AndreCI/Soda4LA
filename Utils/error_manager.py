from PyQt5.QtWidgets import QMessageBox


class ErrorManager:
    _instance = None

    @staticmethod
    def getInstance():
        if not ErrorManager._instance:
            ErrorManager()
        return ErrorManager._instance

    def __init__(self):
        if ErrorManager._instance is None:
            ErrorManager._instance = self
            self.warning = {"datetime_replacement":True,
                            "timestamp_notfound":True,
                            "sorted_data":True}

    def sorted_data_warning(self):
        if(self.warning["sorted_data"]):
            self.warning["sorted_data"] = True
            msg = QMessageBox()
            ans = msg.question(None,'Warning: data are not sequential!',
                                'Soda requires sequential data. The selected timestamp column is either invalid or the data needs to be reformated.\nDo you want Soda to sort your data?',
                                msg.Yes | msg.No )
            return ans == msg.Yes

    def datetime_replacement_warning(self):
        if(self.warning["datetime_replacement"]):
            self.warning["datetime_replacement"] = False
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Warning: years before 1971 will be replaced!")
            msg.setInformativeText('Some or all years found in data will be replaced by 1971. If this is an issue, you need to reformat your data.')
            msg.setWindowTitle("Warning")
            msg.exec_()

    def timestamp_warning(self):
        if(self.warning["timestamp_notfound"]):
            self.warning["timestamp_notfound"] = False
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Warning: no candidate column found that can be used as timestamp!")
            msg.setInformativeText('Soda requires data to be sequential, but no column has been found that can '
                                   'be used a timestamp. \nIf your data does contain a column that can be used as '
                                   'timestamp, you need to inform Soda of the format used and the name of the '
                                   'column.')
            msg.setWindowTitle("Warning")
            msg.exec_()
    def timeformat_error(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error: No format found for this timestamp!")
        msg.setInformativeText('No valid format have been found for this timestamp. You will need to manually '
                               'set the timestamp format while loading your data. The format should follow '
                               'python formatting found here: \n'
                               'https://docs.python.org/3.10/library/datetime.html#strftime-and-strptime-format-codes')
        msg.setWindowTitle("Error")
        msg.exec_()
    def wrong_data_error(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error: additional data do not match already loaded data!")
        msg.setInformativeText('Loading additional data to compare it with already loaded data requires the new'
                               ' files header to be the same as the original data \nTry loading another file'
                               ' as additional, load this file directly as primary data or reformat your data.')
        msg.setWindowTitle("Error")
        msg.exec_()

    @staticmethod
    def compare_headers(header_primary, header)->bool:
        for value in header:
            if value not in header_primary:
                return False
        return True
