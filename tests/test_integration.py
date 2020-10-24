from athena.views import app
import unittest


class TestViews(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_location_list(self):
        response = self.app.get('/v1/locations')
        self.assertEqual(200,response.status_code)

    def test_find_route_not_pass_source_destionation(self):
        response = self.app.post('/v1/route',data={}, follow_redirects=True)
        self.assertEqual(401, response.status_code)

    def test_find_route_not_found_source(self):
        response = self.app.post('/v1/route',data={'source':"not found","destination":"not founnd"}, follow_redirects=True)
        self.assertEqual(404, response.status_code)

    def test_find_route_not_found_destination(self):
        response = self.app.post('/v1/route',data={'source':"Holland Village","destination":"not founnd"}, follow_redirects=True)
        self.assertEqual(404, response.status_code)

    def test_find_route(self):
        response = self.app.post('/v1/route',data={'source':"Holland Village","destination":"Bugis"}, follow_redirects=True)
        self.assertEqual(200, response.status_code)
        expected_route = ['CC21', 'CC20', 'CC19', 'DT9', 'DT10', 'DT11', 'DT12', 'DT13', 'DT14']
        self.assertEqual(len(expected_route), response.json['number_station'])
        self.assertEqual(len(expected_route) - 1, len(response.json['instruction']))
        self.assertListEqual(expected_route, response.json['route'])

    def test_find_route_time_constraint(self):
        response = self.app.post('/v1/route/time',data={'source':"Boon Lay","destination":"Little India", "start_time":"2019-01-31T16:00"}, 
            follow_redirects=True)
        self.assertEqual(200, response.status_code)
        expected_route = ['EW27', 'EW26', 'EW25', 'EW24', 'EW23', 'EW22', 'EW21', 'CC22', 'CC21', 'CC20', 'CC19', 'DT9', 'DT10', 'DT11', 'DT12']
        expected_time = 134
        self.assertEqual(expected_time, response.json['time'])
        self.assertListEqual(expected_route, response.json['route'])

    def test_cannot_find_route_time_constraint(self):
        response = self.app.post('/v1/route/time',data={'source':"Expo","destination":"Stevens", "start_time":"2019-01-31T23:00"}, 
            follow_redirects=True)
        self.assertEqual(200, response.status_code)
        expected_route = []
        expected_time = 0
        expected_instruction = ['Cannot found any path from given source and destination, some station is not operation now']
        self.assertEqual(expected_time, response.json['time'])
        self.assertListEqual(expected_route, response.json['route'])
        self.assertEqual(expected_instruction, response.json['instruction'])

if __name__ == '__main__':
    unittest.main()