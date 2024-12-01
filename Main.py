from Env import Timetable, Course, Classroom
import GA

c1 = Course("ETC", "di nucci", 200, 8)
c2 = Course("Math", "smith", 190, 6, 3)
c3 = Course("Physics", "johnson", 75, 8)
c4 = Course("Physics", "di nucci", 150, 8)
c5 = Course("Physics", "smith", 75, 8)
c6 = Course("Programming", "johnson", 75, 9, 3)
c7 = Course("Chemistry", "lee", 100, 7)
c8 = Course("Biology", "kim", 120, 6)
c9 = Course("History", "brown", 80, 5)
c10 = Course("Geography", "davis", 90, 4)
c11 = Course("Art", "miller", 60, 3)
c12 = Course("Music", "wilson", 50, 2)
c13 = Course("Philosophy", "adams", 60, 3)
c14 = Course("Economics", "clark", 80, 5)
c15 = Course("Literature", "evans", 70, 4)
c16 = Course("Sociology", "martin", 85, 6)
c17 = Course("Psychology", "robinson", 90, 7)
c18 = Course("Anthropology", "walker", 65, 4)
c19 = Course("Political Science", "young", 75, 5)
c20 = Course("Linguistics", "allen", 55, 3)
c21 = Course("Astronomy", "taylor", 85, 6)
c22 = Course("Statistics", "moore", 95, 5)
c23 = Course("Computer Science", "thompson", 100, 7)

d = Classroom("p1", 200)
e = Classroom("p2", 75)
f = Classroom("p3", 100)
g = Classroom("p4", 150)
h = Classroom("p5", 90)

def testing():
    agent = Timetable([d,e,f,g,h], [c1])
    timetable_data = [
        [[0, 0, 4], [0, 0, 4], [0, 2, 4], [4, 0, 5], [4, 0, 7], [4, 0, 4], [4, 0, 6], [3, 0, 0]]
    ]
    agent.test(timetable_data)
    GA.fitness(agent)

# if __name__ == "__main__":
#     testing()

if __name__ == "__main__":
    courses = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, c20, c21, c22, c23]
    classrooms = [d, e, f, g, h]
    agents = [Timetable(classrooms, courses) for _ in range(30)]

    result, fitness, statistics = GA.run(agents, generations=500, mutation_rate=0.7, k=16, m=20)
    print(result.display_as_table())
    GA.fitness(result)