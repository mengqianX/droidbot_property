import os
import networkx as nx
from xml.dom import minidom
#import matplotlib.pyplot as plt


class Guide(object):
    def __init__(
        self,
        xml_path="None",
        source_activity=None,
        target_activity=None,
    ):
        self.G_activity = nx.DiGraph()
        self.xml_path = xml_path
        if not os.path.exists(self.xml_path):
            print(os.getcwd())
            print("Graph file not found")
        self.read_graph_from_xml_file(self.xml_path)
        self.target_activity = target_activity
        self.source_activity = source_activity

    def read_graph_from_xml_file(self, file_path):
        '''
        read the xml file and parse it into the graph, only the Act2Act edges are added

        '''
        if not os.path.exists(file_path):
            return None
        try:
            xml_doc = minidom.parse(file_path)
            sources = xml_doc.getElementsByTagName("source")

            for source in sources:
                destinations = source.getElementsByTagName("destination")
                for destination in destinations:
                    type = destination.getAttribute("type")
                    if (
                        type == "Act2Act"
                        and "service" not in destination.getAttribute("name")
                        and source.getAttribute("name")
                        != destination.getAttribute("name")
                    ):
                        self.G_activity.add_edge(
                            source.getAttribute("name").split(".")[-1],
                            destination.getAttribute("name").split(".")[-1],
                        )
        except Exception as e:
            print(e)
            return None

    def draw_graph(self):
        '''
        Draws the graph
        '''

        nx.draw(self.G_activity, with_labels=True)
        #plt.show()

    def get_shortest_path(self, source, target):
        '''
        Finds the shortest path between the source and destination
        '''
        if source is None or target is None:
            return None
        return nx.shortest_path(self.G_activity, source=source, target=target)

    def get_nodes_list_to_target(self):
        '''
        Returns a list of nodes that are connected to the target node, include the target activity
        '''
        nodes_connected_to_target = list(
            self.G_activity.predecessors(self.target_activity)
        )
        nodes_connected_to_target.append(self.target_activity)
        return nodes_connected_to_target

    def check_node_connect_to_target(self, activity: str):
        '''
        Checks if the node is connected to the target node
        '''
        return activity in self.get_nodes_list_to_target()


if __name__ == "__main__":
    g = Guide()
    g.draw_graph()
    for path in g.get_shortest_path(source=g.source_activity, target=g.target_activity):
        print(path)
    for node in g.get_nodes_list_to_target():
        print(node)
