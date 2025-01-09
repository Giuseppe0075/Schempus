import multiprocessing
import matplotlib.pyplot as plt
from Env import Timetable, Course, Classroom, Professor, Subjects
import GA

# Example first semester UNISA 2024/25
professors = {
    "ZIZZA": Professor("ZIZZA"),
    "D'ANGELO": Professor("D'ANGELO"),
    "NICOTERA": Professor("NICOTERA"),
    "TUCCI": Professor("TUCCI"),
    "DE MARCO": Professor("DE MARCO"),
    "LAPENTA": Professor("LAPENTA"),
    "TOTA": Professor("TOTA"),
    "NAPPI": Professor("NAPPI"),
    "CASTIGLIONE": Professor("CASTIGLIONE"),
    "MASUCCI": Professor("MASUCCI"),
    "VINCENZI": Professor("VINCENZI"),
    "NARDUCCI": Professor("NARDUCCI"),
    "RESCIGNO": Professor("RESCIGNO"),
    "LA TORRE": Professor("LA TORRE"),
    "TORTORA": Professor("TORTORA"),
    "CARPENTIERI": Professor("CARPENTIERI"),
    "FICCO": Professor("FICCO"),
    "POLESE": Professor("POLESE"),
    "CATTANEO": Professor("CATTANEO"),
    "DEUFEMIA": Professor("DEUFEMIA"),
    "SEBILLO": Professor("SEBILLO"),
    "DE LUCIA": Professor("DE LUCIA"),
    "SCARANO": Professor("SCARANO"),
    "FERRUCCI": Professor("FERRUCCI"),
    "MALANDRINO": Professor("MALANDRINO"),
    "GRAVINO": Professor("GRAVINO"),
    "COSENZA": Professor("COSENZA"),
    "DE BONIS": Professor("DE BONIS"),
    "PALOMBA": Professor("PALOMBA"),
    "DE PRISCO": Professor("DE PRISCO"),
    "ROMEO": Professor("ROMEO"),
}
courses = [
    Course("Programmazione I (A-C)", professors["ZIZZA"], 200, 7, Subjects.COMPUTER_SCIENCE, 3),
    Course("Matematica Discreta (A-C)", professors["NICOTERA"], 200, 6, Subjects.MATH),
    Course("Architettura degli Elaboratori (A-C)", professors["D'ANGELO"], 200, 6, Subjects.COMPUTER_SCIENCE),
    Course("Programmazione I (D-G)", professors["TUCCI"], 200, 7, Subjects.COMPUTER_SCIENCE, 3),
    Course("Matematica Discreta (D-G)", professors["LAPENTA"], 200, 6, Subjects.MATH),
    Course("Architettura degli Elaboratori (D-G)", professors["DE MARCO"], 200, 6, Subjects.COMPUTER_SCIENCE),
    Course("Programmazione I (H-PET)", professors["NAPPI"], 200, 7, Subjects.COMPUTER_SCIENCE, 3),
    Course("Matematica Discreta (H-PET)", professors["TOTA"], 200, 6, Subjects.MATH),
    Course("Architettura degli Elaboratori (H-PET)", professors["CASTIGLIONE"], 200, 6, Subjects.COMPUTER_SCIENCE),
    Course("Programmazione I (PEU-Z)", professors["NARDUCCI"], 200, 7, Subjects.COMPUTER_SCIENCE, 3),
    Course("Matematica Discreta (PEU-Z)", professors["VINCENZI"], 200, 6, Subjects.MATH),
    Course("Architettura degli Elaboratori (PEU-Z)", professors["RESCIGNO"], 200, 6, Subjects.COMPUTER_SCIENCE),
    Course("Sistemi Operativi (Resto 0)", professors["LA TORRE"], 160, 7, Subjects.COMPUTER_SCIENCE, 3),
    Course("Programmazione Object Oriented (Resto 0)", professors["TORTORA"], 160, 7, Subjects.COMPUTER_SCIENCE, 3),
    Course("Basi di Dati (Resto 0)", professors["CARPENTIERI"], 160, 7, Subjects.COMPUTER_SCIENCE, 3),
    Course("Sistemi Operativi (Resto 1)", professors["FICCO"], 160, 7, Subjects.COMPUTER_SCIENCE, 3),
    Course("Programmazione Object Oriented (Resto 1)", professors["POLESE"], 160, 7, Subjects.COMPUTER_SCIENCE, 3),
    Course("Basi di Dati (Resto 1)", professors["CATTANEO"], 160, 7, Subjects.COMPUTER_SCIENCE, 3),
    Course("Sistemi Operativi (Resto 2)", professors["DEUFEMIA"], 160, 7, Subjects.COMPUTER_SCIENCE, 3),
    Course("Programmazione Object Oriented (Resto 2)", professors["SEBILLO"], 160, 7, Subjects.COMPUTER_SCIENCE, 3),
    Course("Basi di Dati (Resto 2)", professors["SEBILLO"], 160, 7, Subjects.COMPUTER_SCIENCE, 3),
    Course("Ingegneria del Software (Resto 0)", professors["DE LUCIA"], 150, 7, Subjects.COMPUTER_SCIENCE, 3),
    Course("Programmazione Distribuita (Resto 0)", professors["SCARANO"], 150, 7, Subjects.COMPUTER_SCIENCE, 3),
    Course("Ingegneria del Software (Resto 1)", professors["FERRUCCI"], 150, 7, Subjects.COMPUTER_SCIENCE, 3),
    Course("Programmazione Distribuita (Resto 1)", professors["MALANDRINO"], 150, 7, Subjects.COMPUTER_SCIENCE, 3),
    Course("Ingegneria del Software (Resto 2)", professors["GRAVINO"], 150, 6, Subjects.COMPUTER_SCIENCE),
    Course("Programmazione Distribuita (Resto 2)", professors["COSENZA"], 150, 7, Subjects.COMPUTER_SCIENCE, 3),
    Course("Fondamenti di Intelligenza Artificiale", professors["PALOMBA"], 180, 4, Subjects.COMPUTER_SCIENCE),
    Course("Programmazione Avanzata", professors["DE BONIS"], 20, 4, Subjects.COMPUTER_SCIENCE),
    Course("Machine Learning", professors["POLESE"],60, 4, Subjects.COMPUTER_SCIENCE),
    Course("Mobile Programming",professors["DE PRISCO"], 90, 4, Subjects.COMPUTER_SCIENCE),
    Course("Musimatica", professors["DE PRISCO"], 90, 4, Subjects.COMPUTER_SCIENCE),
    Course("Fisica", professors["ROMEO"], 40, 4, Subjects.PHYSICS),
]
classrooms = [
    Classroom("P3", 200),
    Classroom("P4", 200),
    Classroom("F8", 200),
    Classroom("F1", 200),
    Classroom("F4", 150),
    Classroom("P6", 100),
    Classroom("P13", 200, True, Subjects.COMPUTER_SCIENCE),
    Classroom("Hopper", 200, True, Subjects.COMPUTER_SCIENCE),
    Classroom("Sammet", 200, True, Subjects.COMPUTER_SCIENCE),
]
# End Example

