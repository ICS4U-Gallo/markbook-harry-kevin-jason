'''Run this file to open markbook
'''

from fastcode import *
import os
import markbook_

class Option(object):
    '''option object, saves option attributes
    '''

    def __init__(self):
        self.name = None
        self.index = None
        self.event = None
        pass




class Client(object):
    '''user interpertation object
    '''

    def __init__(self):
        self.markbook = markbook_.Markbook
        self.classroom_option_list = []
        self.classroom_student_option_list = []
        self.classroom_assignment_opotion_list = []
        

    def set_up(self):
        self.markbook.set_up()
        if self.markbook.classroom_list:
            pass
        print()
    
    def get_input(self, str: str=None) -> str:
        s = input(f'{str}')
        return s





if __name__ == "__main__":
    path = os.path.abspath(os.path.dirname(__file__))
    os.chdir(path)

    client = Client()
    client.set_up()