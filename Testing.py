import os
import multiprocessing
import matplotlib.pyplot as plt
from Env import Timetable, Course, Classroom
import GA

# Define courses and classrooms
courses = [
    Course("ETC", "di nucci", 200, 8),
    Course("Math", "smith", 190, 6, 3),
    Course("Physics", "johnson", 75, 8),
    Course("Physics", "di nucci", 150, 8),
    Course("Physics", "smith", 75, 8),
    Course("Programming", "johnson", 75, 9, 3),
    Course("Chemistry", "lee", 100, 7),
    Course("Biology", "kim", 120, 6),
    Course("History", "brown", 80, 5),
    Course("Geography", "davis", 90, 4),
    Course("Art", "miller", 60, 3),
    Course("Music", "wilson", 50, 2),
    Course("Philosophy", "adams", 60, 3),
    Course("Economics", "clark", 80, 5),
    Course("Literature", "evans", 70, 4),
    Course("Sociology", "martin", 85, 6),
    Course("Psychology", "robinson", 90, 7),
    Course("Anthropology", "walker", 65, 4),
    Course("Political Science", "young", 75, 5),
    Course("Linguistics", "allen", 55, 3),
    Course("Astronomy", "taylor", 85, 6),
    Course("Statistics", "moore", 95, 5),
    Course("Computer Science", "thompson", 100, 7)
]

classrooms = [
    Classroom("p1", 200),
    Classroom("p2", 75),
    Classroom("p3", 100),
    Classroom("p4", 150),
    Classroom("p5", 90)
]

# Create plots directory if it doesn't exist
if not os.path.exists('plots'):
    os.makedirs('plots')

# Function to run the GA and save the results
def run_ga_test(process_id,results, statistics_list,  _generations, mutation_rate, k, m):
    agents = [Timetable(classrooms, courses) for _ in range(50)]
    result, fitness, statistics = GA.run(agents, generations=_generations, mutation_rate=mutation_rate, k=k, m=m)
    results[process_id] = fitness
    statistics_list[process_id] = statistics

if __name__ == '__main__':
    # Number of tests to run
    num_tests = 15
    num_processes = 10
    manager = multiprocessing.Manager()
    results = manager.list([None] * num_processes)
    statistics_list = manager.list([None] * num_processes)

    # Clear the results file
    with open('results.txt', 'w'):
        pass

    for j in range(1, num_tests + 1):
        processes = []
        generations = 200 * j
        # Create and start processes
        for i in range(num_processes):
            process = multiprocessing.Process(target=run_ga_test, args=(i,results,statistics_list, generations, 0.7, 20, 20))
            processes.append(process)
            process.start()

        # Wait for all processes to complete
        for process in processes:
            process.join()

        print(f"Test {j} completed")

        # Plot the learning curves for all threads
        for stats in statistics_list:
            if stats is not None:
                plt.plot(stats)
        plt.xlabel('Generation')
        plt.ylabel('Normalized Best Fitness')
        plt.title(f'Learning Curve of the Genetic Algorithm (Test {j})')
        plt.grid(True)
        plt.xlim(0, generations-1)
        plt.ylim(0, 1)
        plt.savefig(f'plots/learning_curve_test_{j}.png')
        plt.close()

        # Save results for statistical analysis
        with open('results.txt', 'a') as f:
            valid_results = [r for r in results if r is not None]
            if valid_results:
                mean = sum(valid_results) / len(valid_results)
                f.write(f"Test {j}: {mean}\n")

        results = manager.list([None] * num_processes)
        statistics_list = manager.list([None] * num_processes)