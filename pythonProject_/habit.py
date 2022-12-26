# class Habit
class Habit:
    def __init__(self, name: str, description: str, periodicity: str):
        self.name = name
        self.description = description
        self.periodicity = periodicity

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
        """
