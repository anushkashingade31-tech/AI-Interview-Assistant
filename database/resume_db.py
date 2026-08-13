from database.connection import get_connection

def save_resume(user_id, file_name, file_path):

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO resumes
    (user_id, file_name, file_path)
    VALUES
    (%s, %s, %s)
    """

    cursor.execute(
        sql,
        (
            user_id,
            file_name,
            file_path
        )
    )

    conn.commit()

    cursor.close()
    conn.close()


def get_user_resumes(user_id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM resumes WHERE user_id=%s",
        (user_id,)
    )

    resumes = cursor.fetchall()

    cursor.close()
    conn.close()

    return resumes