from Env import Timetable, Course, Classroom
import GA

if __name__ == "__main__":
    c1 = Course("ETC", "di nucci", 100, 8)
    c2 = Course("Math", "smith", 50,8)
    c3 = Course("Physics", "johnson", 75,8)
    d = Classroom("p1", 200)
    e = Classroom("p2", 100)
    time_table = Timetable([d,e])
    time_table.first_initialization([c1,c2,c3])
    print(time_table)
    GA.mutation(time_table)
    print(time_table)