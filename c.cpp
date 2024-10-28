#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;

Scalar getWallColor(VideoCapture& cap) {
    Mat frame;
    cout << "Adjust the camera to focus on the wall and press 'c' to capture the wall color." << endl;

    while (true) {
        cap >> frame;
        if (frame.empty()) {
            break;
        }

        imshow("Wall Color Calibration", frame);
        if (waitKey(1) == 'c') {
            Vec3b color = frame.at<Vec3b>(240, 320);
            return Scalar(color[0], color[1], color[2]);
        }
    }

    return Scalar(0, 0, 0);
}

void pickUpColoredBalls(VideoCapture& cap, Scalar wallColorBGR) {
    Scalar lowerYellow(10, 74, 130);
    Scalar upperYellow(50, 255, 240);

    Scalar lowerBlue(100, 70, 70);
    Scalar upperBlue(150, 255, 255);

    Scalar lowerRed(150, 104, 70);
    Scalar upperRed(180, 255, 255);

    Mat img, hsv, maskBlue, maskRed, maskYellow, imgBlue, imgRed, imgYellow;

    while (true) {
        cap >> img;
        if (img.empty()) {
            break;
        }

        Size size(640, 480);
        Mat cimg1 = img.clone();

        // ノイズ除去
        medianBlur(img, img, 5);

        // Convert to HSV
        cvtColor(img, hsv, COLOR_BGR2HSV);

        // Create masks
        inRange(hsv, lowerBlue, upperBlue, maskBlue);
        inRange(hsv, lowerRed, upperRed, maskRed);
        inRange(hsv, lowerYellow, upperYellow, maskYellow);

        // Apply masks
        bitwise_and(img, img, imgBlue, maskBlue);
        bitwise_and(img, img, imgRed, maskRed);
        bitwise_and(img, img, imgYellow, maskYellow);

        // Hough transformation
        flip(img, img, 1);

        vector<tuple<Mat, Mat, string>> colors = {
            make_tuple(imgBlue, maskBlue, "Blue"),
            make_tuple(imgRed, maskRed, "Red"),
            make_tuple(imgYellow, maskYellow, "Yellow")
        };

        for (const auto& [imgColor, mask, colorName] : colors) {
            Mat resizedColor, grayColor;
            resize(imgColor, resizedColor, size);
            GaussianBlur(resizedColor, resizedColor, Size(15, 15), 1);
            cvtColor(resizedColor, grayColor, COLOR_BGR2GRAY);

            vector<Vec3f> circles;
            HoughCircles(grayColor, circles, HOUGH_GRADIENT, 1, 20, 50, 23, 5, 150);

            for (const auto& circle : circles) {
                Point center(cvRound(circle[0]), cvRound(circle[1]));
                int radius = cvRound(circle[2]);

                // Draw the outer circle
                circle(cimg1, center, radius, Scalar(0, 255, 0), 2);
                // Draw the center of the circle
                circle(cimg1, center, 2, Scalar(0, 0, 255), 3);
                // Add color label
                putText(cimg1, colorName, Point(center.x - 10, center.y - 10), FONT_HERSHEY_SIMPLEX, 0.5, Scalar(255, 255, 255), 2);
            }

            imshow(colorName + " Mask", resizedColor);
        }

        imshow("Original", cimg1);
        if (waitKey(10) == 27) {
            break;
        }
    }
}

int main() {
    VideoCapture cap(0);
    if (!cap.isOpened()) {
        cerr << "Error: Could not open the camera." << endl;
        return -1;
    }
    cap.set(CAP_PROP_FRAME_WIDTH, 640);
    cap.set(CAP_PROP_FRAME_HEIGHT, 480);

    Scalar wallColorBGR = getWallColor(cap);
    pickUpColoredBalls(cap, wallColorBGR);

    cap.release();
    destroyAllWindows();

    return 0;
}
