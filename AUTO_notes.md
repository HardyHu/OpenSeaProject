## 解决思路：

```English
先获取页面商品的接口，爬取关键信息，组建成字典
去重后，根据字典顺序，点击每个商品，获取点击效果
将点击效果反馈到列表里
合并字典和列表，组成最终table
导出为excel或者直接打印
```

## 操作：

第一个接口：（直接提取）需要token。

https://opensea.io/__api/tokens/?limit=100

第二个：下拉刷新后新数据接口，请求拉取，需要提供请求串。

https://opensea.io/__api/graphql/

以上两个接口的访问和连接出了问题，只能页面自动提取连接了





顺利完成：

![image-20220810152841776](C:\Users\KaiHe\AppData\Roaming\Typora\typora-user-images\image-20220810152841776.png)
[AUTO_notes.md](https://github.com/HardyHu/OpenSeaProject/files/9300563/AUTO_notes.md)

## 遇到问题：

*1、VPN问题*

找了不少朋友，还有人不知道什么是VPN，最后通过蓝灯VPN过了这关。

*2、python3的urllib与驱动不兼容问题*

报错是：

![image-20220809104559369](C:\Users\KaiHe\AppData\Roaming\Typora\typora-user-images\image-20220809104559369.png)

检验原码要求：

<img src="C:\Users\KaiHe\AppData\Roaming\Typora\typora-user-images\image-20220809104519111.png" alt="image-20220809104519111" style="zoom:67%;" />

降级urllib3库后，仍然有报错，但是py库能正常运行。主要为了解决题目的方案尽快出来，暂搁置selenium库过高的问题

![image-20220809104946565](C:\Users\KaiHe\AppData\Roaming\Typora\typora-user-images\image-20220809104946565.png)

解决后无报错。

![image-20220809105016832](C:\Users\KaiHe\AppData\Roaming\Typora\typora-user-images\image-20220809105016832.png)

*3、*http连接太多，报错

![image-20220809114307205](C:\Users\KaiHe\AppData\Roaming\Typora\typora-user-images\image-20220809114307205.png)

4、动态获取页面的元素链接

​	使用execute_script(js)和get_attribute

5、运行三遍后，突然报错，提示executable_path被弃用。

![image-20220809202353915](C:\Users\KaiHe\AppData\Roaming\Typora\typora-user-images\image-20220809202353915.png)

6、浏览器自动升级，导致驱动不兼容

![image-20220810112910075](C:\Users\KaiHe\AppData\Roaming\Typora\typora-user-images\image-20220810112910075.png)

​	重新下载驱动试试，解决了浏览器自动升级导致的驱动失效



