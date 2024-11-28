from Env import Timetable
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

def crossover(agent1: Timetable, agent2: Timetable):
    #for each course
    for i in range(len(agent1.courses)):
        #select a random point
        point = rd.randint(0, len(agent1.timetable[i]) - 1)

        #swap the lessons after the point
        agent1.timetable[i][point :], agent2.timetable[i][point :] = agent2.timetable[i][point :], agent1.timetable[i][point :]

#Selection with k-way tournament
def selection(agents: list, k, m):
    if len(agents) < k:
        raise ValueError("The number of agents must be greater than k")
    if len(agents) < m:
        raise ValueError("The number of agents must be greater than m")

    #calculate the fitness of each agent
    fits = []
    for agent in agents:
        fits.append(fitness(agent))

    #select m agents
    winners = []
    winners_fits = []
    for _ in range(m):
        #select k agents at random
        selected_agents = []
        selected_agents_fits = []
        available_indices = list(range(len(agents)))
        for _ in range(k) :
            i = rd.choice(available_indices)
            available_indices.remove(i)
            selected_agents.append(agents[i])
            selected_agents_fits.append(fits[i])
        #select the best agent
        max_fitness = max(selected_agents_fits)
        winners.append(selected_agents[selected_agents_fits.index(max_fitness)])
        winners_fits.append(max_fitness)

    return winners, winners_fits

def fitness(_agent: Timetable):
    #calculate the fitness of the agent
    fit = 0

    def count_collisions(agent):
        collisions = 0
        for course in agent.timetable:
            for lesson in course:
                if course.count(lesson) > 1:
                    collisions += 1
        return collisions

    def count_professor_conflicts(agent):
        pass

    def check_capacity(agent):
        pass

    def check_distribution(agent):
        pass

    fit -= count_collisions(_agent) * 100
    return fit