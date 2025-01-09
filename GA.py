import copy
import random as rd
from collections import Counter
from Env import Timetable
import pickle

NUMBER_OF_DAYS = 5
NUMBER_OF_HOURS = 8
NUMBER_OF_CLASSES = 0

def run(
    agents,
    generations=100,
    mutation_rate=0.9,
    k=20,
    m=20,
    elitism = 7,
    update_callback=None,
    stop_check=None
):
    n_agents = len(agents)
    best_agent = agents[0]
    best_fit = fitness(agents[0])
    best_agents = []
    best_fits = []
    global NUMBER_OF_CLASSES
    NUMBER_OF_CLASSES = len(agents[0].classrooms)

    for i in range(1, generations + 1):

        # print(f"Generation {i}/{generations}")

        # Early stop if needed:
        if stop_check and stop_check():
            return best_agent, best_fit

        # Selection
        agents, fits = selection(agents, k, m)

        # Find the best agent
        if fits[0] < best_fit:
            best_agent = copy.deepcopy(agents[0])
            best_fit = fits[0]
            # When you find a new best_agent
            with open("best_agent.pkl", "wb") as f:
                pickle.dump(best_agent, f)
            with open("best_agent.txt", "w") as f:
                f.write(str(best_agent))
            if best_fit == 0:
                if update_callback:
                    update_callback(i, generations, best_fit)
                return best_agent, 0
        best_agents.append(best_agent)
        best_fits.append(best_fit)
        new_agents = []
        new_agents.extend(copy.deepcopy(agents[:elitism]))

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
        # Update progress after each generation
        if update_callback:
            update_callback(i, generations, best_fit)

    return best_agent, best_fit# , best_fits

def mutation(agent: Timetable, day_mutation, class_mutation, hour_mutation):
    # Select a random lesson
    course_index = rd.randint(0, len(agent.timetable) - 1)
    lesson_index = rd.randint(0, len(agent.timetable[course_index]) - 1)
    old_lesson = agent.timetable[course_index][lesson_index]

    # Mutate the lesson
    new_lesson = [
        (old_lesson[0] + rd.randint(-day_mutation, day_mutation)) % NUMBER_OF_DAYS,
        (old_lesson[1] + rd.randint(-class_mutation, class_mutation)) % len(agent.classrooms),
        (old_lesson[2] + rd.randint(-hour_mutation, hour_mutation)) % NUMBER_OF_HOURS,
        old_lesson[3]
    ]

    # Check if there is already a lesson with the same day, classroom, and hour as the new lesson
    found = False
    for i in range(len(agent.timetable)):
        for j in range(len(agent.timetable[i])):
            lesson = agent.timetable[i][j]
            # Compare only day, classroom, and hour
            if (lesson[0] == new_lesson[0] and
                    lesson[1] == new_lesson[1] and
                    lesson[2] == new_lesson[2]):
                # If found, swap only the first 3 elements (day, classroom, hour)
                temp_coords = old_lesson[:3]  # Save [day, classroom, hour] of old_lesson

                # Update the original lesson with the first 3 elements of the found lesson
                agent.timetable[course_index][lesson_index][:3] = lesson[:3]

                # Update the found lesson with the first 3 elements of old_lesson
                agent.timetable[i][j][:3] = temp_coords

                found = True
                break
        if found:
            break

    # If no lesson with the same day, classroom, and hour is found,
    # replace old_lesson with new_lesson.
    if not found:
        agent.timetable[course_index][lesson_index] = new_lesson


def crossover(agent1: Timetable, agent2: Timetable):
    # Create deep copies of the agents to avoid modifying the originals
    child1 = copy.deepcopy(agent1)
    child2 = copy.deepcopy(agent2)

    # Swap courses from a random index
    for i in range(rd.randint(0,len(child1.timetable)),len(child1.timetable)):
        for j in range(len(child1.timetable[i])):
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
    # Sort the winners by fitness
    winners, winners_fits = zip(*sorted(zip(winners, winners_fits), key=lambda x: x[1]))
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
    collisions_weight = 60
    conflicts_weight = 60
    capacity_weight = 1
    week_distribution_weight = 30
    distribution_in_day_weight = 10
    lab_allocation_weight = 71

    # Total lessons
    all_courses = agent.timetable

    # -------------------------------------------------------------------
    # 1. Count collisions (same classroom and same hour)
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
                else:
                    total_error -= error/100
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

            # Theory should have 2 hours per day
            for day in days_for_theory:
                theory_hours = [l for l in theory_lessons if l[0] == day]
                total_error += abs(len(theory_hours) - 2)

            # Lab should have 3 hours per day
            for day in days_for_lab:
                lab_hours = [l for l in lab_lessons if l[0] == day]
                total_error += abs(len(lab_hours) - 3)

            # Lab and theory should not be on the same day
            for day in range(NUMBER_OF_DAYS):
                theory_hours = [l for l in theory_lessons if l[0] == day]
                lab_hours = [l for l in lab_lessons if l[0] == day]
                if theory_hours and lab_hours:
                    # penalize overlap in the day
                    total_error += len(theory_hours) + len(lab_hours)

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
                    total_error += (len(classes_in_day) - 1) * 5

        return total_error

    # -------------------------------------------------------------------
    # 6. Lab allocation
    #    - Lab should be allocated to the correct classroom
    # -------------------------------------------------------------------
    def check_lab_allocation():
        total_error = 0
        for i, course in enumerate(all_courses):
            lab_lessons = [l for l in course if l[3]]       # l[3] == True => Lab
            theory_lessons = [l for l in course if not l[3]]
            for lesson in theory_lessons:
                if agent.classrooms[lesson[1]].is_lab:
                    total_error += 1
            for lesson in lab_lessons:
                if not agent.classrooms[lesson[1]].is_lab or agent.classrooms[lesson[1]].subject != agent.courses[i].subject:
                    total_error += 1
        return total_error

    # Calculate individual contributions
    fit_collisions = count_collisions() * collisions_weight
    fit_prof_conf = count_professor_conflicts() * conflicts_weight
    fit_capacity = capacity_error() * capacity_weight
    fit_week_dist = check_week_distribution() * week_distribution_weight
    fit_day_dist = check_day_distribution() * distribution_in_day_weight
    fit_lab_alloc = check_lab_allocation() * lab_allocation_weight

    # Total fitness
    total_fit = (
        fit_collisions +
        fit_prof_conf +
        fit_capacity +
        fit_week_dist +
        fit_day_dist +
        fit_lab_alloc
    )
    print(f"fit: {total_fit} <- collisions: {fit_collisions}, professor conflicts: {fit_prof_conf}, capacity: {fit_capacity}, week distribution: {fit_week_dist}, day distribution: {fit_day_dist}, lab allocation: {fit_lab_alloc}")
    return total_fit