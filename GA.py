import copy
import random as rd
from collections import Counter
from Env import Timetable

NUMBER_OF_DAYS = 5
NUMBER_OF_HOURS = 8

def run(agents, generations=100, mutation_rate=0.9, k=20, m=20):
    n_agents = len(agents)
    best_agent = agents[0]
    best_fit = fitness(agents[0])
    best_fitness_values = []

    NUMBER_OF_CLASSES = len(agents[0].classrooms)

    for i in range(1, generations):
        # Selection
        agents, fits = selection(agents, k, m)

        # Find the best agent
        for agent, fit_val in zip(agents, fits):
            if fit_val < best_fit:
                best_agent = copy.deepcopy(agent)
                best_fit = fit_val
                # Save the best agent
                with open("best_agent.txt", "w") as f:
                    f.write(str(best_fit) + "\n")
                    f.write(best_agent.display_as_table())
                    f.write("\n" + str(best_agent))

        best_fitness_values.append(best_fit)
        new_agents = [best_agent]

        # Crossover
        while len(new_agents) < n_agents:
            agent1 = rd.choice(agents)
            agent2 = rd.choice(agents)
            child1, child2 = crossover(agent1, agent2)
            new_agents.append(child1)
            if len(new_agents) < n_agents:
                new_agents.append(child2)

        # Calculate mutation ranges based on generation progress
        day_mutation = NUMBER_OF_DAYS - int(NUMBER_OF_DAYS / (generations / i))
        class_mutation = NUMBER_OF_CLASSES - int(NUMBER_OF_CLASSES / (generations / i))
        hour_mutation = NUMBER_OF_HOURS - int(NUMBER_OF_HOURS / (generations / i))

        # Mutation
        for ag in new_agents:
            if rd.random() < mutation_rate:
                mutation(ag, day_mutation, class_mutation, hour_mutation)

        agents = new_agents

    # Normalize fitness values
    normalized_fitness_values = [(fit_val / 1000) for fit_val in best_fitness_values]

    return best_agent, best_fit / 1000, normalized_fitness_values


def mutation(agent: Timetable, day_mutation, class_mutation, hour_mutation, number_of_mutations=1):
    for _ in range(number_of_mutations):
        # Select a random lesson
        course_index = rd.randint(0, len(agent.timetable) - 1)
        lesson_index = rd.randint(0, len(agent.timetable[course_index]) - 1)
        old_lesson = agent.timetable[course_index][lesson_index]

        # Mutate the lesson
        new_lesson = [
            (old_lesson[0] + rd.randint(0, day_mutation)) % NUMBER_OF_DAYS,
            (old_lesson[1] + rd.randint(0, class_mutation)) % len(agent.classrooms),
            (old_lesson[2] + rd.randint(0, hour_mutation)) % NUMBER_OF_HOURS,
            old_lesson[3]
        ]
        agent.timetable[course_index][lesson_index] = new_lesson


def crossover(agent1: Timetable, agent2: Timetable):
    # Create deep copies of the agents to avoid modifying the originals
    child1 = copy.deepcopy(agent1)
    child2 = copy.deepcopy(agent2)

    # For each course
    for i in range(len(child1.courses)):
        # Select a random point
        point = rd.randint(0, len(child1.timetable[i]) - 1)
        # Swap lessons after the point, keeping the Lab field unchanged
        for j in range(point, len(child1.timetable[i])):
            c1_lesson = child1.timetable[i][j]
            c2_lesson = child2.timetable[i][j]
            child1.timetable[i][j] = [c2_lesson[0], c2_lesson[1], c2_lesson[2], c1_lesson[3]]
            child2.timetable[i][j] = [c1_lesson[0], c1_lesson[1], c1_lesson[2], c2_lesson[3]]

    return child1, child2


def selection(agents: list, k, m):
    """
    Selection with K-way tournament.
    k = number of agents competing in the tournament
    m = number of final winners
    """
    if len(agents) < k:
        raise ValueError("The number of agents must be greater than k")
    if len(agents) < m:
        raise ValueError("The number of agents must be greater than m")

    # Calculate the fitness of each agent
    fits = [fitness(ag) for ag in agents]

    winners = []
    winners_fits = []

    # Select m agents
    for _ in range(m):
        # Select k random agents
        selected_indices = rd.sample(range(len(agents)), k)
        selected_agents = [agents[idx] for idx in selected_indices]
        selected_fits = [fits[idx] for idx in selected_indices]

        # Determine the tournament winner (lowest fitness)
        min_fit = min(selected_fits)
        min_idx = selected_fits.index(min_fit)
        winners.append(selected_agents[min_idx])
        winners_fits.append(min_fit)

    return winners, winners_fits


