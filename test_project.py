from db import get_db, check, reset, predefined, maximum_given
from freezegun import freeze_time


# the Test class
# tests the most important functions
class Test:
    """
    Methods
    -------
    setup_method()
        create the test db
        add the predefined habits to test db
    test_check_daily()
        test the reset function in case the user broke the daily streak
        shows the streak
    test_check_weekly()
        test the reset function in case the user broke the weekly streak
        shows the streak
    """

    @freeze_time('2023-02-01')
    def setup_method(self):
        self.db = get_db("test.db")
        predefined(self.db)
        check(self.db, "Swim")
        check(self.db, "Yoga")
        check(self.db, "Swim")
        check(self.db, "Yoga")
        check(self.db, "Swim")
        check(self.db, "Yoga")

    @freeze_time('2023-02-04')
    def test_check_daily(self):
        reset(self.db)
        maximum_given(self.db, "Swim")

    @freeze_time('2023-03-01')
    def test_check_weekly(self):
        reset(self.db)
        maximum_given(self.db, "Yoga")
