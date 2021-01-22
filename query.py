# Executes a query on the given cursor. and returns te result in a list.

# MYSQL greenstar passsword od41zLDLwosDmonr
# MYSQL greenstar ip 34.123.165.253
from mysql.connector import connection

show = True


def creds(db="finance"):
    sql_gs = dict()
    sql_gs["user"] = "root"
    sql_gs["password"] = "od41zLDLwosDmonr"
    sql_gs["host"] = "34.123.165.253"
    sql_gs["database"] = db
    return sql_gs


# Making the Mysql connection
# cnx = connection.MySQLConnection(
#     user=db_dict["user"],
#     password=db_dict["password"],
#     host=db_dict["host"],
#     database=db_dict["database"],
# )


def make_connection(db_dict = creds()):
    cnx = connection.MySQLConnection(
        user=db_dict["user"],
        password=db_dict["password"],
        host=db_dict["host"],
        database=db_dict["database"],
    )
    return cnx



def single_q(query, cursor):
    # for submitting big one liner queries.
    try:
        for _ in cursor.execute(query, multi=True):
            pass
    except Exception as e:
        if show:
            print(query, "\nError is:\n", e)
    result = []
    try:
        result = cursor.fetchall()
    except:
        if show:
            print("\nThis is an insert query\n")
    return result


# executes a list of queries on a given cursor and returns the results in a list.
def multi_q(querylist, cursor):
    result = []
    for q in querylist:
        result.append(single_q(q, cursor))
    return result


# sends a query or list of queries to a db.
def make_query(query,array=False, commit=True):
    cnx = make_connection()
    # make an sql query q where q is a query string.
    cursor = cnx.cursor(dictionary=True)
    result = []
    if array:
        result = multi_q(query, cursor)
    else:
        result = single_q(query, cursor)
    if commit:
        cnx.commit()
    cnx.close()
    return result


wait_string = ""


# takes a table, list of fields, and list of values.
def insert_query(table, insertdict, wait=False):
    fields = [f for f in insertdict]
    values = [str(insertdict[f]) for f in fields]
    f_string = ", ".join(fields)
    v_string = "', '".join(values)
    query = "insert into {} ({}) VALUES ('{}'); ".format(table, f_string, v_string)
    if not wait:
        return make_query(query)
    else:
        global wait_string
        wait_string = wait_string + query


def send_waiting_queries_raw():
    global wait_string
    make_query(wait_string)
    wait_string = ""


# makes the string of equivalency statements for select queries.
def eq_string(eq_dict, separator='and'):
    statements = []
    for field in eq_dict:
        
        #modify the value to be proper
        value = eq_dict[field]
        if isinstance(value, str):
            value = "'"+value + "'"
        elif value == None:
            value = "NULL"
        
        #make the corresponding statement
        comp = " {} = {} ".format(field, value)

        #for anything other than = comparisons
        if isinstance(value, tuple):
            sym = value[0]
            val = value[1]
            comp = " {} {} {} ".format(field, sym, val)
        statements.append(comp)

    eq_string = separator.join(statements)
    return eq_string



# takes a table, list of fields, and list of values.
def select_query(table, eq_dict=None, desc_field=None):
    # make the query
    qp1 = "select * from {} where".format(table) + eq_string(eq_dict)
    qp2 = ";"
    if desc_field is not None:
        qp2 = "ORDER BY {} DESC;".format(desc_field)
    query = qp1 + qp2
    print(query,flush=True)
    return make_query(query, commit=True)


def change_string(change_dict):
    return eq_string(change_dict, separator=',')


def update_query(table, eq_dict, change_dict):
    query = "UPDATE {} SET {} WHERE {};".format(table, change_string(change_dict), eq_string(eq_dict))
    return make_query(query)


def safe_query_literal(query):
    global cnx
    cursor = cnx.cursor(dictionary=True, buffered=True)
    try:
        cursor.execute(query)
        cursor.fetchall()
        cnx.commit()
        return
    except Exception as e:
        print("There was an error submitting your query to the database: ", e)

