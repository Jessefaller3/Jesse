import json
from datetime import date, timedelta
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


def log_item(food: str, calories: int) -> None:
    """Record a food item and calorie amount for today."""
    data = load_data()
    d = str(date.today())
    day = data['records'].setdefault(d, {"total": 0, "items": []})
    day['items'].append({"food": food, "calories": calories})
    day['total'] += calories
    save_data(data)
    print(f"Logged {calories} calories for '{food}' on {d}.")


def end_day() -> None:
    """Finalize the current day and update streak information."""
    data = load_data()
    d = str(date.today())
    day = data['records'].get(d, {"total": 0})
    total = day.get('total', 0)
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


def show_status() -> None:
    """Display today's calorie total and current streak."""
    data = load_data()
    d = str(date.today())
    day = data['records'].get(d, {"total": 0})
    total = day.get('total', 0)
    goal = data['goal']
    print(f"Today: {total}/{goal} calories")
    print(f"Current streak: {data['streak']} day(s)")


def set_goal(amount: int) -> None:
    """Set a new daily calorie goal."""
    data = load_data()
    data['goal'] = amount
    save_data(data)
    print(f"New daily goal set to {amount} calories.")


def show_history(days: int = 7) -> None:
    """Display calorie totals for the last `days` days."""
    data = load_data()
    today = date.today()
    for i in range(days):
        d = str(today - timedelta(days=i))
        day = data['records'].get(d)
        if day:
            print(f"{d}: {day['total']} calories")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Simple calorie tracker")
    subparsers = parser.add_subparsers(dest='command')

    log_parser = subparsers.add_parser('log', help='Log calories for today')
    log_parser.add_argument('food', help='Name of the food item')
    log_parser.add_argument('calories', type=int, help='Calories for the item')

    subparsers.add_parser('status', help="Show today's progress")
    subparsers.add_parser('end', help='Finalize today and update streak')

    goal_parser = subparsers.add_parser('setgoal', help='Set new calorie goal')
    goal_parser.add_argument('amount', type=int)

    hist_parser = subparsers.add_parser('history', help='Show calorie totals from previous days')
    hist_parser.add_argument('--days', type=int, default=7, help='How many days to show')

    args = parser.parse_args()

    if args.command == 'log':
        log_item(args.food, args.calories)
    elif args.command == 'status':
        show_status()
    elif args.command == 'end':
        end_day()
    elif args.command == 'setgoal':
        set_goal(args.amount)
    elif args.command == 'history':
        show_history(args.days)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
