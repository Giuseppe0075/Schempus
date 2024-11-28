from Env import Timetable, Course, Classroom
import random as rd

def mutation(agent: Timetable, number_of_mutations=1):
    for _ in range(number_of_mutations):
        course_index = rd.randint(0, len(agent.timetable) - 1)
        lesson_index = rd.randint(0, len(agent.timetable[course_index]) - 1)
        lesson = agent.timetable[course_index][lesson_index]
        new_lesson = [(lesson[0] + rd.randint(-1, 1))%5,
                      (lesson[1] + rd.randint(-1, 1))%len(agent.classrooms),
                      (lesson[2] + rd.randint(-1, 1))%8]
        agent.timetable[course_index][lesson_index] = new_lesson
        print(f"Mutation: {lesson} -> {new_lesson}")


def crossover(parent1: Timetable, parent2: Timetable):
    import copy
    child1 = copy.deepcopy(parent1)
    child2 = copy.deepcopy(parent2)

def selection():
    pass

def fitness():
    pass
