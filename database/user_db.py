from database.connection import get_connection

def create_user(name, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO users(full_name,email,password)
    VALUES(%s,%s,%s)
    """

    cursor.execute(query,(name,email,password))

    conn.commit()

    cursor.close()
    conn.close()


def get_user_by_email(email):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user