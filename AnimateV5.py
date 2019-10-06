class Animation:
    def __init__(self,
                 lower_left = [0, 0],
                 upper_right = [640, 480],
                 length = 1,
                 file_name = 'my_file.tex',
                 additional = ''):

        self.length = length
        self.file_name = file_name
        
        self.camera_center = [ (upper_right[i] + lower_left[i])/2 for i in range(2) ]
        self.camera_size = [ upper_right[i] - lower_left[i] for i in range(2) ]
        self.camera_zoom = 1
        
        self.camera = []
        self.camera_move_current_frame = 1
        self.camera_move_total_frames = 0
        self.camera_start_center = [ (upper_right[i] + lower_left[i])/2 for i in range(2) ]
        self.camera_start_zoom = 1
        self.camera_end_center = [ (upper_right[i] + lower_left[i])/2 for i in range(2) ]
        self.camera_end_zoom = 1
        self.canvas_shift = [0, 0]

        self.draw_boundary = '\\newcommand{\\BoundingBox}' + \
                             '{{\\clip ({},{}) '.format(lower_left[0], lower_left[1]) + \
                             'rectangle ({},{});}} \n\n'.format(upper_right[0], upper_right[1])
    
        self.additional = additional

        self.contents = []
        

    def make_me(self):
        f = open(self.file_name, 'w')
        
        # Write the Preamble
        f.write('\\documentclass[multi={img},preview]{standalone} \n')
        f.write('\\usepackage{amsmath,amssymb} \n')
        f.write('\\usepackage{tikz} \n\n')
        f.write('\\newenvironment{img}{}{} \n\n')
        f.write(self.draw_boundary)
        f.write(self.additional)
        f.write('\n\n\\begin{document} \n')

        for frame in range(1,self.length + 1):
            print(frame)
            f.write('% Frame {}\n'.format(frame))
            f.write('\\begin{img} \n')
            f.write('\\begin{tikzpicture}[x=0.7229pt,y=0.7229pt] \n')
            f.write('\\BoundingBox \n')

            for cam_move in self.camera:
                if cam_move.start_frame == frame:
                    self.camera_move_current_frame = 0
                    self.camera_move_total_frames = cam_move.end_frame - cam_move.start_frame
                    self.camera_start_center = self.camera_center
                    self.camera_start_zoom = self.camera_zoom
                    self.camera_end_center = cam_move.end_center
                    self.camera_end_zoom = cam_move.end_zoom

            if self.camera_move_current_frame <= self.camera_move_total_frames:
                t = self.camera_move_current_frame/self.camera_move_total_frames
                self.camera_zoom = self.camera_start_zoom * (1 - t) + self.camera_end_zoom * t
                
                self.camera_center = [ self.camera_start_center[i] * (1 - t) + self.camera_end_center[i] * t for i in range(2) ]                
                camera_shift = [ self.camera_center[i] - self.camera_size[i]/(2 * self.camera_zoom) for i in range(2) ]

                self.canvas_shift = [ -camera_shift[i] for i in range(2) ]
                self.camera_move_current_frame += 1

            print(self.camera_center, self.canvas_shift, self.camera_zoom)

            f.write('\\begin{{scope}}[shift={{({},{})}}, '.format(self.canvas_shift[0], self.canvas_shift[1]) + \
                    'transform canvas={{scale={}}} ] \n'.format(self.camera_zoom))

            for obj in self.contents:
                if obj.start_frame <= frame and obj.stop_frame >= frame:
                    f.write(obj.draw_me(frame))
                    f.write('\n')
                elif obj.stop_frame <= frame and obj.persist == True:
                    f.write(obj.draw_me(obj.stop_frame))
                    f.write('\n')                    
            
            f.write('\\end{scope} \n')
            f.write('\\end{tikzpicture} \n')
            f.write('\\end{img} \n \n')
                             
        f.write('\\end{document} \n')
        f.close()    
        return(True)

class Camera_Move:
    def __init__(self,
                 frames = [1,2],
                 end_center = [0,0],
                 end_zoom = 1):

        self.start_frame = frames[0]
        self.end_frame = frames[1]
        self.end_center = end_center
        self.end_zoom = end_zoom

