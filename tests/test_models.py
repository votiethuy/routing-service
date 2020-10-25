import unittest

from athena.models import StationMap
from dateutil.parser import parse

class TestStationMap(unittest.TestCase):
    def setUp(self):
        self.station_map = StationMap()

    def test_location_list(self):
        """
        Test that it can return location list
        """
        self.assertEqual(len(self.station_map.get_location_list()), 136)

    def test_station_list(self):
        """
        Test that it can return line list
        """
        self.assertEqual(len(self.station_map.get_station_list()), 166)

    def test_filter_by_station_name(self):
        """
        Test that it can filter by station name
        """
        station_list = self.station_map.filter_by_station_name("Marina Bay")
        self.assertEqual(len(station_list), 3)

    def test_filter_by_station_code(self):
        """
        Test that it can filter by station code
        """
        station_list = self.station_map.filter_by_station_code("NS1")
        self.assertEqual(station_list[0]['Station Name'], 'Jurong East')
    
    def test_find_route_by_station_name(self):
        """
        Test that it can find route between 2 station
        """
        source = "Holland Village"
        destination = "Bugis"
        expected_route = ['CC21', 'CC20', 'CC19', 'DT9', 'DT10', 'DT11', 'DT12', 'DT13', 'DT14']
        route = self.station_map.find_route_by_station_name(source, destination)
        self.assertListEqual(route, expected_route)

    def test_get_instruction_from_route(self):
        """
        Test that it can find route between 2 station
        """
        source = "Holland Village"
        destination = "Bugis"
        route = ['CC21', 'CC20', 'CC19', 'DT9', 'DT10', 'DT11', 'DT12', 'DT13', 'DT14']
        instruction_list = self.station_map.get_instruction_from_route(route)
        self.assertEqual(8, len(instruction_list))
    
    def test_get_time_of_day(self):
        """
        Test that get time of day
        """
        start_time = parse("2019-01-31T20:00")
        time = self.station_map.get_time_of_day(start_time)
        expected_time = 'peak'
        self.assertEqual(expected_time, time)
    
    def test_time_between_station(self):
        """
        Test that get time travel between station in time
        """
        travel_time = self.station_map.get_time_between_station('DT1','DT2','night')
        self.assertIsNone(travel_time)
        travel_time = self.station_map.get_time_between_station('NS1','NS2','peak')
        self.assertEqual(12,travel_time)
        travel_time = self.station_map.get_time_between_station('TE1','TE2','non_peak')
        self.assertEqual(8,travel_time)
        travel_time = self.station_map.get_time_between_station('CC19','DT9','non_peak')
        self.assertEqual(10, travel_time)

    def test_route_with_time_constraint(self):
        """
        Test that it can find route between 2 station with time constraint
        """
        source = "Boon Lay"
        destination = "Little India"
        start_time = parse("2019-01-31T16:00")
        expected_route = ['EW27', 'EW26', 'EW25', 'EW24', 'EW23', 'EW22', 'EW21', 'CC22', 'CC21', 'CC20', 'CC19', 'DT9', 'DT10', 'DT11', 'DT12']
        expected_time = 134
        route, time = self.station_map.find_route_with_time_constraint(source, destination, start_time)
        self.assertEqual(expected_time, time)
        self.assertListEqual(expected_route, route)



if __name__ == '__main__':
    unittest.main()