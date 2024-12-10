import os
import threading
import time
from collections import defaultdict

from args import args
from utils import chunks_indexes_by_number_of_chunks, is_text_file


def search_in_files(files, keyword, results, lock):
    for file in files:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                if keyword in f.read():
                    with lock:
                        results[keyword].append(file)
        except Exception as e:
            print(f"error processing file {file}: {e}")


def main():
    files = [os.path.join(root, f) for root, _, filenames in os.walk(args.directory) for f in filenames if
             is_text_file(os.path.join(root, f))]

    n_threads = os.cpu_count() or 4

    indexes = chunks_indexes_by_number_of_chunks(len(files), n_threads)

    results = defaultdict(list)
    threads = []
    lock = threading.Lock()

    start_time = time.time()

    for chunk in indexes:
        thread_files = [files[i] for i in chunk]
        thread = threading.Thread(target=search_in_files, args=(thread_files, args.keyword, results, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()

    print(f"results: {dict(results)}")
    print(f"execution time: {end_time - start_time:.5f} seconds")


if __name__ == "__main__":
    main()
