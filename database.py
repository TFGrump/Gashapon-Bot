import sqlite3

# database configuration variables

# the column names and types for each of the three tables
# the first column is the primary key
# if you modify these lists in ways other than appending to them, you need to change the functions
hero_attrs = ['id INTEGER', 
              'name text NOT NULL']

user_attrs = ['id BLOB', 
              'join_timestamp DATE NOT NULL', 
              'orb_count INTEGER NOT NULL']

unit_attrs = ['id INTEGER',
              'owner_id BLOB NOT NULL',
              'hero_id INTEGER NOT NULL',
              'birth_timestamp DATE NOT NULL',
              'FOREIGN KEY(owner_id) REFERENCES user(id)', 
              'FOREIGN KEY(hero_id) REFERENCES heroes(id)'] 


hero_table_name = "heroes"
unit_table_name = "units"
user_table_name = "users"


def init_tables(db):
    def list_to_sql_create_table_cmd(name, lis):
        cols = lis[0] + " PRIMARY KEY"
        for e in lis[1:]:
            cols += ", " + e

        command = f"CREATE TABLE {name} ({cols})"
        return command
        
    # convert the attribute lists into a SQL create table command
    hero_cmd = list_to_sql_create_table_cmd("heroes", hero_attrs)
    user_cmd = list_to_sql_create_table_cmd("users", user_attrs)
    unit_cmd = list_to_sql_create_table_cmd("units", unit_attrs)

    cur = db.cursor()
    cur.execute(hero_cmd)
    cur.execute(user_cmd)
    cur.execute(unit_cmd)
    db.commit()
    return

def open_db(filename):
    db = sqlite3.connect(filename)
    return db


# basic lookup functions

def lookup_user(db, user_id):
    cur = db.cursor()
    cur.execute(f"SELECT * FROM {user_table_name} WHERE id = :0", (user_id,))
    user = cur.fetchone()
    return user

def lookup_hero(db, name):
    cur = db.cursor()
    cur.execute(f"SELECT * FROM {hero_table_name} WHERE name = :0", (name,))
    hero = cur.fetchone()
    return hero

def lookup_all_heroes(db):
    cur = db.cursor()
    cur.execute(f"SELECT * FROM {hero_table_name}")
    heroes = cur.fetchall()
    return heroes

def lookup_units_for_user(db, user_id):
    cur = db.cursor()
    cur.execute(f"SELECT * FROM {unit_table_name} WHERE owner_id = :0", (user_id,))
    units = cur.fetchall()
    return units

# basic adding functions

def add_hero(db, name):
    cur = db.cursor()
    cur.execute(f"INSERT INTO {hero_table_name} (name) VALUES (:0)", (name,))
    db.commit()
    return

def add_unit(db, owner_id, hero_id, add_user=True):
    if add_user:
        if lookup_user(db, owner_id) == None:
            add_user(db, owner_id)

    cur = db.cursor()
    cur.execute(f"INSERT INTO {unit_table_name} (owner_id, hero_id, birth_timestamp) " 
            f"VALUES (:0, :1, datetime('now'))", (owner_id, hero_id))
    db.commit()
    return

def add_user(db, user_id):
    cur = db.cursor()
    cur.execute(f"INSERT INTO {user_table_name} (id, join_timestamp, orb_count) " 
            f"VALUES (:0, datetime('now'), 0)", (user_id,))
    db.commit()
    return


# more complicated functions

def update_user_orb_count(db, user_id, difference):
    user = lookup_user(db, user_id)
    orb_count = user[2]
    
    orb_count += difference
    
    # check if this is a valid update
    if orb_count < 0:
        return False

    cur = db.cursor()
    cur.execute(f"UPDATE {user_table_name} SET orb_count = {orb_count} where id = :0", (user_id,))
    db.commit()
    return True
