import os
import multiprocessing
import matplotlib.pyplot as plt
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
    Course("Math", professors[1], 190, 6, 3),
    Course("Physics", professors[2], 75, 8),
    Course("Programming", professors[3], 75, 9, 3),
    Course("Chemistry", professors[4], 100, 7),
    Course("Biology", professors[0], 120, 6),
    Course("History", professors[1], 80, 5),
    Course("Geography", professors[2], 90, 4),
    Course("Art", professors[3], 60, 3),
    Course("Music", professors[4], 50, 2),
    Course("Philosophy", professors[0], 60, 3),
    Course("Economics", professors[1], 80, 5),
    Course("Literature", professors[2], 70, 4),
    Course("Sociology", professors[3], 85, 6),
    Course("Psychology", professors[4], 90, 7),
    Course("Anthropology", professors[0], 65, 4),
    Course("Political Science", professors[1], 75, 5),
    Course("Linguistics", professors[2], 55, 3),
    Course("Astronomy", professors[3], 85, 6),
    Course("Statistics", professors[4], 95, 5),
    Course("Computer Science", professors[0], 100, 7),
]

classrooms = [
    Classroom("p1", 200),
    Classroom("p2", 75),
    Classroom("p3", 100),
    Classroom("p4", 150),
    Classroom("p5", 90)
]

# Create plots3 directory if it doesn't exist
if not os.path.exists('plots3'):
    os.makedirs('plots3')

# Function to run the GA and save the results
def run_ga_test(process_id,results, statistics_list,  _generations, mutation_rate, k, m):
    agents = [Timetable(classrooms, courses) for _ in range(50)]
    result, fitness, statistics = GA.run(agents, generations=_generations, mutation_rate=mutation_rate, k=k, m=m)
    results[process_id] = fitness
    statistics_list[process_id] = statistics

if __name__ == '__main__':
    # Number of tests to run
    num_tests = 10
    num_processes = 10
    manager = multiprocessing.Manager()
    results = manager.list([None] * num_processes)
    statistics_list = manager.list([None] * num_processes)

    # Clear the results file
    with open('results.txt', 'w'):
        pass

    for j in range(1, num_tests + 1):
        processes = []
        generations = 500
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
        plt.savefig(f'plots'
                    f'/learning_curve_test_{j}.png')
        plt.close()

        # Save results for statistical analysis
        with open('results.txt', 'a') as f:
            valid_results = [r for r in results if r is not None]
            if valid_results:
                mean = sum(valid_results) / len(valid_results)
                f.write(f"Test {j}: {mean}\n")

        results = manager.list([None] * num_processes)
        statistics_list = manager.list([None] * num_processes)