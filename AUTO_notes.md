## 解决思路：

```English
第一，先拿到全部的2.1K商品数据；第二，为这些数据建个列表；第三，依次点击访问列表，查看商品的状态；第四，获取到商品状态，并生成一个等长的列表，两个等长的列表组成一个新列表；第五，这些列表和序号打包起来，就是一个字典，可以导出该新“Table”了.
```

## 操作：
第一个接口：（直接提取）需要token。

https://opensea.io/__api/tokens/?limit=100

第二个：下拉刷新后新数据接口，请求拉取，需要提供请求串。

https://opensea.io/__api/graphql/

以上两个接口的访问和连接出了问题，只能页面自动提取连接了



要求：
| 访问站点：https://opensea.io/collection/perdidos-no-tempo    |                                                              |      |                                |
| ------------------------------------------------------------ | :----------------------------------------------------------- | ---- | ------------------------------ |
| 每个收藏品中都有很多物品。在本例中，集合中有2.1k项(NFTs)。   |                                                              |      |                                |
| 请使用自动化web框架如selenium或robot框架等编写一个自动化web流程，以执行以下功能 |                                                              |      |                                |
| 1)为所有唯一的2.1k项创建一个表。用蓝色值填结果               |                                                              |      |                                |
| No.                                                          | URL                                                          |      | Status                         |
| 1                                                            | https://opensea.io/assets/matic/Oxecc82095b2e23605cd95552d90216faa87606C40/3305 |      | **Clicked \| Queued \| Error** |
|                                                              |                                                              |      |                                |
| 2)查看收藏品中的每一件物品                                   |                                                              |      |                                |
| 3)点击右上角按钮(红色)刷新按钮(示例)                         |                                                              |      |                                |
| 4)验证“我们刷新并重新排序后的数据”                           |                                                              |      |                                |
| 5)用值填充状态                                               |                                                              |      |                                |
| a)Clicked=您的程序已单击元数据                               |                                                              |      |                                |
| b) Queued =你的程序检测到文本“We've Queued…”                 |                                                              |      |                                |
| c)Error=您的程序检测到一些错误                               |                                                              |      |                                |

