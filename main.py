import os
import shutil
import time
import zipfile

from tqdm import tqdm


def brute_force_zip_password(zip_file_path, max_length=10):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    password_found = False

    zip_file_dir = os.path.dirname(zip_file_path)
    auxiliary_folder_path = os.path.join(zip_file_dir, "auxiliary")
    if not os.path.exists(auxiliary_folder_path):
        os.makedirs(auxiliary_folder_path)

    threshold = 4
    with zipfile.ZipFile(zip_file_path, 'r') as archive:
        for length in range(1, threshold):
            start_time = time.time()
            combinations = generate_bruteforce_passwords(characters, length)
            elapsed_time = time.time() - start_time
            print(f"Time to generate combinations for length {length}: {elapsed_time:.2f} seconds")
            print("Trying combinations of size:", length)

            if length >= 3:
                combinations = tqdm(combinations, desc="Trying combinations")
            for combination in combinations:
                try:
                    archive.extractall(pwd=combination.encode('utf-8'), path=auxiliary_folder_path)
                    print(f"Parola gasita: {combination}")
                    if os.path.exists(auxiliary_folder_path):
                        shutil.rmtree(auxiliary_folder_path)
                    password_found = True
                    return combination
                except:
                    pass

        # If the password is not found, try passwords from rockyou.txt
        if not password_found:
            with open(r'C:\Users\Dragos\Desktop\rockyou.txt', 'r', encoding='utf-8') as rockyou_file:
                for password in tqdm(rockyou_file, desc="Trying passwords from rockyou.txt"):
                    password = password.strip()
                    if len(password) <= max_length:
                        try:
                            archive.extractall(pwd=password.encode('utf-8'), path=auxiliary_folder_path)
                            print(f"Parola gasita: {password}")
                            if os.path.exists(auxiliary_folder_path):
                                shutil.rmtree(auxiliary_folder_path)
                            password_found = True
                            return password
                        except:
                            pass

    if not password_found:
        print("Nu s-a gasit nicio parola.")
        
    if os.path.exists(auxiliary_folder_path):
        shutil.rmtree(auxiliary_folder_path)


def generate_bruteforce_passwords(characters, length, current_password=""):
    if length == 0:
        return [current_password]

    passwords = []
    for char in characters:
        passwords.extend(generate_bruteforce_passwords(characters, length - 1, current_password + char))

    return passwords


if __name__ == '__main__':
    zip_file_path = r"C:\Users\Dragos\Desktop\lucrupython\ArchiveCracker\Archive.zip"
    brute_force_zip_password(zip_file_path)
