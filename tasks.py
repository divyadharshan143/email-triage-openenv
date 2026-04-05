from models import Action


# ----------- Correct action logic -----------

def correct_action(email):
    if email.type == "spam":
        return "delete"
    elif email.type == "important":
        return "reply"
    elif email.type == "normal":
        return "archive"


# ----------- SAFE GRADER FUNCTION -----------

def grade(actions, emails):
    correct = 0
    total = len(emails)

    for action in actions:
        email = next((e for e in emails if e.id == action.email_id), None)

        # ❌ invalid action
        if not email:
            correct -= 0.5
            continue

        if action.action_type == correct_action(email):
            correct += 1
        else:
            correct -= 0.5   # ❌ penalty for wrong action

    # Normalize score between 0 and 1
    score = correct / total if total > 0 else 0

    return max(0.0, min(1.0, score))


# ----------- TASK-SPECIFIC GRADERS -----------

def easy_grader(actions, emails):
    return grade(actions, emails)


def medium_grader(actions, emails):
    score = grade(actions, emails)
    return score * 0.9   # slightly stricter


def hard_grader(actions, emails):
    score = grade(actions, emails)
    return score * 0.8   # strict grading


# ----------- TASK DEFINITIONS -----------

def easy_task():
    return {
        "name": "Easy Task",
        "description": "Classify 3 emails correctly (spam, normal, important)",
        "num_emails": 3,
        "grader": easy_grader
    }


def medium_task():
    return {
        "name": "Medium Task",
        "description": "Handle 5 emails with fewer mistakes allowed",
        "num_emails": 5,
        "grader": medium_grader
    }


def hard_task():
    return {
        "name": "Hard Task",
        "description": "Handle 10 emails with strict grading and penalties",
        "num_emails": 10,
        "grader": hard_grader
    }