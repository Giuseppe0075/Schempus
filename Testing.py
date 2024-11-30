import threading
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

# Function to run the GA and save the results
def run_ga_test(thread_id, results, generations=500, mutation_rate=0.7, k=16, m=20):
    agents = [Timetable(classrooms, courses) for _ in range(33)]

    result, fitness, statistics = GA.run(agents, generations=generations, mutation_rate=mutation_rate, k=k, m=m)
    # Plot the learning curve
    plt.plot(statistics)
    plt.xlabel('Generation')
    plt.ylabel('Normalized Best Fitness')
    plt.title('Learning Curve of the Genetic Algorithm')
    plt.grid(True)
    plt.xlim(0, generations - 1)
    plt.ylim(0, 1)
    results[thread_id] = fitness

# Number of tests to run
num_tests = 10
num_threads = 10
threads = []
results = [None] * num_threads
with open("results.txt", "w"):
    pass

for j in range(1, num_tests+1):
    # Create and start threads
    for i in range(num_threads):
        thread = threading.Thread(target=run_ga_test, args=(i, results), kwargs={"generations": 1000, "mutation_rate": j/10, "k": 10, "m": 10})
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print(f"Test {j} completed")
    # Save the plot
    plt.savefig(f'plots/learning_curve_test_{j}.png')
    plt.close()

    # Save results for statistical analysis
    with open("results.txt", "a") as f:
        valid_results = [r for r in results if r is not None]
        if valid_results:
            mean = sum(valid_results) / len(valid_results)
            f.write(f"Test:{j}: {mean}\n")

    threads = []
    results = [None] * num_threads