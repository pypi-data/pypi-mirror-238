################################################################################
# UNIT TESTS
################################################################################

from interval import *

import unittest


class test_interval_integers(unittest.TestCase):

    def runTest(self):

        interval = Interval(0,100)

        with self.assertRaises(ValueError): interval[101]
        with self.assertRaises(ValueError): interval[-1]

        self.assertEqual(Interval.__str__(interval),
                         "Interval{[0.,100.]: None}")
        self.assertEqual(interval[(0,100)], [None])
        interval[(11,30)] = "a"
        interval[(31,60)] = "b"
        interval[(61,90)] = "c"
        self.assertEqual(Interval.__str__(interval),
                         "Interval{[0.,11.): None, [11.,30.]: 'a', " +
                         "(30.,31.): None, [31.,60.]: 'b', " +
                         "(60.,61.): None, [61.,90.]: 'c', " +
                         "(90.,100.]: None}")

        self.assertEqual(interval[(0,100)], [None, "a", "b", "c"])
        for i in range(0,101):
            if i < 11:
                self.assertEqual(interval[i], None)
            elif i > 10 and i <31:
                self.assertEqual(interval[i], "a")
            elif i > 30 and i < 61:
                self.assertEqual(interval[i], "b")
            elif i > 60 and i < 91:
                self.assertEqual(interval[i], "c")
            else:
                self.assertEqual(interval[i], None)

        interval[(15,45)] = "d"
        self.assertEqual(Interval.__str__(interval),
                         "Interval{[0.,11.): None, [11.,15.): 'a', " +
                         "[15.,45.]: 'd', (45.,60.]: 'b', " +
                         "(60.,61.): None, [61.,90.]: 'c', " +
                         "(90.,100.]: None}")

        self.assertEqual(interval[(0,100)], [None, "a", "b", "c", "d"])
        self.assertEqual(interval[(10,40)], [None, "a", "d"])
        for i in range(0,101):
            if i < 11:
                self.assertEqual(interval[i], None)
            elif i > 10 and i < 15:
                self.assertEqual(interval[i], "a")
            elif i > 14 and i < 46:
                self.assertEqual(interval[i], "d")
            elif i > 45 and i < 61:
                self.assertEqual(interval[i], "b")
            elif i > 60 and i < 91:
                self.assertEqual(interval[i], "c")
            else:
                self.assertEqual(interval[i], None)

        interval[(45,100)] = "e"
        self.assertEqual(interval[(0,100)], [None, "a", "d", "e"])
        for i in range(0,101):
            if i < 11:
                self.assertEqual(interval[i], None)
            elif i > 10 and i < 15:
                self.assertEqual(interval[i], "a")
            elif i > 14 and i < 45:
                self.assertEqual(interval[i], "d")
            elif i > 44 and i < 101:
                self.assertEqual(interval[i], "e")

        interval[(50,60)] = "c"
        self.assertEqual(interval[(0,100)], [None, "a", "d", "e", "c"])
        for i in range(0,101):
            if i < 11:
                self.assertEqual(interval[i], None)
            elif i > 10 and i < 15:
                self.assertEqual(interval[i], "a")
            elif i > 14 and i < 45:
                self.assertEqual(interval[i], "d")
            elif i > 44 and i < 50:
                self.assertEqual(interval[i], "e")
            elif i > 50 and i < 61:
                self.assertEqual(interval[i], "c")
            elif i > 60 and i < 101:
                self.assertEqual(interval[i], "e")

        interval[(-20,20)] = "f"
        self.assertEqual(interval[(0,100)], ["d", "e", "c", "f"])
        self.assertEqual(Interval.__str__(interval),
                         "Interval{[0.,20.]: 'f', (20.,45.): 'd', " +
                         "[45.,50.): 'e', [50.,60.]: 'c', (60.,100.]: 'e'}")

        interval[(90, 110)] = "g"
        self.assertEqual(interval[(0,100)], ["d", "e", "c", "f", "g"])
        self.assertEqual(Interval.__str__(interval),
                         "Interval{[0.,20.]: 'f', (20.,45.): 'd', " +
                         "[45.,50.): 'e', [50.,60.]: 'c', (60.,90.): 'e', " +
                         "[90.,100.]: 'g'}")

        self.assertEqual(interval[(55.5,70.5)], ["e", "c"])

        interval = Interval(0,10)
        interval[(5.1,5.5)] = "a"
        self.assertEqual(interval[(0,10)], [None, "a"])
        self.assertEqual(Interval.__str__(interval),
                         "Interval{[0.,5.1): None, [5.1,5.5]: 'a', " +
                         "(5.5,10.]: None}")

        for i in np.arange(0.0, 10.0, 0.1).tolist():
            if i >= 5.1 and i <= 5.5:
                self.assertEqual(interval[i], "a")
            else:
                self.assertEqual(interval[i], None)

        interval[(5.6,6.1)] = "b"
        self.assertEqual(interval[(0,10)], [None, "a", "b"])
        self.assertEqual(Interval.__str__(interval),
                         "Interval{[0.,5.1): None, [5.1,5.5]: 'a', " +
                         "(5.5,5.6): None, [5.6,6.1]: 'b', (6.1,10.]: None}")

        for i in np.arange(0.0, 10.0, 0.1).tolist():
            if i >= 5.1 and i <= 5.5:
                self.assertEqual(interval[i], "a")
            elif i >= 5.6 and i <= 6.1:
                self.assertEqual(interval[i], "b")
            else:
                self.assertEqual(interval[i], None)


        interval[(5.3,5.8)] = "c"

        self.assertEqual(interval[(0,10)], [None, "a", "b", "c"])
        self.assertEqual(interval[(5.3,5.8)], ["c"])
        self.assertEqual(interval[(5.1,5.9)], ["a", "b", "c"])
        self.assertEqual(interval[(5,6)], [None, "a","b","c"])
        self.assertEqual(interval[(6,7)], [None, "b"])
        self.assertEqual(interval[(5.05,5.06)], [None])

        self.assertEqual(Interval.__str__(interval),
                         "Interval{[0.,5.1): None, [5.1,5.3): 'a', " +
                         "[5.3,5.8]: 'c', (5.8,6.1]: 'b', (6.1,10.]: None}")

        for i in np.arange(0.0, 10.0, 0.1).tolist():
            if i >= 5.1 and i < 5.3:
                self.assertEqual(interval[i], "a")
            elif i >= 5.3 and i <= 5.8:
                self.assertEqual(interval[i], "c")
            elif i > 5.8 and i <= 6.1:
                self.assertEqual(interval[i], "b")
            else:
                self.assertEqual(interval[i], None)
