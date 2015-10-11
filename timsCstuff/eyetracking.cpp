#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include <stdlib.h>
#include <stdio.h>

using namespace cv;

/// Global variables

int threshold_value = 70;
int threshold_type = 2;
int circle_size = 100;
int const max_value = 255;
int const max_type = 4;
int const max_BINARY_value = 255;
int scan = 0;

Mat src, src_gray, dst;
char* window_name = "Threshold Demo";

char* trackbar_type = "Type: \n 0: Binary \n 1: Binary Inverted \n 2: Truncate \n 3: To Zero \n 4: To Zero Inverted";
char* trackbar_value = "Value";

char* trackbar_circle_size = "circle:";

/// Function headers
void Threshold_Demo( int, void* );

/**
 * @function main
 */
int main( int argc, char** argv )
{
  /// Load an image
  src = imread( argv[1], 1 );

  /// Convert the image to Gray
  cvtColor( src, src_gray, CV_RGB2GRAY );
  
  /// Create a window to display results
  namedWindow( window_name, CV_WINDOW_AUTOSIZE );

  /// Create Trackbar to choose type of Threshold
  createTrackbar( trackbar_type,
		  window_name, &threshold_type,
		  max_type, Threshold_Demo );

  createTrackbar( trackbar_circle_size,
		  window_name, &circle_size,
		  max_value, Threshold_Demo );

  createTrackbar( trackbar_value,
		  window_name, &threshold_value,
		  max_value, Threshold_Demo );

  int folderNum = 1;
  char eye = 'L';
  int bmp = 1;
  
  while(true)
  {
  /// Call the function to initialize
  Threshold_Demo( 0, 0 );

  /// Wait until user finishes program
  //  while(true)
    //  {
    int c;
    c = waitKey( 20 );
    if( (char)c == 27 )
    { break; }
    if( (char)c == 's')
    {
      scan = 1;
    }
    if( (char)c == 'a')
    {
      std::string file = "../UTIRIS_V.1/Infrared_Images/00" + std::to_string(folderNum) + "/00"
	+ std::to_string(folderNum) + "_" + eye + "/" + "Img_00" + std::to_string(folderNum)
	+ "_" + eye + "_" + std::to_string(bmp) + ".bmp";
      src = imread( file, 1 );
      cvtColor( src, src_gray, CV_RGB2GRAY );

      bmp++;
      if(bmp > 5)
      {
	if(eye == 'L')
	{
	  eye = 'R';
	}
	else
	{
	  eye = 'L';
	  folderNum++;
	}
	bmp = bmp%5;
      }
      
    }
    
  }

}


/**
 * @function Threshold_Demo
 */
void Threshold_Demo( int, void* )
{
  /* 0: Binary
     1: Binary Inverted
     2: Threshold Truncated
     3: Threshold to Zero
     4: Threshold to Zero Inverted
  */

  /*
    for image testing:
    circle size ~= 100
    thresholding at Threshold Truncated
    value = 125
   */

  threshold( src_gray, dst, threshold_value, max_BINARY_value,threshold_type );
  absdiff(dst, 255, dst);
  
  //fill in the partial sections of the image
  Mat dst_cpy;
  dst.copyTo(dst_cpy);
  std::vector<std::vector<Point> > contours;
  std::vector<Vec4i> hierarchy;
  findContours( dst_cpy, contours, hierarchy, RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE, Point(0, 0) );
  

  bool notOneCircleDetected = 1;
  double circleVal = 20;
  std::vector<Vec3f> circles;

  if(scan)
  {
  for(int i = 0; i < 100 && notOneCircleDetected; ++i)
  {
    HoughCircles( dst, circles, CV_HOUGH_GRADIENT, 1, dst.rows/32, 100, circleVal, 35, circle_size );

    //  cvtColor( dst, dst_output, CV_GRAY2RGB );
    if(circles.size() < 1)
    {
      notOneCircleDetected = 1;
      circleVal--;
      circles.clear();
      if(circleVal > 100)
      {
	notOneCircleDetected = 0;  //ERROR CASE
      }
    }
    else if(circles.size() > 1)
    {
      //too sensitive
      if(circleVal > 1)
	circleVal++;
      else
	notOneCircleDetected = 0;
    }
    else
    {
      notOneCircleDetected;
    }
  }
  }
  else
  {
    HoughCircles( dst, circles, CV_HOUGH_GRADIENT, 1, dst.rows/32, 100, 5, 35, circle_size );
  }
  
  for( size_t i = 0; i < circles.size(); i++ )
  {
    Point center(cvRound(circles[i][0]), cvRound(circles[i][1]));
    int radius = cvRound(circles[i][2]);
    // circle center
    circle( dst, center, 3, Scalar(125,125,0), -1, 8, 0 );
    // circle outline
    circle( dst, center, radius, Scalar(125,125,0), 3, 8, 0 );
  }
    
  imshow( window_name, dst );
}
