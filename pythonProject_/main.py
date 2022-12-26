import questionary
from db import get_db, predefined, show_all, show_daily_habits, show_weekly_habits, \
    check, maximum_daily, maximum_weekly, maximum_given, delete_habit, habit_progress, \
    add_habit_daily, add_habit_weekly, reset


def cli():
    db = get_db()
    questionary.confirm("Are you ready?").ask()

    choice = questionary.select(
        "What do you want to do?",
        choices=["Try with predefined", "Create", "Check", "Analyze", "Edit: Delete", "Exit"]
    ).ask()

    reset(db)

    if choice == "Try with predefined":
        predefined(db)
        print("Now you can press on Analyze to see the habits")
        cli()

    elif choice == "Create":
        choice = questionary.select("Choose:",
                                    choices=["Daily", "Weekly"]).ask()
        if choice == "Daily":
            add_habit_daily(db)
        else:
            add_habit_weekly(db)
        cli()

    elif choice == "Check":
        check(db)
        cli()

    elif choice == "Analyze":
        choice = questionary.select("Choose:",
                                    choices=["Show all habits", "Show due date", "Show daily habits",
                                             "Show weekly habits", "Show maximum streak daily",
                                             "Show maximum streak weekly", "Show maximum streak given habit"]).ask()
        if choice == "Show all habits":
            show_all(db)
        elif choice == "Show due date":
            name = questionary.text("What is the name of the habit?").ask()
            habit_progress(db, name)
        elif choice == "Show daily habits":
            show_daily_habits(db)
        elif choice == "Show weekly habits":
            show_weekly_habits(db)
        elif choice == "Show maximum streak daily":
            maximum_daily(db)
        elif choice == "Show maximum streak weekly":
            maximum_weekly(db)
        elif choice == "Show maximum streak given habit":
            name = questionary.text("What is the name of the habit?").ask()
            maximum_given(db, name)
        cli()

    elif choice == "Edit: Delete":
        delete_habit(db)
        cli()

    else:
        print("Bye!")


if __name__ == '__main__':
    cli()
