import math
import time

#It calculates distances between to city by using Euclidian distance.
def calculateDistance(city1, city2):
    x1 = city1[0]
    y1 = city1[1]
    x2 = city2[0]
    y2 = city2[1]
    result = round(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))
    return result

#Checks nearest neighbor of the city by looking distance between city and unvisitied cities.
def nearestNeighbor(city, unvisited_cities):

    minimum_distance = float('inf')
    for neighbor_city in unvisited_cities:

        distance = calculateDistance(city, neighbor_city)

        #if new distance is smaller than minimum distance that is assigned before, assign new minimum distance and nearest neighbor.
        if distance < minimum_distance:
            minimum_distance = distance
            nearest_neighbor = neighbor_city

    return nearest_neighbor, minimum_distance

#Finds half tsp tour, and returns the tour with coordinates and total distance in tour.
def findHalfTspTour(cities):

    total_distance = 0 #initial assignment for total distance.
    start_city = cities[0][1:] #take just coordinates not id.
    unvisited_cities = []

    for i in cities[1:]:
        unvisited_cities.append(i[1:]) #take all cities as unvisited except start city.
    
    tour = [start_city]
    initial_city = start_city
    
    #creating tour with searching nearest neighbor of the cities one by one. 
    for i in range(len(tour),math.ceil(len(cities) / 2)):

        nearest_neighbor, distance = nearestNeighbor(initial_city, unvisited_cities) #choose nearest neighbor
        total_distance += distance #add distance to total distance.

        tour.append(nearest_neighbor) #add to tour
        unvisited_cities.remove(nearest_neighbor) #remove visited city in unvisited_cities list.
        initial_city = nearest_neighbor
        
    tour.append(start_city)  # Return to the start city at the end of the tour.
    total_distance += calculateDistance(tour[-1], tour[-2]) #distance between start point and last point before start

    return tour, total_distance

#calculate total distance of the tour to use it improving function.
def calculateTotalDistanceOfTour(tour, distances):
    distance = 0 #initial distance
    size_of_the_tour = len(tour)

    #calculating total distance in tour by calculating distance between cities in the tour respectively.
    for index in range(size_of_the_tour-1):
        #take two cities from tour.
        city1 = tour[index]
        city2 = tour[index + 1]
        #add distance
        distance += distances[city1][city2]


    #distance between start point and last point before start
    distance += distances[tour[size_of_the_tour - 1]][tour[0]]  
    return distance

""" this function is the key point of our project. we send tour which is found by nearest neighbor algorithm to check 
    if there are better way to connect cities to create new tour. we take each city and create new tour by changing the
    route. It calculates the total distance again, if it is better than before, this will be our new route. We keep same
    start and end city."""
def improveTourAlgorithm(tour, distances):

    improved = True
    #initial best distance which is nearest neighbor result.
    best_distance = calculateTotalDistanceOfTour(tour, distances)
    
    #algorithm continues until there is no more improving.
    while improved:
        improved = False
        #starts from second index of the coordinates
        for i in range(1, len(tour) - 1):
            for j in range(i + 1, len(tour)):
                
                #creates new tour by changing cities in the tour.
                improved_tour = tour[:i] + tour[i:j][::-1] + tour[j:]
                #calculates new distance to check if it is improved or not.
                improved_tour_distance = calculateTotalDistanceOfTour(improved_tour, distances)

                #assign new tour if new distance is better.
                if improved_tour_distance < best_distance:
                    improved = True
                    tour = improved_tour
                    best_distance = improved_tour_distance
                    
        return tour


#MAIN FUNCTION
def main():
    input_file = open("test-input-1.txt",mode="r") #taking input
    all_cities = []
    cities_with_coordinates = []
    id_list = []
    distance = 0
    i = 0

    #preperation input data
    for city in input_file.readlines():
        all_cities.append(city.split())
        all_cities[i][0] = int(all_cities[i][0])
        all_cities[i][1] = int(all_cities[i][1])
        all_cities[i][2] = int(all_cities[i][2])
        i += 1
    input_file.close()


    """ -------------------------------------------- NEAREST NEIGHBOR -------------------------------------------- """
    #taking cities with just coordinates
    for city in all_cities:
        cities_with_coordinates.append(city[1:])

    start_time = time.time()
    nearest_neighbour_tour, distance = findHalfTspTour(all_cities) #Nearest neighbor is called and our tour is created.

    #preparing id's to print, but it is not important.
    """ for city in nearest_neighbour_tour:
        id_list.append(cities_with_coordinates.index(city))

    id_list = id_list[:-1] #Removing start_city """

    #print("\nCity ID's Half TSP Tour (Nearest Neighbor):", id_list)
    print("-------------------------------------------------------------------------------------")
    print('\x1b[6;30;41m' + 'Total Distance (Nearest Neighbor):' + '\x1b[0m'+' '+str(distance))


    """ -------------------------------------------- NEAREST NEIGHBOR -------------------------------------------- """



    """ -------------------------------------------- IMPROVE FUNCTION -------------------------------------------- """

    number_of_cities = len(nearest_neighbour_tour)
    #creating an array to keep all distances between each city.
    distances = [[0] * number_of_cities for _ in range(number_of_cities)]

    i = 0
    #distances between each city.
    for city1 in nearest_neighbour_tour:
        j=0
        for city2 in nearest_neighbour_tour:
            distances[i][j] = calculateDistance(city1, city2)
            j += 1
        i += 1

    #creating initial tour -> nearest_neighbor_tour
    initial_tour = list(range(number_of_cities))
    
    #call improving function
    improved_tour = improveTourAlgorithm(initial_tour, distances)
    improved_id_list = []

    #calculate improved distance of new tour
    improved_distance = calculateTotalDistanceOfTour(improved_tour, distances)
    end_time = (time.time() - start_time)

    for city in improved_tour:
        improved_id_list.append(cities_with_coordinates.index(nearest_neighbour_tour[city]))

    improved_id_list = improved_id_list[:-1]

    #print("-------------------------------------------------------------------------------------")
    #print("City ID's Half TSP Tour (Improved):", improved_id_list)
    print("-------------------------------------------------------------------------------------")
    print('\x1b[6;30;41m' + 'Total Distance (Improved):' + '\x1b[0m'+' '+str(improved_distance))
    print("-------------------------------------------------------------------------------------")
    print('\x1b[6;30;42m' + 'Distance improved:' + '\x1b[0m' +' '+str(distance-improved_distance))

    """ -------------------------------------------- IMPROVE FUNCTION -------------------------------------------- """


    #output process
    output_file = open("test-output-1.txt", mode="w")
    output_file.write(str(improved_distance)+"\n")
    for id in improved_id_list:
        output_file.write(str(id)+"\n")

    output_file.close()
    print("-------------------------------------------------------------------------------------")
    print('\x1b[6;30;45m' + 'Running Time in Seconds:' + '\x1b[0m' + ' ' +'{:.3f}'.format(end_time))
    
main()