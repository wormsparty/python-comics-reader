
Description
-----------

A comics reader, as simple as it should be.

The window is fullscreen and displays the image to fit correctly rotated 90° to the left.

The program will read all archives passed as argument after another. 

The program exits when you read the last frame of the last archive.


Keys
----

- To go to the next image, hit on any key stroke but Q, escape, and left.
- Left allows to go back one frame, or the the previous archive.
- Q and escape exit the program.


Dependencies
------------

- python3
- pyarchive
- pyglet (as of writing, need alpha version for python3 support)


BUGS 
----

Pyarchive segfaults if you pass a non-archive file as argument.

As of writing, pyglet alpha is requiered for python3 support,
but doesn't work on Mac OS X :/

