import os
import time
from collections import defaultdict
from multiprocessing import Process, Queue, cpu_count

from args import args
from utils import chunks_indexes_by_number_of_chunks, is_text_file


def search_in_files(files, keyword, queue):
    local_results = defaultdict(list)

    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                if keyword in f.read():
                    local_results[keyword].append(file)
        except Exception as e:
            print(f"Error processing file {file}: {e}")

    queue.put(local_results)


def main():
    files = [os.path.join(root, f) for root, _, filenames in os.walk(args.directory) for f in filenames if
             is_text_file(os.path.join(root, f))]

    n_processes = cpu_count() or 4
    indexes = chunks_indexes_by_number_of_chunks(len(files), n_processes)

    queue = Queue()
    processes = []

    start_time = time.time()

    for chunk in indexes:
        process_files = [files[i] for i in chunk]
        process = Process(target=search_in_files, args=(process_files, args.keyword, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    results = defaultdict(list)
    while not queue.empty():
        local_results = queue.get()
        for key, value in local_results.items():
            results[key].extend(value)

    end_time = time.time()

    print(f"results: {dict(results)}")
    print(f"execution time: {end_time - start_time:.5f} seconds")


if __name__ == "__main__":
    main()
