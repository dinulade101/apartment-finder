from graph import Graph
from breadth_first_search import *
import math
import settings
from binary_heap import BinaryHeap

class RouteFinder:
    """
    A class that returns the shortest path between several different locations
        1) List of all LRT Stations
        2) University of Alberta
    """

    def __init__(self, mapsFile):
        # load up .txt file with lat and lon coordinates
        self.graph, self.locations = load_city_graph(mapsFile)

    def computeDistanceFromPath(self, path):
        '''
        This function computes the distance from a path. However, this is not
        in meters. This compute the distance use lat and lon coordinates, so a
        special formula will have to be used to convert to meters.
        However, this will allow for comparison of distances of apartments
        within the constraints of this program.
        '''

        # compute distance between each vertex in a path array to get the total
        # distance
        distanceSoFar = 0
        for i, val in enumerate(path):
            if i == (len(path)-1):
                # skip the first vertex beacuse there is no vertex before it
                pass
            else:
                distanceSoFar += convertLatLonDistToMetres(self.locations[val], self.locations[path[i+1]])
                # convertLatLonDistToMetres(self.locations[val], self.locations[path[i+1]])
        #print(distanceSoFar)
        return distanceSoFar

    def computePathToUni(self, houseLocationInCoords):
        #find the corresponding vertex using the lat and lon coordinates of the house, as well as the university
        houseVertex = computeClosestVertexFromLatLonCoord(houseLocationInCoords, self.locations)
        uniVertex = computeClosestVertexFromLatLonCoord((5352133.1248, -11352133.1248), self.locations)

        #calls function to build least cost path from each LRT station to house under consideration
        minStation, distToStation = self.computePathFromLRTToHouse(houseVertex, "listOfLRTStations.txt")

        #calls function to find least cost path from the house vertex to the vertex of the University of Alberta
        path = self.least_cost_path(houseVertex, uniVertex)
        if path == None:
            return "Path could not be computed", 0, minStation, distToStation
        else:
            #compute distance in km from path
            dist = self.computeDistanceFromPath(path)

            #return both the path and distance
            return path, dist, minStation, distToStation

    def computePathFromLRTToHouse(self, house, lrtfilepath):
        dictOfLRT = dict()
        dictOfPaths = dict()
        dictOfDistances = dict()

        #get LRT coordinates from text file and add to dictionary
        with open(lrtfilepath, 'r') as myFile:
            for line in myFile:
                lineItems = line.split(',')
                coord = (float(lineItems[1])*100000, float(lineItems[2])*100000)
                dictOfLRT[(lineItems[0])]=computeClosestVertexFromLatLonCoord(coord, self.locations)

        
        path, closestLRT = self.least_cost_path_lrt(dictOfLRT, house)
        #print("new way", closestLRT, self.computeDistanceFromPath(path))
        #iterate through dictionary to find least cost path from each LRT to house
        '''for key, val in dictOfLRT.items():
            dictOfPaths[key] = self.least_cost_path(val, house)

        for key, path in dictOfPaths.items():
            dictOfDistances[key] = self.computeDistanceFromPath(path)
        '''
        #compute the closest LRT locaiton to house
        #minStation = min(dictOfDistances.items(), key=lambda x:x[1])
        if closestLRT == None:
            return "Error: Could not find closest LRT", 0
        else:
            return closestLRT, self.computeDistanceFromPath(path)

    def least_cost_path_lrt(self, lrts, end):
        reached = {}
        events = BinaryHeap()

        #insert start location with time of 0 into the heap
        counter  = 0
        for key, val in lrts.items():
            events.insert((val, val, 0), 0)
        
        while (len(events)) > 0:
            pair, time = events.popmin()
            #print(time)

            #account for heuristic so it is not compounded
            if (pair[2]):
                time -= pair[2]

            if pair[1] not in reached:
                # add to reached dictionary
                reached[pair[1]] = pair[0]

                #consider neighbors around each point and distance to each neighbor
                for neighbour in self.graph.neighbours(pair[1]):
                    point1 = self.locations[pair[1]]
                    point2 = self.locations[neighbour]

                    # maybe we could save distances between objects in a dict, and reuse them?


                    # add heuristic in for the form of euclidean distance. This will helps lead the searching algorithm
                    # more towards the end location

                    heuristic = euclidean_distance(point2, self.locations[end])

                    # add key and val to BinaryHeap called events
                    events.insert((pair[1], neighbour, heuristic), time + euclidean_distance(point1, point2) + heuristic)

            # end loop right after destination is popped
            if (pair[1] == end):
                break

        # use the get_path included with the breadth_first_search helper file to find path from reached dictionary
        path = None
        closestLRT = None
        for key, val in lrts.items():
            if val in reached:
                path = get_path(reached, val, end)
            if path == None:
                pass
            else:
                closestLRT = key
                break 
        return path, closestLRT

    def least_cost_path(self, start, end):
        reached = {}
        events = BinaryHeap()

        #insert start locatin with time of 0 into the heap
        events.insert((start, start, 0), 0)
        while (len(events)) > 0:
            pair, time = events.popmin()

            #account for heuristic so it is not compounded
            if (pair[2]):
                time -= pair[2]

            if pair[1] not in reached:
                # add to reached dictionary
                reached[pair[1]] = pair[0]

                #consider neighbors around each point and distance to each neighbor
                for neighbour in self.graph.neighbours(pair[1]):
                    point1 = self.locations[pair[1]]
                    point2 = self.locations[neighbour]

                    # maybe we could save distances between objects in a dict, and reuse them?


                    # add heuristic in for the form of euclidean distance. This will helps lead the searching algorithm
                    # more towards the end location

                    heuristic = euclidean_distance(point2, self.locations[end])

                    # add key and val to BinaryHeap called events
                    events.insert((pair[1], neighbour, heuristic), time + euclidean_distance(point1, point2) + heuristic)

            # end loop right after destination is popped
            if (pair[1] == end):
                break

        # use the get_path included with the breadth_first_search helper file to find path from reached dictionary
        return get_path(reached, start, end)

