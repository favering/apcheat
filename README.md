
apcheat, 做钓鱼WIFI的一系列脚本。（尚需优化和功能增强）

# aphost.py
创建AP。可以创建一个单纯的AP，也可创建一个热点（共享网络连接）。

输入aphost.py -h 查看使用方法。

# cheat.py
通过上述创建的AP进行页面欺诈。

输入aphost.py -h 查看使用方法。

实现原理：
* DNS欺骗，将所有的域名请求都重定向到本地IP
* iptables NAT透明代理，将所有TCP连接的目的IP都重定向到本地IP（针对不通过DNS请求的对外连接）
* 通过以上两步，所有对外连接都经过本地（扮演代理或中间人角色），但因这里只进行web欺诈，所以仅在本地的80、443、8080端口建立web服务。
  其中443、8080的web服务将所有请求都301重定向到80端口web。
  80端口web服务总是返回一个钓鱼页面。目前该页面仅仅只是一个钓WIFI密码的简单页面。
  
该钓鱼WIFI主要针对手机。手机连接上该钓鱼WIFI后，有些APP会探测到地址跳转，误以为是需要认证的WIFI，于是引导用户或主动转到钓鱼页面。（如360手机卫士、QQ）。
有些手机APP内置嵌入了浏览器，所以也可能呈现钓鱼页面。因443端口的https服务使用的是虚假证书，所以有些浏览器或APP打开钓鱼页面会不成功。测试过一些APP，在以下APP出现或被嵌入过钓鱼页面（不保证总是能）:

各种浏览器、新浪微博、支付宝、QQ、链家、58同城、安居客

微信始终不能被嵌入钓鱼页面，看来微信的安全性还是可以的。

# server目录
建立web服务的相关脚本或文件。

serve_http.py 		建立80端口web服务

serve_http_alt.py 	建立8080端口web服务

serve_https.py 		建立443端口web服务

bottle.py	 微web服务框架

htts_server.pem https服务端证书

helpinfo.html	 静态钓鱼页面


# jammer.py
干扰正常AP和客户端连接的脚本。（功能还未实现）

断开客户端和正常AP的连接，诱使客户端连接到上述建立的钓鱼AP。

# 存在的主要问题
* cheat.py运行不是很稳定，运行久了可能失效，需重新运行。
* https欺诈不太稳定（不知是不是跟虚假证书有关）。特别是360浏览器，似乎对抗欺诈的能力比一般浏览器更强一些。



