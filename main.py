
'''Run this file to open markbook
python -m main
  '''

from fastcode import *
import os
import markbook_

class Option(object):
    '''option object, saves option attributes
    '''

    def __init__(self, name=None, index=-1, event=None, content=None, classroom=None):
        self.name = name
        self.index = index
        self.event = event
        self.content = content
        self.classroom = classroom
    
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
                    elif input_ == 'Gallo':
                        list[index] = 'バカ' 
                        break                     
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
                        return self.event_enter_a_classroom(classroom, string='Cancelled addition')
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
        self.header_2(f'Remove {dict_[COURSE_NAME]}')
        if self.get_assurance(f' to {classroom.name}'):
            self.markbook.del_classroom(dict_)
            return self.view_all_classroom(f'Successful removed {dict_[COURSE_NAME]}')
        else:
            return self.event_enter_a_classroom(classroom, f'Removement Cancelled')

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
        self.classroom_options.append(Option('view all students', index+1, self.view_all_students, classroom.content))
        self.classroom_options.append(Option('view all assignments', index+2, self.view_all_assignments, classroom.content))
        self.classroom_options.append(Option('edit this classroom', index+3, self.event_edit_a_classroom, classroom.content))              
        self.classroom_options.append(Option('remove this classroom', index+4, self.event_remove_a_classroom, classroom.content))         
        self.classroom_options.append(Option('exit', index+5, self.event_exit))     
        #view   
        self.header_1(f'Menu: Classroom {classroom.content[COURSE_NAME]}', string)
        self.header_2('Detials')
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
        list = self.markbook.get_all_student(dict_)
        self.all_student_options = []
        index = 0

        for student in list:#add all classrooms
            name = f'{student[FIRST_NAME]} {student[LAST_NAME]}'
            event = self.event_view_a_student
            option = Option(name, index, event, student, classroom)

            self.all_student_options.append(option)
            index += 1        
        self.all_student_options.append(Option('back to last menu', index, self.event_enter_a_classroom, classroom.content))
        self.all_student_options.append(Option('add a student', index+1, self.event_add_a_student, classroom.content))
        self.all_student_options.append(Option('exit', index+2, self.event_exit))

        #view
        self.header_1(f'Menu: Students in {classroom.content[COURSE_NAME]}', string)
        self.header_2('Students')
        for student in self.all_student_options:
            if int(str(student)) < index:
                print(f'{student.index}. {student.name}, ', end='')
        print()
        self.header_2('Options')
        print(f'type [0-{index-1}] the index before student name to view student profile')
        print(f'type {index} to go back to last menu')
        print(f'type {index+1} to add a student')
        print(f'type {index+2} to exit')

        #contronller
        while True:
            option = self.get_input(f"Please enter the option index[0-{index+2}]: ")
            for opt in self.all_student_options:
                if str(opt) == str(option):
                    return opt.trigger()
            else:
                print("invalid input, please try again")

    def event_add_a_student(self, classroom: object, string=''):
        self.header_1('Menu: Add Student', string)
        self.header_2('Student has following attributes')
        for attr in STUDENT_ATTRIBUTES.keys():
          print(attr)

        def create_student(list):
            if self.get_assurance():
                self.markbook.add_student(classroom.content, list[0], list[1], list[2], list[3], list[4], list[5], list[6])
                self.view_all_students(classroom, string='Successfully added a classroom')
            else:
                enter_attributes()

        def enter_attributes():
            self.header_2("Please Enter Student Attributes")
            print("{:-^60}".format("type 'enter' to skip this attributes"))
            print("{:-^60}".format("type 'c' to cancel this addition"))
            list = ['','','','',-1,-1,''] 


            for index, (key, value) in enumerate(STUDENT_ATTRIBUTES.items()):
                while True:
                    self.skip_line()
                    input_ =  self.get_input("please enter the {}(type: {},     defualt={})".format(key, type(value), value))
                    print(f'{key}: {input_}')
                    if input_ == 'c':
                        return self.event_enter_a_classroom(classroom, str1='Cancelled addition')
                    elif input_:
                        list[index] = input_
                        break
                    elif not input_:
                        break     

            self.header_2("Review New student")
            for index, key in enumerate(STUDENT_ATTRIBUTES.keys()):
                    print(f'{key}: {list[index]}')
            
            create_student(list)
        enter_attributes()

    def event_view_a_student(self, student: object, string=''):
        dict_ = student.content
        list = dict_.items()
        self.student_options = []       
        index = 0 
        #add options
        self.student_options.append(Option('back to last menu', index, self.view_all_students, student.classroom.content))
        self.student_options.append(Option('print student report', index+1))
        self.student_options.append(Option('add conmments', index+2, self.event_add_comment, student.content, student.classroom))
        self.student_options.append(Option('view student assignments', index+3, self.event_view_student_assignments, student.content, student.classroom))
        self.student_options.append(Option('edit student profile', index+4, self.event_edit_student_profile, student.content))
        self.student_options.append(Option('remove this student', index+5, self.event_remove_a_student, student.content, student.classroom))
        self.student_options.append(Option('exit', index+6, self.event_exit))   

        #view
        self.header_1(f'Menu: Student {student.content[FIRST_NAME]}', string)
        self.header_2('Profile')    
        for value in list:
            if value[0] != MARKS:
                print(f'{value[0]}: {value[1]}')
        print('student has following assignment:', end='')
        for ass in dict_[MARKS]:
            print(f'{ass[ASSIGNMENT_NAME]}: {ass[MARKS]}, ', end='')
        print()
        self.header_2('Options')
        for option in self.student_options:
            print(f'type {option.index} to {option.name}')

        #user
        while True:
            option = self.get_input(f"Please enter the option index[0-{index+5}]: ")
            for opt in self.student_options: 
                if str(opt) == str(option):    
                    return opt.trigger()
            else:
                print("invalid input, please try again")

    def event_edit_student_profile(self, student: object, string=''):
        dict_ = student.content
        self. header_1(f'Menu: Edit Student {student.name}')
        self.header_2('Student has following attributes')
        for attr in STUDENT_ATTRIBUTES.keys():
          print(attr) 
        
        def update_student(list):
            if self.get_assurance():
                self.markbook.edit_student(student.content, first_name=list[0], last_name=list[1], gender=list[2], image=list[3], student_number=list[4], grade=list[5], marks=list[6])
                self.event_view_a_student(student, string='Successfully updated student profile')
            else:
                enter_attributes()

        def enter_attributes():
            self.header_2("Please Enter Student Attributes")
            print("{:-^60}".format("type 'enter' to skip this attributes"))
            print("{:-^60}".format("type 'c' to cancel this addition"))
            list = [dict_[FIRST_NAME], dict_[LAST_NAME], dict_[GENDER], dict_[IMAGE], dict_[STUDENT_NUMBER], dict_[GRADE], dict_[EMAIL]]

            for index, (key, value) in enumerate(STUDENT_ATTRIBUTES.items()):
                while True:
                    self.skip_line()
                    input_ =  self.get_input("please enter the {}(type: {}, defualt={})".format(key, type(value), list[index]))
                    print(f'{key}: {input_}')
                    if input_ == 'c':
                        return self.event_view_a_student(student, string='Cancelled addition')
                    elif input_:
                        list[index] = input_
                        break
                    elif not input_:
                        break

            self.header_2("Review New student")
            for index, key in enumerate(STUDENT_ATTRIBUTES.keys()):
                    print(f'{key}: {list[index]}')
            
            update_student(list)
        
        enter_attributes() 

    def event_add_comment(self, student: object, string=''):
        dict_ = student.content
        self.header_2(f'Add Comments to {dict_[FIRST_NAME]}')
        comments = self.get_input('Please add the comments:')
        print(f'The new comment is {comments}')
        if self.get_assurance():
            self.markbook.add_student_comments(dict_, comments)
            self.event_view_a_student(student, 'Successfully added the comment')
        else:
            self.event_view_a_student(student, 'Addtion Cancelled')

    def event_remove_a_student(self, student: object):
        dict_ = student.content

        self.header_2(f'Remove {dict_[FIRST_NAME]}')
        if self.get_assurance(f' to {student.name}'):
            self.markbook.del_student(student.classroom.content, dict_)
            return self.view_all_students(student.classroom, f'Successful removed {dict_[FIRST_NAME]}')
        else:
            return self.event_view_a_student(student, f'Removement Cancelled')

    def event_view_student_assignments(self, student: object, string=''):
        dict_ = student.content
        list = self.markbook.get_student_marks(student.classroom.content, student.content)
        self.student_all_assignments_options = []
        #model
        index_ = len(list) - 1
        for index, value in enumerate(list):
            self.student_all_assignments_options.append(Option(value[0], index_, self.event_edit_student_assignment, student.content, student.classroom))
            self.student_all_assignments_options.append(Option(value[0], f'r{index_}', self.event_edit_student_assignment, student.content, student.classroom))        
        self.student_all_assignments_options.append(Option('back to last menu', index+1, self.event_view_a_student, student.content, student.classroom))
        self.student_all_assignments_options.append(Option('add an assignment', index+2, None, student.content))
        self.student_all_assignments_options.append(Option('exit', index+3, self.event_exit))

        #view
        self.header_2(f'Assignments of {dict_[FIRST_NAME]}')
        print('{:<20}{:<10}{:<15}{:<10}'.format('Assignment Name', 'Marks', 'Class Average', 'Class Median'))
        for index, value in enumerate(list):
            name, marks, ave, med = value[0], value[1], value[2], value[3]
            print('{:<20}{:<10}{:<15}{:<10}'.format(f'{index}.{name}',f'{marks}', f'{ave}', f'{med}'))   

        self.header_2('Options')
        print(f'type [0-{index-1}] the index before assignment name to edit assignment')
        print(f'type r[0-{index-1}] the index before assignment name to remove assignment example: r3')        
        print(f'type {index+1} to go back to last menu')
        print(f'type {index+2} to add a assignment')
        print(f'type {index+3} to exit')

        #contronller
        while True:
            option = self.get_input(f"Please enter the option index[0-{index+3}]: ")
            for opt in self.student_all_assignments_options:
                if str(opt) == str(option):
                    return opt.trigger()
            else:
                print("invalid input, please try again")

    def event_edit_student_assignment(self, assignment: object, string=''):
        dict_ = assignment.content[MARKS][assignment.index]
        self.header_2(f'Edit Assignment {dict_[ASSIGNMENT_NAME]}')

        def update_assignment(list):
            if self.get_assurance():
                self.markbook.update_assignment(assignment.content[MARKS][assignment.index], assignment_name=list[0], marks=list[1])
                self.event_view_student_assignments(assignment, string='Successfully updated assignment')
            else:
                enter_attributes()

        def enter_attributes():
            print("{:-^60}".format("type 'enter' to skip this attributes"))
            print("{:-^60}".format("type 'c' to cancel this addition"))
            list = [dict_[ASSIGNMENT_NAME], dict_[MARKS]]

            for index, (key, value) in enumerate(ASSIGNMENTS_ATTRIBUTES.items()):
                while True:
                    self.skip_line()
                    input_ =  self.get_input("please enter the {}(type: {}, defualt={})".format(key, type(value), list[index]))
                    print(f'{key}: {input_}')
                    if input_ == 'c':
                        return self.event_view_student_assignments(assignment, string='Cancelled addition')
                    elif input_:
                        list[index] = input_
                        break
                    elif not input_:
                        break

            self.header_2("Review New Assignment")
            for index, key in enumerate(ASSIGNMENTS_ATTRIBUTES.keys()):
                    print(f'{key}: {list[index]}')
            
            update_assignment(list)
        
        enter_attributes() 

    def event_remove_student_assignment(self, assignment: object, string=''):
        index_ = assignment.index[1]
        dict_ = assignment.content[MARKS][index_] 

        self.header_2(f'Remove {dict_[ASSIGNMENT_NAME]}')
        if self.get_assurance(f' to remove {dict_[ASSIGNMENT_NAME]}'):
            


    #Events of assignment    
    def view_all_assignments(self, classroom: object, string=''):
        dict_ = classroom.content
        


if __name__ == "__main__":
    path = os.path.abspath(os.path.dirname(__file__))
    os.chdir(path)

    client = Client()
    client.set_up()
