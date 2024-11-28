import copy

from Env import Timetable
import random as rd

def run(agents, generations=100, mutation_rate=0.4, k=4, m=2):
    n_agents = len(agents)
    fits = []
    best_agent = agents[0]
    best_fit = fitness(agents[0])
    while best_fit > 0:
        # Select agents
        agents, fits = selection(agents, k, m)

        # Find the best agent
        for agent, fit in zip(agents, fits):
            if fit < best_fit:
                best_agent = copy.deepcopy(agent)
                best_fit = copy.deepcopy(fit)

        # Crossover
        new_agents = []
        while len(new_agents) < n_agents:
            agent1 = rd.choice(agents)
            agent2 = rd.choice(agents)
            child1, child2 = crossover(agent1, agent2)
            new_agents.append(child1)
            if len(new_agents) < n_agents:
                new_agents.append(child2)

        # Mutation
        for agent in new_agents:
            if rd.random() < mutation_rate:
                mutation(agent)

        agents = new_agents

    return best_agent, best_fit

def mutation(agent: Timetable, number_of_mutations=1):
    for _ in range(number_of_mutations):
        course_index = rd.randint(0, len(agent.timetable) - 1)
        lesson_index = rd.randint(0, len(agent.timetable[course_index]) - 1)
        new_lesson = [rd.randint(0,4), rd.randint(0,len(agent.classrooms) - 1), rd.randint(0, 7)]
        agent.timetable[course_index][lesson_index] = new_lesson

def crossover(agent1: Timetable, agent2: Timetable):
    # Create deep copies of the agents to avoid modifying the original agents
    child1 = copy.deepcopy(agent1)
    child2 = copy.deepcopy(agent2)

    # For each course
    for i in range(len(child1.courses)) :
        # Select a random point
        point = rd.randint(0, len(child1.timetable[i]) - 1)
        # Swap the lessons after the point
        child1.timetable[i][point :], child2.timetable[i][point :] = copy.deepcopy(
            child2.timetable[i][point :]), copy.deepcopy(child1.timetable[i][point :])

    return child1, child2

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
        #select the best agent on a probability proportional to its fitness
        # total_fitness = sum(selected_agents_fits) + 1e-6
        # probabilities = [fit / total_fitness for fit in selected_agents_fits]
        # selected_agent = rd.choices(selected_agents, weights=probabilities, k=1)[0]
        selected_agent = selected_agents[selected_agents_fits.index(min(selected_agents_fits))]
        winners.append(selected_agent)
        winners_fits.append(selected_agents_fits[selected_agents.index(selected_agent)])
    return winners, winners_fits

def fitness(_agent: Timetable):
    #calculate the fitness of the agent
    fit = 0

    def count_collisions(agent):
        collisions = 0
        lessons = [lesson for course in agent.timetable for lesson in course]
        for lesson in lessons :
            if lessons.count(lesson) > 1 :
                collisions += 1
        return collisions

    #A Professor should not have two lessons at the same time
    def count_professor_conflicts(agent):
        pass


    def check_capacity(agent):
        pass

    def check_distribution(agent):
        pass

    n_collisions = count_collisions(_agent)
    fit = n_collisions * 100
    print(f"fit: {fit} <- collisions: {n_collisions}")
    return fit