
'''Run this file to open markbook
python -m main
  '''

from fastcode import *
import os
import markbook_

class Option(object):
    '''option object, saves option attributes
    '''

    def __init__(self, name=None, index=-1, event=None, content=None):
        self.name = name
        self.index = index
        self.event = event
        self.content = content
    
    def __str__(self):
        return str(self.index)
    
    def trigger(self):
        if self.event:
            return self.event(self)
  


class Client(object):
    '''user interpertation object
    '''

    def __init__(self):
        self.markbook = markbook_.Markbook()

    def set_up(self):
        print("{:=^60}".format('Markbook'))
        print("{}".format('Loading...'))
        self.markbook.set_up()
        print("{}".format('Wellcome to Markbook'))
        self.view_all_classroom()
    
    def get_input(self, str: str) -> str:
        i = input(str)
        return i

    def get_assurance(self, str='') -> bool:
        while True:
            i = input(f'Are you sure{str}?(y/n):')
            if i == 'y' or i == '':
                return True
            elif i == 'n':
                return False
            else:
                print("invalid input, please enter 'y' or 'n'")
    
    def header_1(self ,str:str, str1=''):
        print('\n'*40)
        if str1:
            print(str1)
        print("{:=^60}".format(str))     

    def header_2(self, str:str):
        print("\n"+"{:-^60}".format(str))

    def skip_line(self):
        print("\n")      
  
    #model - view - controller
    def event_exit(self, obj: object):
        self.header_2('Exited')
        self.markbook.close()
    
    #Events of all classroom
    def view_all_classroom(self, str1=''):
        '''a menu shows all classrooms and options
        '''
        #model part
        list = self.markbook.get_all_classroom()
        self.all_classroom_options = []#a list contents option objects in this menu 
        index = 0

        for classroom in list:#add all classrooms
            name = f'period {classroom[PERIOD]}, {classroom[COURSE_NAME]}'
            event = self.event_enter_a_classroom
            option = Option(name, index, event, classroom)

            self.all_classroom_options.append(option)
            index += 1

        #add other options
        self.all_classroom_options.append(Option('add a classroom', index, self.event_add_a_classroom))
        self.all_classroom_options.append(Option('exit', index+1, self.event_exit))

        #view part: print everything
        self.header_1('Menu: All Classrooms', str1)
        self.header_2('classrooms')
        for classes in self.all_classroom_options:
            if int(str(classes)) < index:
              print (f"period{classes.content[PERIOD]}: {classes.content[COURSE_CODE]} {classes.content[COURSE_NAME]} by {classes.content[TEACHER_NAME]}")
        self.header_2('Options')
        for classes in self.all_classroom_options:
            if int(str(classes)) < index:
                print (f'type {classes.index} to enter class "{classes.name}"')
            else:
                print(f'type {classes.index} to {classes.name}')
        self.header_2('Please Enter')

        #User and controller part
        while True:
            option = self.get_input(f"Please enter the option index[0-{index+1}]: ")
            for opt in self.all_classroom_options: 
                if str(opt) == str(option):    
                    return opt.trigger()
            else:
                print("invalid input, please try again")

    def event_add_a_classroom(self, obj: object, str1=''):
        self.header_1('Menu: Add Classroom')
        self.header_2('Classroom has following attributes')
        for attr in CLASSROOM_ATTRIBUTES.keys():
          print(attr)
  
        def create_classroom(list):
            if self.get_assurance():
                self.markbook.add_classroom(list[0], list[1], list[2], list[3])
                self.view_all_classroom(str1='Successfully added a classroom')
            else:
                enter_attributes()

        def enter_attributes():
            self.header_2("Please Enter Classroom Attributes")
            print("{:-^60}".format("type 'enter' to skip this attributes"))
            print("{:-^60}".format("type 'c' to cancel this addition"))
            list = ['', '', 0, '']
            for index, (key, value) in enumerate(CLASSROOM_ATTRIBUTES.items()):
                while True:
                    self.skip_line()
                    input_ =  self.get_input("please enter the {}(type: {},     defualt={})".format(key, type(value), value))
                    print(f'{key}: {input_}')
                    if input_ == 'c':
                        return self.view_all_classroom(str1='Cancelled addition')
                    elif input_:
                        list[index] = input_
                        break
                    elif not input_:
                        break

            self.header_2("Review New classroom")
            for index, key in enumerate(CLASSROOM_ATTRIBUTES.keys()):
                    print(f'{key}: {list[index]}')
            
            create_classroom(list)
        
        enter_attributes()

    #Events of classroom
    def event_edit_a_classroom(self, classroom: object, stirng=''):
        dict_ = classroom.content
        self.header_1(f'Menu: Edit Classroom {classroom.name}')
        self.header_2('Classroom has following attributes')
        for attr in CLASSROOM_ATTRIBUTES.keys():
          print(attr)
        
        def update_classroom(list):
            if self.get_assurance():
                self.markbook.update_classroom(classroom.content, course_code=list[0], course_name=list[1], period=list[2], teacher_name=list[3])
                self.event_enter_a_classroom(classroom, string='Successfully updated a classroom')
            else:
                enter_attributes()

        def enter_attributes():
            self.header_2("Please Enter Classroom Attributes")
            print("{:-^60}".format("type 'enter' to skip this attributes"))
            print("{:-^60}".format("type 'c' to cancel this addition"))
            list = [dict_[COURSE_CODE], dict_[COURSE_NAME], dict_[PERIOD], dict_[TEACHER_NAME]]
            for index, (key, value) in enumerate(CLASSROOM_ATTRIBUTES.items()):
                while True:
                    self.skip_line()
                    input_ =  self.get_input("please enter the {}(type: {}, defualt={})".format(key, type(value), list[index]))
                    print(f'{key}: {input_}')
                    if input_ == 'c':
                        return self.view_all_classroom(str1='Cancelled addition')
                    elif input_:
                        list[index] = input_
                        break
                    elif not input_:
                        break

            self.header_2("Review New classroom")
            for index, key in enumerate(CLASSROOM_ATTRIBUTES.keys()):
                    print(f'{key}: {list[index]}')
            
            update_classroom(list)
        
        enter_attributes()

    def event_remove_a_classroom(self, classroom: object):
        dict_ = classroom.content
        if self.get_assurance(f' to {classroom.name}'):
            self.markbook.del_classroom(dict_)
            return self.view_all_classroom(f'Successful removed {classroom.name}')

    def event_enter_a_classroom(self, classroom: object, string=''):
        '''A menu shows all classroom detials and options
             -> all_classrooms, view all students, view all assignments, remove
        '''
        dict_ = classroom.content
        list = dict_.items()
        self.classroom_options = []
        index = 0

        #add options
        self.classroom_options.append(Option('back to last menu', index, self.view_all_classroom))
        self.classroom_options.append(Option('view all students', index+1, self.view_all_assignments, classroom.content))
        self.classroom_options.append(Option('view all assignments', index+2, self.view_all_students, classroom.content))
        self.classroom_options.append(Option('edit this classroom', index+3, self.event_edit_a_classroom, classroom.content))              
        self.classroom_options.append(Option('remove this classroom', index+4, self.event_remove_a_classroom, classroom.content))         
        self.classroom_options.append(Option('exit', index+5, self.event_exit))     
        #view   
        self.header_1(f'Menu: Classroom {classroom.name}', string)
        self.header_2('detials')
        for value in list:
            if value[0] != STUDENT_LIST and value[0] != ASSIGNMENTS_LIST:
                print(f'{value[0]}: {value[1]}')
        print('class has following students:', end='')
        for student in dict_[STUDENT_LIST]:
            print(f'{student[FIRST_NAME]} ', end='')
        print()
        print('class has following assignments:', end='')
        for assignment in dict_[ASSIGNMENTS_LIST]:
            print(f'{assignment[ASSIGNMENT_NAME]} ', end='')
        print()       
        self.header_2('Options')
        for option in self.classroom_options:
            print(f'type {option.index} to {option.name}')
        #user
        while True:
            option = self.get_input(f"Please enter the option index[0-{index+5}]: ")
            for opt in self.classroom_options: 
                if str(opt) == str(option):    
                    return opt.trigger()
            else:
                print("invalid input, please try again")  
        
    #Events of student
    def view_all_students(self, classroom: object, string=''):
        dict_ = classroom.content
        list = dict_.items()
        
    def view_all_assignments(self, classroom: object, string=''):
        dict_ = classroom.content
        


if __name__ == "__main__":
    path = os.path.abspath(os.path.dirname(__file__))
    os.chdir(path)

    client = Client()
    client.set_up()
