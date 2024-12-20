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
    Course("Math", professors[1], 190, 7, 3),
    Course("Physics", professors[2], 75, 8),
    Course("Programming", professors[3], 75, 9, 3),
    Course("Chemistry", professors[4], 100, 6),
    Course("Biology", professors[0], 120, 6),
    Course("History", professors[1], 80, 6),
    Course("Geography", professors[2], 90, 4),
    Course("Art", professors[3], 60, 4),
    Course("Music", professors[4], 50, 2),
    Course("Philosophy", professors[0], 60, 4),
    Course("Economics", professors[1], 80, 6),
    Course("Literature", professors[2], 70, 6),
    Course("Sociology", professors[3], 85, 6),
    Course("Psychology", professors[4], 90, 8),
    Course("Anthropology", professors[0], 65, 4),
    Course("Political Science", professors[1], 75, 7, 3),
    Course("Linguistics", professors[2], 55, 4),
    Course("Astronomy", professors[3], 85, 6),
    Course("Statistics", professors[4], 95, 9, 3),
    Course("Computer Science", professors[0], 100, 9, 3),
]

classrooms = [
    Classroom("p1", 200),
    Classroom("p2", 75),
    Classroom("p3", 100),
    Classroom("p4", 150),
    Classroom("p5", 90)
]


def testing():
    agent1 = Timetable(classrooms, [courses[0]])
    agent2 = Timetable(classrooms, [courses[0]])
    timetable_data1 = [
        [[1, 0, 2, True], [1, 0, 3, True], [0, 2, 4, True], [4, 0, 5, False], [4, 0, 7, False], [4, 0, 4, False], [4, 0, 6, False], [3, 0, 0, False]]
    ]
    timetable_data2 = [
        [[1, 0, 2, True], [1, 0, 3, True], [0, 2, 4, True], [4, 0, 5, False], [4, 0, 7, False], [4, 3, 1, True], [4, 0, 6, True], [3, 0, 0, True]]
    ]

    agent1.test(timetable_data1)
    agent2.test(timetable_data2)
    print(agent1, "\n", agent2)
    child1, child2 = GA.crossover(agent1, agent2)
    GA.fitness(child1)
    print("\n", child1, "\n", child2)

# if __name__ == "__main__":
#     testing()

if __name__ == "__main__":
    agents = [Timetable(classrooms, courses) for _ in range(30)]

    result, fitness, statistics = GA.run(agents, generations=5000, mutation_rate=0.7, k=20, m=20)
    print(result.display_as_table())
    GA.fitness(result)