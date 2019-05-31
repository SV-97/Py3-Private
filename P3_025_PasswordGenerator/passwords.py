from pathlib import Path
import getpass
import hashlib
import os
import random
import sqlite3 as sql
import string

from termcolor import colored

path = Path("totally_not_my_passwords.db")
print()


def input_():
    return input(">> ")


def print_failure(text):
    print(f"{colored('✗', 'red')} {text}")


def print_success(text):
    print(f"{colored('✔', 'green')} {text}")


def print_colored(text, print_args={}, *args, **kwargs):
    print(colored(text, *args, **kwargs), **print_args)


def show_list():
    global con
    print()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM domains")
    matches = cursor.fetchall()
    if len(matches) <= 0:
        print_colored("Database is empty", attrs=["bold"])
        return True

    def find_indexed_max(iterable, index):
        tuple_with_longest = max(iterable, key=lambda t: len(str(t[index])))
        longest =  len(str(tuple_with_longest[index]))
        return longest + 2 # +2 to create one space on either side

    len_finder = matches[:]
    len_finder.append(('uid', 'Domain', 'Prohibited Chars', 'PD Version'))
    uid_width = find_indexed_max(len_finder, 0)
    domain_width = find_indexed_max(len_finder, 1)
    prohib_chars_width = find_indexed_max(len_finder, 2)
    version_width = find_indexed_max(len_finder, 3)
    print_colored(f"{'uid':^{uid_width}} | {'Domain':^{domain_width}} | {'Prohibited Chars':^{prohib_chars_width}} | {'PD Version':^{version_width}}", attrs=["bold", "underline"])    
    for i, (uid, domain, length, prohibited_chars, version) in enumerate(matches):
        color = "yellow" if i%2 else "white"
        #on_color = "on_white" if i%2 else "on_yellow"
        on_color = None
        print_colored(f"{uid:^{uid_width}} | {domain:^{domain_width}} | {prohibited_chars:^{prohib_chars_width}} | {version:^{version_width}}", color=color, on_color=on_color)
    cursor.close()
    return True


def get_master_password():
    master_password = False
    master_password_check = True
    while master_password != master_password_check:
        print_colored("Enter Master Password:", attrs=["bold"]) # get password
        master_password = getpass.getpass()
        master_password_check = getpass.getpass("Reenter Password: ")
        if master_password != master_password_check:
            print_failure("Passwords don't match!")
    return master_password


def generate_password(domain, length, prohibited_chars, version):
    def version_0(domain, length, prohibited_chars, version):
        salt = "I'm not gonna publish my salt you fuck"
        seed = salt + "neither my seed"
        rnd = random.Random(seed) # initialize random with seed

        prohibited_chars = f"{prohibited_chars}OIlL"
        alphabet = string.ascii_letters
        alphabet = "".join(filter(lambda c: c not in prohibited_chars, alphabet))
        alphabet = f"{alphabet}Or the chars"

        master_password = get_master_password()

        absolute_salt = "".join(rnd.choices(alphabet, k=50))
        hash_str = f"{absolute_salt}{master_password}{domain}"
        iterations = 9600
        hashed = hashlib.pbkdf2_hmac("sha512", hash_str.encode(), str(rnd.randint(0, int(1e100))+length).encode(), iterations)
        rnd2 = random.Random(hashed.hex())
        print_success("Generated password")
        return "".join(rnd2.choices(alphabet, k=length))
    
    def version_1(domain, length, prohibited_chars, version):
        salt = "just_another_salt"
        prohibited_chars = f"{prohibited_chars}OIlL"
        candidate_chars = f"{string.ascii_letters}{string.digits}""!,;.-_+-*()[]{}$%=?€#'~ß§&"
        chars = "".join(filter(lambda char: char not in prohibited_chars, candidate_chars))

        master_password = get_master_password()
        random.seed(salt)
        hash_string = f"{''.join(rnd.choices(candidate_chars, k=50))}{master_password}{domain}"
        iterations = 38400
        raise NotImplementedError()

    try:
        return {"0": version_0, "1": version_1}[version](domain, length, prohibited_chars, version)
    except (KeyError, NotImplementedError) as e:
        print_failure("Unknown or not implemented version")
        return colored(str(e), color="red")


