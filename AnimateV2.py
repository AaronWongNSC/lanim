class Animation:
    def __init__(self, size = [640, 480], length = 1, file_name = 'MyFile.tex', additional = ''):
        self.length = length
        self.file_name = file_name

        self.draw_boundary = '\\newcommand{\\BoundingBox}' + \
                             '{\\clip (0,0) rectangle (' + \
                             str(size[0]) + ',' + str(size[1]) + ');} \n\n'
    
        self.additional = additional


    def make_me(self, obj_list):
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
            
            for obj in obj_list:
                if obj.start_frame <= frame and obj.stop_frame >= frame:
                    f.write(obj.draw_me(frame))
                    f.write('\n')
            
            f.write('\\end{tikzpicture} \n' + \
                    '\\end{img} \n \n')
                             
        f.write('\\end{document} \n')
        f.close()    
        return(True)

class Line:
    def __init__(self, ref, start_point_list, stop_point_list, start_frame, stop_frame, closed=False, options = ''):
        self.ref = ref
        
        self.start_frame = start_frame
        self.stop_frame = stop_frame
        self.closed = closed
        self.options = options

        self.points = []

        for i in range(len(start_point_list)):
            self.points.append( Point( self.ref + str(i),
                                      start_point_list[i],
                                      stop_point_list[i],
                                      start_frame, stop_frame) )
        
    def draw_me(self, frame):
        draw_commands = ''
        
        for point in self.points:
            draw_commands += point.draw_me(frame)
        
        draw_commands += '\draw[{}] ({})'.format(self.options, self.points[0].ref)
        for point in self.points[1:]:
            draw_commands += '-- ({})'.format(point.ref)
        if self.closed == True:
            draw_commands += '-- cycle'
        draw_commands += '; \n'
        
        return draw_commands
        

class Point:
    def __init__(self, ref, start_point, stop_point, start_frame, stop_frame):
        self.ref = ref
        self.start_x = start_point[0]
        self.start_y = start_point[1]
        self.stop_x= stop_point[0]
        self.stop_y = stop_point[1]
        self.start_frame = start_frame
        self.stop_frame = stop_frame
        
        self.x = self.start_x
        self.y = self.start_y
    
    def linear_interpolate(self, frame):
        t = (frame - self.start_frame)/(self.stop_frame - self.start_frame)
        self.x = (1-t) * self.start_x + t * self.stop_x
        self.y = (1-t) * self.start_y + t * self.stop_y
    
    def draw_me(self, frame):
        self.linear_interpolate(frame)
        return '\\coordinate ({}) at ({},{}); \n'.format(self.ref, self.x, self.y)

class Node_Point:
    def __init__(self, point_name, start_frame, stop_frame, contents = '', options = ''):
        self.point_name = point_name
        self.start_frame = start_frame
        self.stop_frame = stop_frame
        self.contents = contents
        self.options = options
        
    def draw_me(self, frame):
        return '\\draw (' + self.point_name + ') node[' + self.options + '] {' + self.contents + '}; \n'

class Node_Path:
    def __init__(self, first_point, second_point, start_frame, stop_frame, contents = '', options = ''):
        self.first_point = first_point
        self.second_point = second_point
        self.start_frame = start_frame
        self.stop_frame = stop_frame
        self.contents = contents
        self.options = options

    def draw_me(self, frame):
        return '\\path (' + self.first_point + ') -- (' + self.second_point + \
               ') node[' + self.options + '] {' + self.contents + '}; \n'

class Circle:
    def __init__(self, point_name, start_frame, stop_frame, start_radius, stop_radius, options = ''):
        self.point_name = point_name
        self.start_frame = start_frame
        self.stop_frame = stop_frame
        self.start_radius = start_radius
        self.stop_radius = stop_radius
        self.options = options
        
        self.radius = start_radius

    def linear_interpolate(self, frame):
        t = (frame - self.start_frame)/(self.stop_frame - self.start_frame)
        self.radius = (1-t) * self.start_radius + t * self.stop_radius

    def draw_me(self, frame):
        self.linear_interpolate(frame)
        return '\\draw[' + self.options + '] (' + self.point_name + ') circle (' + str(self.radius) + '); \n'

class Literal:
    def __init__(self, start_frame, stop_frame, literal):
        self.start_frame = start_frame
        self.stop_frame = stop_frame
        self.literal = literal

    def draw_me(self, frame):
        return self.literal

class Scope:
    def __init__(self, start_frame, stop_frame, options = ''):
        self.start_frame = start_frame
        self.stop_frame = stop_frame
        self.options = options
        
        self.contents = []

    def draw_me(self, frame):
        scope = '\\begin{scope} \n'
        
        for obj in self.contents:
            if obj.start_frame <= frame and obj.stop_frame >= frame:
                scope += obj.draw_me(frame) + '\n'
        
        scope += '\\end{scope} \n'
        return(scope)
        







