import pandas as pd
import numpy as np

capacity = 20
max_route_length = 15
'''Creating a list of routes of one node with distance of route, load carried by route, and nodes included in route'''
def routesInit(distance):
    routes_list = []
    empty_list = []

    numrows = len(distanceArray)
    routes_list.append(empty_list)

    for i in range(1, numrows - 1):
        indiv_route = []
        distance = distanceArray[0, i] + distanceArray[i, numrows-1]
        load = distanceArray[i,numrows]
        indiv_route.append(distance)
        indiv_route.append(load)
        indiv_route.append(i)
        routes_list.append(indiv_route)
        #indiv_route.clear()

    return routes_list

def readcsv(filename):
    data = pd.read_csv(filename, delimiter = ',')
    return(np.array(data))

'''Savings of joining routes'''
def dist_combined_Ri_Rj(routes_list, i, j, index_of_f):
    '''Function calculates length of route resulting from joining route i and j'''
    '''Calculate dist of last node of Ri to f and start to first node of j first'''
    #for i in range(0, numrows - 1):
    #    for j in range(0, numcols -1):
    #        if j > i:


    last_node_of_route_Ri = routes_list[i][-1]
    first_node_of_route_Rj = routes_list[j][2]
    distance_from_last_node_of_Ri_to_f = distanceArray[last_node_of_route_Ri, index_of_f]
    distance_from_s_to_first_node_of_Rj = distanceArray[0, first_node_of_route_Rj]
    if last_node_of_route_Ri < first_node_of_route_Rj:
        distance_between_last_node_of_Ri_to_first_node_of_Rj = distanceArray[last_node_of_route_Ri, first_node_of_route_Rj]
    else:
        distance_between_last_node_of_Ri_to_first_node_of_Rj = distanceArray[first_node_of_route_Rj, last_node_of_route_Ri]

    distanceRoute_Ri_and_Rj_combined = routes_list[i][0] + routes_list[j][0] - distance_from_last_node_of_Ri_to_f - distance_from_s_to_first_node_of_Rj + distance_between_last_node_of_Ri_to_first_node_of_Rj

    return distanceRoute_Ri_and_Rj_combined

def create_savings_matrix(list_of_routes, index_of_f):
    num_of_routes = len(list_of_routes)
    routes_savings_matrix = np.full((num_of_routes, num_of_routes), -1000.0)
    temp_routes_first_route_matrix = np.zeros(shape=(num_of_routes, num_of_routes))
    for i in range(1, len(list_of_routes)):
        for j in range(i + 1, len(list_of_routes)):
            savings_Ri_Rj = list_of_routes[i][0] + list_of_routes[j][0] - min(
                dist_combined_Ri_Rj(list_of_routes, i, j, index_of_f), dist_combined_Ri_Rj(list_of_routes, j, i, index_of_f))
            routes_savings_matrix[i, j] = savings_Ri_Rj
            if min(dist_combined_Ri_Rj(list_of_routes, i, j, index_of_f),
                   dist_combined_Ri_Rj(list_of_routes, j, i, index_of_f)) == dist_combined_Ri_Rj(list_of_routes, i, j,
                                                                                              index_of_f):
                savings_ordered_path = i
            else:
                savings_ordered_path = j
            temp_routes_first_route_matrix[i, j] = savings_ordered_path
    return routes_savings_matrix, temp_routes_first_route_matrix
#Main Program
distanceArray = readcsv('C:\Python Files\Distances 2.csv')

routesList = routesInit(distanceArray)

print(distanceArray)

numrows = len(distanceArray)
print(numrows)
numcols = len(distanceArray[0])
print(numcols)

print("Some element", distanceArray[1,1])


'''Creating savings matrix of one-node routes old way
savings_matrix = np.zeros(shape=(numrows, numcols))
#for i in range(1, 11):
for i in range(0, numrows - 1):
#    for j in range(i, 11):
    for j in range(0, numcols - 1):
        if j>i:
            #print("Distance between 0 and ", i, " is", distanceArray[0, i])
            #print("Distance between ", i, "and 11", " is", distanceArray[i, 11])
            #print("Distance between 0 and ", j, " is", distanceArray[0, j])
            #print("Distance between ", j, "and 11", " is", distanceArray[j, 11])

            old = (distanceArray[0, i] + distanceArray[i, 11]) + (distanceArray[0, j] + distanceArray[j, 11])
            #print("Old distance is", old)

            #old_1 = (distanceArray[0, i] + distanceArray[i, j] + distanceArray[j, 11])
            #print("First distance is", old_1)

            #old_2 = (distanceArray[0, j] + distanceArray[i, j] + distanceArray[i, 11])
            #print("Second distance is", old_2)

            new = min((distanceArray[0, i] + distanceArray[i, j] + distanceArray[j, 11]), (distanceArray[0, j] + distanceArray[i, j] + distanceArray[i, 11]))
            #print("New distance is", new)

            savings = old - new
            #print("Savings is", savings)

            savings_matrix[i, j] = savings

print("Old savings are:")
print(savings_matrix)
print()
'''
number_of_routes = len(routesList)

