from db import add_habit_daily, add_habit_weekly


# class Habit
class Habit:
    """
                            A class used to represent a habit
                            Attributes
                            ----------
                            name: str
                                the name of the habit
                            description: str
                                the description of the habit
                            periodicity: str
                                the periodicity, daily or weekly

                            Methods
                            -------
                            store_daily()
                            function to store the daily habits in the database
                            store_weekly()
                            function to store weekly habits in the database

    """
    def __init__(self, name: str, description: str, periodicity: str):
        self.name = name
        self.description = description
        self.periodicity = periodicity

    def store_daily(self, db):
        add_habit_daily(db, self.name, self.description, self.periodicity)

    def store_weekly(self, db):
        add_habit_weekly(db, self.name, self.description, self.periodicity)
