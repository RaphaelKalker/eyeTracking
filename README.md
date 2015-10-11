# MuthaFokusing

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
