import json
from datetime import date
from pathlib import Path

DATA_FILE = Path('calorie_data.json')

def load_data():
    if DATA_FILE.exists():
        with DATA_FILE.open() as f:
            return json.load(f)
    return {"goal": 2000, "streak": 0, "records": {}}

def save_data(data):
    with DATA_FILE.open('w') as f:
        json.dump(data, f, indent=2)

def log_calories(amount):
    data = load_data()
    d = str(date.today())
    data['records'].setdefault(d, 0)
    data['records'][d] += amount
    save_data(data)
    print(f"Logged {amount} calories for {d}.")

def end_day():
    data = load_data()
    d = str(date.today())
    total = data['records'].get(d, 0)
    goal = data['goal']
    if total >= goal:
        data['streak'] += 1
        print(f"Congrats! You hit your goal with {total} calories.")
        if data['streak'] >= 3:
            print("Streak is 3! You earned $20.")
    else:
        print(f"You only logged {total} calories, under the goal of {goal}.")
        if data['streak'] != 0:
            print("Streak reset.")
        data['streak'] = 0
    save_data(data)


def show_status():
    data = load_data()
    d = str(date.today())
    total = data['records'].get(d, 0)
    goal = data['goal']
    print(f"Today: {total}/{goal} calories")
    print(f"Current streak: {data['streak']} day(s)")


def set_goal(amount):
    data = load_data()
    data['goal'] = amount
    save_data(data)
    print(f"New daily goal set to {amount} calories.")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Simple calorie tracker")
    subparsers = parser.add_subparsers(dest='command')

    log_parser = subparsers.add_parser('log', help='Log calories for today')
    log_parser.add_argument('amount', type=int, help='Calories to add')

    subparsers.add_parser('status', help='Show today\'s progress')
    subparsers.add_parser('end', help='Finalize today and update streak')

    goal_parser = subparsers.add_parser('setgoal', help='Set new calorie goal')
    goal_parser.add_argument('amount', type=int)

    args = parser.parse_args()

    if args.command == 'log':
        log_calories(args.amount)
    elif args.command == 'status':
        show_status()
    elif args.command == 'end':
        end_day()
    elif args.command == 'setgoal':
        set_goal(args.amount)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
