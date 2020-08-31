'''
数字图形验证码识别
'''

from appium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
from time import sleep
import pytesseract

# Appium配置
desired_capabilities = {
    'platformName': 'Android',
    'deviceName': '3HX5T16C11014114',  # 模拟器地址及端口号
    'platformVersion': '8.0.0',  # Android版本
    'appPackage': 'com.tencent.mm',  # 包名，获取方式详见appPackage、appActivity获取
    'appActivity': 'com.tencent.mm.ui.LauncherUI',
    'noReset': 'true',  # 每次重新打开不重置app，为false时表示每次打开均重置
    'newCommandTimeout': 600,  # 设置超时时间，如果不设置，1分钟appium没接收到新请求就会关闭链接
    'autoAcceptAlerts': 'true',
    'chromeOptions': {"androidProcess": "com.tencent.mm:tools"}
}
remote_url = 'http://localhost:4725/wd/hub'

# 元素定位'
codeimg = (By.XPATH, '//android.webkit.WebView[@text=\"wx4bf8ed4d0545742b:pages/login/index.html:VISIBLE\"]'
                     '/android.view.View[2]/android.view.View[3]/android.view.View[2]')
submit = (By.XPATH, '//android.view.View[@text=\"登录\"]')
title = (By.XPATH, '//android.webkit.WebView[@text=\"wx4bf8ed4d0545742b:pages/login/index.html:VISIBLE\"]'
                   '/android.view.View[1]')
# Appium webdriver启动
driver = webdriver.Remote(remote_url, desired_capabilities)


# 方法封装
def find(locator):
    return driver.find_element(*locator)


def togetCode():
    getImage(find(codeimg))
    return getcode()


def sendlogincode(inputcode='验证码'):
    getcode = togetCode().replace(' ', '')[:4]  # 去除可能识别误差的空格,并保留前4位
    driver.find_element_by_android_uiautomator('new UiSelector().text("%s")' % inputcode).clear()
    driver.find_element_by_android_uiautomator('new UiSelector().text("验证码")').send_keys(getcode)
    global code
    code = getcode


def sublogin():
    find(submit).click()


def checklogin():
    '''
    判断是否登录成功，失败则重新识别重新尝试登录
    :return:
    '''
    while 0 < 1:
        try:
            cach = find(title)
            print('验证码识别为：%s' % code)
            sendlogincode(inputcode=code)
            sublogin()
            continue
        except Exception:
            print('登录成功')
            break


def getImage(element):
    driver.get_screenshot_as_file('./screenshotimg.png')  # 保存当前界面为图片
    print('已保存截图至./screenshotimg.png')
    left = element.location['x']  # element为定位到的元素
    top = element.location['y']
    right = element.location['x'] + element.size['width']  # 右边界
    bottom = element.location['y'] + element.size['height']  # 下边界
    im = Image.open('screenshotimg.png')  # 打开图片
    im = im.crop((left, top, right, bottom))  # 裁剪，从界面图片中裁剪出验证码图片，如果实际返回为base64数据，可直接保存不需要截图裁剪操作
    im.save('./screenshotimg.png')  # 保存处理后的
    print('已保存处理图像至./screenshotimg.png')


def getcode():
    im = Image.open('./screenshotimg.png')
    sleep(0.5)
    ##转换成黑白图
    threshold = 140
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    img1 = im.convert('L')  # 灰度图
    out = img1.point(table, '1')
    out.save('./screenshot_gray_img.png')
    img2 = Image.open('./screenshot_gray_img.png')
    ##去除斜线
    w, h = img2.size  # 图片的长宽
    # data.getpixel((x,y))获取目标像素点颜色。
    # data.putpixel((x,y),255)更改像素点颜色，255代表颜色。
    try:
        for x in range(1, w - 1):
            if x > 1 and x != w - 2:
                # 获取目标像素点左右位置
                left = x - 1
                right = x + 1
            for y in range(1, h - 1):
                # 获取目标像素点上下位置
                up = y - 1
                down = y + 1
                if x <= 2 or x >= (w - 2):
                    img2.putpixel((x, y), 255)
                elif y <= 2 or y >= (h - 2):
                    img2.putpixel((x, y), 255)
                elif img2.getpixel((x, y)) == 0:
                    if y > 1 and y != h - 1:

                        # 以目标像素点为中心点，获取周围像素点颜色
                        # 0为黑色，255为白色
                        up_color = img2.getpixel((x, up))
                        down_color = img2.getpixel((x, down))
                        left_color = img2.getpixel((left, y))
                        left_down_color = img2.getpixel((left, down))
                        right_color = img2.getpixel((right, y))
                        right_up_color = img2.getpixel((right, up))
                        right_down_color = img2.getpixel((right, down))

                        # 去除竖线干扰线
                        if down_color == 0:
                            if left_color == 255 and left_down_color == 255 and \
                                    right_color == 255 and right_down_color == 255:
                                img2.putpixel((x, y), 255)

                        # 去除横线干扰线
                        elif right_color == 0:
                            if down_color == 255 and right_down_color == 255 and \
                                    up_color == 255 and right_up_color == 255:
                                img2.putpixel((x, y), 255)

                    # 去除斜线干扰线
                    if left_color == 255 and right_color == 255 \
                            and up_color == 255 and down_color == 255:
                        img2.putpixel((x, y), 255)
                else:
                    pass

                    # 保存去除干扰线后的图片
                    img2.save('./screenshot_gray_img.png', "png")
    except:
        return False
    img3 = Image.open('./screenshot_gray_img.png')
    logincode = pytesseract.image_to_string(img3)  # 识别经过两次处理的验证码
    return logincode
