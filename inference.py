import os
from openai import OpenAI
from environment import EmailEnv
from models import Action
from tasks import easy_task, medium_task, hard_task, grade

# 🔐 Read environment variables
API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=OPENAI_API_KEY
)

env = EmailEnv()

tasks = [
    ("easy", easy_task()),
    ("medium", medium_task()),
    ("hard", hard_task())
]

print("[START]")

for difficulty, task in tasks:

    def reset(self, difficulty="easy", num_emails=3):
    original_emails = obs.emails.copy()

    actions = []
    total_reward = 0
    done = False

    while not done:
        for e in obs.emails:

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are an email assistant."},
            {
                "role": "user",
                "content": f"Email subject: {e.subject}. What action should be taken? Choose only one: delete, reply, archive."
            }
        ],
        temperature=0
    )

    act = response.choices[0].message.content.strip().lower()

    # safety fallback (VERY IMPORTANT)
    if act not in ["delete", "reply", "archive"]:
        act = "archive"

            action = Action(email_id=e.id, action_type=act)

            obs, reward, done, _ = env.step(action)

            actions.append(action)
            total_reward += reward.value

            print(f"[STEP] task={task['name']} email_id={action.email_id} action={action.action_type} reward={reward.value}")

            if done:
                break

    # ✅ Correct grading
    score = grade(actions, original_emails)

    print(f"[STEP] task={task['name']} total_reward={total_reward} score={score}")

print("[END]")