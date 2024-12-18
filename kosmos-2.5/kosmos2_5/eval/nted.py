
from zss import simple_distance, Node
from lxml import etree
import markdown

def html_to_tree(html):
    parser = etree.HTMLParser()
    tree = etree.fromstring(html, parser)
    return tree

def count_tree_nodes(node):
    count = 1
    for child in node.getchildren():
        count += count_tree_nodes(child)  
    return count

def print_tree(node, level=0):  
    print('  ' * level + node.label)  
    for child in node.children:  
        print_tree(child, level + 1)  

def calculate_tree_distance(tree1, tree2):
    root1 = Node(tree1.tag)
    root2 = Node(tree2.tag)
    build_tree(tree1, root1)
    build_tree(tree2, root2)
    # print_tree(root1)
    # print_tree(root2)
    distance = simple_distance(root1, root2)
    return distance

def build_tree(element, node):
    for child in element.getchildren():
        child_node = Node(child.tag)
        node.addkid(child_node)
        build_tree(child, child_node)

def calculate_nted(str1, str2):
    try: # in case of markdown parse error
        html1 = markdown.markdown(str1)
        # print(f'html1: {html1}\n')
        tree1 = html_to_tree(html1)
        html2 = markdown.markdown(str2)
        # print(f'html2: {html2}\n')
        tree2 = html_to_tree(html2)
        # how to draw tree
        # obtain the true number of nodes by subtracting 2.
        node_count1 = count_tree_nodes(tree1) - 2
        node_count2 = count_tree_nodes(tree2) - 2

        distance = min(calculate_tree_distance(tree1, tree2), max(node_count1, node_count2))
        # print(node_count1, node_count2, distance)
        nted = 1 - distance / max(node_count1, node_count2)
        # print(f'node_count1: {node_count1}; node_count2: {node_count2}')
        # if abs(node_count1 - node_count2) > 1000000:
        #     print(f'node_count1: {node_count1}; node_count2: {node_count2}; nted {nted}')
        #     # print(html1)
        #     print(str1)
        #     print("")
        #     # print(html2)
        #     print(str2)
        #     return 0

        return nted
    except Exception as e:
        # print(e)
        return 0


# test
if __name__ == '__main__':
    str1 = open("sampled/arxiv_md/mds/214381_7.md").read()
    str2 = open("outcome/gpt-4o-md/arxiv_md/214381_7.md").read()
    print("NTED:", calculate_nted(str1, str2))