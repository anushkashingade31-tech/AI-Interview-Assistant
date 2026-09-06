from database.connection import get_connection


# --------------------------------------------------
# SAVE ANSWER
# --------------------------------------------------

def save_answer(
    interview_id,
    question,
    user_answer,
    voice_analysis=None
):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO answers
    (
        interview_id,
        question,
        user_answer,
        voice_duration,
        words_per_minute,
        pause_count,
        silence_percentage,
        voice_energy,
        confidence_indicator
    )
    VALUES
    (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    )
    """

    # ----------------------------------------------
    # VOICE ANSWER
    # ----------------------------------------------

    if voice_analysis:

        values = (
            interview_id,
            question,
            user_answer,

            voice_analysis.get("duration"),
            voice_analysis.get("words_per_minute"),
            voice_analysis.get("pause_count"),
            voice_analysis.get("silence_percentage"),
            voice_analysis.get("voice_energy"),
            voice_analysis.get("confidence_indicator")
        )

    # ----------------------------------------------
    # TEXT ANSWER
    # ----------------------------------------------

    else:

        values = (
            interview_id,
            question,
            user_answer,

            None,
            None,
            None,
            None,
            None,
            None
        )

    cursor.execute(query, values)

    conn.commit()

    answer_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return answer_id


# --------------------------------------------------
# GET ANSWERS
# --------------------------------------------------

def get_answers(interview_id):

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM answers
        WHERE interview_id = %s
        ORDER BY answer_id
        """,
        (interview_id,)
    )

    answers = cursor.fetchall()

    cursor.close()
    conn.close()

    return answers


# --------------------------------------------------
# UPDATE AI EVALUATION
# --------------------------------------------------

def update_answer_evaluation(
    answer_id,
    score,
    feedback,
    ideal_answer
):

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
