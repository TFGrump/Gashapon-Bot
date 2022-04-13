import sqlite3     # for the database  
import numpy as np # for summon

# database configuration variables

# the column names and types for each of the three tables
# the first column is the primary key

hero_cols = ['id INTEGER',
             'name text NOT NULL',
             'release_ts DATE NOT NULL']

hero_attrs = []

user_cols = ['id BLOB',
             'join_ts DATE NOT NULL',
             'orb_count INTEGER DEFAULT 0',
             'ascendant_shard_count INTEGER DEFAULT 0',
             'level_up_shard_count INTEGER DEFAULT 0']

user_attrs = []

unit_cols = ['id INTEGER',
             'owner_id BLOB NOT NULL',
             'hero_id INTEGER NOT NULL',
             'obtain_ts DATE NOT NULL',
             'level INTEGER NOT NULL']

unit_attrs = ['FOREIGN KEY(owner_id) REFERENCES user(id)',
              'FOREIGN KEY(hero_id) REFERENCES heroes(id)']

pool_cols = ['id INTEGER',
             'name text NOT NULL']

pool_attrs = []

hero_table_name = "heroes"
unit_table_name = "units"
user_table_name = "users"
pool_table_name = "pools"


def _tuple_to_hero_dict(hero_tuple):
    if hero_tuple is None:
        return None

    hero_dict = {}

    for ii, col in enumerate(hero_cols):
        hero_dict[col.split()[0]] = hero_tuple[ii]

    return hero_dict


def _tuple_list_to_hero_dicts(list_of_heroes):
    return [_tuple_to_hero_dict(x) for x in list_of_heroes]


def _tuple_to_user_dict(user_tuple):
    if user_tuple is None:
        return None

    user_dict = {}

    for ii, col in enumerate(user_cols):
        user_dict[col.split()[0]] = user_tuple[ii]

    return user_dict


def _tuple_list_to_user_dicts(list_of_users):
    return [_tuple_to_user_dict(x) for x in list_of_users]


def _tuple_to_unit_dict(unit_tuple):
    if unit_tuple is None:
        return None

    unit_dict = {}

    for ii, col in enumerate(unit_cols):
        unit_dict[col.split()[0]] = unit_tuple[ii]

    return unit_dict


def _tuple_list_to_unit_dicts(list_of_units):
    return [_tuple_to_unit_dict(x) for x in list_of_units]


def _augment_unit_dict_with_hero_info(db, unit_dict):
    hero = lookup_hero(db, unit_dict["hero_id"]) 
    if hero is None:
        return None
    hero.update(unit_dict)
    return hero


def init_tables(db):
    """
    Initializes the hero, unit, and user tables in the database
    This should only be run once. 
    params:
        - db - the database to initialize the tables in
    """
    def list_to_sql_create_table_cmd(name, cols, attrs):
        table_attrs = cols[0] + " PRIMARY KEY"
        for e in cols[1:] + attrs:
            table_attrs += ", " + e

        command = f"CREATE TABLE {name} ({table_attrs})"
        return command
        
    # convert the attribute lists into a SQL create table command
    hero_cmd = list_to_sql_create_table_cmd(hero_table_name, hero_cols, hero_attrs)
    user_cmd = list_to_sql_create_table_cmd(user_table_name, user_cols, user_attrs)
    unit_cmd = list_to_sql_create_table_cmd(unit_table_name, unit_cols, unit_attrs)
    pool_cmd = list_to_sql_create_table_cmd(pool_table_name, pool_cols, pool_attrs)

    cur = db.cursor()
    cur.execute(hero_cmd)
    cur.execute(user_cmd)
    cur.execute(unit_cmd)
    cur.execute(pool_cmd)
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


# BASIC LOOKUP FUNCTIONS

def lookup_user(db, user_id, add_nonexistent_user=True):
    """
    Looks up the user in the database.
    params:
        - db      - the database to look for the user in
        - user_id - the id of the user to look for
    returns:
        a dict of the attributes of the user 
    """
    
    cur = db.cursor()
    cur.execute(f"SELECT * FROM {user_table_name} WHERE id = :0", (user_id,))
    user = cur.fetchone()

    if user is None and add_nonexistent_user: 
        add_user(db, user_id)
        cur.execute(f"SELECT * FROM {user_table_name} WHERE id = :0", (user_id,))
        user = cur.fetchone()

    return _tuple_to_user_dict(user)


