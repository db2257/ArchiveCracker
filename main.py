import os
import time
import zipfile

from tqdm import tqdm


def brute_force_zip_password(zip_file_path, max_length=10):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    password_found = False
    extracted_file_name = 'textulet.txt'
    extracted_file_path = os.path.join(os.getcwd(), extracted_file_name)

    with zipfile.ZipFile(zip_file_path, 'r') as archive:
        for length in range(1, 4):
            start_time = time.time()
            combinations = generate_bruteforce_passwords(characters, length)
            elapsed_time = time.time() - start_time
            print(f"Time to generate combinations for length {length}: {elapsed_time:.2f} seconds")
            print("Trying combinations of size:", length)
            if length >= 3:
                combinations = tqdm(combinations, desc="Trying combinations")
            for combination in combinations:
                try:
                    archive.extract(extracted_file_name, pwd=combination.encode('utf-8'))
                    print(f"Parola gasita: {combination}")
                    password_found = True
                    break
                except:
                    pass

        # If the password is not found, try passwords from rockyou.txt
        if not password_found:
            with open(r'C:\Users\Dragos\Desktop\rockyou.txt', 'r', encoding='latin-1') as rockyou_file:
                for password in tqdm(rockyou_file, desc="Trying passwords from rockyou.txt"):
                    password = password.strip()
                    if len(password) <= max_length:
                        try:
                            archive.extract(extracted_file_name, pwd=password.encode('utf-8'))
                            print(f"Password found in rockyou.txt: {password}")
                            password_found = True
                            break
                        except:
                            pass

    if not password_found:
        print("Nu s-a gasit nicio parola.")
    if os.path.exists(extracted_file_path):
        os.remove(extracted_file_path)
        print(f"Deleted {extracted_file_path} after extraction.")
    else:
        print(f"{extracted_file_path} not found after extraction.")


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
    #fac cu threading
    #fac o functie care genereaza in fct de prima litera
    #hashcat
