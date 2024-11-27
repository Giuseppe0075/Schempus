from Env import Timetable, Course, Classroom
import random as rd

def mutation(agent: Timetable, number_of_mutations=1):
    for _ in range(number_of_mutations):
        # Select a random day and classroom
        day1 = rd.randint(0, 4)
        classroom1 = rd.randint(0, len(agent.classrooms) - 1)
        hour1 = rd.randint(0, 7)

        day2 = rd.randint(0, 4)
        classroom2 = rd.randint(0, len(agent.classrooms) - 1)
        hour2 = rd.randint(0, 7)

        # Swap the lessons
        agent.timetable[day1][classroom1].hours[hour1], agent.timetable[day2][classroom2].hours[hour2] = \
            agent.timetable[day2][classroom2].hours[hour2], agent.timetable[day1][classroom1].hours[hour1]
        print(f"Swapped {day1+1} {classroom1+1} {hour1+1} with {day2+1} {classroom2+1} {hour2+1}")

def crossover():
    pass

def selection():
    pass

def fitness():
    pass
