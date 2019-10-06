# lanim
LaTeX Animation

This is a program so that I can use TikZ to make animated math graphics. It works with my workflow, but I'm making no promises that this will make sense to anyone else.

The basic structure is that the Animation class contains a list of objects that represent things to be drawn. Once the objects are inserted, the make_me() method then produces a LaTeX file that can be compiled into a PDF, which can then be exported into PNG files using GIMP, and then loaded into Da Vinci Resolve to be turned into movie file of any type.

History:

V1 - This was just a first attempt. It was mostly a test of my ability to export LaTeX that creates an animation of some type, and it was the firs test of the linear interpolation to calculate the position of objects. This one ran entirely as functions instead of objects, and was therefore pretty clumsy.
V2 - This was the first move to using the object oriented structure. The Animation class didn't actually contain the objects, but rather it took in a list of objects that it would then attempt to animate. This introduced the Line, Point, Node_Point, Node_Path, Circle, and Literal classes. Each one was coded separately.
V3 - I changed the structure of the objects to have defaults that I could use instead of having to type in all of the features every time. The Scope and Graph classes were added.
V4 - This was my first attempt at adding a camera. The Camera class could be used to move the camera and adjust the zoom. I'm not 100% confident that it actually worked the way I wanted it to.
V5 - This is the second major refactorization of the code. I now have a hierarchy of classes so that I can take advantage of inheritance. This feels like a better approach, though I'm not certain that it is. I also fixed the camera so that I know it works the way I want. I also made the strings more consistent. Here is the tower of dependencies and the features at each level.

| [Obj(ref, frames, persist)]
| ----> The Obj class is the most general class. All animation objects must have these basic features:
| ---->>> ref: All objects have a reference, though most of them are meaningless for now. Eventually, I will want
| ---->>>      to be able to use these references in some way, though I'm not entirely sure how I'll do that.
| ---->>> frames: This is a list of two objects. The first is the entry frame and the second is the stop frame.
| ---->>>         To keep me from going insane, the frame count starts at 1 and not 0.
| ---->>> persist: If True, then the object will continue to be displayed after the last frame in its final position
| ---->>>          If False, the object disappears after the last frame.
| | [Line(start_point_list, stop_point_list, closed, options)]
| | ----> A Line is a multi-line that connects a sequence of points in order. Movement is linearly interpolated from
| | ----> the initial positions to the final positions.
| | ---->>> start_point_list: The initial positions of the vertices
| | ---->>> stop_point_list: The final positions of the vertices
| | ---->>> closed: If True, the last point will be connected back to the initial point to make a closed figure.
| | ---->>>         If False, the last point will not be connected back to the initial point, leaving the figure open.
| | [Node_On_Path(first_point, second_point, contents, options)]
| | ----> A Node_On_Path creates a node along a path between two points. These points can be coordinates or names
| | ----> of existing TikZ coordinates or Point_Obj-s.
| | ---->>> first_point: The first point of the path
| | ---->>> last_point: The last point of the path
| | ---->>> contents: The contents of the node.
| | ---->>> options: These are optional parameters that will be applied to the node.
| | [Literal(contents)]
| | ----> This just drops the literal contents into LaTeX. This is good for things that I haven't programmed yet.
| | ---->>> contents: The exact text to be dropped into LaTeX.
| | [Graph(start_domain, stop_domain, x, y, parameter, samples, options)]
| | ----> This creates a parametric graph. Having both a starting and stopping domain means that the graphing process
| | ----> can be animated.
| | ---->>> start_domain: This is the initial domain for the parametric plot
| | ---->>> stop_domain: This is the final domain for the parametric plot
| | ---->>> x: The x-coordinate as a function of the parameter
| | ---->>> y: The y-coordinate as a function of the parameter
| | ---->>> parameter: This is the symbol used for the parameter. The x and y functions must explicitly use this.
| | ---->>> samples: This affects the smoothness of the graph. More samples will lead to a smoother graph.
| | ---->>> options: This sets the options for the parametric plot.
| | [Anim_Obj(start_point, stop_point)]
| | ----> This sets up an animated object that can be referenced by a single point.
| | ---->>> start_point_list: The initial position of the object
| | ---->>> stop_point_list: The final position of the object
| | | [Circle(radii, options, at_point)]
| | | ----> A circle whose radius may be changing. Ellipses cannot currently be used with this because of the interpolation.
| | | ---->>> radii: A list containing the starting and stopping radius
| | | ---->>> options: Options to be applied to the circle
| | | ---->>> at_point: If True, the point is an existing reference and not a coordinate
| | | ---->>>           If False, this uses the start_point and stop_point coordinates for the animation
| | | [Point_Obj()]
| | | ----> Creates a TikZ coordinate at the specified location. I actually created this so that I could have a method
| | | ----> that will allow me to gain access to the coordinates of these types of objects. I haven't used this yet, but
| | | ----> it seems like it would be useful.
| | | | [Scope()]
| | | | ----> This creates a scope, which is a container that can hold lots of objects together. It's essentially a grouping
| | | | ----> function inside of TikZ. The scope contains a list called contents in which more animated objects can be placed.
| | | | [Node(contents, options, at_point)]
| | | | ----> This creates a node at the specified point.
| | | | ---->>> contents: The contents of the node
| | | | ---->>> options: Options to be applied to the node
| | | | ---->>> at_point: If True, the point is an existing reference and not a coordinate
| | | | ---->>>           If False, this uses the start_point and stop_point coordinates for the animation
| | | | | Text()
| | | | | ----> Text is always drawn at nodes. This simply feeds certain information into the contents and options
| | | | | ----> to create better uniformity of presentation.

Goals for V6:
* Make an Anchor scope that will do linearly interpolated translations and rotations around an anchor point. This will simplify more complex animations
* I think Point_Obj should get the at_point property.

Eventual goals: When I'm happy enough with it, make a tutorial
