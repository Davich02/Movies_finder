import pymysql

config = {
         'host': 'ich-db.edu.itcareerhub.de',
         'user': 'ich1',
         'password': 'password',
         'database': 'sakila',
     }


with pymysql.connect(**config) as conn:
    with conn.cursor() as cursor:
        '''cursor.execute('SHOW TABLES')
        tables = cursor.fetchall()
        for table in tables:
            print(table)'''
        cursor.execute('DESCRIBE film')
        film = cursor.fetchall()
        for film in film:
            print(film)
        cursor.execute('DESCRIBE category')
        category = cursor.fetchall()
        for category in category:
            print(category)
        cursor.execute('DESCRIBE film_category')
        film_category = cursor.fetchall()
        for film_category in film_category:
            print(film_category)








