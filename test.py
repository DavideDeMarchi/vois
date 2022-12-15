import unittest

from vois import geojsonUtils


class Text_geojsonUtils(unittest.TestCase):

    def test_geojsonLoadFile(self):
        """
        Test geojsonLoadFile
        """
        result = geojsonUtils.geojsonLoadFile('./vois/data/example.geojson')
        self.assertEqual(len(result), 163690)

        
    def test_geojsonCount(self):
        """
        Test geojsonCount
        """
        geojson = geojsonUtils.geojsonLoadFile('./vois/data/ItalyProvinces.geojson')
        result = geojsonUtils.geojsonCount(geojson)
        self.assertEqual(result, 107)


if __name__ == '__main__':
    unittest.main()