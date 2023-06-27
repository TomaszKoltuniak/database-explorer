import sqlite3, click

from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("database.sqlite3", detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    print("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_column_values(column_name="Company name"):
    with sqlite3.connect("database.sqlite3") as db:
        all_values = db.execute(f"SELECT `{column_name}` FROM companies;").fetchall()
    result = []
    for name in all_values:
        if name[0] not in result:
            result.append(name[0])
    return result


def get_columns_names():
    with sqlite3.connect("database.sqlite3") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.execute("select * from companies;")
        row = cursor.fetchone()
        columns = row.keys()
        columns = columns[:14] + ['Comments']
    return columns


def get_companies(name=None, field_of_work=None):
    try:
        name.strip()
    except:
        pass
    try:
        field_of_work.strip()
    except:
        pass
    if name == "":
        name = None
    if field_of_work == "":
        field_of_work = None
    with sqlite3.connect("database.sqlite3") as connection:
        connection.row_factory = sqlite3.Row
        if name == None and field_of_work == None:
            query = "select * from companies;"
        elif name == None and field_of_work != None:
            query = f"select * from companies where `Field of work` like '%{field_of_work}%';"
        # elif name != None and field_of_work == None:
        else:
            query = f"select * from companies where `Company name` like '%{name}%';"

        cursor = connection.execute(query)
        rows = cursor.fetchall()
        columns = rows[0].keys()
        records = []
        for row in rows:
            record = {}
            for column in columns:
                if column != "Creation date" and column != "Last update":
                    record[column] = row[column]
            record["Comments"] = get_comments(record["id"])
            records.append(record)
        return records


def add_company(new_record: dict):
    with sqlite3.connect("database.sqlite3") as connection:
        cursor = connection.cursor()
        query = f"""INSERT INTO
        companies (`Company name`, `Field of work`, `Address`, `Name of Mentor/ Contact person`, `Phone number`, `Email`, `Website`, `Max number of students`, `Current student count`, `Status`, `Commute`, `Required additional equipment/ clothes`, `Important information`, `Creation date`, `Last update`)
        values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, strftime('%Y-%m-%d %H:%M', 'now', 'localtime'), strftime('%Y-%m-%d %H:%M', 'now', 'localtime'))"""
        values = (
            new_record["Company name"],
            new_record["Field of work"],
            new_record["Address"],
            new_record["Name of Mentor/ Contact person"],
            new_record["Phone number"],
            new_record["Email"],
            new_record["Website"],
            new_record["Max number of students"],
            new_record["Current student count"],
            new_record["Status"],
            new_record["Commute"],
            new_record["Required additional equipment/ clothes"],
            new_record["Important information"],
        )
        cursor.execute(query, values)
        new_record_id = cursor.lastrowid
        # connection.commit()
    return new_record_id


def add_comments(comments: list, author: str, company_id: int):
    for comment in comments:
        with sqlite3.connect("database.sqlite3") as connection:
            cursor = connection.cursor()
            query = f"""INSERT INTO
            comments (`Content`, `Author`, `Creation date`, `company_id`)
            values (?, ?, strftime('%Y-%m-%d %H:%M', 'now', 'localtime'), ?)"""
            values = (comment, author, company_id)
            cursor.execute(query, values)
    return True

def get_comments(company_id: int):
    with sqlite3.connect("database.sqlite3") as db:
        query = """
        SELECT *
        FROM comments
        WHERE company_id = ?
        """
        comments = db.execute(query, (company_id, )).fetchall()
    result = []
    for comment in comments:
        new_comment = {
            "Content": comment[1],
            "Author": comment[2],
            "Creation date": comment[3],
        }
        result.append(new_comment)
    return result

def edit_company(edited_record: dict):
    print('--------------------')
    print(edited_record)
    # with sqlite3.connect("database.sqlite3") as connection:
    #     cursor = connection.cursor()
    #     query = f"""UPDATE companies
    #     SET `Company name` = ?, `Field of work` = ?, `Address` = ?, `Name of Mentor/ Contact person` = ?, `Phone number` = ?, `Email` = ?, `Website` = ?, `Max number of students` = ?, `Current student count` = ?, `Status` = ?, `Commute` = ?, `Required additional equipment/ clothes` = ?, `Important information` = ?, `Last update` = strftime('%Y-%m-%d %H:%M', 'now', 'localtime')
    #     WHERE id = ?"""
    #     values = (
    #         edited_record["Company name"],
    #         edited_record["Field of work"],
    #         edited_record["Address"],
    #         edited_record["Name of Mentor/ Contact person"],
    #         edited_record["Phone number"],
    #         edited_record["Email"],
    #         edited_record["Website"],
    #         edited_record["Max number of students"],
    #         edited_record["Current student count"],
    #         edited_record["Status"],
    #         edited_record["Commute"],
    #         edited_record["Required additional equipment/ clothes"],
    #         edited_record["Important information"],
    #         edited_record["id"],
    #     )
    #     cursor.execute(query, values)
    return True


def edit_comments(comments, user, company_id):
    print('+++++++++++++++++++++')
    print(comments, user, company_id)
    return comments