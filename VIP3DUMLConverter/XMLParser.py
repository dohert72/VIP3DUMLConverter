try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class ParsedDiagram:
    def __init__ (self, diagram, models):
        '''
            Initializes an instance of a
            class diagram.

            Args: self method, XML root

            Return: Nothing
        '''
        self.diagram = diagram
        self.models = models
        self.shapes = self.diagram.find('Shapes')
        self.connectors = self.diagram.find('Connectors')
        #May need to rethink the following; tag could be parent tag
        self.diagram_type = diagram.tag 

    def keys (self):
        '''
            Accesses the keys for the diagram attributes dictionary

            Args: self method

            Return: attribute dictionary keys as list
        '''
        return self.diagram.keys()

    def get (self, key):
        '''
            Accesses the key value for the diagram attributes dictionary
            based on keyinput

            Args: self method, key

            Return: key value
        '''
        return self.diagram.get(key)

    def tag (self):
        '''
            Accesses the tag string for the diagram 

            Args: self method

            Return: attribute dictionary keys as list
        '''
        return self.diagram.tag()

    def get_agg_relationship_info(self):

        agg_dict = {}
        
        for association in self.models.iter('Association'):
            from_end = association.find('FromEnd')
            association_end = from_end.find('AssociationEnd')
            agg_dict[association.get('Id')] = association_end.get('AggregationKind')

        for key in agg_dict.keys():
            if agg_dict[key] == 'None':
                agg_dict[key] = 'no_agg'
            else:
                pass

        return agg_dict

    def get_msg_relationship_info(self):

        msg_dict = {}

        for message in self.models.iter('Message'):
            msg_dict[message.get('Id')] = message.get('ToActivation')

        return msg_dict