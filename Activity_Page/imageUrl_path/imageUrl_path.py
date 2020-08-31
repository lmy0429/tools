'''
 1.配置Python环境，安装xlrd、selenium第三方库；
 2. 提前下载对应Chrome版本的Chromedriver到本地，并配置到环境变量；或者在webdriver.Chrome()中增加参数executable_path=driverpath
    ，driverpath为实际Chromedriver路径；
 3.通过修改filepath配置Excel用例路径
'''

import xlrd, time, difflib, os
from selenium import webdriver

# Excel用例路径配置
filepath = r"./demo.xlsx"


def excledata():
    file = xlrd.open_workbook(filepath)
    sheet = file.sheet_by_index(0)
    activity_baseinfo = {"host": sheet.row_values(0)[1], "activity_url": sheet.row_values(0)[3]}

    # 打印测试活动页链接
    print("activity_url:{0}".format(activity_baseinfo["activity_url"]))
    test_data = []
    for row in range(2, sheet.nrows):
        data = dict(zip(sheet.row_values(1), sheet.row_values(row)))
        test_data.append(data)
    data = [activity_baseinfo, test_data]
    return data


def startweb():
    chromeoptions = webdriver.ChromeOptions()
    chromeoptions.add_argument("--headless")
    # 配置页面分辨率
    chromeoptions.add_argument("window-size=760,1080")
    driver = webdriver.Chrome(chrome_options=chromeoptions)
    return driver


def result():
    activity_baseinfo, test_data = excledata()
    driver = startweb()
    driver.get(activity_baseinfo.get("activity_url"))
    time.sleep(2)
    for id in range(len(test_data)):
        # 根据XPATH路径获取元素定位，并提取href中实际url；不同项目可自行调整
        actual_url = driver.find_element_by_xpath(test_data[id].get("xpath")).get_attribute("href")
        except_url = activity_baseinfo.get("host") + test_data[id].get("except_url")
        if actual_url != except_url:
            print("第{0}个链接错误,期望：{1}，实际：{2}".format(int(test_data[id].get("id")), except_url, actual_url))
        with open("actual_url.txt", "a")as f:
            f.write(actual_url + "\n")
        with open("except_url.txt", "a")as file:
            file.write(except_url + "\n")
    with open("actual_url.txt", "r") as f:
        actual_url_all = f.read().splitlines()
    with open("except_url.txt", "r") as file:
        except_url_all = file.read().splitlines()
    diff = difflib.HtmlDiff()
    diffresult = diff.make_file(except_url_all, actual_url_all)
    with open("testresult.html", "w") as f:
        f.write(diffresult)
    os.remove("actual_url.txt")
    os.remove("except_url.txt")
    driver.quit()


if __name__ == "__main__":
    result()
