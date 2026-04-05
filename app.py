import gradio as gr
import pandas as pd
from environment import EmailEnv
from models import Action, Email
from tasks import grade

# -----------------------------
# 🔥 SMART AGENT
# -----------------------------
def smart_agent(email):
    subject = email.subject.lower()

    if "win" in subject or "free" in subject or "offer" in subject:
        return "delete"
    elif "urgent" in subject or "meeting" in subject or "project" in subject:
        return "reply"
    else:
        return "archive"

# -----------------------------
# INIT
# -----------------------------
env = EmailEnv()
obs = env.reset("easy")

# -----------------------------
# 📩 LOAD RANDOM EMAILS
# -----------------------------
def load_emails(difficulty):
    global obs
    obs = env.reset(difficulty)

    email_text = ""

    for e in obs.emails:
        suggestion = smart_agent(e)

        email_text += (
            f"{e.id}. {e.sender} | {e.subject} ({e.type})\n"
            f"   👉 Suggested: {suggestion}\n\n"
        )

    return email_text

# -----------------------------
# 📤 UPLOAD EMAILS (CSV)
# -----------------------------
def upload_emails(file):
    global obs

    df = pd.read_csv(file.name)

    emails = []
    text = ""

    for i, row in df.iterrows():
        email_obj = Email(
            id=i + 1,
            sender=row["sender"],
            subject=row["subject"],
            type=row["type"]
        )

        emails.append(email_obj)

        suggestion = smart_agent(email_obj)

        text += (
            f"{email_obj.id}. {email_obj.sender} | {email_obj.subject} ({email_obj.type})\n"
            f"   👉 Suggested: {suggestion}\n\n"
        )

    env.emails = emails
    obs = env.state()

    return text

# -----------------------------
# 🤖 AUTO SOLVE
# -----------------------------
def auto_solve():
    actions = []

    for e in obs.emails:
        actions.append(smart_agent(e))

    while len(actions) < 10:
        actions.append(None)

    return actions

# -----------------------------
# ⚡ PROCESS ACTIONS
# -----------------------------
def process_emails(*actions):
    try:
        action_objs = []

        for i, act in enumerate(actions):
            if act is not None:
                action_objs.append(Action(email_id=i + 1, action_type=act))

        total_reward = 0
        output = ""

        for action in action_objs:
            _, reward, _, _ = env.step(action)
            total_reward += reward.value

            output += f"Email {action.email_id} → {action.action_type} → Reward: {reward.value}\n"

        score = grade(action_objs, env.emails)

        output += f"\n  Total Reward: {total_reward}"
        output += f"\n  Score: {score}"

        return output

    except Exception as e:
        return str(e)

# -----------------------------
# 🎨 UI
# -----------------------------
with gr.Blocks() as demo:
    gr.Markdown("Smart Email Triage System (AI Powered)")

    difficulty = gr.Dropdown(
        ["easy", "medium", "hard"],
        value="easy",
        label="Difficulty"
    )

    email_box = gr.Textbox(label="Emails + AI Suggestions", lines=15)

    # 🔘 Buttons
    load_btn = gr.Button("📩 Load Random Emails")
    file_input = gr.File(label="📤 Upload Emails (CSV)")
    upload_btn = gr.Button("Upload Emails")

    # 🔽 Action dropdowns
    actions = []
    for i in range(10):
        actions.append(
            gr.Dropdown(
                ["delete", "reply", "archive"],
                label=f"Email {i+1} Action"
            )
        )

    # 🤖 Auto + Process
    auto_btn = gr.Button("Auto Solve (AI)")
    process_btn = gr.Button("Process")

    output = gr.Textbox(label="Result", lines=15)

    # 🔗 Connect actions
    load_btn.click(load_emails, inputs=difficulty, outputs=email_box)
    upload_btn.click(upload_emails, inputs=file_input, outputs=email_box)
    auto_btn.click(auto_solve, outputs=actions)
    process_btn.click(process_emails, inputs=actions, outputs=output)

demo.launch()