new_savings_matrix, routes_first_route_matrix = create_savings_matrix(routesList, numcols-2)

'''new savings matrix code was replaced with function create_savings_matrix'''
#new_savings_matrix = np.full((number_of_routes, number_of_routes), -1000.0)

'''New matrix indicates in combination of two routes which node is first between Ri and Rj'''

#routes_first_route_matrix = np.zeros(shape=(number_of_routes, number_of_routes))
'''  REPLACED WITH NEW FUNCTION ??
# Calculation of savings matrix new way through list of routes
for i in range(1, len(routesList)):
    for j in range(i + 1, len(routesList)):
        savings_Ri_Rj = routesList[i][0] + routesList[j][0] - min(dist_combined_Ri_Rj(routesList, i, j, numcols - 2), dist_combined_Ri_Rj(routesList, j, i, numcols - 2))
        new_savings_matrix[i,j] = savings_Ri_Rj
        if min(dist_combined_Ri_Rj(routesList, i, j, numcols - 2),
               dist_combined_Ri_Rj(routesList, j, i, numcols - 2)) == dist_combined_Ri_Rj(routesList, i, j,
                                                                                          numcols - 2):
            savings_ordered_path = i
        else:
            savings_ordered_path = j
        routes_first_route_matrix[i, j] = savings_ordered_path
'''
print("New savings are:")
print(new_savings_matrix)
print()

print(routes_first_route_matrix)


'''Flatten savings matrix'''
#flattened_new_savings_matrix = new_savings_matrix.flatten()

'''Sort the matrix for maxes'''
#flattened_new_savings_matrix.sort()

#print(new_savings_matrix)
#print(flattened_new_savings_matrix)

'''Find max savings in savings matrix'''
max_savings_of_matrix = np.amax(new_savings_matrix)
print(max_savings_of_matrix)

'''Find indices of max savings value'''
location = np.where(new_savings_matrix == max_savings_of_matrix)
print(location)

'''Convert indices to usable indices'''
#coordinates = list(zip(location[0], location[1]))
route_1 = (location[0])[0]
route_2 = (location[1])[0]


'''Find indices i, j of max in savings'''
print(route_1)

'''Finish = numcols - 2'''
'''Check if combined routes capacity is less than set capacity of bus'''

'''If SRiRj does not work out, set savings equal to -1000'''
'''If savings are super low, then program cannot join routes together'''

