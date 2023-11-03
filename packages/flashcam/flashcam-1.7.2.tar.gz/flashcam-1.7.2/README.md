Project flashcam
================

`FLASk supported webCAM`

*IN DEVELOPMENT*

Here, the merge of several ideas forms an easy (pip) installable webcam
server. The basic goal is to

-   view various technical devices during an experiment
    -   with an info on delay
    -   some record capabilities
-   have some tools to get more from the stream

Technical
=========

-   the camera itself is launched from *web.py* function *frames()*,
    where

*Camera()* class (defined in *real~camerra~.py*) is called first.

Usage
=====

See README.howto.org

Or run with *-h*

Some references
===============

<https://longervision.github.io/2017/03/12/ComputerVision/OpenCV/opencv-external-posture-estimation-ArUco-board/>

<https://github.com/LongerVision/Examples_OpenCV/blob/master/01_internal_camera_calibration/chessboard.py>

<https://markhedleyjones.com/projects/calibration-checkerboard-collection>
