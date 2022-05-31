from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
from faker import Faker

app = Flask(__name__)
mysql = MySQL()
fake = Faker()

# mysql configuration
app.config['MYSQL_DATABASE_USER'] = 'vaib'
app.config['MYSQL_DATABASE_PASSWORD'] = 'qwe123'
app.config['MYSQL_DATABASE_DB'] = 'join_us'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

drop_table_sql = """drop table if exists users"""
create_table_sql = """
                CREATE TABLE users(
                    email VARCHAR(100) PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT NOW()
                );
                """

try:

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(drop_table_sql)
    cursor.execute(create_table_sql)
    the_table = []
    row = {}
    for i in range(500):
        row = [fake.email(), fake.date_time()]
        if row in the_table:
            pass
        the_table.append(row)
        cursor.execute('INSERT INTO users(email,created_at)\
                        VALUES ("%s","%s")' % (row[0], row[1]))
    cursor.execute('SELECT * FROM users;')
    records = len(cursor.fetchall())
    print("Records Inserted: %s" % records)
    conn.commit()
except Exception as e:
    print(e)
finally:
    cursor.close()
    conn.close()


@ app.route("/", methods=['get', 'POST'])
def home():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        if request.method == 'POST':
            _email = request.form['email']
            print(_email)
            cursor.execute('INSERT INTO users(email)\
                            VALUES ("%s");' % (_email))
            conn.commit()

        cursor.execute('SELECT * FROM users;')
        records = len(cursor.fetchall())
        cursor.close()
        conn.close()
        print(records)
        return render_template('home.html', data=records)

    except Exception as e:
        return json.dumps({'error': str(e)})


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
