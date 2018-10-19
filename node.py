class Node:
    def __init__(self):
        self.label = None
        self.children = {}
        self.attribute = None
        self.to_val = None
        self.child_counter = 0
        self.modal_classification = None
        self.modal_att_lab = None
        # you may want to add additional fields here...

    def set_label(self, label):
        self.label = label

    def set_children(self, child_dict):
        self.children = child_dict

    def set_attribute(self, attribute):
        self.attribute = attribute

    def add_new_child(self, child):
        self.children[child.to_val] = child
        self.child_counter += 1

    def set_to_val(self, value):
        self.to_val = value

    def set_modal_classification(self,modal_classification):
        self.modal_classification = modal_classification

    def set_modal_att_lab(self, modal_att_lab):
        self.modal_att_lab = modal_att_lab
