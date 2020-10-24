import pandas as pd
from json import JSONEncoder
from collections import deque
from dateutil.parser import parse
from collections import defaultdict

STATION_CODE_COLUMN = 'Station Code'
STATION_NAME_COLUMN = 'Station Name'

PEAK_TIME = 'peak'
NON_PEAK_TIME = 'non_peak'
NIGH_TIME = 'night'

TIME_STATION = {
    'NS' : {PEAK_TIME:12, NON_PEAK_TIME:10, NIGH_TIME:10},
    'NE' : {PEAK_TIME:12, NON_PEAK_TIME:10, NIGH_TIME:10},
    'DT' : {PEAK_TIME:10, NON_PEAK_TIME:8, NIGH_TIME:None},
    'TE' : {PEAK_TIME:10, NON_PEAK_TIME:8, NIGH_TIME:8},
    'CG' : {PEAK_TIME:10, NON_PEAK_TIME:10, NIGH_TIME:None},
    'CE' : {PEAK_TIME:10, NON_PEAK_TIME:10, NIGH_TIME:None},
    'EW' : {PEAK_TIME:10, NON_PEAK_TIME:10, NIGH_TIME:10},
    'CC' : {PEAK_TIME:10, NON_PEAK_TIME:10, NIGH_TIME:10},
    'CHANGE_LINE': {PEAK_TIME:15, NON_PEAK_TIME:10, NIGH_TIME:10}
}

class Location:
    
    def __init__(self, name, station):
        self.name = name
        self.station_list = [station]
        self.connected_to = {}
    
    def add_station(self, station):
        self.station_list.append(station)
    
    def add_neighbor(self, nbr):
        self.connected_to[nbr] = 1

