# File: hash.py
# https://www.geeksforgeeks.org/hashing-passwords-in-python-with-bcrypt

import bcrypt
import time

ROUNDS = 11

def hash_password(password: str, rounds: int = ROUNDS) -> str:
    """
    Hashes a password using bcrypt with a specified number of rounds

    password: The plaintext password to hash
    rounds: The cost factor
    
    return: The hashed password as a string
    """
    salt = bcrypt.gensalt(rounds)  # generate a salt with given rounds
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plaintext password against a hashed password

    plain_password: The plaintext password to verify
    hashed_password: The hashed password to compare against
    
    return: True if the passwords match, False otherwise
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def hash_password_test():
    plaintext_password = "42Mutlu$%"
    rounds = ROUNDS # not the same as "hashing password x amount of times"
                    # but providess even more security

    start_time = time.time()
    hashed_password = hash_password(plaintext_password, rounds)
    elapsed_time = time.time() - start_time

    # check correct password
    is_correct = verify_password(plaintext_password, hashed_password)

    # check incorrect password
    false_password = "Retche Gospod Gospodevi Moyemu"
    is_false_correct = verify_password(false_password, hashed_password)

    print("Password Hashing Test")
    print("=====================")
    print("Plaintext password:", plaintext_password)
    print("False password:", false_password)
    print("Hashed password:", hashed_password)
    print(f"Rounds used: {rounds}")
    print(f"Time taken: {elapsed_time:.4f} sec")
    print("Is correct password valid?", is_correct)  # should be True
    print("Is incorrect password valid?", is_false_correct)  # should be False

if __name__ == "__main__":
    hash_password_test()
