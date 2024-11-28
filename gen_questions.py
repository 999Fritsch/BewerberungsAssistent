import sqlite3
from IQG import InterviewQuestionGenerator
import random

def get_position(cursor, position_id):
    cursor.execute("SELECT * FROM position WHERE id = ?", (position_id,))
    return cursor.fetchone()

def get_skillset(cursor, position_id):
    cursor.execute("""
        SELECT skillset.*, skill.name
        FROM skillset
        JOIN skill ON skill.id = skillset.skill
        JOIN position ON position.skillset = skillset.id
        WHERE position.id = ?
    """, (position_id,))
    return cursor.fetchall()

def get_all_skills(cursor):
    cursor.execute("SELECT id, name FROM skill")
    return cursor.fetchall()

def generate_and_insert_questions(position_id, N):
    connection = sqlite3.connect("./data/assessment.db")
    cursor = connection.cursor()

    position = get_position(cursor, position_id)
    skillset = get_skillset(cursor, position_id)

    print("Position:", position)
    print("Skillset:", skillset)

    # Initialize the InterviewQuestionGenerator
    local_model = "Mistral-Nemo-Instruct-2407-Q4_K_M.gguf"
    iqg = InterviewQuestionGenerator(local_model)

    # Generate a question for each skill and save it to the database
    cursor.execute("SELECT max(id) FROM questionset")
    current_questionset_id = cursor.fetchone()[0]
    if current_questionset_id is not None:
        next_questionset_id = current_questionset_id + 1
    else:
        next_questionset_id = 1
    for skill in skillset:
        _, skill_id, skill_grade, skill_name = skill
        questions = iqg.generate_interview_questions(f"{skill_name}, {skill_grade}", N)

        for question in questions:
            # Insert the question into the database
            cursor.execute(
                "INSERT INTO question (description, skill, grade) VALUES (?, ?, ?)" "RETURNING id",
                (question.question, skill_id, random.randint(1,3))  # Assuming 'Experte' as the grade
            )
            question_id = cursor.fetchone()
            cursor.execute(
                "INSERT INTO questionset (id, question) VALUES (?, ?)",
                (next_questionset_id, question_id[0])  # Assuming 'Experte' as the grade
            )
            cursor.execute(
                "UPDATE position SET questionset = ? WHERE id = ?",
                (next_questionset_id, position_id)
            )

    connection.commit()
    connection.close()

if __name__ == "__main__":
    generate_and_insert_questions(4, 1)
    generate_and_insert_questions(16, 1)