![[img](https://img-blog.csdnimg.cn/4a2ca06c8e534a7ba40630e4eb658d7c.png)](https://img-blog.csdnimg.cn/4a2ca06c8e534a7ba40630e4eb658d7c.png)

示例如下![[img](https://img-blog.csdnimg.cn/b4e28a2342aa46b885d99cf29150f65d.png)](https://img-blog.csdnimg.cn/b4e28a2342aa46b885d99cf29150f65d.png)





### **那么说一下整体思路，**

**第一，**先拿到全部的2.1K商品数据；**第二，**为这些数据建个列表；**第三，**依次点击访问列表，查看商品的状态；**第四，**获取到商品状态，并生成一个等长的列表，两个等长的列表组成一个新列表；**第五，**这些列表和序号打包起来，就是一个字典，可以导出该新“Table”了.

### **环境准备：**

更新pip工具，下载selenium库，如果使用beautifulsoup就要下载bs库和lxml解析器。

自动化的基础：chromedriver.exe（驱动，在[这里下载](http://chromedriver.storage.googleapis.com/index.html)）

-- 下载驱动前，确认chome浏览器的版本，在上面地址查看notes，大版本是否对应，windows只能下载32位驱动，但是够用了。

### **实际操作：**

万事开头难，第一步怎么那到这2.1K的商品数据，

当时定位到了该海外网站的两个接口：

```
https://opensea.io/__api/tokens/?limit=100
```

与https://opensea.io/__api/graphql/



该接口地址不知道因为什么原因无法正常连接，只能才用计划B了。

![[img](https://img-blog.csdnimg.cn/4a2ca06c8e534a7ba40630e4eb658d7c.png)](https://img-blog.csdnimg.cn/578a34c5acba47a9b29a83175a8c7b06.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑

 *进入首页，动态滚动页面，动态捕获页面商品信息，生成列表  -- 计划B 采纳！*



于是：

```
wd = webdriver.Chrome()
url = "https://opensea.io/collection/perdidos-no-tempo"     # 需要搭梯子才能访问
wd.get(url)    # 打开首页

wd.implicitly_wait(5)  #默认等待
wd.maximize_window()
wd.find_element(by=By.XPATH,value="//main[@id='main']/div/div/div[5]/div/div[3]/div/div/div/div/div/div[4]/div/div/button[2]").click()  # 点击布局,用来最大量获取url <xpath不能用“//”跳写>

urll = []
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
```

![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)

打印出来的效果为：当前页面每轮展示15条数据，全部被捕获到！
![[img](https://img-blog.csdnimg.cn/4a2ca06c8e534a7ba40630e4eb658d7c.png)](https://img-blog.csdnimg.cn/0e414525584c4957b2798409a145f627.png)

很好，第一步解决了，后续的每个链接的访问和处理就有着落了。

再次创建状态列表，

```python
statusl = []
```

![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)

根据之前的链接列表，建立循环，在循环内，遍历每个商品的详情页，以获取状态效果，

主要关注一个刷新按钮，一个非固定浮层：

刷新按钮的处理：

```python
def is_visible(locator, timeout=5):
    try:
        ui.WebDriverWait(wd,timeout).until(lambda x:x.find_element(By.XPATH,locator))
        return True
    except TimeoutException:
        return False
putele = "//[@id='main']/div/div/div/div[1]/div/div[1]/div[2]/section[1]/div/div[2]/div/button[1]"  # 元素的刷新按钮
a = is_visible(putele)  # 元素的刷新按钮是否可见
```

![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)

非固定浮层的处理方法：等待出现

```python
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
```

![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)

然后输出状态，列表是对应的：

```python
if a == True:

    if msg:
        statusl.append("Queued.")   # 已确认，
    else:
        statusl.append("Clicked.")     # 已点击
        wd.find_element(By.XPATH,putele).click()
else:
     statusl.append("Error.")    # 错误
```

![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)

打印下商品链接和状态合并的结果：

```
newl = [[m,n] for m in urll for n in statusl]
print(newl)

#效果如下：
[['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/132', 'Clicked.'], ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/4111', 'Clicked.']]
```

![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)

再建立个字典生成式，就有了。

```
dic = {str(v+1):newl[v] for v in range(getItem)}
print("table已整理，可输出为Excel或者以字典方式打印！")
print(dic)

# 效果如下：
table已整理，可输出为Excel或者以字典方式打印！
{'1': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '2': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '3': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '4': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '5': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '6': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '7': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '8': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '9': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '10': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '11': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '12': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '13': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '14': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '15': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '16': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '17': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '18': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '19': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '20': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '21': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '22': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '23': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '24': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '25': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '26': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '27': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '28': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '29': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.'], '30': ['https://opensea.io/assets/matic/0xecc82095b2e23605cd95552d90216faa87606c40/5549', 'Clicked.']}
```

![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)
顺利完成！！success！
![img](https://img-blog.csdnimg.cn/c3b6fc820ebe43f28a3c1fed0ada8ea4.png)

## 遇到问题：

### 过程中遇到的问题与解决办法：

*1、VPN问题*

找了不少朋友，还有人不知道什么是VPN，最后通过蓝灯VPN过了这关。

*2、python3的urllib3与驱动不兼容问题*

报错是：RequestsDependencyWarning: urllib3 (1.26.11) or chardet (3.0.4) doesn't match a supported version!![[img](https://img-blog.csdnimg.cn/0e414525584c4957b2798409a145f627.png)](https://img-blog.csdnimg.cn/0f538bac049f4a8293776e747c41e739.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑

 



检验原码要求：![img](https://img-blog.csdnimg.cn/0a42d0b753c14d99a863aa329ef842c5.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑

 **看来是urllib3库过高，降到源码要求的版本即可。**



降级urllib3库后，仍然有报错，但是py库能正常运行。主要为了解决题目的方案尽快出来，暂搁置selenium库过高的问题

![img](https://img-blog.csdnimg.cn/6a532d0388be43d5a662383459c88c38.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑

 



解决后无报错。



![img](https://img-blog.csdnimg.cn/5b1decd6d3e5472ea6c6f23de9114ffb.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑

*3、*http连接太多，报错

![img](https://img-blog.csdnimg.cn/d9dca907f29a4c478a5827460684c039.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑

 有些博主说把keep_alive=False改成False就好。

webdriver.Chrome(executable_path=“chromedriver”, port=0, options=None,keep_alive=True)
 但是这里没效果

4、一次无法拉取全部商品信息，

动态获取页面的元素链接

使用execute_script(js)和get_attribute，get后的效果： 

![[img](https://img-blog.csdnimg.cn/5b1decd6d3e5472ea6c6f23de9114ffb.png)](https://img-blog.csdnimg.cn/7407d33c56264613b8340c6ecf2cdb32.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑

5、运行三遍后，突然报错，提示executable_path被弃用。

![[img](https://img-blog.csdnimg.cn/5b1decd6d3e5472ea6c6f23de9114ffb.png)](https://img-blog.csdnimg.cn/4684e7d52f0b44b0af533e2dda61247d.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑

 

那就干掉

```
webdriver.Chrome()
```

括号里的调用

6、浏览器自动升级，导致驱动不兼容

![[img](https://img-blog.csdnimg.cn/5b1decd6d3e5472ea6c6f23de9114ffb.png)](https://img-blog.csdnimg.cn/610eeddfcca3433dab84c868873e0daf.png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)编辑

 This version of ChromeDriver only supports Chrome version 92 Current browser version is 104.0.5112.81 with binary path C:(Program Files (x86)\Google)Chrome ) Application)chrome.exe

重新下载驱动并在Python的Scripts目录替换掉，解决了浏览器自动升级导致的驱动失效。

所以自动化的执行机里一般对环境要求严格，输入法统一，界面分辨率统一，浏览器要弹框确认，更要禁用升级。

