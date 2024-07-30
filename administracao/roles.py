from rolepermissions.roles import AbstractUserRole 

class Moderator(AbstractUserRole):
    available_permissions = {'create_new_users': True}

class Student(AbstractUserRole):
    available_permissions = {'read_information':True}


class Teacher(AbstractUserRole):
    available_permissions = {'publish_grades_and_warnings':True}
