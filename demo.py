# -*- coding:utf-8 -*-

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import NoSuchElementException

"""
先获取页面商品的接口，爬取关键信息，组建成字典
去重后，根据字典顺序，点击每个商品，获取点击效果
将点击效果反馈到列表里
合并字典和列表，组成最终table
导出为excel或者直接打印
"""
# url = "https://opensea.io/__api/tokens/?limit=100"  # 访问存在连接问题，暂弃用
# Headers = {
# "cookie":'__os_session=eyJpZCI6IjUyZTBiNDc0LWJiOTktNGEyMi05MjFkLTFiOWMyNzBlYzQ3OSJ9; __os_session.sig=YZQAUe_Yvt8y-Mbj9X93xbmDDgBnc7ud24bG_Ey_mX4; __cf_bm=whWq2Zl74tMFaLyz.OFMGeA5KliPVoEs5oHLU8_CEYw-1660011697-0-AZmxM+FELE1XkqJdHk/BQWlfJzM5K/eAtPW6WMFP8BBnIv4UWM3CR/Xg+bWsz5o8wQQ4bLIdeORzxnc/1ClLyek=; ajs_anonymous_id=8f7f44d9-321b-4b7a-800c-1c7dcb48fd74; _gid=GA1.2.421289818.1660011700; csrftoken=SnxDTzc8wX1AzpS28wzyfddo41AMeqd8XF3ZHAY33jBI4hjdMUs3mMSJVHqQd8Ch; _ga=GA1.1.58126105.1660011700; sessionid=eyJzZXNzaW9uSWQiOiI1MmUwYjQ3NC1iYjk5LTRhMjItOTIxZC0xYjljMjcwZWM0NzkifQ:1oLEsr:loyEJnwYw_-eOIzPAVMOsYn5HdSoPbnvs1Vf2iDX3Sk; amp_ddd6ec=UB-BUx5hMsMuCopeci0d56...1ga06gntu.1ga06htlu.9.a.j; assets_card_variant="compact"; _dd_s=rum=0&expire=1660013143591; _ga_9VSBF2K4BX=GS1.1.1660011700.1.1.1660012252.0',
# "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
# "referer":"https://opensea.io/",
# 'sec-fetch-mode': 'cors',
# "sec-fetch-site": 'same-origin',
# "x-api-key":"2f6f419a083c46de9d83ce3dbe7db601",
# "x-build-id":"071758781c4b8278b9a69f489929939a83eb65d9"
# }

start_time = time.time()
chrome_driver = "C:\Python\install doc\Scripts\chromedriver.exe"
# driver = webdriver.Chrome(executable_path=chrome_driver)     # executable_path=chrome_driver
wd = webdriver.Chrome()
url = "https://opensea.io/collection/perdidos-no-tempo"
wd.get(url)    # 打开首页

wd.implicitly_wait(5)  #默认等待
wd.maximize_window()
wd.find_element(by=By.XPATH,value="//main[@id='main']/div/div/div[5]/div/div[3]/div/div/div/div/div/div[4]/div/div/button[2]").click()  # 点击布局,用来最大量获取url <xpath不能用“//”跳写>

urll = []
# link=wd.find_element(by=By.XPATH,value="//*[@href]")   # //*[@id='main']//article/a
# hitid = link.get_attribute("href")
# print(hitid)

i = 0
while int(i) <= 2000:    # 目前暂对这两轮数据做处理
    print("*************")
    i = int(i) + 2000    # 滚动两次，分别挪动滚动js：0,2000,4000

    for link in wd.find_elements(by=By.XPATH,value="//*[@id='main']//article/a"):
        hitid = link.get_attribute("href")
        print(hitid)
        if hitid not in urll and hitid:
            urll.append(hitid)
    js = "var q=document.documentElement.scrollTop=" + str(i)
    wd.execute_script(js)  # 每次滚动一点
    time.sleep(3)

getItem = len(urll)
print("当前获取的Item数量为：",getItem,"\n",urll)

# test0 = "https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/7061"
# wd.get(test0)
statusl = []
for i in range(getItem):
    testURL = urll[i]
    wd.get(testURL)
    # 一直等待某元素可见，默认超时10秒
    def is_visible(locator, timeout=5):
        try:
            ui.WebDriverWait(wd,timeout).until(lambda x:x.find_element(By.XPATH,locator))
            return True
        except TimeoutException:
            return False
    # if ui.WebDriverWait(wd,timeout).until(lambda x:x.find_element(By.XPATH,locator)):
    #     print("看见刷新按钮。")
    #     return True
    # else:
    #     return False
    putele = "//*[@id='main']/div/div/div/div[1]/div/div[1]/div[2]/section[1]/div/div[2]/div/button[1]"  # 元素的刷新按钮
    # putele = "//*[@id='main']/div/div/div/div[1]/div/div[1]/div[2]/section[1]/div/div[2]/div/button[last()-2]"
    a = is_visible(putele)  # 元素的刷新按钮是否可见

    # 浮层处理
    def readyToTips(ele_floating,timeout=1):    # 设置浮层校验最大时长
        try:
            ui.WebDriverWait(wd,timeout).until(EC.visibility_of_element_located((By.XPATH,ele_floating)))
            msg = wd.find_element(By.XPATH,ele_floating)
            return msg
        except TimeoutException:
            return False
    ele_floating = "//*[@id='__next']/div[2]/div/div[last()-1]"
    msg = readyToTips(ele_floating) # 判断True or False

    if a == True:

        if msg:
            statusl.append("Queued.")   # 已确认，
        else:
            statusl.append("Clicked.")     # 已点击
            wd.find_element(By.XPATH,putele).click()
    else:
        statusl.append("Error.")    # 错误
    # print(statusl)
newl = [[m,n] for m in urll for n in statusl]
print(newl)

# if len(newl) == getItem:
dic = {str(v+1):newl[v] for v in range(getItem)}
print("table已整理，可输出为Excel或者以字典方式打印！")
print(dic)

time.sleep(2)   # 等待2秒
end_time = time.time()
print("总共耗时：%.2fS"%(end_time - start_time))  # 查看全套耗时
wd.quit()


