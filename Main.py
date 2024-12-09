from Env import Timetable, Course, Classroom, Professor
import GA

professors = [
    Professor("di nucci", [[1, 2], [1, 3]]),
    Professor("smith", [[2, 3], [3, 4]]),
    Professor("johnson", [[2, 3], [3, 4]]),
    Professor("lee", [[1, 2], [1, 3]]),
    Professor("kim", [[2, 3], [3, 4]]),
]

# Define courses and classrooms
courses = [
    Course("ETC", professors[0], 200, 8),
    Course("Math", professors[1], 190, 6, 3),
    Course("Physics", professors[2], 75, 8),
    Course("Programming", professors[3], 75, 9, 3),
    Course("Chemistry", professors[4], 100, 7),
    Course("Biology", professors[0], 120, 6),
    Course("History", professors[1], 80, 5),
    Course("Geography", professors[2], 90, 4),
    Course("Art", professors[3], 60, 3),
    Course("Music", professors[4], 50, 2),
    Course("Philosophy", professors[0], 60, 3),
    Course("Economics", professors[1], 80, 5),
    Course("Literature", professors[2], 70, 4),
    Course("Sociology", professors[3], 85, 6),
    Course("Psychology", professors[4], 90, 7),
    Course("Anthropology", professors[0], 65, 4),
    Course("Political Science", professors[1], 75, 5),
    Course("Linguistics", professors[2], 55, 3),
    Course("Astronomy", professors[3], 85, 6),
    Course("Statistics", professors[4], 95, 5),
    Course("Computer Science", professors[0], 100, 7),
]

classrooms = [
    Classroom("p1", 200),
    Classroom("p2", 75),
    Classroom("p3", 100),
    Classroom("p4", 150),
    Classroom("p5", 90)
]


def testing():
    agent = Timetable(classrooms, [courses[0]])
    timetable_data = [
        [[1, 0, 2], [1, 0, 3], [0, 2, 4], [4, 0, 5], [4, 0, 7], [4, 0, 4], [4, 0, 6], [3, 0, 0]]
    ]
    agent.test(timetable_data)
    GA.fitness(agent)

# if __name__ == "__main__":
#     testing()

if __name__ == "__main__":
    agents = [Timetable(classrooms, courses) for _ in range(30)]

    result, fitness, statistics = GA.run(agents, generations=5000, mutation_rate=0.7, k=20, m=20)
    print(result.display_as_table())
    GA.fitness(result)