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
        self.camera_shift = [0, 0]

        self.draw_boundary = '\\newcommand{\\BoundingBox}' + \
                             '{\\clip (' + str(lower_left[0]) + ',' + str(lower_left[1]) + \
                             ') rectangle (' + str(upper_right[0]) + ',' + str(upper_right[1]) + ');} \n\n'
    
        self.additional = additional

        self.contents = []
        

    def make_me(self):
        f = open(self.file_name, 'w')
        
        # Write the Preamble
        f.write('\\documentclass[multi={img},preview]{standalone} \n' + \
                '\\usepackage{amsmath,amssymb} \n' + \
                '\\usepackage{tikz} \n\n' + \
                '\\newenvironment{img}{}{} \n\n' + \
                self.draw_boundary + \
                self.additional + '\n\n' + \
                '\\begin{document} \n')

        for frame in range(1,self.length + 1):
            print(frame)
            f.write('% Frame ' + str(frame) + '\n')
            f.write('\\begin{img} \n' + \
                    '\\begin{tikzpicture}[x=0.7229pt,y=0.7229pt] \n' + \
                    '\\BoundingBox \n')

            for cam_move in self.camera:
                if cam_move.start_frame == frame:
                    self.camera_move_current_frame = 0
                    self.camera_move_total_frames = cam_move.end_frame - cam_move.start_frame + 1
                    self.camera_start_center = self.camera_center
                    self.camera_start_zoom = self.camera_zoom
                    self.camera_end_center = cam_move.end_center
                    self.camera_end_zoom = cam_move.end_zoom

            if self.camera_move_current_frame > self.camera_move_total_frames:
                self.camera_shift = [ -self.camera_end_center[i] + self.camera_size[i]/2 for i in range(2) ]
                self.camera_zoom = self.camera_end_zoom

            else:
                self.camera_center = [ self.camera_start_center[i] * (1 - self.camera_move_current_frame/self.camera_move_total_frames) + \
                    self.camera_end_center[i] * (self.camera_move_current_frame/self.camera_move_total_frames) for i in range(2) ]
                self.camera_shift = [ -self.camera_center[i] + self.camera_size[i]/2 for i in range(2) ]
                self.camera_zoom = self.camera_start_zoom * (1 - self.camera_move_current_frame/self.camera_move_total_frames) + \
                    self.camera_end_zoom * (self.camera_move_current_frame/self.camera_move_total_frames)
                self.camera_move_current_frame += 1

            f.write('\\begin{scope}[transform canvas={scale=' + str(self.camera_zoom) + \
                    '}, shift={(' + str(self.camera_shift[0]) + ',' + str(self.camera_shift[1]) + ')} ]') 

            for obj in self.contents:
                if obj.start_frame <= frame and obj.stop_frame >= frame:
                    f.write(obj.draw_me(frame))
                    f.write('\n')
            
            f.write('\\end{scope} \n \\end{tikzpicture} \n' + \
                    '\\end{img} \n \n')
                             
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

class Line:
    def __init__(self,
                 ref = 'my_line',
                 start_point_list = [ [0,0] ],
                 stop_point_list = [ [0,0] ],
                 frames = [1, 1],
                 closed=False,
                 options = ''):

        self.ref = ref
        
        self.start_frame = frames[0]
        self.stop_frame = frames[1]
        self.closed = closed
        self.options = options

        self.points = []

        for i in range(len(start_point_list)):
            self.points.append( Point( name = self.ref + str(i),
                                       start_point = start_point_list[i],
                                       stop_point = stop_point_list[i],
                                       frames = [self.start_frame, self.stop_frame]) )
        
    def draw_me(self, frame):
        draw_commands = ''
        
        for point in self.points:
            draw_commands += point.draw_me(frame)
        
        draw_commands += '\draw[{}] ({})'.format(self.options, self.points[0].name)
        for point in self.points[1:]:
            draw_commands += '-- ({})'.format(point.name)
        if self.closed == True:
            draw_commands += '-- cycle'
        draw_commands += '; \n'
        
        return draw_commands
        

