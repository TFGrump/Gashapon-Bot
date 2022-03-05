import sqlite3

# database configuration variables

# the column names and types for each of the three tables
# the first column is the primary key
# if you modify these lists in ways other than appending to them, you need to change the functions
hero_attrs = ['id INTEGER', 
              'name text NOT NULL'
              'release_ts DATE NOT NULL']

user_attrs = ['id BLOB', 
              'join_ts DATE NOT NULL', 
              'orb_count INTEGER NOT NULL']

unit_attrs = ['id INTEGER',
              'owner_id BLOB NOT NULL',
              'hero_id INTEGER NOT NULL',
              'obtain_ts DATE NOT NULL',
              'level INTEGER NOT NULL', 
              'FOREIGN KEY(owner_id) REFERENCES user(id)', 
              'FOREIGN KEY(hero_id) REFERENCES heroes(id)'] 


hero_table_name = "heroes"
unit_table_name = "units"
user_table_name = "users"


def init_tables(db):
    """
    Initializes the hero, unit, and user tables in the database
    This should only be run once. 
    params:
        - db - the database to initialize the tables in
    """
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
    """
    Opens the database
    params:
        - filename - the filename of the SQLite database
    returns:
        a SQLite3 connection to the database contained in the file
    """
    db = sqlite3.connect(filename)
    return db


# basic lookup functions

def lookup_user(db, user_id):
    """
    Looks up the user in the database.
    params:
        - db      - the database to look for the user in
        - user_id - the id of the user to look for
    returns:
        a tuple of the attributes of the user 
    """
    cur = db.cursor()
    cur.execute(f"SELECT * FROM {user_table_name} WHERE id = :0", (user_id,))
    user = cur.fetchone()
    return user

def lookup_hero(db, name):
    """
    Looks up a hero in the database.
    params:
        - db      - the database to look for the hero in
        - name    - the name of the hero
    returns:
        a tuple of the attributes of the hero
    """
    cur = db.cursor()
    cur.execute(f"SELECT * FROM {hero_table_name} WHERE name = :0", (name,))
    hero = cur.fetchone()
    return hero

def lookup_all_heroes(db):
    """
    Looks up all the heroes in the database. 
    params:
        - db - the database to look for heroes in
    returns:
        a list of tuples of hero attributes
    """
    cur = db.cursor()
    cur.execute(f"SELECT * FROM {hero_table_name}")
    heroes = cur.fetchall()
    return heroes

def lookup_units_for_user(db, user_id):
    """
    Looks up all the units owned by a particular user
    params:
        - db - the database to look for units in
        - user_id - whose units to look up
    returns:
        a list of tuples of unit attributes
    """
    cur = db.cursor()
    cur.execute(f"SELECT * FROM {unit_table_name} WHERE owner_id = :0", (user_id,))
    units = cur.fetchall()
    return units

# basic adding functions

def add_hero(db, name):
    """
    Adds a hero to the database
    params:
        - db      - the database to add the hero to
        - name    - the name of the hero 
    """
    cur = db.cursor()
    cur.execute(f"INSERT INTO {hero_table_name} (name, release_ts) VALUES (:0, datetime('now))", (name,))
    db.commit()
    return

def add_unit(db, owner_id, hero_id, level=0, add_user=True):
    """
    Adds a unit to the database
    params:
        - db        - the database to add the unit to
        - owner_id  - the id of the owner of the new hero
        - hero_id   - the type of hero that this unit is
        - level     - the initial level of the unit, defaults to 0
        - add_user  - if true, adds the user owner_id to the database, defaults to True 
    """
    if add_user:
        if lookup_user(db, owner_id) == None:
            add_user(db, owner_id)

    cur = db.cursor()
    cur.execute(f"INSERT INTO {unit_table_name} (owner_id, hero_id, obtain_ts, level) " 
            f"VALUES (:0, :1, datetime('now'), :2)", (owner_id, hero_id, level))
    db.commit()
    return

def add_user(db, user_id):
    """
    Adds a user to the database
    params:
        - db        - the database to add the user to
        - user_id   - the id of the user
    """
    cur = db.cursor()
    cur.execute(f"INSERT INTO {user_table_name} (id, join_ts, orb_count) " 
            f"VALUES (:0, datetime('now'), 0)", (user_id,))
    db.commit()
    return


# more complicated functions

def update_user_orb_count(db, user_id, change):
    """
    Updates the orb count of a user by adding to it
    Orb counts cannot go below 0 and orbs cannot be given or taken away from non-existent users.
    params:
        - db - the database to check for the user in
        - user_id - the user whose orbs we want to update
        - change - the change in orbs
    returns:
        True if the database was updated, False otherwise
    """
    user = lookup_user(db, user_id)
    
    if user is None:
        return False

    orb_count = user[2]
    
    orb_count += change
    
    # check if this is a valid update
    if orb_count < 0:
        return False

    cur = db.cursor()
    cur.execute(f"UPDATE {user_table_name} SET orb_count = {orb_count} where id = :0", (user_id,))
    db.commit()
    return True
