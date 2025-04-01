# File: accounts.py
from app import app

from app.utils import hash
from app.utils import mysql_util

def insert_test_data():
    users = [
        ("bigbrovc@gmail.com", "bigbrovc", "42Farrah$%"),
        ("alice@example.com", "alice123", "A1ice@2024!"),
        ("bob@secure.com", "bob_secure", "B0b$Pass99!"),
        ("eve@hacker.com", "eve", "Ev1l@Attack123!"),
        ("john@doe.com", "john_doe", "J0hn$Secret!42"),
        ("sarah@cool.com", "sarahcool", "S@rah#Rocks22"),
        ("mike@work.com", "mike_dev", "M1keC0d3s!!"),
        ("jane@blog.com", "jane_writer", "Wr!tingFun123$"),
        ("admin@site.com", "admin", "Adm!nSecure99$"),
        ("test@dummy.com", "testuser", "DummY1Pass@3!"),
        ("robert@company.com", "robert123", "C0rp0rate$Pass1!"),
        ("lisa@home.com", "lisa_home", "L1sa$Home99!"),
        ("kevin@ai.com", "kevin_ai", "A!Future42Tech$"),
        ("harry@potter.com", "hp_fan", "H@rry1Potter99!"),
        ("sam@secure.net", "sam_sec", "S@fePassw0rd!24"),
        ("oliver@tech.com", "oliver_tech", "T3ch@Geek42!!"),
        ("emma@design.com", "emma_design", "Cr3ativeM!nd@99"),
        ("noah@math.com", "noah_math", "Algebr@Lover#42"),
        ("ava@music.com", "ava_music", "RockN@Roll2024!"),
        ("jack@fitness.com", "jack_fit", "W0rkoutTime@42!"),
        ("sophia@foodie.com", "sophia_foodie", "F00dLover@99!"),
        ("liam@space.com", "liam_space", "NASA@fan123!"),
        ("mia@fashion.com", "mia_fashion", "Tr3ndySt@yles#1"),
        ("william@cars.com", "william_cars", "Fast&Furious42!!"),
        ("isabella@pets.com", "isabella_pets", "IL0veDogs@123!"),
    ]

    sql = "INSERT INTO User (email, username, password_hash) VALUES (%s, %s, %s);"

    profiles = [(email, username, hash.hash_password(password)) for email, username, password in users]

    mysql_util.execute_many_sql(sql, profiles, commit=True)
