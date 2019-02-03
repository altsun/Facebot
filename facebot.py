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
            self.sendMessage('`Đây là tin nhắn tự động`\n_`from Facebot with love`_', thread_id=thread_id, thread_type=thread_type)
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
        self.height = 150
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
        ## Checkbox login
        self.check_login = QCheckBox('Login')
        ## Checkbox auto-message
        self.check_auto_message = QCheckBox('Auto-messsage')

        # Add elements to layout
        layout.addWidget(self.input_email, 0, 0)
        layout.addWidget(self.input_password, 1, 0)
        layout.addWidget(self.check_login, 2, 0)
        layout.addWidget(self.check_auto_message, 3, 0)

        # Set layout
        self.setLayout(layout)

        # Initialize UI
        self.init_ui()

        # Handle events
        self.check_login.clicked.connect(self.handle_login)
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
        self.messenger = AutoMessageBackgroundThread(self, self.check_login, self.check_auto_message)

        # IMPORTANT: ALWAYS start()
        self.messenger.start()
    # handle_auto_message

    def handle_login(self):
        if self.check_login.isChecked:
            # Input info
            self.email = self.input_email.text()
            self.password = self.input_password.text()
            
            try:
                # Create client, login to FB
                self.client = Facebot(self.email, self.password, max_tries=1)
            except FBchatException:
                warning = QMessageBox.warning(
                    facebot_gui, 'Error', 'Login not succesful')
                self.check_login.setChecked(False)
                return None

        else:
            # Logout
            self.client.logout()
            print('Logout of {} succesful.'.format(self.email))
    # handle_login
# FacebotGui



# Class AutoMessageBackgroundThread
class AutoMessageBackgroundThread(QThread):
    
    def __init__(self, facebot_gui, check_login, check_auto_message):
        '''
        facebot_gui: FacebotGui
        check_login: QCheckBox
        check_auto_message: QCheckBox

        return: None
        '''
        # Initialize QThread
        QThread.__init__(self)

        # Initialize attributes
        self.facebot_gui = facebot_gui
        self.check_login = check_login
        self.check_auto_message = check_auto_message

    def run(self):
        auto_message(self.facebot_gui, self.check_login, self.check_auto_message)
# AutoMessageBackgroundThread



def auto_message(facebot_gui, check_login, check_auto_message):
    '''
    facebot_gui: FacebotGui
    check_login: QCheckBox
    check_auto_message: QCheckBox

    return: None
    '''
    if check_login.isChecked() and check_auto_message.isChecked():
        # Listen to messages
        facebot_gui.client.listen()

    elif not check_login.isChecked():
        # Do nothing
        pass

    elif check_login.isChecked and not check_auto_message.isChecked():
        # Stop listening to messages
        facebot_gui.client.listening = False
        print('Stop listening.')

    return None
# auto_message



# Run Gui
app = QApplication(sys.argv)
facebot_gui = FacebotGui()
app.exec_()
