
from solid import *
from solid.utils import *
from cmath import *
from openSCADShapes import *
from BrailleText import *



class Builder:
    @staticmethod
    def build_shape(shape_type, attrs, width_norm, height_norm):
        if shape_type == 'Class':
           shape = ClassCard3D(attrs['Id'], float(attrs['X']), float(attrs['Y']),
                  float(attrs['Width']), float(attrs['Height']),
                  width_norm, height_norm, attrs['Name'])

        elif shape_type == 'InteractionLifeLine':
            shape = LifelineInteraction3D(attrs['Id'], float(attrs['X']), float(attrs['Y']),
                  float(attrs['Width']), float(attrs['Height']),
                  width_norm, height_norm, attrs['Name'])

        elif shape_type == 'InteractionActor':
            shape = ActorInteraction3D(attrs['Id'], float(attrs['X']), float(attrs['Y']),
                  float(attrs['Width']), float(attrs['Height']),
                  width_norm, height_norm)

        elif shape_type == 'Activation':
            shape = ActivationCard3D(attrs['MetaModelElement'], float(attrs['X']), float(attrs['Y']),
                  float(attrs['Width']), float(attrs['Height']),
                  width_norm, height_norm)

            
        return shape

    @staticmethod
    
    def build_connector(connector_type, attrs, from_point, to_point, msg_dict, agg_dict, shape_coord_dict):
        print(agg_dict, shape_coord_dict)
        if connector_type == 'Association':
            print(attrs['Id'], attrs['MetaModelElement'])
            connector = Association3D(attrs['Id'],
                 from_point, to_point, agg_dict[attrs['MetaModelElement']])

        elif connector_type == 'Generalization':
            connector = Generalization3D(attrs['Id'],
                 from_point, to_point)

        elif connector_type == 'Message':
            connector = Message3D(attrs['Id'],
                 from_point, to_point,
                 shape_coord_dict[msg_dict[attrs['MetaModelElement']]])
        return connector

    @staticmethod
    def make_3d_shape(shape):
        print(shape.specific_shape)
        if shape.specific_shape == 'Class':
            shape_product = shape.create_3d_card()
            #Clear up the naming for the spec. shapes
        elif shape.specific_shape == 'LifelineInteraction':
            shape_product = shape.create_3d_lifeline()

        elif shape.specific_shape == 'ActorInteraction':
            shape_product = shape.create_3d_actor()

        elif shape.specific_shape == 'Activation':
            shape_product = shape.create_3d_card()

        return shape_product

    @staticmethod
    def make_3d_connector(connector):
        if connector.specific_connector == 'Association':
            product = connector.create_3d_association()

        elif connector.specific_connector == 'Generalization':
            product = connector.create_3d_generalization()
            
        elif connector.specific_connector == 'Message':
            product = connector.create_3d_message()

        return product


class Shape3D:

    def __init__ (self, specific_shape, unique_id, orig_x, orig_y, width_norm, height_norm):
        '''
            Instantiates parent object Shape3D

            Args: self method, specific shape type, shape id,
            original x and y, original diagram dims, new diagram dims

            Return: nothing
        '''
        #Normalized width ratio
        self.nw = width_norm
        #Normalized height ratio
        self.nh = height_norm

        self.specific_shape = specific_shape
        self.unique_id = unique_id
        self.new_shape_x = round (orig_x*self.nw, 2)
        self.new_shape_y = round (orig_y*self.nh, 2)

    def shape_3d_location (self):
        '''
            Accesses the location of the top left corner of the 3d shape

            Args: self method

            Return: coordinates of the top left hand corner of shape as tuple
        '''
        return (self.new_shape_x, self.new_shape_y)
    
    def shape_get_id (self):
        '''
            Accesses the unique ID of the shape

            Args: self method

            Return: Unique ID of shape as string
        '''
        return self.unique_id


class ClassCard3D (Shape3D):

    def __init__ (self, unique_id, orig_x, orig_y,
                  orig_card_width, orig_card_height, width_norm, height_norm, name):

        Shape3D.__init__ (self, 'Class', unique_id, orig_x, orig_y,
                          width_norm, height_norm)
        self.name = name
        self.new_card_height = round(orig_card_height*self.nh, 2)
        self.new_card_width = round(orig_card_width*self.nw, 2)

    def create_braille_name(self):
        text =[self.name]
        text_container = text_box(text, self.new_card_width)
        return text_container

    def create_3d_card (self):
        '''
            Using the instance variables, generates a 3d card

            Args: self method

            Return: a 3d openSCAD compatible card
        '''

        card_3d = up(0)(
                    right(self.new_shape_x)(
                        forward(self.new_shape_y)(union()(self.create_braille_name(),
                            cube([int(self.new_card_width),
                                  int(self.new_card_height), 6],True)))))
        return card_3d


