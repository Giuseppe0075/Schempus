from Env import Timetable, Course, Classroom, Professor, Subjects
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
Course("ETC", professors[0], 200, 8, Subjects.COMPUTER_SCIENCE),
Course("Math", professors[1], 190, 7, Subjects.MATH, 3),
Course("Physics", professors[2], 75, 8, Subjects.PHYSICS),
Course("Programming", professors[3], 75, 9, Subjects.COMPUTER_SCIENCE, 3),
Course("Chemistry", professors[4], 100, 6, Subjects.CHEMISTRY),
Course("Biology", professors[0], 120, 6, Subjects.BIOLOGY),
Course("History", professors[1], 80, 6, Subjects.HISTORY),
Course("Geography", professors[2], 90, 4, Subjects.GEOGRAPHY),
Course("Art", professors[3], 60, 4, Subjects.ART),
Course("Music", professors[4], 50, 2, Subjects.MUSIC),
Course("Philosophy", professors[0], 60, 4, Subjects.PHILOSOPHY),
Course("Economics", professors[1], 80, 6, Subjects.ECONOMICS),
Course("Literature", professors[2], 70, 6, Subjects.LITERATURE),
Course("Sociology", professors[3], 85, 6, Subjects.SOCIOLOGY),
Course("Psychology", professors[4], 90, 8, Subjects.PSYCHOLOGY),
Course("Anthropology", professors[0], 65, 4, Subjects.ANTHROPOLOGY),
Course("Political Science", professors[1], 75, 7, Subjects.POLITICAL_SCIENCE, 3),
Course("Linguistics", professors[2], 55, 4, Subjects.LINGUISTICS),
Course("Astronomy", professors[3], 85, 6, Subjects.ASTRONOMY),
Course("Statistics", professors[4], 95, 9, Subjects.STATISTICS, 3),
Course("Programming 1", professors[0], 100, 9, Subjects.COMPUTER_SCIENCE, 3),
]

classrooms = [
    Classroom("p1", 200),
    Classroom("p2", 75),
    Classroom("p3", 100),
    Classroom("p4", 150),
    Classroom("p5", 90),
    Classroom("labCS", 200, True, Subjects.COMPUTER_SCIENCE),
    Classroom("labS", 95, True, Subjects.STATISTICS),
    Classroom("labPS", 90, True, Subjects.POLITICAL_SCIENCE),
    Classroom("labM", 200, True, Subjects.MATH),
]


def testing():
    agent1 = Timetable(classrooms, courses)
    timetable_data1 = [
    [[4, 0, 4, False], [0, 0, 4, False], [2, 0, 1, False], [0, 0, 5, False], [1, 0, 0, False], [4, 0, 3, False], [2, 0, 0, False], [0, 0, 3, False]],
    [[4, 0, 2, True], [4, 0, 0, True], [4, 0, 1, True], [3, 0, 0, False], [0, 0, 7, False], [0, 0, 6, False], [3, 0, 1, False]],
    [[2, 3, 6, False], [2, 3, 5, False], [2, 3, 7, False], [1, 1, 1, False], [1, 1, 0, False], [2, 3, 4, False], [3, 4, 2, False], [0, 4, 0, False]],
    [[1, 3, 6, True], [1, 3, 7, True], [1, 3, 5, True], [2, 1, 4, False], [2, 1, 5, False], [2, 1, 6, False], [0, 2, 3, False], [0, 2, 2, False], [3, 3, 6, False]],
    [[0, 3, 6, False], [0, 3, 5, False], [4, 2, 2, False], [1, 3, 0, False], [0, 3, 7, False], [4, 2, 3, False]],
    [[2, 0, 3, False], [0, 3, 0, False], [2, 0, 4, False], [0, 3, 1, False], [1, 0, 2, False], [2, 0, 5, False]],
    [[2, 4, 7, False], [4, 4, 4, False], [2, 4, 5, False], [4, 4, 3, False], [1, 3, 3, False], [2, 4, 6, False]],
    [[4, 2, 7, False], [1, 4, 2, False], [1, 4, 3, False], [1, 4, 4, False]],
    [[1, 2, 2, False], [4, 1, 7, False], [4, 1, 6, False], [4, 1, 5, False]],
    [[3, 0, 5, False], [3, 0, 6, False]],
    [[1, 1, 6, False], [1, 1, 7, False], [1, 1, 5, False], [3, 1, 0, False]],
    [[3, 2, 4, False], [1, 0, 6, False], [1, 0, 7, False], [3, 2, 6, False], [3, 2, 5, False], [4, 0, 7, False]],
    [[1, 4, 6, False], [1, 4, 5, False], [4, 3, 1, False], [3, 4, 4, False], [1, 4, 7, False], [4, 3, 2, False]],
    [[0, 4, 5, False], [3, 3, 5, False], [0, 4, 6, False], [3, 3, 4, False], [4, 4, 0, False], [0, 4, 4, False]],
    [[1, 0, 3, False], [2, 2, 0, False], [2, 2, 1, False], [0, 0, 0, False], [2, 2, 2, False], [1, 0, 4, False], [0, 0, 1, False], [3, 2, 3, False]],
    [[4, 1, 2, False], [3, 1, 5, False], [3, 1, 6, False], [3, 1, 7, False]],
    [[0, 1, 1, True], [0, 1, 2, True], [0, 1, 3, True], [2, 4, 1, False], [2, 4, 3, False], [2, 4, 2, False], [1, 3, 4, False]],
    [[0, 4, 2, False], [0, 4, 1, False], [0, 4, 3, False], [2, 0, 2, False]],
    [[4, 3, 4, False], [4, 3, 3, False], [3, 2, 2, False], [2, 4, 0, False], [3, 2, 1, False], [3, 2, 0, False]],
    [[0, 3, 3, True], [0, 3, 4, True], [0, 3, 2, True], [4, 0, 6, False], [1, 2, 6, False], [4, 0, 5, False], [1, 2, 5, False], [1, 2, 7, False], [2, 3, 3, False]],
    [[4, 3, 5, True], [4, 3, 7, True], [4, 3, 6, True], [3, 3, 1, False], [3, 3, 3, False], [0, 2, 7, False], [3, 3, 2, False], [0, 2, 6, False], [1, 2, 4, False]]
]


    agent1.set_timetable(timetable_data1)
    GA.fitness(agent1)
    print(agent1.display_as_table())

# if __name__ == "__main__":
#     testing()

if __name__ == "__main__":
    import time

    agents = [Timetable(classrooms, courses) for _ in range(50)]

    start_time = time.time()
    result, fitness = GA.run(agents, generations=10000, mutation_rate=0.9, k=20, m=20)
    end_time = time.time()

    print(result.display_as_table())
    GA.fitness(result)
    print(f"Execution time: {end_time - start_time} seconds")