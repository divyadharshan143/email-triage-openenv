from environment import EmailEnv
from models import Action
from tasks import grade

def policy_from_obs(obs):
    actions = []
    for email in obs.emails:
        if email.type == "spam":
            act = "delete"
        elif email.type == "important":
            act = "reply"
        else:
            act = "archive"
        actions.append(Action(email_id=email.id, action_type=act))
    return actions

def run_episode():
    env = EmailEnv()
    obs = env.reset()

    actions = policy_from_obs(obs)

    total_reward = 0
    for action in actions:
        obs, reward, done, info = env.step(action)
        total_reward += reward.value

    score = grade(actions, env.emails)
    return total_reward, score

if __name__ == "__main__":
    reward, score = run_episode()
    print("Baseline Reward:", reward)
    print("Baseline Score:", score)