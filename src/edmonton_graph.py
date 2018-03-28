from graph import Graph


def load_edmonton_graph(filename):
    location = {}
    graph = Graph()
    # opens filename for reading and iterates through each line in the file
    # each line is split by a commana delimiter
    # the type of a line is determine by checking for the start character
    with open(filename, 'r') as myfile:
        for line in myfile:
            line_items = line.split(',')
            if (line_items[0] == 'V'):
                graph.add_vertex(line_items[1])
                location[line_items[1]] = (line_items[2], line_items[3])
            elif (line_items[0] == 'E'):
                graph.add_edge(line_items[1], line_items[2])

    return graph, location


if __name__ == "__main__":
    pass