max_savings_of_matrix = np.max(new_savings_matrix)
while max_savings_of_matrix > -1000:
    '''Identify the location of max savings in the savings matrix'''
    location = np.where(new_savings_matrix == max_savings_of_matrix)
    route_1 = (location[0])[0]
    route_2 = (location[1])[0]
    '''Find loads on routes candidates to be joined'''
    load_of_route_1 = routesList[route_1][1]
    load_of_route_2 = routesList[route_2][1]

    '''If total load on routes to be joined exceeds bus capacity, it is a no-go'''
    '''Replace max_savings in savings matrix with -1000.0, eliminating the routes pair from join candidates'''
    '''Find a max in the remaining savings matrix'''
    if load_of_route_1 + load_of_route_2 > capacity:
        new_savings_matrix[route_1][route_2] = -1000.0
        max_savings_of_matrix = np.amax(new_savings_matrix)
    else:
        '''From matrix routes_first_route_matrix find which route should be run first, and which second'''
        first_route_to_run = int(routes_first_route_matrix[route_1][route_2])
        if first_route_to_run == route_1:
            second_route_to_run = route_2
        else:
            second_route_to_run = route_1

        '''Find all distances to be used in calculation of combined routes distance'''
        length_of_route_1 = routesList[first_route_to_run][0]
        length_of_route_2 = routesList[second_route_to_run][0]
        distance_of_last_node_of_first_route_to_run_to_finish = distanceArray[routesList[first_route_to_run][-1], numcols - 2]
        distance_of_start_to_first_node_of_second_route_to_run = distanceArray[0, routesList[second_route_to_run][2]]
        if routesList[first_route_to_run][-1] < routesList[second_route_to_run][2]:
            distance_from_last_node_of_first_route_to_run_to_first_node_of_second_route_to_run = distanceArray[routesList[first_route_to_run][-1], routesList[second_route_to_run][2]]
        else:
            distance_from_last_node_of_first_route_to_run_to_first_node_of_second_route_to_run = distanceArray[routesList[second_route_to_run][2], routesList[first_route_to_run][-1]]

        '''Calculate combined routes distance'''
        combined_distance_of_route_1_and_route_2 = length_of_route_1 + length_of_route_2 - distance_of_last_node_of_first_route_to_run_to_finish - distance_of_start_to_first_node_of_second_route_to_run + distance_from_last_node_of_first_route_to_run_to_first_node_of_second_route_to_run

        '''If combined routes distance exceeds max_route_length, it is a no-go'''
        '''Replace element of savings matrix with -1000.0, eliminating this routes pair form candidates for joining'''
        if combined_distance_of_route_1_and_route_2 > max_route_length:
            new_savings_matrix[route_1][route_2] = -1000.0
            max_savings_of_matrix = np.amax(new_savings_matrix)
        else:
            '''If routes to be joined pass both capacity and max_length test, create a new route'''
            '''With load = sum of loads and distance = combined distance'''
            '''And list of nodes consisting of all nodes of first route to run plus all nodes of second route to run'''
            new_combined_route = []

            new_combined_route.append(combined_distance_of_route_1_and_route_2)
            new_load = load_of_route_1 + load_of_route_2
            new_combined_route.append(new_load)
            for i in routesList[first_route_to_run][2:]:
                new_combined_route.append(i)
            for j in routesList[second_route_to_run][2:]:
                new_combined_route.append(j)

            '''Identify route to be eliminated and route to be replaced'''
            route_to_be_replaced = min(first_route_to_run, second_route_to_run)
            route_to_be_eliminated = max(first_route_to_run, second_route_to_run)
            routesList.pop(route_to_be_eliminated)
            routesList[route_to_be_replaced] = new_combined_route

            '''At this point routesList contains a shorter list as a result of joining to routes'''
            '''new_savings_matrix and routes_first_route_matrix have to be updated'''
            new_savings_matrix, routes_first_route_matrix = create_savings_matrix(routesList, numcols - 2)
            max_savings_of_matrix = np.max(new_savings_matrix)

print(routesList)
#print(new_empty_route)













#for i in range(1, len(routesList)):
    #for j in range(1, len(routesList)):
        #new_route = []
        #load_1 = routesList[route_1][1]
        #load_2 = routesList[route_2][1]
        #if load_1 + load_2 <= capacity:
            #new_load = load_1 + load_2
            #distance_route_1 = routesList[route_1][0]
            #distance_route_2 = routesList[route_2][0]
            #distance_from_last_node_of_Ri_to_finish = distanceArray[routesList[route_1][-1], numcols - 2]
            #distance_from_start_to_first_node_of_Rj = distanceArray[0, routesList[route_2][2]]
            #Check if first node of Route 2 is greater than last node of Route 1
            #if routesList[route_2][2] > routesList[route_1][-1]:
                #distance_last_node_Ri_to_first_node_Rj = distanceArray[routesList[route_1][-1],routesList[route_2][2]]
            #else:
                #distance_last_node_Ri_to_first_node_Rj = distanceArray[routesList[route_2][-1], routesList[route_1][2]]
            #new_distance = distance_route_1 + distance_route_2 - distance_from_last_node_of_Ri_to_finish - distance_from_start_to_first_node_of_Rj + distance_last_node_Ri_to_first_node_Rj


        #new_route.append(new_distance)
        #new_route.append(new_load)

        #if route_2 > route_1:
            #for i in routesList[route_1][2:]:
                #for j in routesList[route_2][2:]:
                    #new_route.append(i)
                    #new_route.append(j)
        #else:
            #for i in routesList[route_2][2:]:
                #for j in routesList[route_1][2:]:
                    #new_route.append(i)
                    #new_route.append(j)



'''Testing joinging routes, remove last route, and updating first route'''
#print(new_route)
#print(route_2)
#print(routesList)
#routesList.pop(route_2)
#print(routesList)
#routesList[route_1] = new_route
#print(routesList)

