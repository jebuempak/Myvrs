#include <stdio.h>
#include <opencv2/opencv.h>
#include <opencv2/highgui/highgui_c.h>

int main() {
    CvCapture* capture = cvCaptureFromCAM(0);
    if (!capture) {
        fprintf(stderr, "Error: Couldn't open the webcam.\n");
        return -1;
    }

    IplImage* frame = NULL;
    IplImage* background = NULL;
    IplImage* diffImage = NULL;

    while (1) {
        frame = cvQueryFrame(capture);
        if (!frame) break;

        if (!background) {
            background = cvCloneImage(frame);
            diffImage = cvCreateImage(cvGetSize(frame), IPL_DEPTH_8U, 3);
        }

        cvAbsDiff(frame, background, diffImage);

        // Convert to grayscale
        IplImage* grayDiff = cvCreateImage(cvGetSize(frame), IPL_DEPTH_8U, 1);
        cvCvtColor(diffImage, grayDiff, CV_BGR2GRAY);

        // Threshold to get the mask
        cvThreshold(grayDiff, grayDiff, 25, 255, CV_THRESH_BINARY);

        // Use the mask to extract the foreground
        IplImage* foreground = cvCreateImage(cvGetSize(frame), IPL_DEPTH_8U, 3);
        cvCopy(frame, foreground, grayDiff);

        cvShowImage("Webcam", frame);
        cvShowImage("Foreground", foreground);

        // Release the temporary images
        cvReleaseImage(&grayDiff);
        cvReleaseImage(&foreground);

        char c = cvWaitKey(33);
        if (c == 27) break;
    }

    cvReleaseCapture(&capture);
    cvReleaseImage(&background);
    cvReleaseImage(&diffImage);
    cvDestroyAllWindows();

    return 0;
}