def fitness(agent: Timetable):
    """
    Calculate the fitness of an agent based on:
    - collisions (same classroom/hour)
    - professor conflicts
    - classroom capacity
    - weekly distribution
    - daily distribution
    """
    conflicts_weight = 10
    collisions_weight = 10
    capacity_weight = 1.5
    week_distribution_weight = 5
    distribution_in_day_weight = 5

    # Total lessons
    all_courses = agent.timetable
    n_courses = len(all_courses)

    # -------------------------------------------------------------------
    # 1. Count collisions (same classroom and same hour)
    #    Using Counter, we avoid the O(n^2) of lessons.count(lesson)
    # -------------------------------------------------------------------
    def count_collisions():
        lessons = [tuple(lesson[0:3]) for course in all_courses for lesson in course]
        lesson_counter = Counter(lessons)
        # Each duplicate adds (count - 1) to the number of collisions
        return sum(cnt - 1 for cnt in lesson_counter.values() if cnt > 1)

    # -------------------------------------------------------------------
    # 2. Professor conflicts
    #    - A professor cannot teach multiple courses simultaneously
    #    - If the professor has free hours, they should not have lessons during those hours
    # -------------------------------------------------------------------
    def count_professor_conflicts():
        conflicts = 0
        # To speed up: use enumerate to link timetable and courses
        # professor_lessons[prof] = list of (day, hour) where they teach
        professor_lessons_map = {}

        for i, course in enumerate(all_courses):
            prof = agent.courses[i].professor
            if prof not in professor_lessons_map:
                professor_lessons_map[prof] = []
            # Add all (day, hour) for this course
            for lesson in course:
                professor_lessons_map[prof].append((lesson[0], lesson[2]))

        # Count time conflicts
        for prof, lesson_list in professor_lessons_map.items():
            day_hour_counter = Counter(lesson_list)
            # If there are 2 or more lessons in a (day, hour) => conflict
            conflicts += sum(cnt - 1 for cnt in day_hour_counter.values() if cnt > 1)

            # Count conflicts with free hours
            for free_hour in prof.free_hours:
                if free_hour in lesson_list:
                    conflicts += 1

        return conflicts

    # -------------------------------------------------------------------
    # 3. Classroom capacity should not be exceeded
    # -------------------------------------------------------------------
    def capacity_error():
        total_error = 0
        for i, course in enumerate(all_courses):
            course_students = agent.courses[i].number_of_students
            for lesson in course:
                class_capacity = agent.classrooms[lesson[1]].capacity
                error = course_students - class_capacity
                if error > 0:
                    total_error += error
        return total_error

    # -------------------------------------------------------------------
    # 4. Weekly distribution of Lab and Theory
    #    - Example constraints: 3 hours of lab or 2 hours of theory per day
    #    - No overlap of lab/theory on the same day
    # -------------------------------------------------------------------
    def check_week_distribution():
        total_error = 0
        for i, course in enumerate(all_courses):
            lab_lessons = [l for l in course if l[3]]       # l[3] == True => Lab
            theory_lessons = [l for l in course if not l[3]]

            days_for_lab = set(lab[0] for lab in lab_lessons)
            days_for_theory = set(thy[0] for thy in theory_lessons)

            # Count of hours vs number of dedicated days
            # Example: if lab_lessons = 6, 6/3 = 2 "blocks of 3 hours", days_for_lab = 2 => zero error
            total_error += abs((len(lab_lessons) / 3) - len(days_for_lab))
            total_error += abs((len(theory_lessons) / 2) - len(days_for_theory))

            # Lab and theory should not be on the same day
            for day in range(NUMBER_OF_DAYS):
                theory_hours = [l for l in theory_lessons if l[0] == day]
                lab_hours = [l for l in lab_lessons if l[0] == day]
                if theory_hours and lab_hours:
                    # penalize overlap in the day
                    total_error += min(len(theory_hours), len(lab_hours))

        return total_error

    # -------------------------------------------------------------------
    # 5. Daily distribution:
    #    - consecutive lessons and in the same classroom are preferred
    # -------------------------------------------------------------------
    def check_day_distribution():
        total_error = 0
        for day in range(NUMBER_OF_DAYS):
            for course in all_courses:
                # Hours this course is held on the day
                hours_in_day = set([lesson[2] for lesson in course if lesson[0] == day])
                if hours_in_day:
                    max_h = max(hours_in_day)
                    min_h = min(hours_in_day)
                    total_error += (max_h - min_h - len(hours_in_day) + 1)

                # Classrooms used for this course on the same day
                classes_in_day = set(lesson[1] for lesson in course if lesson[0] == day)
                if len(classes_in_day) > 1:
                    # penalize classroom change
                    total_error += len(classes_in_day) - 1

        return total_error

    # Calculate individual contributions
    fit_collisions = count_collisions() * collisions_weight
    fit_prof_conf = count_professor_conflicts() * conflicts_weight
    fit_capacity = capacity_error() * capacity_weight
    fit_week_dist = check_week_distribution() * week_distribution_weight
    fit_day_dist = check_day_distribution() * distribution_in_day_weight

    # Total fitness
    total_fit = (
        fit_collisions +
        fit_prof_conf +
        fit_capacity +
        fit_week_dist +
        fit_day_dist
    )
    print(f"fit: {total_fit} <- collisions: {fit_collisions}, professor conflicts: {fit_prof_conf}, capacity: {fit_capacity}, week distribution: {fit_week_dist}, day distribution: {fit_day_dist}")
    return total_fit