import os
import shutil
from sage import *

# Parallelism().set(nproc=8)


# Store all the graph strings
ALL_GRAPH6_STRINGS = []

MIN_VERTICES = 4  # Default=4 || In DATA/raw_graphs you'll find "crit_4_x.g6" graphs
MAX_VERTICES = 14  # Default=14 || In DATA/raw_graphs you'll find "crit_14_x.g6" graphs

# Define the CHROMATIC_NUMBER "./DATA/graph-[CHROMATIC_NUMBER]"
CHROMATIC_NUMBER = 9

# Graph of study path
GRAPH_OF_STUDY_FILENAME = f'graph-{CHROMATIC_NUMBER}'

print(
    f'**** STARTING AT {MIN_VERTICES} to {MAX_VERTICES} Vertices - Finding {GRAPH_OF_STUDY_FILENAME} Free Edge Critical Graphs ****')

# Create the path for the graphs to be stored
SOURCE_PATH = f'{os.getcwd()}/DATA/{GRAPH_OF_STUDY_FILENAME}'

# Create the path for the graphs to be stored
P5_SAVE_PATH = f'{os.getcwd()}/{GRAPH_OF_STUDY_FILENAME}/P5 Free'
P4UP1_SAVE_PATH = f'{os.getcwd()}/{GRAPH_OF_STUDY_FILENAME}/P4+P1 Free'
P7_SAVE_PATH = f'{os.getcwd()}/{GRAPH_OF_STUDY_FILENAME}/P7 Free'

TEMP_PATH = f'{os.getcwd()}/temp/{GRAPH_OF_STUDY_FILENAME}'
TEMP_P5_SAVE_PATH = f'{TEMP_PATH}/P5 Free'
TEMP_P4UP1_SAVE_PATH = f'{TEMP_PATH}/P4+P1 Free'
TEMP_P7_SAVE_PATH = f'{TEMP_PATH}/P7 Free'

# Define all the temp paths
TEMP_PATHs = [TEMP_PATH, TEMP_P5_SAVE_PATH, TEMP_P4UP1_SAVE_PATH, TEMP_P7_SAVE_PATH]
SAVE_PATHs = [P5_SAVE_PATH, P4UP1_SAVE_PATH, P7_SAVE_PATH]

# Store all the P5_FREE_EDGE_CRITICAL_GRAPHS
P5_FREE_EDGE_CRITICAL_GRAPHS = []

# Store all the P4UP1_FREE_EDGE_CRITICAL_GRAPHS
P4UP1_FREE_EDGE_CRITICAL_GRAPHS = []

# The p7 free storage unit
P7_FREE_EDGE_CRITICAL_GRAPHS = []

# Define the path manager
def path_manager(*paths):

    for path in paths:

        # Check whether the specified path exists or not
        isExist = os.path.exists(path)

        if not isExist:

            # Create a new directory because it does not exist
            os.makedirs(path)
            print(f"The new directory {path} has been created!")

        else:

            # Clear file path for new data
            shutil.rmtree(path)
            path_manager(path)


# Is p5 free boolean flag function
def is_p5_free(G):

    P5 = graphs.PathGraph(5)
    sub_search = G.subgraph_search(P5, induced=True)

    # Return True or False
    return (sub_search == None)

# Is p4Up1 free boolean flag function [Corrected]
def is_p4Up1_free(G):

    P4UP1 = graphs.PathGraph(4).disjoint_union(Graph(1))
    sub_search = G.subgraph_search(P4UP1, induced=True)

    # Return True or False
    return (sub_search == None)

def is_p7_free(G):

    P7 = graphs.PathGraph(7)
    sub_search = G.subgraph_search(P7, induced=True)

    # Return True or False
    return (sub_search == None)


# The save function
def save(SAVE_PATH, string, order):

    DEFAULT_GRAPH6_STRING_SAVE_PATH = f'{SAVE_PATH}'

    # Store this graph in the grpahs folder
    f = open(
        f'{DEFAULT_GRAPH6_STRING_SAVE_PATH}/crit{order}_{CHROMATIC_NUMBER}.g6', "a+")

    # Write to file
    f.write(f'{string}\n')

    # CLose the file save
    f.close()


print('. . . Gathering graph data files from raw graphs folder')
# Loop through all graphs with {MIN_VERTICES} to {MAX_VERTICES}
for order in range(MIN_VERTICES, MAX_VERTICES + 1):

    # Defien a  path to the graph (may not actually exist)
    path = f'{SOURCE_PATH}/crit_{order}_{CHROMATIC_NUMBER}.g6'

    # Try: If the GRAPH_PATH does exist
    try:

        # Open up and read the file graph
        f = open(path, "r")

        # FOr every line in the file
        for line in f:

            # Attain the raw graph numbers
            string = line.split(None)[0]

            # Append the string to the ALL_GRAPH6_STRINGS
            ALL_GRAPH6_STRINGS.append((order, string))

        # CLose the file
        f.close()

    except:

        # If the graph path doesn't exist skip
        pass

# Before saving
# Create paths if they doesn't exist
print('. . . Creating TEMP directory')
path_manager(*TEMP_PATHs)


print('. . . Analyzing graph data')
# For all the raw graphs
for (index, data) in enumerate(ALL_GRAPH6_STRINGS):

    # Progress report
    if (index % int(0.05 * len(ALL_GRAPH6_STRINGS))) == 0:

        print(f'{index} out of {len(ALL_GRAPH6_STRINGS)}')

    # Define the order
    order, graph6_string = data

    # Create graphs and get details
    graph = Graph(graph6_string)




    # Is this a p5 free graph
    if is_p5_free(graph):

        # iF so, append it to the P5_FREE_EDGE_CRITICAL_GRAPHS
        P5_FREE_EDGE_CRITICAL_GRAPHS.append((graph6_string, order))

        # Save the graph
        save(TEMP_P5_SAVE_PATH, graph6_string, order)

    # Check out the p4+p1 free graphs
    if is_p4Up1_free(graph):

        P4UP1_FREE_EDGE_CRITICAL_GRAPHS.append((graph6_string, order))

        # Save the graph
        save(TEMP_P4UP1_SAVE_PATH, graph6_string, order)

    # Check out the p7 free graphs
    if is_p7_free(graph):

        P7_FREE_EDGE_CRITICAL_GRAPHS.append((graph6_string, order))

        # Save the graph
        save(TEMP_P7_SAVE_PATH, graph6_string, order)


# Before saving
# Create paths if they doesn't exist
path_manager(*SAVE_PATHs)

# Define the save manager
def save_manager(SAVE_PATH, ARRAY_TO_SAVE):

    # Print the generated graphs
    for graph in ARRAY_TO_SAVE:

        # Unpack the graph data
        graph6_string, order = graph

        # Save the graph
        save(SAVE_PATH, graph6_string, order)

# Call the save manager
save_manager(P5_SAVE_PATH, P5_FREE_EDGE_CRITICAL_GRAPHS)
save_manager(P4UP1_SAVE_PATH, P4UP1_FREE_EDGE_CRITICAL_GRAPHS)
save_manager(P7_SAVE_PATH, P7_FREE_EDGE_CRITICAL_GRAPHS)

print(
    f'. . . Success! Saved {GRAPH_OF_STUDY_FILENAME}')

# Delete the temp folder
shutil.rmtree(TEMP_PATH)
