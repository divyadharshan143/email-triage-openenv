from models import Email, Observation, Action, Reward
import random


def generate_random_emails(n=3):
    data = [
        ("amazon@shop.com", "Order shipped", "normal"),
        ("spam@ads.com", "Win iPhone", "spam"),
        ("boss@company.com", "Project update", "important"),
        ("newsletter@news.com", "Daily news", "normal"),
        ("promo@shop.com", "Big sale", "spam"),
        ("ceo@company.com", "Urgent meeting", "important"),
        ("friend@mail.com", "Weekend plans", "normal"),
        ("ads@random.com", "Earn money fast", "spam"),
        ("team@company.com", "Weekly sync", "important"),
    ]

    emails = []
    for i in range(1, n + 1):
        sender, subject, etype = random.choice(data)
        emails.append(Email(id=i, sender=sender, subject=subject, type=etype))

    return emails


class EmailEnv:

    def __init__(self):
        self.emails = []

    def reset(self, difficulty="easy"):
        random.seed(42)  # ✅ reproducibility

        if difficulty == "easy":
            self.emails = generate_random_emails(3)
        elif difficulty == "medium":
            self.emails = generate_random_emails(5)
        else:
            self.emails = generate_random_emails(10)

        return Observation(emails=self.emails)

    def state(self):
        return Observation(emails=self.emails)

    def step(self, action: Action):
        email = next((e for e in self.emails if e.id == action.email_id), None)

        if not email:
            return Observation(emails=self.emails), Reward(value=-1), False, {}

        if email.type == "spam":
            if action.action_type == "delete":
                reward = 1
            elif action.action_type == "archive":
                reward = 0.5
            else:
                reward = -1

        elif email.type == "important":
            if action.action_type == "reply":
                reward = 1
            elif action.action_type == "archive":
                reward = 0.5
            else:
                reward = -1

        else:
            if action.action_type == "archive":
                reward = 1
            elif action.action_type == "reply":
                reward = 0.5
            else:
                reward = -1

        self.emails = [e for e in self.emails if e.id != action.email_id]

        done = len(self.emails) == 0

        return Observation(emails=self.emails), Reward(value=reward), done, {}