#use formula for convert difference in lat and lon coordinates between points into km
def convertLatLonDistToMetres(point1, point2):
    diffX = abs(point2[0]-point1[0])/100000
    diffY = abs(point2[1]-point1[1])/100000

    #convert latitude to km
    diffXKM = diffX * 110.574

    #convert longitude to km
    #print((point1[0]+point2[0])/200000)
    diffYKM = diffY * 111.320*math.cos(math.radians((point1[0]+point2[0])/200000))

    return diffXKM+diffYKM


def euclidean_distance(u, v):
    # euclidean distance between 2 sets
    return ((u[0]-v[0])**2+(u[1]-v[1])**2) ** 0.5

def computeClosestVertexFromLatLonCoord(locationInCoords, locations):
    # initialize variables to keep track closest vertex as we interate through the city graph
    closestDist = float('inf')
    locationVertex = 0

    # loop through all items in locations dictionary until we find the vertex that is closest to the given lat and lon coordinate
    for key, val in locations.items():
        dist = euclidean_distance(locationInCoords, val)
        if dist < closestDist:
            locationVertex = key
            closestDist = dist
    return locationVertex


def load_city_graph(filename):
    #loads up the graph of a given city (only Edmonton for now) from a given textfile


    vertices = []
    edges = []
    locations = dict()
    graph = Graph()

    #parse txt file containing vertices and indices to build graph
    with open(filename, 'r') as myfile:
        for line in myfile:
            lineItems = line.split(',')
            if (lineItems[0] == 'V'):
                graph.add_vertex(int(lineItems[1]))
                locations[int(lineItems[1])] = (int(float(lineItems[2])*100000),int(float(lineItems[3])*100000))
            elif (lineItems[0] == 'E'):
                graph.add_edge((int(lineItems[1]), int(lineItems[2])))

    return graph, locations


# some testing code to ensure everything works
if __name__ == "__main__":
    #print(manhattan_distance([0,0], [3,4]))
    new = RouteFinder("edmonton.txt")
    #start = time.time()
    path, dist, minstation, distToStation = new.computePathToUni((5352133.1248, -11352133.1248))
    print(len(path), dist, minstation, distToStation)
    #end = time.time()
    #print(len(path), end-start)
    #new.computePathFromLRTToHouse("listOfLRTStations.txt")

    #graph, locations  = load_city_graph("edmonton.txt")
