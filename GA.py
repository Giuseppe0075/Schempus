import copy
import random as rd
from Env import Timetable

def run(agents, generations=100, mutation_rate=0.4, k=4, m=2):
    n_agents = len(agents)
    best_agent = agents[0]
    best_fit = fitness(agents[0])
    best_fitness_values = []

    for i in range(generations):
        print(f"{int(i/generations * 100)}%")
        # Select agents
        agents, fits = selection(agents, k, m)

        # Find the best agent
        for agent, fit in zip(agents, fits):
            if fit < best_fit:
                best_agent = copy.deepcopy(agent)
                best_fit = copy.deepcopy(fit)
                with open("best_agent.txt", "w") as f:
                    f.write(str(best_fit) + "\n")
                    f.write(best_agent.display_as_table())
                    f.write("\n" + str(best_agent))

        best_fitness_values.append(best_fit)

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
                mutation(agent, number_of_mutations=rd.randint(1, 5))

        agents = new_agents

    # Normalize the fitness values
    normalized_fitness_values = [(fit - 0) / (5000 - 0) for fit in best_fitness_values]

    return  best_agent, best_fit,normalized_fitness_values

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

    #select m agents
    for _ in range(m):
        #select k agents at random
        selected_agents = []
        selected_agents_fits = []
        available_indices = list(range(len(agents)))

        #select k agents at random
        for _ in range(k) :
            i = rd.choice(available_indices)
            available_indices.remove(i)
            selected_agents.append(agents[i])
            selected_agents_fits.append(fits[i])

        #select the agent with the minimum fitness
        selected_agent = selected_agents[selected_agents_fits.index(min(selected_agents_fits))]
        winners.append(selected_agent)
        winners_fits.append(selected_agents_fits[selected_agents.index(selected_agent)])

    return winners, winners_fits

def fitness(agent: Timetable):
    #calculate the fitness of the agent
    conflicts_weight = 10
    collisions_weight = 10
    capacity_weight = 1.5
    distribution_weight = 3.1
    distribution_in_day_weight = 5

    #There should not be more lessons in the same classroom at the same time
    def count_collisions():
        collisions = 0
        lessons = [lesson for course in agent.timetable for lesson in course]
        for lesson in lessons :
            if lessons.count(lesson) > 1 :
                collisions += 1
        return collisions

    #A Professor should not have two different lessons at the same time
    def count_professor_conflicts():
        conflicts = 0
        professors = set([course.professor for course in agent.courses])
        for professor in professors:
            lessons = [lesson for course in agent.timetable for lesson in course if agent.courses[agent.timetable.index(course)].professor == professor]
            for day in range(5):
                for hour in range(8):
                    lessons_in_hour = [lesson for lesson in lessons if lesson[2] == hour and lesson[0] == day]
                    classes = set([lesson[1] for lesson in lessons_in_hour])
                    if len(classes) > 1:
                        conflicts += len(classes) - 1

        return conflicts

    #The number of students in a classroom should not exceed its capacity
    def capacity_error():
        total_error = 0
        course_objects = agent.courses
        classrooms = agent.classrooms
        courses = agent.timetable
        for course in courses:
            course_index = courses.index(course)
            course_students = course_objects[course_index].number_of_students
            for lesson in course:
                class_capacity = classrooms[lesson[1]].capacity
                error = course_students - class_capacity
                if error < 0: error = 0
                total_error += error

        return total_error

    #Each course should follow a preferred number of hours per day
    def check_week_distribution():
        total_error = 0
        courses_object = agent.courses
        courses = agent.timetable
        for course in courses:
            course_index = courses.index(course)
            hours_goal = courses_object[course_index].preferred_hours_a_day
            for day in range(5):
                lessons = [lesson for lesson in course if lesson[0] == day]
                if len(lessons) == 0:
                    continue
                hours = len(lessons)
                total_error += abs(hours - hours_goal)
        return total_error

    #It is preferred that a course have consecutive hours in the same classroom
    def check_day_distribution():
        total_error = 0
        for day in range(5) :
            for course in agent.timetable :
                hours = set(lesson[2] for lesson in course if lesson[0] == day)
                if hours :
                    total_error += max(hours) - min(hours) - len(hours) + 1
                classes = set(lesson[1] for lesson in course if lesson[0] == day)
                if classes :
                    total_error += len(classes) - 1

        return total_error

    fit_collisions = count_collisions() * collisions_weight
    fit_professor_conflicts = count_professor_conflicts() * conflicts_weight
    fit_capacity = capacity_error() * capacity_weight
    fit_hours_per_day = check_week_distribution() * distribution_weight
    fit_distribution_in_day = check_day_distribution() * distribution_in_day_weight

    fit = fit_collisions + fit_professor_conflicts + fit_capacity + fit_hours_per_day + fit_distribution_in_day
            #print(f"fit: {fit} <- collisions: {fit_collisions}, professor conflicts: {fit_professor_conflicts}, capacity: {fit_capacity}, hours per day: {fit_hours_per_day}, distribution in day: {fit_distribution_in_day}")
    return fit