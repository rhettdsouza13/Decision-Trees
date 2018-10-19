from node import Node
import math
from statistics import mode
from parse import *

def ID3(examples, default):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node)
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''
  root = Node()
  try:
      root.set_modal_classification(mode([x['Class'] for x in examples]))
  except:
      root.set_modal_classification(examples[0]['Class'])

  return ID3_helper(root, examples, default)



def ID3_helper(curr_node,examples,default):

    labels = [x['Class'] for x in examples]

    if not examples:
        curr_node.set_label(default)
        curr_node.set_attribute('leaf_label')
        return curr_node
    elif len(set(labels)) <= 1:
        curr_node.set_label(mode(labels))
        curr_node.set_attribute('leaf_label')
        return curr_node
    else:
        splitter = min_entropy(examples)
        att_labels = [x[splitter] for x in examples]

        for value in list(set(att_labels)):
            examplesi = []

            for example in examples:
                if example[splitter] == value:
                    examplei = {}

                    for key,val in example.items():
                        if key != splitter:
                            examplei[key] = val

                    examplesi.append(examplei)

            att_class_labels = [x['Class'] for x in examplesi]

            try:
                default_out = mode(att_class_labels)
                modal_att_lab = mode(att_labels)
            except:
                default_out = att_class_labels[0]
                modal_att_lab = att_labels[0]

            new_child = Node()
            new_child.set_to_val(value)
            new_child.set_modal_classification(default_out)

            curr_node.add_new_child(new_child)
            curr_node.set_attribute(splitter)
            curr_node.set_modal_att_lab(modal_att_lab)

            ID3_helper(new_child, examplesi, default_out)

        return curr_node

def prune(node, examples):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''

  visited = []
  prune_helper(node, None, examples, node)

def prune_helper(node, parent, examples, root):

    #consider pruning children, if not, prune myself
    for child in node.children.values():
        if child.attribute != 'leaf_label':
            prune_helper(child, node, examples, root)

    child = 0
    for nod in node.children.values():
        if nod.children:
            child = 1

    if child == 0 and parent != None:
        pre_acc = test(root, examples)
        parent.children.pop(node.to_val)

        new_leaf = Node()
        new_leaf.set_to_val(node.to_val)
        new_leaf.set_attribute('leaf_label')
        new_leaf.set_label(node.modal_classification)

        parent.children[new_leaf.to_val] = new_leaf
        post_acc = test(root, examples)
        if post_acc < pre_acc:
            parent.children[node.to_val] = node

    if parent == None:
        pre_acc = test(root, examples)
        children = node.children
        node.set_label(node.modal_classification)
        node.set_children({})

        post_acc = test(root, examples)
        if post_acc < pre_acc:
            node.children = children

def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''
  correct = 0
  for example in examples:
      if example['Class'] == evaluate(node,example):
          correct += 1
  return float(correct)/len(examples)


def evaluate(node, example):
  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
  while node.children:
      if example[node.attribute] not in node.children.keys():
          node = node.children[node.modal_att_lab]
      else:
          node = node.children[example[node.attribute]]
  return node.label

def min_entropy(examples):
    min_entropy_att = ''
    entropy = 1000000
    set_labels = set([x['Class'] for x in examples])

    for attribute in examples[0].keys():
        if attribute == 'Class':
            continue
        current_ent = 0
        unique_attval = list(set([x[attribute] for x in examples if x[attribute] != '?' ]))
        split_bin = {x:[] for x in unique_attval}
        
        #binning classes based on values of given attribute
        for example in examples:
            if example[attribute] != '?':
                if len(split_bin) <= 1:
                    split_bin[list(split_bin.keys())[0]].append(example['Class'])
                    continue
                split_bin[example[attribute]].append(example['Class'])

        #calculating class label frequency and then entropy using calculated frequency
        for att,bin in split_bin.items():
            freq = list(set([bin.count(x) for x in bin]))
            frac = [x/sum(freq) for x in freq]

            bin_entropy = 0
            for sec in frac:
                bin_entropy += sec*(math.log(sec, 2))
            current_ent += (float(len(bin))/float(len(examples))) * bin_entropy
        current_ent = abs(current_ent)
        if current_ent < entropy:
            min_entropy_att = attribute
            entropy = current_ent
    return min_entropy_att
