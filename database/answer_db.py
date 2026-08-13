from database.connection import get_connection


def save_answer(interview_id, question, user_answer):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO answers
    (
        interview_id,
        question,
        user_answer
    )
    VALUES
    (
        %s,
        %s,
        %s
    )
    """

    cursor.execute(
        query,
        (
            interview_id,
            question,
            user_answer
        )
    )

    conn.commit()

    answer_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return answer_id


def get_answers(interview_id):

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM answers
        WHERE interview_id=%s
        ORDER BY answer_id
        """,
        (interview_id,)
    )

    answers = cursor.fetchall()

    cursor.close()
    conn.close()

    return answers

def update_answer_evaluation(answer_id, score, feedback, ideal_answer):

    conn = get_connection()

    cursor = conn.cursor()

    query = """
    UPDATE answers
    SET
        ai_score = %s,
        feedback = %s,
        ideal_answer = %s
    WHERE answer_id = %s
    """

    cursor.execute(
        query,
        (
            score,
            feedback,
            ideal_answer,
            answer_id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()