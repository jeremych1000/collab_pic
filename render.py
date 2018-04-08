import cv2


def greyscale_to_bw():
    img = cv2.imread("C:/Users/Jeremy/Documents/GitHub/collab_pic/example_pic/dxV2T1v_g.jpg", cv2.IMREAD_GRAYSCALE)
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    (thresh, im_bw) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    (thresh, im_bw_blur) = cv2.threshold(blur, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    cv2.imshow("bnw", im_bw)
    cv2.imwrite("bw.jpg", im_bw)

    cv2.imshow("bw_blur", im_bw_blur)
    cv2.imwrite("bw_blur.jpg", im_bw_blur)

