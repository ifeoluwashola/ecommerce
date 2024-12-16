#!/usr/bin/env python3

# Import
import string
import secrets

# Define a custom character set excluding #, ", and '
custom_charset = (
    string.ascii_letters
    + string.digits
    + "".join(
        char
        for char in string.punctuation
        if char not in ["#", '"', "'", ";", "{", "}"]
    )
)

# Generate the secret key
secret_key = "".join(secrets.choice(custom_charset) for _ in range(32))
salt = "".join(secrets.choice(custom_charset) for _ in range(32))

env_path = ".env"

# check if secret key exists
with open(env_path, "r") as env_file:
    if "SECRET_KEY=" and "SALT=" not in env_file.read():
        with open(env_path, "a") as env_file_append:
            # append the secret key to .env
            env_file_append.write(f"\nSECRET_KEY={secret_key}\nSALT={salt}")
            print("Secret key generated and stored in .env file")
    else:
        print("SECRET_KEY already exists in .env")
