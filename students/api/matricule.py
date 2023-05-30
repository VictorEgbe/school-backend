from random import randrange


def generate_student_id(queryset):
    while True:
        school = "QIS"  # Change depending on the school
        random_int = randrange(0, 9999)

        if random_int < 10:
            string = "000" + str(random_int)
        elif random_int < 100:
            string = "00" + str(random_int)
        elif random_int < 999:
            string = "0" + str(random_int)
        else:
            string = str(random_int)

        id = school + string

        ids = [student.student_id for student in queryset]

        if id in ids:
            continue
        else:
            return id