'''
Obj: This is a basic object class. It only contains a reference name and
a list that represents the start and stop frames.
* Persist means to continue to draw the object after the listed animation frames.

Obj
'''
class Obj:
    def __init__(self,
                 ref = 'Obj',
                 frames = [1, 1],
                 persist = True):
        
        self.ref = ref
        self.start_frame = frames[0]
        self.stop_frame = frames[1]
        self.persist = persist

'''
Anim_Obj: This is an animated object. It adds the linear interpolation
function. In the future, I may have other types of interpolations, and
they would go here... maybe. It depends on how I end up coding that in.

Anim_Obj <-- Obj
'''
class Anim_Obj(Obj):
    def __init__(self,
                 ref = 'Anim_Obj',
                 frames = [1, 1],
                 persist = True,
                 start_point = [0, 0],
                 stop_point = [0, 0]):
        
        Obj.__init__(self,
                     ref = ref,
                     frames = frames,
                     persist = persist)
        self.start_x = start_point[0]
        self.start_y = start_point[1]
        self.stop_x = stop_point[0]
        self.stop_y = stop_point[1]

        self.x = start_point[0]
        self.y = start_point[1]

    def linear_interpolate_coords(self, frame):
        if self.start_frame == self.stop_frame:
            t = 0
        else:
            t = (frame - self.start_frame)/(self.stop_frame - self.start_frame)
        self.x = (1-t) * self.start_x + t * self.stop_x
        self.y = (1-t) * self.start_y + t * self.stop_y

'''
Point_Obj: This creates a TikZ coordinate at a particular point. These points
can be referenced by other commands.

Point_Obj <-- Anim_Obj <-- Obj
'''
class Point_Obj(Anim_Obj):
    def __init__(self,
                 ref = 'my_point_object',
                 frames = [1, 1],
                 persist = True,
                 start_point = [0,0],
                 stop_point = [0,0]):

        Anim_Obj.__init__(self,
                          ref = ref,
                          frames = frames,
                          persist = persist,
                          start_point = start_point,
                          stop_point = stop_point)

    def draw_me(self, frame):
        self.linear_interpolate_coords(frame)
        return '\\coordinate ({}) at ({},{}); \n'.format(self.ref, self.x, self.y)
    
    def coords(self, frame):
        self.linear_interpolate_coords(frame)
        return [self.x, self.y]

'''
Node: This creates a node at a point.
* If at_point == False, it will create a new point
* If at_point == True, then it will use an existing point. This point can
either be a string or a Point_Obj. In this case, the start_point and end_point
parameters are meaningless and can be skipped.

Node <-- Point_Obj <-- Anim_Obj <-- Obj
'''
class Node(Point_Obj):
    def __init__(self,
                 ref = 'my_node',
                 frames = [1, 1],
                 persist = True,
                 start_point = [0, 0],
                 stop_point = [0, 0],
                 contents = '',
                 options = '',
                 at_point = False):

        Point_Obj.__init__(self,
                           ref = ref,
                           frames = frames,
                           persist = persist,
                           start_point = start_point,
                           stop_point = stop_point)
        self.contents = contents
        self.options = options
        self.at_point = at_point
        
    def draw_me(self, frame):
        draw_commands = ''
        
        if self.at_point == False:
            self.linear_interpolate_coords(frame)
            draw_commands = '\\coordinate ({}) at ({},{}); \n'.format(self.ref, self.x, self.y)

        if type(self.ref) == str:
            ref = self.ref
        else:
            ref = self.ref.ref
        draw_commands += '\\draw ({}) node[{}] {{{}}}; \n'.format(ref, self.options, self.contents)

        return draw_commands

'''
Line: This creates a multi-line. The point list can be a combination of
coordinates and existing points. The existing points can either be point names
or they can be Point_Obj-s.

Line <-- Obj
'''

