# Hocus-Pocus-Focus

### Installing OPEN CV 3

Copy and paste this in terminal (not iterm) within the build folder after pulling from github

  cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local \
	-D PYTHON2_PACKAGES_PATH=~/.virtualenvs/cv/lib/python2.7/site-packages \
	-D PYTHON2_LIBRARY=/usr/local/Cellar/python/2.7.10/Frameworks/Python.framework/Versions/2.7/bin \
	-D PYTHON2_INCLUDE_DIR=/usr/local/Frameworks/Python.framework/Headers \
	-D INSTALL_C_EXAMPLES=OFF -D INSTALL_PYTHON_EXAMPLES=ON \
	-D BUILD_EXAMPLES=ON \
	-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules ..

### Python 
 - Setup your python environment properly and make sure you are using 2.7x with openCV3. 
 - Download PyCharm
 - Run Start.py
 - Dump your pupil images in the imageTest folder within the same directory as the python files

### C++ 

If wanting to run the C version follow these commands:

navigate to the timsCstuff/build directory. If not there, then mkdir it

cmake -DCMAKE_BUILD_TYPE=DEBUG ..

make

now to run the program:

./eyetracking ../test.bmp

this will run it against the test image in the folder above.
sliders above will adjust the:

1) maximum circle size detected by the hough transform

2) thresholding type

3) thresholding value

there are also keybindings to do other things,
pressing "s" will auto-tune the parameters to only find one circle (or it will find a setting closest to finding one value)

pressing "a" will cycle through multiple images. But here you need to put the UTIRIS dataset straight into the timsCstuff directory
and you will need to rename a couple of the images to match the format of the filenames. I know the first person has wrongly named images.
Just give it a rename, and it should work. 
