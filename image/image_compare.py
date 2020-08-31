'''
简单的图形对比，入参为基准图和测试图片，入参为路径时，注意修改对比图文件名处代码；并可通过ignorepercent设置自动忽略范围；
'''

import cv2
from skimage.measure import compare_ssim
import imutils


def compareimage(goodimage, testimage, ignorepercent=float(0), waittime=0):
    # construct the argument parse and parse the arguments
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-f", "--first", required=True,
    #                 help="first input image")
    # ap.add_argument("-s", "--second", required=True,
    #                 help="second")
    # args = vars(ap.parse_args())
    # # load the two input images
    # imageA = cv2.imread(args["first"])
    # imageB = cv2.imread(args["second"])
    #

    imageA = cv2.imread(goodimage)
    imageB = cv2.imread(testimage)

    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    # ​structural similarity index measurement (SSIM) system一种衡量两幅图像结构相似度的新指标，其值越大越好，最大为1。

    (score, diff) = compare_ssim(grayA, grayB, full=True)

    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))

    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # loop over the contours
    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), -1)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # show the output images
    cv2.imshow("Original", imageA)
    cv2.imshow("Modified", imageB)
    # cv2.imshow("Diff", diff)
    # cv2.imshow("Thresh", thresh)
    # save the output images
    cv2.imwrite('%s_diff.png' % testimage[:-4], imageB)
    cv2.waitKey(60000)
    if score >= 1 - ignorepercent:
        return 'pass'
    else:
        # result = tkinter.messagebox.askokcancel('提示', '是否通过?')
        # if result:
        #     return 'pass'
        # else:
        return 'fail'


if __name__ == '__main__':
    a = compareimage('screenshot_goodpdp.png', 'screenshot_testpdp.png', ignorepercent=0.002)
    print(a)