class StationMap:

    def __init__(self):
        self.data_df = pd.read_csv('./data/StationMap.csv')
        self.station_list = self.data_df.to_dict('records')
        self.location_map = dict()
        self.station_map = dict()
        self.edges = defaultdict(list)
        i = 0
        while i < len(self.station_list):
            station = self.station_list[i]
            if station[STATION_NAME_COLUMN] not in self.location_map:
                self.location_map[station[STATION_NAME_COLUMN]] = Location(station[STATION_NAME_COLUMN], station)
            else:
                self.location_map[station[STATION_NAME_COLUMN]].add_station(station)
            station_code = station[STATION_CODE_COLUMN]
            self.station_map[station_code] = {'station':station,'next':None,'prev':None}
            if i < len(self.station_list) - 1:
                station_next = self.station_list[i+1]
                if station_code[:2] == station_next[STATION_CODE_COLUMN][:2]:
                    self.station_map[station_code]['next'] = station_next
                    self.edges[station_code].append(station_next[STATION_CODE_COLUMN])
            if i > 1:
                station_prev = self.station_list[i-1]
                if station_code[:2] == station_prev[STATION_CODE_COLUMN][:2]:
                    self.station_map[station_code]['prev'] = station_prev
                    self.edges[station_code].append(station_prev[STATION_CODE_COLUMN])
            i+=1
        
        # Build graph edge
        for station_name, location  in self.location_map.items():
            if len(location.station_list)>1:
                station_code_list = [station[STATION_CODE_COLUMN] for station in location.station_list]
                for station in location.station_list:
                    for other_station in location.station_list:
                        if station[STATION_CODE_COLUMN] != other_station[STATION_CODE_COLUMN]:
                            self.edges[station[STATION_CODE_COLUMN]].append(other_station[STATION_CODE_COLUMN])

    
    def get_location_list(self):
        return list(self.location_map.keys())
    
    def get_station_list(self):
        return list(self.station_map.keys())
    
    def filter_by_station_name(self,station_name):
        if station_name not in self.location_map:
            return []
        return self.location_map[station_name].station_list

    def filter_by_station_code(self,station_code):
        if station_code not in self.station_map:
            return []
        return [self.station_map[station_code]['station']]
    
    def get_interchange_station_list(self):
        result = []
        for station_name, location  in self.location_map.items():
            if len(location.station_list)>1:                            
                result.append((station_name, location.station_list))
        return result

    def get_instruction_from_route(self, route):
        instruction_list = []
        i = 0
        while i < len(route) - 1:
            station_code = route[i]
            station_code_next = route[i+1]
            if station_code[:2] == station_code_next[:2]:
                instruction = "Take {} line from {} to {}".format(station_code[:2], 
                    self.station_map[station_code]['station'][STATION_NAME_COLUMN],
                    self.station_map[station_code_next]['station'][STATION_NAME_COLUMN])
            else:
                instruction = "Change from {} line to {} line".format(station_code[:2], station_code_next[:2])
            instruction_list.append(instruction)
            i += 1
        return instruction_list

    def find_route_by_station_name(self, source, destination):
        """
        Algorithm: BFS
        """
        visited = dict()
        if source==destination:
            return []
        source_station_list = self.filter_by_station_name(source)
        source_station_code_list = [station[STATION_CODE_COLUMN] for station in source_station_list]
        destination_station_list = self.filter_by_station_name(destination)
        destination_station_code_list = [station[STATION_CODE_COLUMN] for station in destination_station_list]
        queue = deque(source_station_code_list)
        while len(queue) > 0:
            current_station = queue.popleft()
            if current_station in destination_station_code_list:
                break
            destinations = self.edges[current_station]
            for next_station in destinations:
                if next_station not in visited:
                    visited[next_station] = current_station
                    queue.append(next_station)
        
        destination_station_code = None
        for destination_station in destination_station_code_list:
            if destination_station in visited:
                destination_station_code = destination_station
                break
        if destination_station_code:
            path = [destination_station_code]
            prev_station_code = visited[destination_station_code]
            while prev_station_code not in source_station_code_list:
                path.append(prev_station_code)
                prev_station_code = visited[prev_station_code]
            path.append(prev_station_code)
            return path[::-1]
        else:
            return None
    
    def get_time_of_day(self, start_time):
        time_obj = parse(start_time)
        weekday = time_obj.weekday()
        hour = time_obj.hour
        time = NON_PEAK_TIME
        if hour >= 22 or hour < 6:
            time = NIGH_TIME
        elif hour >= 6 and hour < 9 and weekday <= 4:
            time = PEAK_TIME
        elif hour >= 18 and hour < 21 and weekday <= 4:
            time = PEAK_TIME
        elif hour >=9 and hour < 18 and weekday <=4:
            time = NON_PEAK_TIME
        elif hour >= 6 and hour < 22 and weekday >=5:
            time = NON_PEAK_TIME
        return time
    
    def get_time_between_station(self,current_node,next_node, time):
        if TIME_STATION[next_node[:2]][time] is None:
            return None
        elif current_node[:2] == next_node[:2]:
            return TIME_STATION[next_node[:2]][time]
        else:
            return TIME_STATION['CHANGE_LINE'][time]

    def find_route_with_time_constraint(self, source, destination, start_time):
        """
        Algorithm: Djikstra
        """
        time = self.get_time_of_day(start_time)
        visited = set()
        if source==destination:
            return []
        source_station_list = self.filter_by_station_name(source)
        source_station_code_list = [station[STATION_CODE_COLUMN] for station in source_station_list]
        destination_station_list = self.filter_by_station_name(destination)
        destination_station_code_list = [station[STATION_CODE_COLUMN] for station in destination_station_list]
        initial = source_station_code_list[0]
        shortest_paths = dict()
        for source_station_code in source_station_code_list:
            shortest_paths[source_station_code] = (None, 0)
        current_node = initial
        while current_node not in destination_station_code_list:
            visited.add(current_node)
            destinations = self.edges[current_node]
            weight_to_current_node = shortest_paths[current_node][1]
            for next_node in destinations:
                next_weight = self.get_time_between_station(current_node, next_node, time)
                if next_weight is None:
                    continue
                weight = next_weight + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)
            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return None, 0
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
        
        path = []
        travel_time = shortest_paths[current_node][1]
        while current_node is not None:
            path.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node
        
        path = path[::-1]
        return path, travel_time
