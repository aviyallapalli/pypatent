class SVO:
    def __init__(self, subject, verb, object):
        self.subject = subject
        self.verb = verb
        self.object = object

    def triplet(self):
        return [self.subject.lemma, self.verb.lemma, self.object.lemma]


def extract_svo(tree):
    # find all verbs
    action_nodes = []
    for node in tree:
        # if node[3] in verbs:
        if node.upostag[0] == "V":
            action_nodes.append(node)

    svo_list = []
    for verb in action_nodes:
        children = [n for n in tree if n.head == verb.id]
        i_children = [n for n in children if n.deprel == "I"]
        ii_children = [n for n in children if n.deprel == "II"]

        for subject in i_children:
            for object in ii_children:
                svo_list.append(SVO(subject, verb, object))

    return [svo.triplet() for svo in svo_list]
