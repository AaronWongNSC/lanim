# lanim
LaTeX Animation

This is a program so that I can use TikZ to make animated math graphics. It works with my workflow, but I'm making no promises that this will make sense to anyone else.

The basic structure is that the Animation class contains a list of objects that represent things to be drawn. Once the objects are inserted, the make_me() method then produces a LaTeX file that can be compiled into a PDF, which can then be exported into PNG files using GIMP, and then loaded into Da Vinci Resolve to be turned into movie file of any type.

History:

* AnimateV1 - This was just a first attempt. It was mostly a test of my ability to export LaTeX that creates an animation of some type, and it was the firs test of the linear interpolation to calculate the position of objects. This one ran entirely as functions instead of objects, and was therefore pretty clumsy.
* AnimateV2 - This was the first move to using the object oriented structure. The Animation class didn't actually contain the objects, but rather it took in a list of objects that it would then attempt to animate. This introduced the Line, Point, Node_Point, Node_Path, Circle, and Literal classes. Each one was coded separately.
* AnimateV3 - I changed the structure of the objects to have defaults that I could use instead of having to type in all of the features every time. The Scope and Graph classes were added.
* AnimateV4 - This was my first attempt at adding a camera. The Camera class could be used to move the camera and adjust the zoom. I'm not 100% confident that it actually worked the way I wanted it to.
* AnimateV5 - This is the second major refactorization of the code. I now have a hierarchy of classes so that I can take advantage of inheritance. This feels like a better approach, though I'm not certain that it is. I also fixed the camera so that I know it works the way I want. I also made the strings more consistent. Here is the tower of dependencies and the features at each level.
* LanimV1 - I did enough changes to this that I've decided to change the name of the package and start over. The same general ideas are there, but a lot of stuff has been cleaned up and reorganized. (Readme update at some point in the future.)

Eventual goals: When I'm happy enough with it, make a tutorial
