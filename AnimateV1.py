FILENAME = 'MyFile.tex'
MAXFRAME = 50

def LineCoords(frame, object):
    x0, y0 = InterpolateCoord(frame, object[2], object[3], object[4], object[6])
    x1, y1 = InterpolateCoord(frame, object[2], object[3], object[5], object[7])
    return (x0, y0, x1, y1)

def InterpolateCoord(frame, StartFrame, StopFrame, StartCoord, StopCoord):
    x = Interpolate(frame, StartFrame, StopFrame, StartCoord[0], StopCoord[0])
    y = Interpolate(frame, StartFrame, StopFrame, StartCoord[1], StopCoord[1])
    return (x, y)

def Interpolate(frame, StartFrame, StopFrame, StartVal, StopVal):
    t = (frame - StartFrame)/(StopFrame - StartFrame)
    return (1 - t) * StartVal + t * StopVal

PREAMBLE = '''\\documentclass[multi={img},preview]{standalone}
\\usepackage{amsmath,amssymb}
\\usepackage{tikz}

\\usetikzlibrary{arrows.meta}

\\newenvironment{img}{}{}
\n'''

COLORDEFS = '''\\definecolor{ltblue}{rgb} {0.7,0.7,1}
\\definecolor{ltred}{rgb} {1,0.7,0.7}
\n'''

MATHSYM = '''\\newcommand{\\N}{\\mathbb{N}}
\\newcommand{\\Q}{\\mathbb{Q}}
\\newcommand{\\R}{\\mathbb{R}}
\\newcommand{\\Z}{\\mathbb{Z}}
\n'''

# BoundingBox
# -- 1918x1078 for full 1080 HD
# -- 99x99 for 100x100 final box
BOUNDINGBOX = '''\\newcommand{\\BoundingBox}{
  \\clip (0,0) rectangle (399,399);
}
\n'''

# Arrow Styles
ARROWSTYLES = '''\\tikzset{%
   leftarrow/.style = {{Latex[length=5mm, width=2mm]}-},
   rightarrow/.style = {-{Latex[length=5mm, width=2mm]}},
   doublearrow/.style = {{Latex[length=5mm, width=2mm]}-{Latex[length=5mm, width=2mm]}},   
}
\n'''

BEGINDOC = '''\\begin{document}
\n'''

ENDDOC = '''\\end{document}
\n'''

# Text Styles
TEXTSTYLES = '''\\tikzset{%
   bigtext/.style = {scale=3},
   regtext/.style = {scale=2},
}
\n'''

STARTIMG = '''\\begin{img}
  \\begin{tikzpicture}[x=0.005in,y=0.005in]
    \\BoundingBox
\n'''

ENDIMG = '''  \\end{tikzpicture}
\\end{img}
\n'''

IMG1 = '''\\begin{img}
  \\begin{tikzpicture}[x=0.005in,y=0.005in]
    \\BoundingBox
    \\draw[rightarrow] (20,20) -- (80,80);
  \\end{tikzpicture}
\\end{img}
\n'''

drawobjects = []

# Tested
# Line: ['l', params, FirstFrame, LastFrame, [ [xi, yi], ...], [ [xf, yf], ...] ]
# Text: ['t', params, FirstFrame, LastFrame, [xi, yi], [xf, yf], text ]
# Ellipse: ['e', params, FirstFrame, LastFrame, [xi, yi], [ai, bi], [xf, yf], [af, bf] ]
# Circle: ['c', params, FirstFrame, LastFrame, [xi, yi], ri, [xf, yf], rf]

drawobjects.append(['l', 'ultra thick,rightarrow', 10, 40, [[10,10], [290,290], [50,250]], [[150,390], [290,10], [30,30]] ])
drawobjects.append(['t', 'regtext,anchor=mid', 5, 45, [20,300], [350,100], 'Text' ])
drawobjects.append(['e', 'fill=ltblue, opacity=0.5', 15, 30, [100,100], [50,20], [300,100], [10,60] ]) 
drawobjects.append(['c', 'fill=ltred, opacity=0.5', 15, 30, [100,300], 20, [300,100], 100 ]) 

# Untested
# Fill: ['f', params, FirstFrame, LastFrame, [ [xi, yi], ...], [ [xf, yf], ...] ]
# Special: ['s', empty, FirstFrame, LastFrame, FullCommand]

f = open(FILENAME, 'w')

f.write(PREAMBLE
         + COLORDEFS
         + MATHSYM
         + BOUNDINGBOX
         + ARROWSTYLES
         + TEXTSTYLES
         + BEGINDOC)

for frame in range(MAXFRAME):
    print(frame)
    IMG = STARTIMG
    for object in drawobjects:
        if object[2] <= frame and object[3] >= frame:
            print(object)
            
            if object[0] == 'l':
                IMG = IMG + '    \\draw[' + object[1] + '] '
                x, y = InterpolateCoord(frame, object[2], object[3], object[4][0], object[5][0])
                IMG = IMG + '(' + str(x) + ', ' + str(y) + ') '
                for v in range(1, len(object[4])):
                    x, y = InterpolateCoord(frame, object[2], object[3], object[4][v], object[5][v])
                    IMG = IMG +  '-- ' + '(' + str(x) + ', ' + str(y) + ') '
                IMG = IMG + ';\n'
            
            elif object[0] == 't':
                x, y = InterpolateCoord(frame, object[2], object[3], object[4], object[5])
                IMG = IMG + '    \\draw ' + \
                         '(' + str(x) + ', ' + str(y) + ') ' + \
                         'node[' + object[1] + '] ' + \
                         '{' + object[6] + '};\n'

            elif object[0] == 'e':
                x, y = InterpolateCoord(frame, object[2], object[3], object[4], object[6])
                a = Interpolate(frame, object[2], object[3], object[5][0], object[7][0])
                b = Interpolate(frame, object[2], object[3], object[5][1], object[7][1])
                IMG = IMG + '    \\draw[' + object[1] + '] ' + \
                         '(' + str(x) + ', ' + str(y) + ') ' + \
                         'ellipse (' + str(a) + ' and ' + str(b) + ');\n'

            elif object[0] == 'c':
                x, y = InterpolateCoord(frame, object[2], object[3], object[4], object[6])
                r = Interpolate(frame, object[2], object[3], object[5], object[7])
                IMG = IMG + '    \\draw[' + object[1] + '] ' + \
                         '(' + str(x) + ', ' + str(y) + ') ' + \
                         'circle (' + str(r) + ');\n'

    IMG += ENDIMG
    f.write(IMG)
                     
f.write(ENDDOC)

f.close()