class Line(Obj):
    def __init__(self,
                 ref = 'Line',
                 frames = [1, 1],
                 persist = True,
                 start_point_list = [ [0,0] ],
                 stop_point_list = [ [0,0] ],
                 closed = False,
                 options = ''):

        Obj.__init__(self,
                     ref = ref,
                     frames = frames,
                     persist = persist)
        self.closed = closed
        self.options = options

        self.points_list = []

        for i in range(len(start_point_list)):
            if type(start_point_list[i]) == list:
                self.points_list.append( \
                    Point_Obj(ref = self.ref + str(i),
                              start_point = start_point_list[i],
                              stop_point = stop_point_list[i],
                              frames = [self.start_frame, self.stop_frame]) )
            else:
                self.points_list.append(start_point_list[i])

    def draw_me(self, frame):
        draw_commands = ''
        
        # Lays out the coordinates of Point_Obj-s
        for point in self.points_list:
            if type(point) == Point_Obj:
                draw_commands += point.draw_me(frame)
        
        # Draws the multi-line
        if type(self.points_list[0]) == Point_Obj:
            draw_commands += '\draw[{}] ({})'.format(self.options, self.points_list[0].ref)
        elif type(self.points_list[0]) == str:
            draw_commands += '\draw[{}] ({})'.format(self.options, self.points_list)
        else:
            draw_commands += '\draw[{}] ({})'.format(self.options, self.points_list[0])
        for point in self.points_list[1:]:
            if type(point) == Point_Obj:
                point_name = point.ref
            else:
                point_name = point
            draw_commands += '-- ({})'.format(point_name)

        if self.closed == True:
            draw_commands += '-- cycle'
        draw_commands += '; \n'
        
        return draw_commands

'''
Node_On_Path: Creates a node along a path between two points. Points can be
coordinates (as a list) or names of TikZ existing coordinates or Point_Obj-s

Node_On_Path <-- Obj
'''
class Node_On_Path(Obj):
    def __init__(self,
                 ref = 'Node_On_Path',
                 persist = True,
                 frames = [1,1],
                 first_point = 'my_first_point',
                 second_point = 'my_second_point',
                 contents = '',
                 options = ''):
        Obj.__init__(self,
                     ref = ref,
                     frames = frames,
                     persist = persist)
        self.first_point = first_point
        self.second_point = second_point
        self.contents = contents
        self.options = options

    def draw_me(self, frame):
        if type(self.first_point) == str:
            first_point = self.first_point
        elif type(self.first_point) == Point_Obj:
            first_point = self.first_point.ref
        else:
            first_point = '{},{}'.format(self.first_point[0], self.first_point[1])

        if type(self.second_point) == str:
            second_point = self.second_point
        elif type(self.second_point) == Point_Obj:
            second_point = self.second_point.ref
        else:
            second_point = '{},{}'.format(self.second_point[0], self.second_point[1])

        return '\\path ({}) -- ({}) '.format(first_point, second_point) + \
               'node[{}]{{{}}}; \n'.format(self.options,self.contents)

'''
Circle: Draws an animated circle. Both the center and radius are dynamic.
* If at_point == False, it will create a new point
* If at_point == True, then it will use an existing point. This point can
either be a string or a Point_Obj. In this case, the start_point and end_point
parameters are meaningless and can be skipped.

Circle <-- Anim_Obj <-- Obj
'''

class Circle(Anim_Obj):
    def __init__(self,
                 ref = 'Circle_Center',
                 frames = [1, 1],
                 persist = True,
                 start_point = [0, 0],
                 stop_point = [0, 0],
                 radii = [0, 0],
                 options = '',
                 at_point = False):
        
        Anim_Obj.__init__(self,
                          ref = ref,
                          frames = frames,
                          persist = persist,
                          start_point = start_point,
                          stop_point = stop_point)
        self.start_radius = radii[0]
        self.stop_radius = radii[1]
        self.options = options
        self.at_point = at_point
        
        self.radius = radii[0]

    def linear_interpolate_radius(self, frame):
        if self.start_frame == self.stop_frame:
            t = 0
        else:
            t = (frame - self.start_frame)/(self.stop_frame - self.start_frame)
        self.radius = (1-t) * self.start_radius + t * self.stop_radius

    def draw_me(self, frame):
        if self.at_point == False:
            self.linear_interpolate_coords(frame)
            self.linear_interpolate_radius(frame)
            # Fix the coordinates
            return '\\draw[{}] ({},{}) circle ({}); \n'.format(self.options, self.x, self.y, self.radius)
        else:
            self.linear_interpolate_radius(frame)
            return '\\draw[{}] ({}) circle ({}); \n'.format(self.options, self.ref, self.radius)