class Point:
    def __init__(self,
                 name = 'my_point',
                 start_point = [0, 0],
                 stop_point = [0, 0],
                 frames = [1, 1] ):
        self.name = name
        self.start_x = start_point[0]
        self.start_y = start_point[1]
        self.stop_x= stop_point[0]
        self.stop_y = stop_point[1]
        self.start_frame = frames[0]
        self.stop_frame = frames[1]
        
        self.x = self.start_x
        self.y = self.start_y
    
    def linear_interpolate(self, frame):
        if self.start_frame == self.stop_frame:
            t = 0
        else:
            t = (frame - self.start_frame)/(self.stop_frame - self.start_frame)
        self.x = (1-t) * self.start_x + t * self.stop_x
        self.y = (1-t) * self.start_y + t * self.stop_y
    
    def draw_me(self, frame):
        self.linear_interpolate(frame)
        return '\\coordinate ({}) at ({},{}); \n'.format(self.name, self.x, self.y)

class Node_Point:
    def __init__(self,
                 point_name = 'my_point',
                 frames = [1, 1],
                 contents = '',
                 options = ''):
        self.point_name = point_name
        self.start_frame = frames[0]
        self.stop_frame = frames[1]
        self.contents = contents
        self.options = options
        
    def draw_me(self, frame):
        return '\\draw (' + self.point_name + ') node[' + self.options + '] {' + self.contents + '}; \n'

class Node_Path:
    def __init__(self,
                 first_point = 'my_first_point',
                 second_point = 'my_second_point',
                 frames = [1,1],
                 contents = '',
                 options = ''):
        self.first_point = first_point
        self.second_point = second_point
        self.start_frame = frames[0]
        self.stop_frame = frames[1]
        self.contents = contents
        self.options = options

    def draw_me(self, frame):
        return '\\path (' + self.first_point + ') -- (' + self.second_point + \
               ') node[' + self.options + '] {' + self.contents + '}; \n'

class Circle:
    def __init__(self,
                 point_name = 'my_point',
                 frames = [1, 1],
                 radii = [0, 0],
                 options = ''):
        self.point_name = point_name
        self.start_frame = frames[0]
        self.stop_frame = frames[1]
        self.start_radius = radii[0]
        self.stop_radius = radii[1]
        self.options = options
        
        self.radius = self.start_radius

    def linear_interpolate(self, frame):
        t = (frame - self.start_frame)/(self.stop_frame - self.start_frame)
        self.radius = (1-t) * self.start_radius + t * self.stop_radius

    def draw_me(self, frame):
        self.linear_interpolate(frame)
        return '\\draw[' + self.options + '] (' + self.point_name + ') circle (' + str(self.radius) + '); \n'

class Literal:
    def __init__(self,
                 frames = [1, 1],
                 literal = ''):
        self.start_frame = frames[0]
        self.stop_frame = frames[1]
        self.literal = literal

    def draw_me(self, frame):
        return self.literal

class Scope:
    def __init__(self,
                 frames = [1, 1],
                 options = ''):
        self.start_frame = frames[0]
        self.stop_frame = frames[1]
        self.options = options
        
        self.contents = []

    def draw_me(self, frame):
        if self.start_frame <= frame and self.stop_frame >= frame:
            scope = '\\begin{scope}[' + self.options + '] \n'
            
            for obj in self.contents:
                if obj.start_frame <= frame and obj.stop_frame >= frame:
                    scope += obj.draw_me(frame) + '\n'
            
            scope += '\\end{scope} \n'
            return scope
        else:
            return 
        
class Graph:
    def __init__(self,
                 frames = [1, 1],
                 start_domain = [0,0],
                 stop_domain = [0,0],
                 x = '',
                 y = '',
                 parameter = 't',
                 samples = 50,
                 options = ''):
        self.start_frame = frames[0]
        self.stop_frame = frames[1]
        self.options = options
        self.samples = samples
        self.x = x
        self.y = y
        self.parameter = parameter
        self.start_domain = start_domain
        self.stop_domain = stop_domain
        
        self.left_endpoint = start_domain[0]
        self.right_endpoint = start_domain[1]
        
    def linear_interpolate(self, frame):
        t = (frame - self.start_frame)/(self.stop_frame - self.start_frame)
        self.left_endpoint = (1-t) * self.start_domain[0] + t * self.stop_domain[0]
        self.right_endpoint = (1-t) * self.start_domain[1] + t * self.stop_domain[1]

    def draw_me(self, frame):
        self.linear_interpolate(frame)
        return '\\draw[smooth, samples=' + str(self.samples) + \
            ',variable=\\' + self.parameter + \
            ',domain=' + str(self.left_endpoint) + ':' + str(self.right_endpoint) + \
            ',' + self.options + '] plot ( {' + self.x + '}, {' + self.y + '} ); \n'