STRING = "k-m"

def run_ga_test(_generations, mutation_rate, k, m):
    agents = [Timetable(classrooms, courses) for _ in range(100)]
    result, fitness, statistics = GA.run(agents,
                                         generations=_generations,
                                         mutation_rate=mutation_rate,
                                         k=k, m=m,
                                         )
    # Restituisco i due valori: fitness e l'array delle statistiche
    return fitness, statistics

if __name__ == '__main__':
    # Numero di test
    num_tests = 10
    # Numero di processi TOT da lanciare per ogni test
    num_processes = 10
    # Numero di processi massimi in parallelo
    max_workers = 10
    # Numero di generazioni
    generations = 3000

    # Pulisco il file dei risultati
    with open('Testing_KandM/results.txt', 'w'):
        pass

    # Creo la pool con concurrency limitata a max_workers
    pool = multiprocessing.Pool(processes=max_workers)

    for j in range(10, (num_tests + 1) * 10, 10):
        # Invio i job alla pool e mi salvo i riferimenti
        async_results = []
        for i in range(num_processes):
            async_results.append(
                pool.apply_async(
                    run_ga_test,
                    args=(generations, 0.9,j, j)
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
        plt.ylabel('Best Fitness')
        plt.title(f'{STRING}: {j}')
        plt.grid(True)
        plt.xlim(0, generations-1)
        plt.ylim(0, 10000)
        plt.savefig(f'Testing_KandM/{STRING}_{j}.png')
        plt.close()

        # Calcolo e salvo la media dei fitness
        valid_results = [r for r in results if r is not None]
        if valid_results:
            mean_value = sum(valid_results) / len(valid_results)
            with open('Testing_KandM/results.txt', 'a') as f:
                f.write(f"Mean {STRING} ({j}): {mean_value}\n")

    # Chiudo la pool
    pool.close()
    pool.join()
