# Calorie Tracker

This repository contains a simple command-line calorie tracking tool written in Python.

## Usage

```
python3 calorie_tracker.py [command] [arguments]
```

### Commands
- `log <amount>` – add calories to today.
- `status` – show today's total and your current streak.
- `end` – finalize today, check if you met your goal, and update the streak.
- `setgoal <amount>` – change your daily calorie goal.

The app stores data in `calorie_data.json` in the project directory.

A streak of three consecutive days meeting your goal will trigger a message telling you that you've earned $20 to spend as you like.
