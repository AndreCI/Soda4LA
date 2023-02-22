from __future__ import annotations

import logging

import Models.note_model
import Models.parameter_encoding_model as pe


class ParameterEncodingCtrl:
    """
    Controller for the encoding view
    """

    def __init__(self, model: pe.ParameterEncoding):
        # Model
        self.model = model

    def assign_main_var(self, main_var: str) -> None:
        self.model.filter.assign_column(main_var)
        self.model.initialized = True

    def set_default_value(self, value: str) -> None:
        if value == "":
            return
        if self.model.encoded_var == "value":
            if value.isnumeric():
                try:
                    v = Models.note_model.note_to_int(Models.note_model.int_to_note(int(value)), int(self.model.octave))
                    self.model.defaultValue = v
                except ValueError:
                    logging.log(logging.ERROR, "Issue with value in setDefault-value {}".format(value))
            else:
                try:
                    v = Models.note_model.note_to_int(str(value).upper(), int(self.model.octave))
                    self.model.defaultValue = v
                except ValueError:
                    logging.log(logging.ERROR, "Issue with value in setDefault-value-nonnum {}".format(value))
        elif value.isnumeric():
            self.model.defaultValue = int(value)

    def reset_value(self, variable: str) -> None:
        self.model.handpickEncoding.pop(variable, None)

    def set_value(self, value: str, variable: str) -> None:
        if value == "":
            return
        if self.model.encoded_var == "value":
            if value.isnumeric():
                try:
                    v = Models.note_model.note_to_int(Models.note_model.int_to_note(int(value)), int(self.model.octave))
                    self.model.handpickEncoding[variable] = v
                except ValueError:
                    logging.log(logging.WARNING,
                                "Value sent to the pec is numeric but is not a valid note: {}.".format(value))
                    return
            else:
                try:
                    v = Models.note_model.note_to_int(str(value).upper(), int(self.model.octave))
                    self.model.handpickEncoding[variable] = v
                except ValueError:
                    logging.log(logging.WARNING,
                                "Value sent to the pec is not numeric but is not a valid note: {}.".format(value))

                    return
        elif value.isnumeric():
            self.model.handpickEncoding[variable] = int(value) if self.model.maxValue > int(
                value) > 0 else self.model.defaultValue

    def change_octave(self, octave: str) -> None:
        self.model.octave = octave
        for key in self.model.handpickEncoding:
            self.set_value(Models.note_model.int_to_note(self.model.handpickEncoding[key]), key)
        self.set_default_value(Models.note_model.int_to_note(int(self.model.defaultValue)))
