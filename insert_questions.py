import sqlite3

conn = sqlite3.connect("quiz.db")
c = conn.cursor()

questions = [
    {
        "question": "In the Waterfall Model, which phase comes right after Requirements Analysis?",
        "option1": "Design",
        "option2": "Testing",
        "option3": "Deployment",
        "option4": "Maintenance",
        "answer": "Design"
    },
    {
        "question": "A major drawback of the Waterfall Model is:",
        "option1": "Lack of documentation",
        "option2": "Difficult to accommodate changes",
        "option3": "Heavy customer involvement",
        "option4": "Slow testing process",
        "answer": "Difficult to accommodate changes"
    },
    {
        "question": "The Incremental Model delivers software:",
        "option1": "All at once",
        "option2": "In increments over time",
        "option3": "After complete testing",
        "option4": "Only after customer approval",
        "answer": "In increments over time"
    },
    {
        "question": "The Prototyping Model is most useful when:",
        "option1": "Requirements are unclear",
        "option2": "Requirements are complete",
        "option3": "Testing is unnecessary",
        "option4": "Budget is unlimited",
        "answer": "Requirements are unclear"
    },
    {
        "question": "In the Spiral Model, each loop of the spiral represents:",
        "option1": "Only coding",
        "option2": "A complete software release",
        "option3": "A phase of the software process",
        "option4": "A maintenance phase",
        "answer": "A phase of the software process"
    },
    {
        "question": "RAD Model focuses on:",
        "option1": "Long development cycles",
        "option2": "Very high documentation",
        "option3": "Rapid application development",
        "option4": "No customer interaction",
        "answer": "Rapid application development"
    },
    {
        "question": "The Concurrent Model allows:",
        "option1": "Activities to occur sequentially",
        "option2": "Activities to overlap",
        "option3": "No iterations",
        "option4": "No user feedback",
        "answer": "Activities to overlap"
    },
    {
        "question": "The Unified Process is:",
        "option1": "A linear model",
        "option2": "A purely incremental model",
        "option3": "A use-case–driven, iterative model",
        "option4": "A waterfall-based model",
        "answer": "A use-case–driven, iterative model"
    },
    {
        "question": "Agile methods focus primarily on:",
        "option1": "Heavy documentation",
        "option2": "Rigid processes",
        "option3": "Customer collaboration",
        "option4": "Late delivery",
        "answer": "Customer collaboration"
    },
    {
        "question": 'In Agile, "Customer in Agile Methods" refers to:',
        "option1": "Customer writes code",
        "option2": "Customer is part of the development team",
        "option3": "Customer only gives initial requirements",
        "option4": "Customer is not involved",
        "answer": "Customer is part of the development team"
    }
]

for q in questions:
    c.execute(
        "INSERT INTO questions (question, option1, option2, option3, option4, answer) VALUES (?, ?, ?, ?, ?, ?)",
        (q["question"], q["option1"], q["option2"], q["option3"], q["option4"], q["answer"])
    )

conn.commit()
conn.close()
print("Sample questions inserted successfully!")
