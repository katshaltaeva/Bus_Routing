import pandas as pd
import numpy as np
import math as math

def readcsv(filename):
    data = pd.read_csv(filename, delimiter = ',')
    return(np.array(data))


def euclidianDistance(origin, destination): #found here https://gist.github.com/rochacbruno/2883505
    lat1, lon1 = origin[0],origin[1]
    lat2, lon2 = destination[0],destination[1]
    radius = 6371 # km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d_kilometers = radius * c
    d_miles = d_kilometers*0.6214  # converting to miles
    return d_miles

def manhattanDistance(origin, destination):
    #Function uses third lat and long (lat of first point, long of second point)
    #Calculate Euclidian_distance_1 from (lat1, long1) to (lat1, long2)
    #Calculate Euclidian_distance_2 from (lat1, long2) to (lat2, long2)
    #Manhattan distance equals Euclidian_distance_1 + Euclidian_distance_2
    lat1, long1 = origin[0], origin[1]
    lat2, long2 = destination[0], destination[1]
    lat3, long3 = origin[0], destination[1]
    radius = 6371 #km

    dlat1 = math.radians(lat3 - lat1)
    dlon1 = math.radians(long3 - long1)
    a = math.sin(dlat1 / 2) * math.sin(dlat1 / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat3)) * math.sin(dlon1 / 2) * math.sin(dlon1 / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d_kilometers = radius * c
    d_miles1 = d_kilometers * 0.6214

    dlat2 = math.radians(lat2 - lat3)
    dlon2 = math.radians(long2 - long3)
    b = math.sin(dlat2 / 2) * math.sin(dlat2 / 2) + math.cos(math.radians(lat3)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon2 / 2) * math.sin(dlon2 / 2)
    e = 2 * math.atan2(math.sqrt(b), math.sqrt(1 - b))
    dist_kilometers = radius * e
    d_miles2 = dist_kilometers * 0.6214
    manhattan_distance = d_miles1 + d_miles2
    return manhattan_distance


#Main program begins here
lat_long_matrix = readcsv('C:\Python Files\Gloucester_Test_Lats_Longs.csv')
#print(lat_long_matrix)

#print(euclidianDistance(lat_long_matrix[0], lat_long_matrix[1]))
#print(manhattanDistance(lat_long_matrix[0], lat_long_matrix[1]))

num_of_routes = len(lat_long_matrix)
loads_array = []
for i in range(0, num_of_routes):
    loads_array.append(lat_long_matrix[i][-1])
print(loads_array)
#column_to_add = np.array([0, 2, 4, 7, 1, 6, 8, 4, 11, 5, 3])

euclidian_distance_matrix = np.zeros(shape=(num_of_routes, num_of_routes)) #Create a new matrix with the calculated Euclidian distances

for i in range(0, num_of_routes):
    for j in range(i + 1, num_of_routes):
        distance_using_lat_and_long = euclidianDistance(lat_long_matrix[i], lat_long_matrix[j])
        euclidian_distance_matrix[i, j] = distance_using_lat_and_long

output1 = np.column_stack((euclidian_distance_matrix, loads_array))
print(output1)

manhattan_distance_matrix = np.zeros(shape=(num_of_routes, num_of_routes)) #Create a new matrix with the calculated Manhattan distances

for a in range(0, num_of_routes):
    for b in range(a + 1, num_of_routes):
        manhat_distance = manhattanDistance(lat_long_matrix[a], lat_long_matrix[b])
        manhattan_distance_matrix[a, b] = manhat_distance


output2 = np.column_stack((manhattan_distance_matrix, loads_array))
print(output2)