# filename: FlameSlider.py

# -------------------------------------------------------------------------- #

# File Name:        FlameSlider.py
# Version:          0.0.4
# Language:         python script
# Flame Version:    2025.x
# Author:           Phil MAN - phil_man@mac.com
# Toolset:          MAN_MADE_MATERIAL: LOGIK-PROJEKT
# Created:          2024-04-20
# Modified:         2024-05-09
# Modifier:         Phil MAN - phil_man@mac.com

# Description:      This program is part of a library of custom functions
#                   and modules for autodesk flame.

# Installation:     Copy the 'LOGIK-PROJEKT' repo to your GitHub directory,
#                   e.g. '/home/$USER/workspace/GitHub'

# Attribution:      This script is derived from work originally authored by
#                   Michael Vaglienty: 'pyflame_lib_script_template.py'

# Changelist:       The full changelist is at the end of this document.

# -------------------------------------------------------------------------- #

# ========================================================================== #
# This section imports the necessary modules.
# ========================================================================== #

from PySide6 import (
    QtWidgets,
    QtCore,
    QtGui
)
import xml.etree.ElementTree as ET
from typing import (
    Union,
    List,
    Dict,
    Optional,
    Callable
)
import os
import re
import datetime
import shutil
import ast

class FlameSlider(QtWidgets.QLineEdit):
    '''
    Custom Qt Flame Slider Widget

    FlameSlider(start_value, min_value, max_value[, value_is_float=False, slider_width=110])

    start_value: int or float value
    min_value: int or float value
    max_value: int or float value
    value_is_float: (optional) bool value
    slider_width: (optional) default value is 110. [int]

    Usage:

        slider = FlameSlider(0, -20, 20, False)
    '''

    def __init__(self, start_value: int, min_value: int, max_value: int, value_is_float: Optional[bool]=False, slider_width: Optional[int]=110):
        super(FlameSlider, self).__init__()

        # Check argument types

        if not isinstance(start_value, int):
            raise TypeError('FlameSlider: start_value must be integer.')
        if not isinstance(min_value, int):
            raise TypeError('FlameSlider: min_value must be integer.')
        if not isinstance(max_value, int):
            raise TypeError('FlameSlider: max_value must be integer.')
        if not isinstance(value_is_float, bool):
            raise TypeError('FlameSlider: value_is_float must be a boolean.')
        if not isinstance(max_value, int):
            raise TypeError('FlameSlider: slider_width must be integer.')

        # Build slider

        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setMinimumHeight(28)
        self.setMinimumWidth(slider_width)
        self.setMaximumWidth(slider_width)

        if value_is_float:
            self.spinbox_type = 'Float'
        else:
            self.spinbox_type = 'Integer'

        self.min = min_value
        self.max = max_value
        self.steps = 1
        self.value_at_press = None
        self.pos_at_press = None
        self.setValue(start_value)
        self.setReadOnly(True)
        self.textChanged.connect(self.value_changed)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setStyleSheet('QLineEdit {color: rgb(154, 154, 154); background-color: rgb(55, 65, 75); selection-color: rgb(38, 38, 38); selection-background-color: rgb(184, 177, 167); border: none; padding-left: 5px; font: 14px "Discreet"}'
                           'QLineEdit:hover {border: 1px solid rgb(90, 90, 90)}'
                           'QLineEdit:disabled {color: rgb(106, 106, 106); background-color: rgb(55, 65, 75)}'
                           'QToolTip {color: rgb(170, 170, 170); background-color: rgb(71, 71, 71); border: 10px solid rgb(71, 71, 71)}')
        self.clearFocus()

        class Slider(QtWidgets.QSlider):

            def __init__(self, start_value, min_value, max_value, slider_width):
                super(Slider, self).__init__()

                self.setMaximumHeight(4)
                self.setMinimumWidth(slider_width)
                self.setMaximumWidth(slider_width)
                self.setMinimum(min_value)
                self.setMaximum(max_value)
                self.setValue(start_value)
                self.setOrientation(QtCore.Qt.Horizontal)
                self.setStyleSheet('QSlider {color: rgb(55, 65, 75); background-color: rgb(39, 45, 53)}'
                                   'QSlider::groove {color: rgb(39, 45, 53); background-color: rgb(39, 45, 53)}'
                                   'QSlider::handle:horizontal {background-color: rgb(102, 102, 102); width: 3px}'
                                   'QSlider::disabled {color: rgb(106, 106, 106); background-color: rgb(55, 65, 75)}')
                self.setDisabled(True)
                self.raise_()

        def set_slider():
            slider666.setValue(float(self.text()))

        slider666 = Slider(start_value, min_value, max_value, slider_width)
        self.textChanged.connect(set_slider)

        self.vbox = QtWidgets.QVBoxLayout(self)
        self.vbox.addWidget(slider666)
        self.vbox.setContentsMargins(0, 24, 0, 0)

    def calculator(self):
        from functools import partial

        def clear():
            calc_lineedit.setText('')

        def button_press(key):

            if self.clean_line == True:
                calc_lineedit.setText('')

            calc_lineedit.insert(key)

            self.clean_line = False

        def plus_minus():

            if calc_lineedit.text():
                calc_lineedit.setText(str(float(calc_lineedit.text()) * -1))

        def add_sub(key):

            if calc_lineedit.text() == '':
                calc_lineedit.setText('0')

            if '**' not in calc_lineedit.text():
                try:
                    calc_num = eval(calc_lineedit.text().lstrip('0'))

                    calc_lineedit.setText(str(calc_num))

                    calc_num = float(calc_lineedit.text())

                    if calc_num == 0:
                        calc_num = 1
                    if key == 'add':
                        self.setValue(float(self.text()) + float(calc_num))
                    else:
                        self.setValue(float(self.text()) - float(calc_num))

                    self.clean_line = True
                except:
                    pass

        def enter():

            if self.clean_line == True:
                return calc_window.close()

            if calc_lineedit.text():
                try:

                    # If only single number set slider value to that number

                    self.setValue(float(calc_lineedit.text()))
                except:

                    # Do math

                    new_value = calculate_entry()
                    self.setValue(float(new_value))

            close_calc()

        def equals():

            if calc_lineedit.text() == '':
                calc_lineedit.setText('0')

            if calc_lineedit.text() != '0':

                calc_line = calc_lineedit.text().lstrip('0')
            else:
                calc_line = calc_lineedit.text()

            if '**' not in calc_lineedit.text():
                try:
                    calc = eval(calc_line)
                except:
                    calc = 0

                calc_lineedit.setText(str(calc))
            else:
                calc_lineedit.setText('1')

        def calculate_entry():

            calc_line = calc_lineedit.text().lstrip('0')

            if '**' not in calc_lineedit.text():
                try:
                    if calc_line.startswith('+'):
                        calc = float(self.text()) + eval(calc_line[-1:])
                    elif calc_line.startswith('-'):
                        calc = float(self.text()) - eval(calc_line[-1:])
                    elif calc_line.startswith('*'):
                        calc = float(self.text()) * eval(calc_line[-1:])
                    elif calc_line.startswith('/'):
                        calc = float(self.text()) / eval(calc_line[-1:])
                    else:
                        calc = eval(calc_line)
                except:
                    calc = 0
            else:
                calc = 1

            calc_lineedit.setText(str(float(calc)))

            return calc

        def close_calc():
            calc_window.close()
            self.setStyleSheet('QLineEdit {color: rgb(154, 154, 154); background-color: rgb(55, 65, 75); selection-color: rgb(154, 154, 154); selection-background-color: rgb(55, 65, 75); border: none; padding-left: 5px; font: 14pt "Discreet"}'
                               'QLineEdit:hover {border: 1px solid rgb(90, 90, 90)}')
        def revert_color():
            self.setStyleSheet('QLineEdit {color: rgb(154, 154, 154); background-color: rgb(55, 65, 75); selection-color: rgb(154, 154, 154); selection-background-color: rgb(55, 65, 75); border: none; padding-left: 5px; font: 14pt "Discreet"}'
                               'QLineEdit:hover {border: 1px solid rgb(90, 90, 90)}')
        calc_version = '1.2'
        self.clean_line = False

        calc_window = QtWidgets.QWidget()
        calc_window.setMinimumSize(QtCore.QSize(210, 280))
        calc_window.setMaximumSize(QtCore.QSize(210, 280))
        calc_window.setWindowTitle(f'pyFlame Calc {calc_version}')
        calc_window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Popup)
        calc_window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        calc_window.destroyed.connect(revert_color)
        calc_window.move(QtGui.QCursor.pos().x() - 110, QtGui.QCursor.pos().y() - 290)
        calc_window.setStyleSheet('background-color: rgb(36, 36, 36)')

        # Labels

        calc_label = QtWidgets.QLabel('Calculator', calc_window)
        calc_label.setAlignment(QtCore.Qt.AlignCenter)
        calc_label.setMinimumHeight(28)
        calc_label.setStyleSheet('color: rgb(154, 154, 154); background-color: rgb(57, 57, 57); font: 14px "Discreet"')

        #  LineEdit

        calc_lineedit = QtWidgets.QLineEdit('', calc_window)
        calc_lineedit.setMinimumHeight(28)
        calc_lineedit.setFocus()
        calc_lineedit.returnPressed.connect(enter)
        calc_lineedit.setStyleSheet('QLineEdit {color: rgb(154, 154, 154); background-color: rgb(55, 65, 75); selection-color: rgb(38, 38, 38); selection-background-color: rgb(184, 177, 167); border: none; padding-left: 5px; font: 14px "Discreet"}')

        # Limit characters that can be entered into lineedit

        regex = QtCore.QRegularExpression('[0-9_,=,/,*,+,\-,.]+') # Fix for flame 2025
        validator = QtGui.QRegularExpressionValidator(regex) # Fix for flame 2025
        calc_lineedit.setValidator(validator)

        # Buttons

        def calc_null():
            # For blank button - this does nothing
            pass

        class FlameButton(QtWidgets.QPushButton):

            def __init__(self, button_name, size_x, size_y, connect, parent, *args, **kwargs):
                super(FlameButton, self).__init__(*args, **kwargs)

                self.setText(button_name)
                self.setParent(parent)
                self.setMinimumSize(size_x, size_y)
                self.setMaximumSize(size_x, size_y)
                self.setFocusPolicy(QtCore.Qt.NoFocus)
                self.clicked.connect(connect)
                self.setStyleSheet('QPushButton {color: rgb(154, 154, 154); background-color: rgb(58, 58, 58); border: none; font: 14px "Discreet"}'
                                   'QPushButton:hover {border: 1px solid rgb(90, 90, 90)}'
                                   'QPushButton:pressed {color: rgb(159, 159, 159); background-color: rgb(66, 66, 66); border: none}'
                                   'QPushButton:disabled {color: rgb(116, 116, 116); background-color: rgb(58, 58, 58); border: none}')

        blank_btn = FlameButton('', 40, 28, calc_null, calc_window)
        blank_btn.setDisabled(True)
        plus_minus_btn = FlameButton('+/-', 40, 28, plus_minus, calc_window)
        plus_minus_btn.setStyleSheet('color: rgb(154, 154, 154); background-color: rgb(45, 55, 68); font: 14px "Discreet"')
        add_btn = FlameButton('Add', 40, 28, (partial(add_sub, 'add')), calc_window)
        sub_btn = FlameButton('Sub', 40, 28, (partial(add_sub, 'sub')), calc_window)

        #  --------------------------------------- #

        clear_btn = FlameButton('C', 40, 28, clear, calc_window)
        equal_btn = FlameButton('=', 40, 28, equals, calc_window)
        div_btn = FlameButton('/', 40, 28, (partial(button_press, '/')), calc_window)
        mult_btn = FlameButton('/', 40, 28, (partial(button_press, '*')), calc_window)

        #  --------------------------------------- #

        _7_btn = FlameButton('7', 40, 28, (partial(button_press, '7')), calc_window)
        _8_btn = FlameButton('8', 40, 28, (partial(button_press, '8')), calc_window)
        _9_btn = FlameButton('9', 40, 28, (partial(button_press, '9')), calc_window)
        minus_btn = FlameButton('-', 40, 28, (partial(button_press, '-')), calc_window)

        #  --------------------------------------- #

        _4_btn = FlameButton('4', 40, 28, (partial(button_press, '4')), calc_window)
        _5_btn = FlameButton('5', 40, 28, (partial(button_press, '5')), calc_window)
        _6_btn = FlameButton('6', 40, 28, (partial(button_press, '6')), calc_window)
        plus_btn = FlameButton('+', 40, 28, (partial(button_press, '+')), calc_window)

        #  --------------------------------------- #

        _1_btn = FlameButton('1', 40, 28, (partial(button_press, '1')), calc_window)
        _2_btn = FlameButton('2', 40, 28, (partial(button_press, '2')), calc_window)
        _3_btn = FlameButton('3', 40, 28, (partial(button_press, '3')), calc_window)
        enter_btn = FlameButton('Enter', 40, 61, enter, calc_window)

        #  --------------------------------------- #

        _0_btn = FlameButton('0', 89, 28, (partial(button_press, '0')), calc_window)
        point_btn = FlameButton('.', 40, 28, (partial(button_press, '.')), calc_window)

        gridbox = QtWidgets.QGridLayout()
        gridbox.setVerticalSpacing(5)
        gridbox.setHorizontalSpacing(5)

        gridbox.addWidget(calc_label, 0, 0, 1, 4)

        gridbox.addWidget(calc_lineedit, 1, 0, 1, 4)

        gridbox.addWidget(blank_btn, 2, 0)
        gridbox.addWidget(plus_minus_btn, 2, 1)
        gridbox.addWidget(add_btn, 2, 2)
        gridbox.addWidget(sub_btn, 2, 3)

        gridbox.addWidget(clear_btn, 3, 0)
        gridbox.addWidget(equal_btn, 3, 1)
        gridbox.addWidget(div_btn, 3, 2)
        gridbox.addWidget(mult_btn, 3, 3)

        gridbox.addWidget(_7_btn, 4, 0)
        gridbox.addWidget(_8_btn, 4, 1)
        gridbox.addWidget(_9_btn, 4, 2)
        gridbox.addWidget(minus_btn, 4, 3)

        gridbox.addWidget(_4_btn, 5, 0)
        gridbox.addWidget(_5_btn, 5, 1)
        gridbox.addWidget(_6_btn, 5, 2)
        gridbox.addWidget(plus_btn, 5, 3)

        gridbox.addWidget(_1_btn, 6, 0)
        gridbox.addWidget(_2_btn, 6, 1)
        gridbox.addWidget(_3_btn, 6, 2)
        gridbox.addWidget(enter_btn, 6, 3, 2, 1)

        gridbox.addWidget(_0_btn, 7, 0, 1, 2)
        gridbox.addWidget(point_btn, 7, 2)

        calc_window.setLayout(gridbox)

        calc_window.show()

    def value_changed(self):

        # If value is greater or less than min/max values set values to min/max

        if int(self.value()) < self.min:
            self.setText(str(self.min))
        if int(self.value()) > self.max:
            self.setText(str(self.max))

    def mousePressEvent(self, event):

        if event.buttons() == QtCore.Qt.LeftButton:
            self.value_at_press = self.value()
            self.pos_at_press = event.pos()
            self.setCursor(QtGui.QCursor(QtCore.Qt.Horizontal)) # Fix for flame 2025
            self.setStyleSheet('QLineEdit {color: rgb(217, 217, 217); background-color: rgb(73, 86, 99); selection-color: rgb(154, 154, 154); selection-background-color: rgb(73, 86, 99); border: none; padding-left: 5px; font: 14pt "Discreet"}'
                               'QLineEdit:hover {border: 1px solid rgb(90, 90, 90)}')

    def mouseReleaseEvent(self, event):

        if event.button() == QtCore.Qt.LeftButton:

            # Open calculator if button is released within 10 pixels of button click

            if event.pos().x() in range((self.pos_at_press.x() - 10), (self.pos_at_press.x() + 10)) and event.pos().y() in range((self.pos_at_press.y() - 10), (self.pos_at_press.y() + 10)):
                self.calculator()
            else:
                self.setStyleSheet('QLineEdit {color: rgb(154, 154, 154); background-color: rgb(55, 65, 75); selection-color: rgb(154, 154, 154); selection-background-color: rgb(55, 65, 75); border: none; padding-left: 5px; font: 14pt "Discreet"}'
                                   'QLineEdit:hover {border: 1px solid rgb(90, 90, 90)}')

            self.value_at_press = None
            self.pos_at_press = None
            self.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
            return

        super(FlameSlider, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):

        if event.buttons() != QtCore.Qt.LeftButton:
            return

        if self.pos_at_press is None:
            return

        steps_mult = self.getStepsMultiplier(event)
        delta = event.pos().x() - self.pos_at_press.x()

        if self.spinbox_type == 'Integer':
            delta /= 10  # Make movement less sensiteve.
        else:
            delta /= 100
        delta *= self.steps * steps_mult

        value = self.value_at_press + delta
        self.setValue(value)

        super(FlameSlider, self).mouseMoveEvent(event)

    def getStepsMultiplier(self, event):

        steps_mult = 1

        if event.modifiers() == QtCore.Qt.ControlModifier: # Fix for flame 2025
            steps_mult = 10
        elif event.modifiers() == QtCore.Qt.ShiftModifier: # Fix for flame 2025
            steps_mult = 0.10

        return steps_mult

    def setMinimum(self, value):

        self.min = value

    def setMaximum(self, value):

        self.max = value

    def setSteps(self, steps):

        if self.spinbox_type == 'Integer':
            self.steps = max(steps, 1)
        else:
            self.steps = steps

    def value(self):

        if self.spinbox_type == 'Integer':
            return int(self.text())
        else:
            return float(self.text())

    def setValue(self, value):

        if self.min is not None:
            value = max(value, self.min)

        if self.max is not None:
            value = min(value, self.max)

        if self.spinbox_type == 'Integer':
            self.setText(str(int(value)))
        else:
            # Keep float values to two decimal places

            self.setText('%.2f' % float(value))

# ========================================================================== #
# This section defines how to handle the main script function.
# ========================================================================== #

# # If this script is executed as main:
# # Call functions for immediate execution
# if __name__ == "__main__":

# ========================================================================== #
# C2 A9 2D 32 30 32 34 2D 4D 41 4E 5F 4D 41 44 45 5F 4D 41 54 45 52 49 61 4C #
# ========================================================================== #

# Changelist:
# -------------------------------------------------------------------------- #
# version:               0.0.1
# modified:              2024-05-07 - 21:48:20
# comments:              Refactored monolithic code to discreet modules
# -------------------------------------------------------------------------- #
# version:               0.0.2
# modified:              2024-05-07 - 21:49:31
# comments:              Added docstrings
# -------------------------------------------------------------------------- #
# version:               0.0.3
# modified:              2024-05-07 - 21:50:00
# comments:              Prep for initial production test
# -------------------------------------------------------------------------- #
# version:               0.0.4
# modified:              2024-05-09 - 13:18:47
# comments:              Refactored code works in flame 2025. Time to tidy up.