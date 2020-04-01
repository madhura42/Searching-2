#!/usr/local/bin/python3


import pandas as pd
from queue import PriorityQueue
from math import radians, cos, sin, asin, sqrt
import sys



def successor(city_name, road_segment_frame):
    to_return1 = road_segment_frame[road_segment_frame['City1']==city_name]
    to_return2 = road_segment_frame[road_segment_frame['City2']==city_name]
    # print(pd.concat([to_return1, to_return2], axis=0))
    return pd.concat([to_return1, to_return2], axis=0)

# the heuristic function is written by Madhura Bartakke
def heuristic(x1, x2, y1, y2):
    #lon1, lon2, lat1, lat2

    # convert decimal degrees to radians 
    x1, y1, x2, y2 = map(radians, (x1, y1, x2, y2))

    # haversine formula 
    dx = x2 - x1 
    dy = y2 - y1 
    a = sin(dy/2)**2 + cos(y1) * cos(y2) * sin(dx/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def check_valid_name(name, city_gps_frame):
    return name in city_gps_frame['City'].values

def return_city(state, city_gps_frame, current_city, goal_lat, goal_long):
    if(state['City1'] == current_city):
        next_city = state['City2']
        # gps_frame_next = city_gps_frame[city_gps_frame['City']==next_city]
        # [next_lat] = gps_frame_next['Latitude'].values
        # [next_long] = gps_frame_next['Longitude'].values
        # next_heuristic = heuristic(next_long, goal_long, next_lat, goal_lat) #heuristic
        #print(next_city)
        return  next_city
                
    if(state['City2'] == current_city):
        next_city = state['City1']
        # gps_frame_next = city_gps_frame[city_gps_frame['City']==next_city]
        # [next_lat] = gps_frame_next['Latitude'].values
        # [next_long] = gps_frame_next['Longitude'].values
        # next_heuristic = heuristic(next_long, goal_long, next_lat, goal_lat) #heuristic
        #print(next_city)
        return next_city

def solve_multiple(cost_type, start_city, goal_city, city_gps_frame, road_segment_frame):
    # print(cost_type)
    if(not check_valid_name(start_city, city_gps_frame)):
        print('print enter valid start_city name')
        return #modify
    if(not check_valid_name(goal_city, city_gps_frame)):
        print('please enter valid goal_city name')
        return #modify
    
    fringe = PriorityQueue()
    goal_lat_long_frame = city_gps_frame[city_gps_frame['City']==goal_city]
    [goal_lat] = goal_lat_long_frame['Latitude'].values #latitude goal
    [goal_long] = goal_lat_long_frame['Longitude'].values #longitude goal
    
    if cost_type == 'time':
        visited=[]
        fringe.put((0, 0, 0, 0, start_city, start_city))
        while not fringe.empty():
#             miles_plus_h, miles,current_city, currentsegments, hours, total_gas, route = fringe.get()
            hours, segments ,miles  ,total_gas ,route ,current_city = fringe.get()
            visited.append(current_city)
            for index, state in successor(current_city, road_segment_frame).iterrows():
                next_city = return_city(state, city_gps_frame, current_city,\
                                                                   goal_lat, goal_long)
                
                if next_city in visited:
                    continue
                #[total-segments] [total-miles] [total-hours] [total-gas-gallons] [start-city] [city-1] [city-2] ... [end-city]
                if next_city == goal_city:
                    return segments+1, miles+state['Distance'], hours + state['Time'], \
                        total_gas+state['Distance']/state['mpg'], route + ' ' + next_city
                fringe.put((hours + state['Time'], segments+1, miles + state['Distance'],   \
                    total_gas+state['Distance']/state['mpg'], route + ' ' +next_city, next_city))
                visited.append(next_city)

    if cost_type == 'mpg':
        visited=[]
        fringe.put((0, 0, 0, 0, start_city, start_city))
        while not fringe.empty():
#             miles_plus_h, miles,current_city, currentsegments, hours, total_gas, route = fringe.get()
            total_gas ,hours, segments ,miles  ,route ,current_city = fringe.get()
            visited.append(current_city)
            for index, state in successor(current_city, road_segment_frame).iterrows():
                next_city = return_city(state, city_gps_frame, current_city,\
                                                                   goal_lat, goal_long)
                
                if next_city in visited:
                    continue

                if next_city == goal_city:
                    return segments+1, miles+state['Distance'], hours + state['Time'], \
                        total_gas+state['Distance']/state['mpg'], route + ' ' + next_city
                fringe.put((total_gas + state['Distance']/state['mpg'], hours + state['Time'],segments+1,\
                     miles+state['Distance'],    route+' '+next_city, next_city))
                visited.append(next_city)

    if cost_type == 'segments':
        emp = ''
        visited=[]
        fringe.put((0, 0, 0, 0, start_city, start_city))
        while not fringe.empty():
#             miles_plus_h, miles,current_city, currentsegments, hours, total_gas, route = fringe.get()
            segments ,miles ,hours ,total_gas ,route ,current_city = fringe.get()
            visited.append(current_city)
            for index, state in successor(current_city, road_segment_frame).iterrows():
                next_city = return_city(state, city_gps_frame, current_city,\
                                                                   goal_lat, goal_long)
                
                if next_city in visited:
                    continue

                if next_city == goal_city:
                    return segments+1, miles+state['Distance'], hours + state['Time'], \
                        total_gas+state['Distance']/state['mpg'], route + ' ' + next_city
                fringe.put((segments+1, miles+state['Distance'],  hours + state['Time'], \
                    total_gas+state['Distance']/state['mpg'], route+' '+next_city, next_city))
                visited.append(next_city)

    emp = ''
    if cost_type == 'distance':
        #fringe = ( heuristic_miles, miles, segments, hours, total_gas, route, city)
        fringe.put((0, 0, 0, 0, start_city, start_city))

        visited = []
        while not fringe.empty():
#             (heuristic_miles, miles, segments, hours, total_gas, route, current_city)
            miles ,segments ,hours ,total_gas ,route ,current_city = fringe.get()

            for index, state in successor(current_city, road_segment_frame).iterrows():
#                 index,row in successor('Bloomington,_Indiana', road_segments).iterrows()
                
                # print(state)
                next_city = return_city(state, city_gps_frame, current_city,\
                                                                   goal_lat, goal_long)
                
                # print(next_city)
                #print(goal_city)
                #print(next_city == goal_city)

                if next_city in visited:
                    continue

                if next_city == goal_city:
                    return segments+1, miles+state['Distance'], hours + state['Time'], \
                        total_gas+state['Distance']/state['mpg'], route + ' ' + next_city
                fringe.put((miles+state['Distance'], segments+1, hours + state['Time'],\
                     total_gas+state['Distance']/state['mpg'], route+' '+next_city, next_city))
                visited.append(next_city)

  
# a = solve_multiple('time', 'Acme,_Michigan', 'Ada,_Minnesota', city_gps, road_segments)
if __name__ == '__main__':
#---------------------------------------------------------------------------------------------------------------
# # this code snippet is written by Siddhart Bhakht
    if(len(sys.argv) != 4):
        raise(Exception("Error: expected 3 arguments [start city] [end city] [cost_function]"))
    
    start_city = sys.argv[1]
    end_city = sys.argv[2]
    cost_type = sys.argv[3]

    city_cols = ['City', 'Latitude', 'Longitude']
    city_gps = pd.read_csv('city-gps.txt', sep=" ", header=None, names=city_cols)

    road_cols = ['City1', 'City2', 'Distance', 'SpeedLimit', 'Highway']
    road_segments = pd.read_csv('road-segments.txt', sep=" ", header=None, names=road_cols)

    #Time
    road_segments['Time'] = road_segments.apply(lambda row: (row['Distance']/row['SpeedLimit']), axis=1)

    #mpg
    road_segments['mpg'] = road_segments.apply(lambda row: (400/150)*row['SpeedLimit']*((1-(row['SpeedLimit']/150))**4), axis=1)
#---------------------------------------------------------------------------------------------------------------
    
segments, miles, hours, total_gas, route =  solve_multiple(cost_type, start_city, end_city, city_gps, road_segments)
print(segments, miles, round(hours, 4), round(total_gas,4) , route)




