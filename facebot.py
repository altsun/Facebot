# -*- coding: utf-8 -*-



# Import
import os
import sys

# fbchat
from fbchat import Client
from fbchat.models import *

# getpass
from getpass import getpass

# PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *



# Set current directory
current_directory = os.path.dirname(os.path.abspath(__file__))



# Class Facebot
class Facebot(Client):

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        # If sender is not myself, send auto-messages
        if author_id != self.uid:
            self.sendMessage('Đây là tin nhắn tự động\n_from Facebot with love_', thread_id=thread_id, thread_type=thread_type)
            self.sendLocalImage(current_directory + '/angelina.jpg', message=Message(text=''),
                                thread_id=thread_id, thread_type=thread_type)
# Facebot



# Class FacebotGui
class FacebotGui(QDialog):

    def __init__(self):
        # Initialize QDialog
        QDialog.__init__(self)

        # Default parameters
        self.width = 250
        self.height = 100
        self.margin = 10

        # Create layout
        layout = QGridLayout()

        # Create and set elements
        ## Input email
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText('Email')
        ## Input password
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText('Password')
        self.input_password.setEchoMode(QLineEdit.Password)
        ## Checkbox auto-message
        self.check_auto_message = QCheckBox('Auto-messsage')

        # Add elements to layout
        layout.addWidget(self.input_email, 0, 0)
        layout.addWidget(self.input_password, 1, 0)
        layout.addWidget(self.check_auto_message, 2, 0)

        # Set layout
        self.setLayout(layout)

        # Initialize UI
        self.init_ui()

        # Handle events
        self.check_auto_message.clicked.connect(self.handle_auto_message)


    # Front-end functions
    def init_ui(self):
        # Set window title
        self.setWindowTitle('Facebot')

        # Set window size
        self.setGeometry(50, 50, self.width, self.height)

        # Set window at center
        self.center()

        # Remove default focus
        self.setFocus()

        # Show window
        self.show()
    # init_ui


    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())
    # center


    # Back-end functions
    def handle_auto_message(self):
        # self <- facebot_gui
        self.messenger = AutoMessageBackgroundThread(self, self.check_auto_message, self.input_email, self.input_password)

        # IMPORTANT: ALWAYS start()
        self.messenger.start()
# FacebotGui



# Class AutoMessageBackgroundThread
class AutoMessageBackgroundThread(QThread):
    
    def __init__(self, facebot_gui, checkbox, input_email, input_password):
        '''
        facebot_gui: FacebotGui
        checkbox: QCheckBox
        input_email: QLineEdit
        input_password: QLineEdit

        return: None
        '''
        # Initialize QThread
        QThread.__init__(self)

        # Initialize attributes
        self.facebot_gui = facebot_gui
        self.checkbox = checkbox
        self.input_email = input_email
        self.input_password = input_password

    def run(self):
        auto_message(self.facebot_gui, self.checkbox, self.input_email, self.input_password)
# AutoMessageBackgroundThread



def auto_message(facebot_gui, checkbox, input_email, input_password):
    '''
    facebot_gui: FacebotGui
    checkbox: QCheckBox
    input_email: QLineEdit
    input_password: QLineEdit

    return: None
    '''
    if checkbox.isChecked():
        # Input info
        facebot_gui.email = input_email.text()
        facebot_gui.password = input_password.text()

        # Create client, login to FB
        facebot_gui.client = Facebot(facebot_gui.email, facebot_gui.password)

        # Wait for messages
        facebot_gui.client.listen()

    elif not checkbox.isChecked():
        # Logout
        facebot_gui.client.logout()
        print('Logout of {} succesful.'.format(facebot_gui.email))

    return None
# auto_message



# Run Gui
app = QApplication(sys.argv)
facebot_gui = FacebotGui()
app.exec_()
