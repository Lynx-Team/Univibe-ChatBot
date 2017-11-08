
def showTableMessage(mod):
    if(mod == "s"):
        return getStudentTable()
    else:
        return getTeacherTable()


def getStudentTable():
    return "Student lesson"

def getTeacherTable():
    return "Teacher lesson"