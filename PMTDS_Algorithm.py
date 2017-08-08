from xlrd import open_workbook
import xlrd
import networkx as nx
import matplotlib.pyplot as plt
from termcolor import colored

#Opening xlsx file and reading the gene1 column as keys and gene2 column as values
data = open_workbook("pathway_data.xlsx")
sheet = data.sheet_by_index(0)
col_keys = sheet.col_values(0)
col_values = sheet.col_values(1)
#zipping both lists and combining them
key_values = zip(col_keys, col_values)
mgraph = dict()
keys = []
#for each set of values in combined list, we are storing lst list as keys and 2nd list as values
for line in key_values:
    key = line[0]
    value = line[1]
#if each key is present in graph dictionary, then append the new number to exsisting array
    if line[0] in mgraph:
        mgraph[line[0]].append(line[1])
#else we create a new array here
    else:
         mgraph[line[0]] = [line[1]]

#method to find nodes, edges and calculate degree of genes/nodes in pathway network
def find_degree():
    g = mgraph
    G = nx.DiGraph(g)
    total = G.degree()

#method to map mutation data and remove upstream nodes of mutated genes
def remove_mut_ge(n,mu):
    G = nx.DiGraph(mgraph)
    list_nodes = []
    col_nodes = n
    col_mut = mu
    dic = dict(zip(col_nodes,col_mut))
    for node, mut in dic.items():
        if mut > 1:
            list_nodes.append(node)
    #print list_nodes
    for i in range(len(list_nodes)):
        try:
            remove = G.predecessors(list_nodes[i])
            G.remove_nodes_from(remove)
            solitary = [n for n,d in G.degree_iter() if d == 0]
            G.remove_nodes_from(solitary)
        except nx.NetworkXError:
            continue
    new_G = nx.DiGraph(G)
    return new_G

def ge_cnv(n,ge,cnv,mut):
    removed_graph = remove_mut_ge(n,mut)
    col_nodes = n
    col_ge = ge
    col_cnv = cnv
    col_mut = mut
    nodes_of_rm = removed_graph.nodes()
    patient_data = {}
    for i in xrange(len(col_nodes)):
        list_targets = set()
        try:
            patient_data[col_nodes[i]] = [col_ge[i], col_cnv[i], col_mut[i]]
            for k, v in patient_data.iteritems():
                if k in nodes_of_rm and v[0] < 0.1 and v[1] > 0.3 and v[2] == 0:
                    list_targets.add(k)
        except TypeError:
            continue
    return list_targets

def drug_lists(n,ge,cnv,mut):
    targets = ge_cnv(n,ge,cnv,mut)
    drug_targets = open_workbook("drug_data.xlsx")
    drugs_sheet = drug_targets.sheet_by_index(0)
    col_targets = drugs_sheet.col_values(1)
    col_drugs = drugs_sheet.col_values(0)
    drugs_dict = dict(zip(col_targets,col_drugs))
    print colored("The drugs for the targets are: ",'blue')
    for i in targets:
        try:
            for k,v in drugs_dict.items():
                if i == k:
                    print k,drugs_dict[k]
        except UnicodeEncodeError:
            continue

if __name__ == "__main__":
    find_degree()
    book = xlrd.open_workbook('patient_data.xlsx')
    nodes = []
    gexp = []
    copy = []
    mutation = []
    for sheet in book.sheets():
        for i in range(2,sheet.nrows):
            row = sheet.row_slice(i)
            n = row[0].value
            ge = row[1].value
            cnv = row[2].value
            mut = row[3].value
            if sheet.row_values == '0':
                break
            nodes.append(n)
            gexp.append(ge)
            copy.append(cnv)
            mutation.append(mut)
        remove_mut_ge(nodes,mutation)
        ge_cnv(nodes,gexp,copy,mutation)
        print colored(sheet.name, 'red')
        drug_lists(nodes,gexp,copy,mutation)
        print "\n"