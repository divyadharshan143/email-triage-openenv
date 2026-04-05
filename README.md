---
title: Email Env Gradio
emoji: 🦀
colorFrom: pink
colorTo: indigo
sdk: gradio
sdk_version: 6.10.0
app_file: app.py
pinned: false
---

# 📧 Email Triage Environment

## Description
This project simulates a real-world email triage system where an agent decides how to handle incoming emails.

## Action Space
- delete
- reply
- archive

## Observation Space
List of emails with:
- sender
- subject
- type (spam, important, normal)

## Tasks
- Easy: 3 emails  
- Medium: 5 emails  
- Hard: 10 emails  

## Reward
+1 for correct action  
-1 or -0.5 for incorrect action  

## Baseline
Baseline score: 1.0

## How to Run
```bash
python app.py