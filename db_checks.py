from db import cursor, mydb


def create_user(discord_id, discord_name, email):
    sql = "INSERT INTO users (discord_id, discord_name, email) VALUES (%s, %s, %s)"
    user = (discord_id, discord_name, email)
    cursor.execute(sql, user)
    mydb.commit()


def get_user(discord_id):
    cursor.execute(f"SELECT * from users where discord_id = {discord_id}")
    user = cursor.fetchone()

    return user
