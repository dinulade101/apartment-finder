from graph import Graph
from breadth_first_search import *
from heapviz import *

class RouteFinder:
    """
    A class that returns the shortest path between several different locations
        1) List of all LRT Stations
        2) University of Alberta
    """

    def __init__(self, mapsFile):
        #load up .txt file with lat and lon coordinates 
        self.graph, self.locations = load_city_graph(mapsFile)
    
    def computeDistanceFromPath(self, path):
        '''
        This function computes the distance from a path. However, this is not in meters.
        This compute the distance use lat and lon coordinates, so a special formula will have to be used
        to convert to meters. 
        However, this will allow for comparison of distances of apartments within the constraints of this program.
        '''
        distanceSoFar = 0
        for i, val in enumerate(path):
            if i == (len(path)-1):
                pass
            else:
                distanceSoFar += euclidean_distance(self.locations[val], self.locations[path[i+1]])
        #print(distanceSoFar)
        return distanceSoFar

    def computePathToUni(self, houseLocationInCoords):
        houseVertex = computeClosestVertexFromLatLonCoord(houseLocationInCoords, self.locations)
        uniVertex = computeClosestVertexFromLatLonCoord((5352133.1248, -11352133.1248), self.locations)
        #print("vertices", houseVertex, uniVertex)

        self.computePathFromLRTToHouse(houseVertex, "listOfLRTStations.txt")

        path = self.least_cost_path(houseVertex, uniVertex)
        dist = self.computeDistanceFromPath(path)

        return path, dist
    
    def computePathFromLRTToHouse(self, house, lrtfilepath):
        dictOfLRT = dict()
        dictOfPaths = dict()
        with open(lrtfilepath, 'r') as myFile:
            for line in myFile:
                lineItems = line.split(',')
                #print(float(lineItems[1]))
                coord = (float(lineItems[1])*100000, float(lineItems[2])*100000)
                #print(lineItems[0], len(lineItems[0]))
                dictOfLRT[(lineItems[0])]=computeClosestVertexFromLatLonCoord(coord, self.locations)
        
        print(dictOfLRT)
        for key, val in dictOfLRT.items():
            dictOfPaths[key] = self.least_cost_path(val, house)
        
        for key, val in dictOfPaths.items():
            print(self.computeDistanceFromPath(val))

        
        


    def least_cost_path(self, start, end):
        reached = {}
        events = BinaryHeap()
        events.insert((start, start, 0), 0)
        while (len(events)) > 0:
            pair, time = events.popmin()
                
            #account for heuristic so it is not compounded
            if (pair[2]):
                time -= pair[2]
            if pair[1] not in reached:
                reached[pair[1]] = pair[0]
                for neighbour in self.graph.neighbours(pair[1]):
                    point1 = self.locations[pair[1]]
                    point2 = self.locations[neighbour]

                    # maybe we could save distances between objects in a dict, and reuse them?
                    

                    #add heuristic in for the form of euclidean distance
                    heuristic = euclidean_distance(point2, self.locations[end])
                    #print(manhattan_distance(point1, point2))
                    events.insert((pair[1], neighbour, heuristic), time + euclidean_distance(point1, point2) + heuristic)
            # end loop right after destination is popped
            if (pair[1] == end):
                #print(pair[1], end)
                break
            
        return get_path(reached, start, end)



'''def manhattan_distance(point1, point2):
   return (((point1[0]-point2[1])**2+(point1[1]-point2[0])**2) ** 0.5)
'''
def euclidean_distance(u, v):
    # euclidean distance between 2 sets
    return ((u[0]-v[0])**2+(u[1]-v[1])**2) ** 0.5

def computeClosestVertexFromLatLonCoord(locationInCoords, locations):
    # initialize variables to keep track closest vertex as we interate through the city graph

    closestDist = float('inf')
    locationVertex = 0
    for key, val in locations.items():
        #print(val)
        dist = euclidean_distance(locationInCoords, val)
        if dist < closestDist:
            #print(locationVertex)
            locationVertex = key 
            closestDist = dist
        #print(manhattanDist)
    return locationVertex
    

def load_city_graph(filename):
    "loads up the graph of a given city (only Edmonton for now) from a given textfile"

    vertices = []
    edges = []
    locations = dict()
    graph = Graph()
    '''
    with open(filename, 'r') as openFile:
        for line in openFile:
            lineItems = line.split(',')
            if (lineItems[0] == 'V'):
                graph.add_vertex(int(lineItems[1]))
                locations[int(lineItems[1])] = (int(float(lineItems[2])*100000), int(float(lineItems[3])*100000))
            elif (lineItems[0] == 'E'):
                graph.add_edge((int(lineItems[1]), int(lineItems[2])))
    '''
    with open(filename, 'r') as myfile:
        for line in myfile:
            lineItems = line.split(',')
            if (lineItems[0] == 'V'):
                graph.add_vertex(int(lineItems[1]))
                locations[int(lineItems[1])] = (int(float(lineItems[2])*100000),int(float(lineItems[3])*100000))
            elif (lineItems[0] == 'E'):
                graph.add_edge((int(lineItems[1]), int(lineItems[2])))
        
    #print(len(locations))
    return graph, locations


if __name__ == "__main__":
    #print(manhattan_distance([0,0], [3,4]))
    new = RouteFinder("edmonton.txt")
    #start = time.time()
    path, dist = new.computePathToUni((5364728, -11335891))
    #end = time.time()
    #print(len(path), end-start)
    #new.computePathFromLRTToHouse("listOfLRTStations.txt")
    
    #graph, locations  = load_city_graph("edmonton.txt")
