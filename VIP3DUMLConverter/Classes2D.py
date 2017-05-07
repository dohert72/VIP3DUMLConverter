
class Shape2D:
    def __init__ (self, shape_attributes, shape_type):
        '''
            Instantiate 2D shape

            Args: self method, dictionary s, shape type

            Returns: Nothing
        '''
        self.shape_attributes = shape_attributes
        self.shape_type = shape_type

    def get_attribs (self):
        '''
            Access the attribute dictionary of the shape

            Args: self method

            Return: Nothing
        '''
        return self.shape_attributes



class Connector2D:

    def __init__ (self, connector_attributes, connector_type):
        '''
            Instantiates 2D connector

            Args: self method, dictionary of connector attributes, 
            connector type

            Return: Nothing
        '''
        self.connector_attributes = connector_attributes
        self.connector_type = connector_type

   
    def get_connector_type (self):
        '''
            Accesses the connector type

            Args: self method

            Return: connector type
        '''
        return self.connector_type

    def get_connector_2d_info(self):
        '''
            Access the dictionary connector_attributes

            Args: self method

            Return: dictionary connector attributes
        '''
        return self.connector_attributes

    def get_param(self, param):
        '''
            Accesses the value indicated by the key input

            Args: self method, string key belonging to desired value

            Return: value associated with the input key
        '''
        return self.connector_attributes[param]

    def get_from(self):
        '''
            Access the ID of the card the connector is from

            Args: self method

            Return: ID of card from as string
        '''
        return self.get_param('From')

    def get_to(self):
        '''
            Access the ID of the card the connector is to

            Args: self method

            Return: ID of card to as string
        '''
        return self.get_param('To')

    def get_id(self):
        '''
            Access the connector ID

            Args: self method

            Return: Connector ID
        '''
        return self.get_param('Model')


         
class Diagram2D:
    def __init__ (self, diagram_attributes, diagram_type):
        '''
            Instantiate a 2D diagram

            Args: self method diagrama, attributes dictionary, diagram type

            Return: Nothing
        '''
        self.diagram_attributes = diagram_attributes
        self.diagram_type = diagram_type

    def get_diagram_2d_info(self):
        '''
            Accesses the dictionary diagram_attributes

            Args: self method

            Return: dictionary diagram_attributes
        '''
        return self.diagram_attributes

    def get_diagram_type(self):
        '''
            Access the diagram type

            Args: self method

            Return: diagram type
        '''
        return self.diagram_type

    def get_param(self, param):
        '''
            Accesses the value indicated by the input key
            in dictionary diagram_attributes

            Args: self method, string key input param

            Return: value assigned to input key in diagram_attributes
        '''
        return self.diagram_attributes[param]

    def get_diagram_width(self):
        '''
            Access the original width of the diagram as specified
            in the XML as an int

            Args: self method

            Return: original width of the diagram
        '''
        return float(self.get_param('Width'))

    def get_diagram_height(self):
        '''
            Access the original height of the diagram as specified
            in the XML as an int

            Args: self method

            Return: original height of the diagram
        '''
        return float(self.get_param('Height'))
        


    #TODO: Make a function or a group of functions that can access text 
    # that describes the attributes of the card and can access the size and
    # location of the text.

    #TODO: Create methods to deal with the type of diagram i.e.
    # class, sequence, state, etc.

    #TODO: Make methods for what type of association connector is,
    # any text associated and its attribs