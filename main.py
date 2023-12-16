import zipfile
import itertools
from tqdm import tqdm
import os
import time


def brute_force_zip_password(zip_file_path, max_length=10):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    combinations_file = 'combinations.txt'

    with zipfile.ZipFile(zip_file_path, 'r') as archive:
        for length in range(1, max_length + 1):
            start_time = time.time()
            combinations = generate_combinations(characters, length, combinations_file)
            elapsed_time = time.time() - start_time
            print(f"Time to generate combinations for length {length}: {elapsed_time:.2f} seconds")

            for combination in combinations:
                password = ''.join(combination)
                try:
                    archive.extractall(pwd=password.encode('utf-8'))
                    print(f"Parola gasita: {password}")
                    return password
                except RuntimeError:
                    pass

    print("Nu s-a gasit nicio parola.")
    return None


def generate_combinations(characters, length, combinations_file):
    if length == 1:
        result = [char for char in characters]
    else:
        prev_combinations = read_combinations_file(combinations_file, length - 1)
        result = [char + prev_char for char in characters for prev_char in prev_combinations]

    write_combinations_file(combinations_file, length, result)
    print(result)
    return result


def read_combinations_file(combinations_file, length):
    if os.path.exists(combinations_file):
        with open(combinations_file, 'r') as file:
            lines = file.readlines()
            return [line.strip() for line in lines if len(line.strip()) == length]
    return []


def write_combinations_file(combinations_file, length, combinations):
    with open(combinations_file, 'w') as file:
        for combination in combinations:
            file.write(combination + '\n')


if __name__ == '__main__':
    zip_file_path = 'C:/Users/Dragos/Desktop/lucrupython/ArchiveCracker/Archive.zip'
    brute_force_zip_password(zip_file_path)
    # 8,5e17 combinatii incercate