def lookup_hero(db, hero_id):
    """
    Looks up a hero in the database.
    params:
        - db      - the database to look for the hero in
        - id      - the id of the hero
    returns:
        a dict of the attributes of the hero
    """
    cur = db.cursor()
    cur.execute(f"SELECT * FROM {hero_table_name} WHERE id = :0", (hero_id,))
    hero = cur.fetchone()
    return _tuple_to_hero_dict(hero)


def lookup_all_heroes(db):
    """
    looks up all the heroes in the database. 
    params:
        - db - the database to look for heroes in
    returns:
        a list of dicts of hero attributes
    """
    cur = db.cursor()
    cur.execute(f"select * from {hero_table_name}")
    heroes = cur.fetchall()
    
    return _tuple_list_to_hero_dicts(heroes)


def lookup_units_for_user(db, user_id, get_hero_info=True):
    """
    Looks up all the units owned by a particular user
    params:
        - db            - the database to look for units in
        - user_id       - whose units to look up
        - get_hero_info - True 
    returns:
        a list of dicts of unit attributes
    """
    cur = db.cursor()
    cur.execute(f"SELECT * FROM {unit_table_name} WHERE owner_id = :0", (user_id,))
    units = cur.fetchall()
    
    units = _tuple_list_to_unit_dicts(units)

    # augment the with hero info
    if get_hero_info:
        units = [_augment_unit_dict_with_hero_info(db, x) for x in units]
    return units


def lookup_all_pools(db):
    """
    looks up all the pools in the database. 
    params:
        - db - the database to look for heroes in
    returns:
        a list of dicts of pool attributes
    """
    cur = db.cursor()
    cur.execute(f"select id, name from {pool_table_name}")
    pools = cur.fetchall()
    pool_dicts = []

    for pool in pools:
        pool_dicts.append({
            "id": pool[0],
            "name": pool[1]
        })
    
    return pool_dicts


# BASIC ADDING FUNCTIONS

def add_hero(db, name):
    """
    Adds a hero to the database
    params:
        - db      - the database to add the hero to
        - name    - the name of the hero 
    """
    try:
        cur = db.cursor()
        
        # add hero to hero table
        cur.execute(f"INSERT INTO {hero_table_name} (name, release_ts) VALUES (:0, datetime('now'))", (name,))

        pool_col_name = "hero_id" + str(cur.lastrowid)

        # add corresponding column into pool table
        cur.execute(f"ALTER TABLE {pool_table_name} ADD COLUMN {pool_col_name} INTEGER DEFAULT 0")
        db.commit()
        return True
    except sqlite3.Error:
        return False


def add_unit(db, owner_id, hero_id, level=0, add_nonexistent_user=True):
    """
    Adds a unit to the database
    params:
        - db        - the database to add the unit to
        - owner_id  - the id of the owner of the new hero
        - hero_id   - the type of hero that this unit is
        - level     - the initial level of the unit, defaults to 0
        - add_user  - if true, adds the user owner_id to the database, defaults to True
    returns:
        True if the unit was added
    """
    if add_nonexistent_user:
        if lookup_user(db, owner_id) is None:
            # if we fail to add the user, we failed to add the unit
            if not add_user(db, owner_id):
                return False

    try:
        cur = db.cursor()
        cur.execute(f"INSERT INTO {unit_table_name} (owner_id, hero_id, obtain_ts, level) " 
                    f"VALUES (:0, :1, datetime('now'), :2)", (owner_id, hero_id, level))
        db.commit()
        return True
    except sqlite3.Error:
        return False


def add_user(db, user_id):
    """
    Adds a user to the database
    params:
        - db        - the database to add the user to
        - user_id   - the id of the user
    return:
        True if the user was added
    """
    
    if lookup_user(db, user_id, add_nonexistent_user=False) is not None:
        return False

    try:
        cur = db.cursor()
        cur.execute(f"INSERT INTO {user_table_name} (id, join_ts) " 
                    f"VALUES (:0, datetime('now'))", (user_id,))
        db.commit()
        return True
    except sqlite3.Error:
        return False


