import multiprocessing
import matplotlib.pyplot as plt
from Env import Timetable, Course, Classroom, Professor, Subjects
import GA

professors = [
    Professor("di nucci"),
    Professor("smith"),
    Professor("johnson"),
    Professor("lee"),
    Professor("kim"),
]

# Define courses and classrooms
courses = [
Course("ETC", professors[0], 200, 8, Subjects.COMPUTER_SCIENCE),
Course("Math", professors[1], 190, 7, Subjects.MATH, 3),
Course("Physics", professors[2], 75, 8, Subjects.PHYSICS),
Course("Programming", professors[3], 75, 9, Subjects.COMPUTER_SCIENCE, 3),
Course("Chemistry", professors[4], 100, 6, Subjects.CHEMISTRY),
Course("Biology", professors[0], 120, 6, Subjects.BIOLOGY),
Course("History", professors[1], 80, 6, Subjects.HISTORY),
Course("Geography", professors[2], 90, 4, Subjects.GEOGRAPHY),
Course("Art", professors[3], 60, 4, Subjects.ART),
Course("Music", professors[4], 50, 2, Subjects.MUSIC),
Course("Philosophy", professors[0], 60, 4, Subjects.PHILOSOPHY),
Course("Economics", professors[1], 80, 6, Subjects.ECONOMICS),
Course("Literature", professors[2], 70, 6, Subjects.LITERATURE),
Course("Sociology", professors[3], 85, 6, Subjects.SOCIOLOGY),
Course("Psychology", professors[4], 90, 8, Subjects.PSYCHOLOGY),
Course("Anthropology", professors[0], 65, 4, Subjects.ANTHROPOLOGY),
Course("Political Science", professors[1], 75, 7, Subjects.POLITICAL_SCIENCE, 3),
Course("Linguistics", professors[2], 55, 4, Subjects.LINGUISTICS),
Course("Astronomy", professors[3], 85, 6, Subjects.ASTRONOMY),
Course("Statistics", professors[4], 95, 9, Subjects.STATISTICS, 3),
Course("Programming 1", professors[0], 100, 9, Subjects.COMPUTER_SCIENCE, 3),
]

classrooms = [
    Classroom("p1", 200),
    Classroom("p2", 75),
    Classroom("p3", 100),
    Classroom("p4", 150),
    Classroom("p5", 90),
    Classroom("labCS", 200, True, Subjects.COMPUTER_SCIENCE),
    Classroom("labS", 95, True, Subjects.STATISTICS),
    Classroom("labPS", 90, True, Subjects.POLITICAL_SCIENCE),
    Classroom("labM", 200, True, Subjects.MATH),
]

STRING = "Mutation +-"

def run_ga_test(_generations, mutation_rate, k, m):
    agents = [Timetable(classrooms, courses) for _ in range(50)]
    result, fitness, statistics = GA.run(agents, generations=_generations,
                                         mutation_rate=mutation_rate,
                                         k=k, m=m)
    # Restituisco i due valori: fitness e l'array delle statistiche
    return fitness, statistics

if __name__ == '__main__':
    # Numero di test
    num_tests = 1
    # Numero di processi TOT da lanciare per ogni test
    num_processes = 30
    # Numero di processi massimi in parallelo
    max_workers = 10

    # Pulisco il file dei risultati
    with open('results.txt', 'w'):
        pass

    # Creo la pool con concurrency limitata a max_workers
    pool = multiprocessing.Pool(processes=max_workers)

    for j in range(1, num_tests + 1):
        generations = 5000

        # Invio i job alla pool e mi salvo i riferimenti
        async_results = []
        for i in range(num_processes):
            async_results.append(
                pool.apply_async(
                    run_ga_test,
                    args=(generations, 0.9, 20, 20)
                )
            )

        # Ora aspetto che tutti i job finiscano
        # e raccolgo i risultati (fitness e statistics)
        results = []
        statistics_list = []
        for ar in async_results:
            fit, stats = ar.get()  # blocca finché non è pronto
            results.append(fit)
            statistics_list.append(stats)

        print(f"{STRING} ({j})")

        # Plotto le statistiche di tutti i processi
        for stats in statistics_list:
            if stats is not None:
                plt.plot(stats)

        plt.xlabel('Generation')
        plt.ylabel('Normalized Best Fitness')
        plt.title(f'{STRING}')
        plt.grid(True)
        plt.xlim(0, generations-1)
        plt.ylim(0, 1)
        plt.savefig(f'plots/{STRING}.png')
        plt.close()

        # Calcolo e salvo la media dei fitness
        valid_results = [r for r in results if r is not None]
        if valid_results:
            mean_value = sum(valid_results) / len(valid_results)
            with open('results.txt', 'a') as f:
                f.write(f"Mean {STRING}  generations: {mean_value}\n")

    # Chiudo la pool
    pool.close()
    pool.join()