'''
Literal: This is for those things that I need to manually program in.

Literal <-- Obj
'''

class Literal(Obj):
    def __init__(self,
                 ref = 'Literal',
                 frames = [1, 1],
                 persist = True,
                 contents = ''):
        
        Obj.__init__(self,
                     ref = ref,
                     frames = frames,
                     persist = persist)

        self.contents = contents

    def draw_me(self, frame):
        return self.contents

'''
Scope: A scope is a class that contains other types of Obj-s.

Scope <-- Point_Obj <-- Anim_Obj <-- Obj
'''

class Scope(Point_Obj):
    def __init__(self,
                 ref = 'Scope',
                 frames = [1, 1],
                 persist = True,
                 start_point = [0, 0],
                 stop_point = [0, 0],
                 options = ''):
        
        Point_Obj.__init__(self,
                           ref = ref,
                           frames = frames,
                           persist = persist,
                           start_point = start_point,
                           stop_point = stop_point)

        self.options = options
        
        self.contents = []

    def draw_me(self, frame):
        self.linear_interpolate_coords(frame)
        options = self.options + ',shift={{({},{})}}'.format(self.x, self.y)
        if self.start_frame <= frame and self.stop_frame >= frame:
            print(self.ref, self.start_frame, self.stop_frame, frame)
            draw_commands = '\\begin{{scope}}[{}] \n'.format(options)
            
            for obj in self.contents:
                if obj.start_frame <= frame and obj.stop_frame >= frame:
                    draw_commands += obj.draw_me(frame) + '\n'
                elif obj.stop_frame <= frame and obj.persist == True:
                    draw_commands += obj.draw_me(obj.stop_frame) + '\n'
            draw_commands += '\\end{scope} \n'
            return draw_commands
        else:
            return 

'''
Graph: Produces an animated parametric graph. The default parameter is \t
and uses the TikZ plot command.

Graph <- Obj
'''

class Graph(Obj):
    def __init__(self,
                 ref = 'Graph',
                 frames = [1, 1],
                 persist = True,
                 start_domain = [0,0],
                 stop_domain = [0,0],
                 x = '',
                 y = '',
                 parameter = 't',
                 samples = 50,
                 options = ''):

        Obj.__init__(self,
                     ref = ref,
                     frames = frames,
                     persist = persist)
        self.options = options
        self.samples = samples
        self.x = x
        self.y = y
        self.parameter = parameter
        self.start_domain = start_domain
        self.stop_domain = stop_domain
        
        self.left_endpoint = start_domain[0]
        self.right_endpoint = start_domain[1]
        
    def linear_interpolate_domain(self, frame):
        t = (frame - self.start_frame)/(self.stop_frame - self.start_frame)
        self.left_endpoint = (1-t) * self.start_domain[0] + t * self.stop_domain[0]
        self.right_endpoint = (1-t) * self.start_domain[1] + t * self.stop_domain[1]

    def draw_me(self, frame):
        self.linear_interpolate_domain(frame)
        return '\\draw[smooth, samples={},variable=\\{},'.format(self.samples, self.parameter) + \
            'domain={}:{},{}] '.format(self.left_endpoint, self.right_endpoint, self.options) + \
            'plot ( {{{}}}, {{{}}} ); \n'.format(self.x, self.y)

'''
Text: Creates a text object. By default, the text is centered with a strut so
that all basic text is handled in the same way. Mathematical notation may spill
above or below the strut, in which case the alignment may vary. The default is
also to double the size of the text so that it is readable at 1920x1080
'''

class Text(Node):
    def __init__(self,
                 ref = 'Text',
                 frames = [1, 1],
                 persist = True,
                 start_point = [0, 0],
                 stop_point = [0, 0],
                 contents = '',
                 options = '',
                 at_point = False):

        Node.__init__(self,
                      ref = ref,
                      frames = frames,
                      persist = persist,
                      start_point = start_point,
                      stop_point = stop_point,
                      contents = contents,
                      options = options,
                      at_point = False)
        self.contents += '\\strut'
        self.options += ',anchor=center,scale=2'
        
