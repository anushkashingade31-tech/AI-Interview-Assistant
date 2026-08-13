from database.connection import get_connection


def create_interview(user_id, total_questions):

    conn = get_connection()

    cursor = conn.cursor()

    sql = """
    INSERT INTO interviews
    (
        user_id,
        total_questions
    )
    VALUES
    (
        %s,
        %s
    )
    """

    cursor.execute(
        sql,
        (
            user_id,
            total_questions
        )
    )

    conn.commit()

    interview_id = cursor.lastrowid

    cursor.close()

    conn.close()

    return interview_id

def update_score(interview_id, score):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """
        UPDATE interviews
        SET total_score=%s
        WHERE interview_id=%s
        """,

        (
            score,
            interview_id
        )

    )

    conn.commit()

    cursor.close()

    conn.close()

def get_interviews(user_id):

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute(

        """
        SELECT *
        FROM interviews
        WHERE user_id=%s
        ORDER BY interview_date DESC
        """,

        (
            user_id,
        )

    )

    interviews = cursor.fetchall()

    cursor.close()

    conn.close()

    return interviews

def get_total_interviews(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM interviews
        WHERE user_id=%s
        """,
        (user_id,)
    )

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return total

def get_average_score(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT AVG(overall_score)

        FROM interviews

        WHERE user_id=%s
        """,
        (user_id,)
    )

    result = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    if result is None:
        return 0

    return round(result, 2)

def get_highest_score(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT MAX(overall_score)

        FROM interviews

        WHERE user_id=%s
        """,
        (user_id,)
    )

    result = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    if result is None:
        return 0

    return round(result, 2)

def update_overall_score(interview_id, overall_score):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE interviews
        SET overall_score=%s
        WHERE interview_id=%s
        """,
        (
            overall_score,
            interview_id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

def get_interview_history(user_id):

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            interview_id,
            interview_date,
            total_questions,
            overall_score

        FROM interviews

        WHERE user_id=%s

        ORDER BY interview_date DESC
        """,
        (user_id,)
    )

    interviews = cursor.fetchall()

    cursor.close()

    conn.close()

    return interviews

def get_user_interview_count(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM interviews
        WHERE user_id = %s
        """,
        (user_id,)
    )

    count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return count