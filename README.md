基于scrapy的校花网图片爬虫
### 需求
1. http://www.xiaohuar.com/hua/ 请求第一页，第一页每一个图集链接获取下来
2. 图集详情页，点击相册
3. 相册画廊页，相册下所有的图片按照图集名保存下来

### 开发步骤
1.scrapy startproject xiaohua_spider
2.scrapy genspider xiaohua xiaohua.com
3.开发
4.检查本地文件