class ActorInteraction3D (Shape3D):

    def __init__ (self, unique_id, orig_x, orig_y, 
                  orig_actor_width, orig_actor_height, width_norm, height_norm):

        Shape3D.__init__ (self, 'ActorInteraction', unique_id, orig_x, orig_y,
                          width_norm, height_norm)

        self.new_actor_height = round(orig_actor_height*self.nh, 2)
        self.new_actor_width = round(orig_actor_width*self.nw, 2)
        self.actor_circle = up(-1)(cylinder(r = 2.5, h=2))

    def create_3d_actor (self):
        '''
            Using the instance variables, generates a 3d actor interaction

            Args: self method

            Return: a 3d openSCAD compatible actor
        '''

        actor_3d = up(0.5)(
                    right(self.new_shape_x)(
                        forward(self.new_shape_y)(union()(self.actor_circle,
                            (forward(0.5*self.new_actor_height)(cube([2.5,
                                  float(self.new_actor_height), 1], True)))))))
        return actor_3d


class LifelineInteraction3D (Shape3D):

    def __init__ (self, unique_id, orig_x, orig_y, 
                  orig_lifeline_width, orig_lifeline_height, width_norm, height_norm, name):

        Shape3D.__init__ (self, 'LifelineInteraction', unique_id, orig_x, orig_y,
                          width_norm, height_norm)

        self.new_lifline_height = round(orig_lifeline_height*self.nh, 2)
        self.new_lifeline_width = round(orig_lifeline_width*self.nw, 2)
        self.name = name

        self.lifeline_box = cube([self.new_lifeline_width, 
                                  20, 3], center = False)

        self.lifeline_line = translate([self.new_lifeline_width/2,
                                       2.5, 0])(
                                           dashed_line(self.new_lifline_height))
    def create_braille_name(self):
        text =[self.name]
        text_container = text_box(text, self.new_lifeline_width)
        return text_container

    def create_3d_lifeline (self):
        '''
            Using the instance variables, generates a 3d lifeline interaction

            Args: self method

            Return: a 3d openSCAD compatible lifeline
        '''

        lifeline_3d = up(0)(
                    right(self.new_shape_x)(
                        forward(self.new_shape_y)(union()
                                                  (self.lifeline_box, self.create_braille_name(),
                                                          self.lifeline_line))))
        return lifeline_3d


class ActivationCard3D (Shape3D):

    def __init__ (self, unique_id, orig_x, orig_y,
                  orig_card_width, orig_card_height, width_norm, height_norm):

        Shape3D.__init__ (self, 'Activation', unique_id, orig_x, orig_y,
                          width_norm, height_norm)

        self.new_card_height = round(orig_card_height*self.nh, 2)
        self.new_card_width = round(orig_card_width*self.nw, 2)

    def create_3d_card (self):
        '''
            Using the instance variables, generates a 3d card

            Args: self method

            Return: a 3d openSCAD compatible card
        '''

        card_3d = up(0.5)(
                    right(self.new_shape_x)(
                        forward(self.new_shape_y)(
                            cube([int(self.new_card_width),
                                  int(self.new_card_height), 3],False))))
        return card_3d


class Connector3D:
    def __init__ (self, unique_id, connector_type,
                  from_point, to_point):
        '''
            Instantiatiates a 3D connector

            Args: self method, connector id, connector type,
            from coord, to coord

            Return: Nothing
        '''
        self.unique_id = unique_id
        self.from_point = from_point
        self.to_point = to_point
        self.specific_connector = connector_type

    def make_length (self):
        '''
            Calculates the required length of the connector

            Args: self method

            Return: the required length of the connector
        '''
        x_len = self.to_point[0] - self.from_point[0]
        y_len = self.to_point[1] - self.from_point[1]
        print(x_len, y_len)
        con_length = math.sqrt((math.pow(x_len,2))
                               + (math.pow(y_len,2)))

        return con_length

    def make_rotation (self):
        '''
            Calculates the rotation of the 3d connector
            about the z-axis

            Args: self method

            Return: the rotation of the connector about the z-axis
        '''
        x_len = self.to_point[0] - self.from_point[0]
        y_len = self.to_point[1] - self.from_point[1]

        if  int(x_len) > 0 and int(y_len) > 0:
            rotation = math.degrees(math.atan((abs(x_len))
                                  / (abs(y_len))))

        elif int(x_len) == 0 and int(y_len) > 0:
            rotation = 90

        elif int(x_len) < 0 and int(y_len) > 0:
            rotation = math.degrees(math.atan((abs(x_len))
                                  / (abs(y_len)))) + 90

        elif int(x_len) < 0 and int(y_len) == 0:
            rotation = 180

        elif int(x_len) < 0 and int(y_len) < 0:
            rotation = math.degrees(math.atan((abs(x_len))
                                  / (abs(y_len)))) + 180

        elif int(x_len) == 0 and int(y_len) < 0:
            rotation = 270

        elif int(x_len) > 0 and int(y_len) < 0:
            rotation = math.degrees(math.atan((abs(x_len))
                                  / (abs(y_len)))) + 270

        elif int(x_len) > 0 and int(y_len) == 0:
            rotation = 0

        else:
            rotation = 0

        return rotation
