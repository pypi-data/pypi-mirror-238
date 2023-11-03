import unittest

from context import geo


class TestCoord(unittest.TestCase):
    def test_isclose(self):
        coord1 = geo.Coord(50, 40)
        coord2 = geo.Coord(50.4, 40.3)
        coord3 = geo.Coord(50, 43)

        self.assertTrue(coord1.isclose(coord2))
        self.assertFalse(coord1.isclose(coord3))

    def test_get_distance(self):
        dist1 = geo.Coord(0, 0).get_distance(geo.Coord(0, 90)).km
        dist2 = geo.Coord(0, 0).get_distance(geo.Coord(0, -90)).km
        dist3 = geo.Coord(
            42.3541165, -71.0693514).get_distance(geo.Coord(40.7791472, -73.9680804)).km

        self.assertTrue(dist1 * 0.999 < 10018.75 < dist1 * 1.001,
                        f"Got: {dist1}, expected: 10018.75")

        self.assertTrue(dist2 * 0.999 < 10018.75 < dist2 * 1.001,
                        f"Got: {dist2}, Expected: 10018.75")

        self.assertTrue(dist3 * 0.999 < 298.396 < dist3 * 1.001,
                        f"Got: {dist3}, Expected: 298.396")

    def test_get_bearing(self):
        brg1 = geo.Coord(0, 0).get_bearing(geo.Coord(0, 90))
        brg2 = geo.Coord(0, 0).get_bearing(geo.Coord(0, -90))
        brg3 = geo.Coord(-30, 0).get_bearing(geo.Coord(-10, 180))
        brg4 = geo.Coord(
            42.3541165, -71.0693514).get_bearing(geo.Coord(40.7791472, -73.9680804))

        self.assertTrue(brg1 - 0.01 < 90 < brg1 + 0.01,
                        f"Got: {brg1}, Expected: 90.0")

        self.assertTrue(brg2 - 0.01 < 270 < brg2 + 0.01,
                        f"Got: {brg2}, Expected: 270.0")

        self.assertTrue(brg3 - 0.01 < 180 < brg3 + 0.01,
                        f"Got: {brg3}, Expected: 180.0")

        self.assertTrue(brg4 - 0.01 < 235.08 < brg4 + 0.01,
                        f"Got: {brg4}, Expected: 235.08")
