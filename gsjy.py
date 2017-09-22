#-*-coding:utf-8-*-
import requests
import re
import StringIO
import random
import math
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from bs4 import BeautifulSoup
from lxml import etree
from PIL import Image
class crack_picture(object):
    def __init__(self, img_url1, img_url2):
        self.img1, self.img2 = self.picture_get(img_url1, img_url2)


    def picture_get(self, img_url1, img_url2):
        hd = {"Host": "static.geetest.com",
              "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}
        img1 = StringIO.StringIO(self.repeat(img_url1, hd).content)
        img2 = StringIO.StringIO(self.repeat(img_url2, hd).content)
        return img1, img2

    #尝试10次
    def repeat(self, url, hd):
        times = 10
        while times > 0:
            try:
                ans = requests.get(url, headers=hd)
                print ans.content
                return ans
            except:
                times -= 1


    def pictures_recover(self):
        xpos = self.judge(self.picture_recover(self.img1, 'img1.jpg'), self.picture_recover(self.img2, 'img2.jpg')) - 6
        return self.darbra_track(xpos)


    def picture_recover(self, img, name):
        a =[39, 38, 48, 49, 41, 40, 46, 47, 35, 34, 50, 51, 33, 32, 28, 29, 27, 26, 36, 37, 31, 30, 44, 45, 43, 42, 12, 13, 23, 22, 14, 15, 21, 20, 8, 9, 25, 24, 6, 7, 3, 2, 0, 1, 11, 10, 4, 5, 19, 18, 16, 17]
        im = Image.open(img)
        im_new = Image.new("RGB", (260, 116))
        for row in range(2):
            for column in range(26):
                right = a[row*26+column] % 26 * 12 + 1
                down = 58 if a[row*26+column] > 25 else 0
                for w in range(10):
                    for h in range(58):
                        ht = 58 * row + h
                        wd = 10 * column + w
                        im_new.putpixel((wd, ht), im.getpixel((w + right, h + down)))
        im_new.save(name)
        return im_new


    def darbra_track(self, distance):
        return [[distance, 0.5, 1]]
        #crucial trace code was deleted


    def diff(self, img1, img2, wd, ht):
        rgb1 = img1.getpixel((wd, ht))
        rgb2 = img2.getpixel((wd, ht))
        tmp = reduce(lambda x,y: x+y, map(lambda x: abs(x[0]-x[1]), zip(rgb1, rgb2)))
        return True if tmp >= 200 else False


    def col(self, img1, img2, cl):
        for i in range(img2.size[1]):
            if self.diff(img1, img2, cl, i):
                return True
        return False


    def judge(self, img1, img2):
        for i in range(img2.size[0]):
            if self.col(img1, img2, i):
                return i
        return -1

    def get_gap(self, image1, image2):
        """
        获取缺口偏移量
        :param image1: 不带缺口图片
        :param image2: 带缺口图片
        :return:
        """
        left = 60
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                # a = 2
                b = random.random()
                a = math.tan(b)
            else:
                # 加速度为负3
                # a = -3
                b = random.random()
                a = math.tan(b)
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track







class gsxt(object):
    def __init__(self, br_name="phantomjs"):
        self.br = self.get_webdriver(br_name)
        self.wait = WebDriverWait(self.br, 10, 1.0)
        self.br.set_page_load_timeout(120)
        self.br.set_script_timeout(120)

    def input_params(self, name):
        self.br.get("http://www.gsxt.gov.cn/index")
        element = self.wait_for(By.ID, "keyword")
        element.send_keys(name)
        time.sleep(1.1)
        element = self.wait_for(By.ID, "btn_query")
        element.click()
        time.sleep(1.1)

    def get_webdriver(self, name):
        if name.lower() == "phantomjs":
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
            return webdriver.PhantomJS(desired_capabilities=dcap)

        elif name.lower() == "chrome":
            # desired_capabilities = DesiredCapabilities.CHROME.copy()
            # my_proxy = {'httpProxy':'112.84.119.175:8888','sslProxy':'112.84.119.175:8888'}
            # proxy = Proxy(my_proxy)
            # proxy.add_to_capabilities(desired_capabilities)
            # return webdriver.Chrome(desired_capabilities = desired_capabilities)
            return webdriver.Chrome()

    def quit_webdriver(self):
        self.br.quit()

    #获取分割
    def drag_pic(self):
        #gt_cut_fullbg_slice 为被扣之前的背景图(乱序完整图)
        #gt_cut_bg_slice 为被扣之后的背景图(乱序残缺图)
        return (self.find_img_url(self.wait_for(By.CLASS_NAME, "gt_cut_fullbg_slice")),
               self.find_img_url(self.wait_for(By.CLASS_NAME, "gt_cut_bg_slice")))

    #显示等待查找,by1为查找方式, by2为条件值
    def wait_for(self, by1, by2):
        return self.wait.until(EC.presence_of_element_located((by1, by2)))

    #获取图片
    def find_img_url(self, element):
        try:
            return re.findall('url\("(.*?)"\)', element.get_attribute('style'))[0].replace("webp", "jpg")
        except:
            return re.findall('url\((.*?)\)', element.get_attribute('style'))[0].replace("webp", "jpg")

    def hack_geetest(self, company=u"招商银行"):
        self.input_params(company)
        img_url1, img_url2 = self.drag_pic()
        cp = crack_picture(img_url1, img_url2)
        img1 = cp.picture_recover(cp.img1,'img1.jpg')
        img2 = cp.picture_recover(cp.img2,'img2.jpg')
        gap = cp.get_gap(img1, img2)
        track = cp.get_track(gap-6)
        print track
        tsb = self.emulate_track(track)
        if '通过' in tsb:
            time.sleep(1)
            soup = BeautifulSoup(self.br.page_source, 'html.parser')
            for sp in soup.find_all("a", attrs={"class":"search_list_item"}):
                print re.sub("\s+", "", sp.get_text().encode("utf-8"))
                #print sp.get_text()
                break
        elif '吃' in tsb:
            time.sleep(5)
        else:
            self.input_params(company)
        #  # 拖动滑块
        # slider = self.br.find_element_by_class_name("gt_slider_knob")
        # ActionChains(self.br).click_and_hold(slider).perform()
        # for x in track:
        #     ActionChains(self.br).move_by_offset(xoffset=x, yoffset=0).perform()
        # time.sleep(0.5)
        # ActionChains(self.br).release().perform()
        # while True:
        #     time.sleep(10)
        #     element = self.wait_for(By.CLASS_NAME, "gt_info_text")
        #     tsb = element.text.encode("utf-8")
        #     if '通过' in tsb:
        #         time.sleep(1)
        #         soup = BeautifulSoup(self.br.page_source, 'html.parser')
        #         for sp in soup.find_all("a", attrs={"class":"search_list_item"}):
        #             print re.sub("\s+", "", sp.get_text().encode("utf-8"))
        #             #print sp.get_text()
        #         break
        #     elif '吃' in tsb:
        #         time.sleep(5)
        #     else:
        #         self.input_params(company)

    #模仿轨迹获取cookies和页面源码
    def emulate_track(self,track):
        element = self.br.find_element_by_class_name("gt_slider_knob")
        ActionChains(self.br).click_and_hold(on_element=element).perform()
        for x in track:
            ActionChains(self.br).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.24)
        ActionChains(self.br).release(on_element=element).perform()
        time.sleep(0.8)
        element = self.wait_for(By.CLASS_NAME, "gt_info_text")
        ans = element.text.encode("utf-8")
        return ans

    def run(self):
        for i in [ u'交通银行', u'中国银行']:
            self.hack_geetest(i)
            time.sleep(1)
        self.quit_webdriver()

if __name__ == '__main__':
    gsxt('chrome').run()