#This class took the argumanent aggregation, the value for the 
# id key for the connector.  It has been excluded due to xml problems for now
class Association3D (Connector3D):
    def __init__(self, unique_id,
                 from_point, to_point, aggregation):
        Connector3D.__init__(self, unique_id, 'Association',
                             from_point, to_point)

        self.aggregation = aggregation

    def determine_aggregation(self):
        '''
            Determine if there is aggregation on the from end and
            in the case that there is creates an aggregation diamond
            and places it on the from end of the connector

            Args: self method

            Return: openSCAD diamond or nothing
        '''
        aggregation_diamond = generate_diamond(0)
        if self.aggregation == 'no_agg':
            aggregation_diamond = generate_diamond(0)
        elif self.aggregation == 'Shared':
           aggregation_diamond = generate_diamond(10)

        return aggregation_diamond

    def create_3d_association(self):
        '''
            Creates a 3d connector for openSCAD use

            Args: self method

            Return: 3d conector for openSCAD
        '''
        assoc_3d = up(-0.5)(
            right(self.from_point[0])(
                forward(self.from_point[1])(
                    rotate (a = self.make_rotation(), v = UP_VEC)
                    (union()(translate([self.make_length()*0.35,0,2])(self.determine_aggregation())),
                        cube([self.make_length(),2,3.5], False)))))
                                                                  
        return assoc_3d
    #Belowis what I previosly had for compiling the 3d connector
    # above, the determine aggregation has been excluded pending 
    # a beeter solution for extracting it from the xml
    '''def create_3d_association(self):
        
        #TODO: Add the association indicator as a union()
        # in assoc fnc, rotate as needed
        # also make a method to rotate and position as needed so its in right orientation
        assoc_3d = up(-0.5)(
            right(self.from_point[0])(
                forward(self.from_point[1])(
                    rotate (a = self.make_rotation(), v = UP_VEC)(
                        union()(self.determine_aggregation(),cube([self.make_length(),1,1], False
                                                                  ))))))
        return assoc_3d
        '''


class Generalization3D (Connector3D):
    def __init__(self, unique_id,
                 from_point, to_point):
        Connector3D.__init__(self, unique_id, 'Generalization',
                             from_point, to_point)

        self.inheritance = generate_solid_arrow(5)

    def create_3d_generalization(self):
        '''
            Creates a 3d connector for openSCAD use

            Args: self method

            Return: 3d conector for openSCAD
        '''
        #TODO: Add the association indicator as a union()
        # in assoc fnc, rotate as needed
        # also make a method to rotate and position as needed so its in right orientation
        gen_3d = up(-0.5)(
            right(self.from_point[0])(
                forward(self.from_point[1])(
                    rotate (a = self.make_rotation(), v = UP_VEC)(
                            union()(self.inheritance, cube([self.make_length(),1,1], False))))))
        return gen_3d
    

class Message3D (Connector3D):
    def __init__(self, unique_id,
                 from_point, to_point, anchor_point):
        Connector3D.__init__(self, unique_id, 'Message',
                             from_point, to_point)

        self.anchor_point = anchor_point
        self.direction = generate_solid_arrow(10)

    def create_3d_message(self):
        '''
            Creates a 3d message for openSCAD use

            Args: self method

            Return: 3d message for openSCAD
        '''
        message_3d = up(0.5)(
            right(self.anchor_point[0]-6.5)(
                forward(self.anchor_point[1])(
                    #This may not be the best way to get the rotation
                    rotate (a = 180, v = UP_VEC)(
                        #Might be a better way to center the arrow
                            union()(up(1)(forward(0.5)(self.direction)), cube([self.make_length()+2 ,2, 3], False))))))
        return message_3d
    

class Diagram3DInfo:
    
    def __init__ (self, diagram_3d_width, diagram_3d_height):
        '''
            Initializes an instance of Diagram3DInfo, 
            the 3D diagram in openSCAD

            Args: self method, desired 3d diagram width, 
                    3d diagram height

            Return: Nothing
        '''
        self.diagram_3d_width = diagram_3d_width
        self.diagram_3d_height = diagram_3d_height
    
    def diagram_3d_dim (self):
        '''
            Accesses the height and width of the 3d diagram
            in openSCAD

            Args: self method

            Return: width and height of the 3d diagram as tuple
        '''
        return (self.diagram_3d_width, self.diagram_3d_height)

    #TODO: Create methods for returning the diagram type to make slat 
class buy:   
    def create_3d_connector(self):
        '''
            Creates a 3d connector for openSCAD use
            
            Args: self method

            Return: 3d conector for openSCAD
        '''
        #TODO: Add the association indicator as a union()
        # in assoc fnc, rotate as needed
        # also make a method to rotate and position as needed so its in right orientation
        conn_3d = up(-0.5)(
            right(self.from_point[0])(
                forward(self.from_point[1])(
                    rotate (a = self.make_rotation(), v = UP_VEC)(
                            cube([self.make_length(),1,1], False)))))
        return conn_3d


