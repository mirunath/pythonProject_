from db import get_db, check, reset, predefined
from freezegun import freeze_time


# the Test class
# tests the most important functions

class Test:
    """
    Methods
    -------
    setup_method()
        create the test db
    test_predefined()
        test the predefined habits(add them to test db)
    test_reset()
        test the reset function in case the user broke the streak
    test_check()
        test the check function
    """

    def setup_method(self):
        self.db = get_db("test.db")

    def test_predefined(self):
        predefined(self.db)

    @freeze_time('2023-02-01')
    def test_reset(self):
        reset(self.db)
        l_habit = self.db.execute('SELECT * FROM habit')
        assert list(l_habit.fetchall()) == [('Swim', 'Daily', 'health', '2023-02-01', '2023-02-02', 0),
                                            ('Walk', 'Daily', 'health', '2023-02-01', '2023-02-02', 0),
                                            ('Yoga', 'Weekly', 'mindfulness', '2023-02-01', '2023-02-08', 0),
                                            ('Code', 'Daily', 'become better', '2023-02-01', '2023-02-02', 0),
                                            ('Meditate', 'Weekly', 'mindfulness', '2023-02-01', '2023-02-08', 0)]

    @freeze_time('2023-02-01')
    def test_check(self):
        check(self.db)
        habit_list = self.db.execute('SELECT * FROM habit')
        assert list(habit_list.fetchall()) == [('Swim', 'Daily', 'health', '2023-02-01', '2023-02-02', 0),
                                               ('Walk', 'Daily', 'health', '2023-02-01', '2023-02-02', 0),
                                               ('Yoga', 'Weekly', 'mindfulness', '2023-02-01', '2023-02-08', 0),
                                               ('Code', 'Daily', 'become better', '2023-02-01', '2023-02-02', 0),
                                               ('Meditate', 'Weekly', 'mindfulness', '2023-02-01', '2023-02-08', 0)]