def add_pool(db, name, drop_rates):
    """
    Adds a pool to the database
    params: 
        - db            - the database to add the pool to
        - name          - the name of the pool
        - drop_rates    - a collection of tuples of the form (hero_id, drop_rates) 

    note: a larger drop-rate means that the hero type will be more common
    """

    col_names = []
    col_values = [name]

    for hero_id, value in drop_rates:
        col_names.append("hero_id" + str(hero_id))
        col_values.append(value)

    # hacking together our insert command
    cmd = f"INSERT INTO {pool_table_name} (name"
    
    # add the column names to add to our INSERT
    for name in col_names:
        cmd += ", " + str(name)
    
    cmd += f") VALUES ("
    cmd += ":0"
    for i in range(1, len(col_values)):
        cmd += ", :" + str(i)
    cmd += ")"
    
    try:
        cur = db.cursor()
        cur.execute(cmd, col_values)
        db.commit()
        return True
    except sqlite3.Error:
        return False


# MORE COMPLICATED FUNCTIONS

def summon_unit(db, pool_id, user_id, unit_level=0):
    """
    Summons a unit from a pool based on the drop-rates
    params:
        - db            - the database to use
        - pool_id       - the pool to pull from
        - user_id       - the user to give the unit to
        - unit_level    - the level of the unit, defaults to 0
    returns:
        a dict of the newly summoned unit's attributes
    """

    cur = db.cursor()
    cur.execute(f"SELECT * FROM {pool_table_name} WHERE id = :0", (pool_id,))
    
    # This is basically going to do a single stochastic uniform sample where the weights are the drop rates
    # Each drop rate corresponds to an interval of the size of the drop rate
    pool = np.array(cur.fetchone()[2:])
    total = np.sum(pool)

    # Select a random number
    threshold = np.random.randint(0, total)

    # Find which interval the random number is in
    running_sum = 0
    i = 0
    while running_sum < threshold and i < len(pool) - 1:
        running_sum += pool[i]
        i += 1
   
    # Hero IDs start at 1
    hero_id = i + 1

    # if we fail to add the unit, we summoned nothing
    if not add_unit(db, user_id, hero_id, unit_level, add_nonexistent_user=False):
        return None
    
    try:
        # UPDATE THIS WHEN YOU UPDATE THE UNIT TABLE
        cur.execute(f"SELECT id, owner_id, hero_id, MAX(obtain_ts), level "
                    f"FROM {unit_table_name} WHERE hero_id = :0", (hero_id,))
        unit = cur.fetchone()
        db.commit()
        
        return _tuple_to_unit_dict(unit)
    except sqlite3.Error as e:
        print(e)
        return None


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
    user = lookup_user(db, user_id, add_nonexistent_user=False)
    
    if user is None:
        return False

    orb_count = user['orb_count']
    
    orb_count += change
    
    # check if this is a valid update
    if orb_count < 0:
        return False

    try:
        cur = db.cursor()
        cur.execute(f"UPDATE {user_table_name} SET orb_count = {orb_count} where id = :0", (user_id, ))
        db.commit()
        return True
    except sqlite3.Error:
        return False


def update_user_ascendant_shards(db, user_id, change):
    """
    Updates the shard count of a user by adding to it
    Shard counts cannot go below 0 and shards cannot be given or taken away from non-existent users.
    params:
        - db - the database to check for the user in
        - user_id - the user whose shards we want to update
        - change - the change in shards
    returns:
        True if the database was updated, False otherwise
    """
    user = lookup_user(db, user_id, add_nonexistent_user=False)
    
    if user is None:
        return False

    ascendant_shards = user['ascendant_shard_count']
    
    ascendant_shards += change
    
    # check if this is a valid update
    if ascendant_shards < 0:
        return False

    try:
        cur = db.cursor()
        cur.execute(f"UPDATE {user_table_name} SET ascendant_shard_count = {ascendant_shards} where id = :0", 
                    (user_id, ))
        db.commit()
        return True
    except sqlite3.Error:
        return False


def update_user_level_up_shards(db, user_id, change):
    """
    Updates the shard count of a user by adding to it
    Shard counts cannot go below 0 and shards cannot be given or taken away from non-existent users.
    params:
        - db - the database to check for the user in
        - user_id - the user whose shards we want to update
        - change - the change in shards
    returns:
        True if the database was updated, False otherwise
    """
    user = lookup_user(db, user_id, add_nonexistent_user=False)
    
    if user is None:
        return False

    level_up_shards = user['level_up_shard_count']
    
    level_up_shards += change
    
    # check if this is a valid update
    if level_up_shards < 0:
        return False

    try:
        cur = db.cursor()
        cur.execute(f"UPDATE {user_table_name} SET level_up_shard_count = {level_up_shards} where id = :0", 
                    (user_id, ))
        db.commit()
        return True
    except sqlite3.Error:
        return False