def get_password():
    global con
    cursor = con.cursor()
    print()
    while True:
        print_colored("Please enter the domain: ", attrs=["bold"])
        domain = input_()
        if domain != "":
            break
    try:
        cursor.execute("SELECT * FROM domains WHERE name=?", [domain])
        uid, domain, length, prohibited_chars, version = next(cursor)
    except StopIteration:
        print_failure(f"Domain is not in database")
        return False
    else:
        con.commit()
    finally:
        cursor.close()
    print(f"Copy password here >>{colored(generate_password(domain, length, prohibited_chars, version), on_color='on_green', attrs=['concealed'])}<<")
    return True
    

def create_new():
    global con
    cursor = con.cursor()
    print()
    while True:
        print_colored("Please enter the new domain: ", attrs=["bold"])
        domain = input_()
        if domain != "":
            break

    while True:
        print_colored("Please enter size of the new password (default is 25): ", attrs=["bold"])
        string = input_()
        if string == "":
            size = 25
            break
        else:
            try:
                size = int(string)
                if size <= 0:
                    print_colored("You have to have at least 1 character in there, come on", color="red")
                    raise ValueError
            except ValueError:
                continue
            else:
                break

    print_colored("Please enter all the prohibited characters (leave blank if the domain doesn't provide any): ", attrs=["bold"])
    prohibited = input_()
    
    print_colored("Enter the password derivation version you want (defaults to 0): ", attrs=["bold"])
    version = input_()
    version = "0" if version == "" else version

    try:
        cursor.execute("INSERT INTO domains VALUES (null, ?, ?, ?, ?)", ( domain, size, prohibited, version))
    except sql.OperationalError as e:
        print_failure(f"Failed to insert domain into database")
        print_colored(f"{indent}{str(e)}", color="red")
        return False
    except sql.IntegrityError as e:
        print_failure(f"Domain already exists")
        return False
    else:
        print_success(f"Successfully added new domain {domain}")
        con.commit()
        return True
    finally:
        cursor.close()
    

def delete():
    global con
    cursor = con.cursor()
    print()
    domain = False
    domain_check = True
    while domain != domain_check:
        print_colored("Please enter the domain that's to be deleted: ", color="red", attrs=["bold"])
        domain = input_()
        print_colored("Please enter the domain again to verify deletion: ", color="red", attrs=["bold"])
        domain_check = input_()
    try:
        cursor.execute("DELETE FROM domains WHERE name=?", [domain])
    except sql.OperationalError:
        print_failure(f"Domain is not in database")
        return False
    else:
        print_success(f"Successfully deleted {colored(domain, 'red')}")
        con.commit()
    finally:
        cursor.close()
    return True


def install():
    global con
    cursor = con.cursor()
    try:
        cursor.execute("""
            CREATE TABLE domains
                (   
                    uid INTEGER PRIMARY KEY,
                    name TEXT UNIQUE,
                    length INTEGER,
                    prohibited_characters TEXT,
                    version TEXT
                )
        """)
    except sql.OperationalError as e:
        print_failure(f"Failed to create table")
        print_colored(str(e), color="red")
        return False
    else:
        print_success(f"Successfully created table {colored('domains', color='cyan')}")
        con.commit()
        global submenus
        submenus = list(filter(lambda t: t[0] is not install, submenus)) # remove install from submenues
        return True
    finally:
        cursor.close()


def close():
    global con
    con.close()
    print_success("Closed database")
    print_colored("Peace ☮", attrs=["blink"])
    exit()


submenus = [
    (get_password, "Get the entry for a given domain"),
    (create_new, "Create a new entry"),
    (delete, "Delete an existing entry"),
    (show_list, "Show all the domains in the database")]

db_string = colored(path, "blue", attrs=["underline"])

if path.is_file():
    print_success(f"Connected to database at {db_string}")
else:
    print_failure(f"Failed to connect to database at {db_string} - you should initialize it via 'Install this CLA'")
    submenus.append((install, "Install this CLA - create a new database"))
    
submenus.append((close, "Exit"))

con = sql.connect(str(path))
indent = "    "
while True:
    print()
    try:
        print_colored("Select Submenu:", attrs=["bold"])
        for i, (_, message) in enumerate(submenus):
            color = "blue" if not i % 2 else "white"
            print(colored(f"{indent}{i}) ", attrs=["bold"], color=color), end="")
            print_colored(message, color=color)
        
        #submenus[int(input_(colored(" ", on_color="on_white", attrs=["blink"])))][0]()
        try:
            inp = int(input_())
            os.system("clear")
            submenus[inp][0]() # call subroutine according to user input_
        except IndexError as e:
            print_colored("Index out of range", color="red")
        except ValueError as e:
            print_colored("Can't interpret input as number", color="red")
    except KeyboardInterrupt:
        print()
        close()