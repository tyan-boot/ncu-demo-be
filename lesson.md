# 前端与后端

## 传统Web开发
在传统Web开发当中, 通常是前端开发人员写好html, css以及js, 再将这些文件交给后端, 后端将这些文件切成模板, 利用模板渲染引擎, 插入需要的数据, 最后拼接成完整的网页内容, 输出给浏览器

例如 `flask` 当中的 `jinja2` 就是这样的模板引擎.

但是使用模板引擎会有很多的问题, 例如

- 后端开发人员往往不熟悉html等, 在转换成模板的时候很容易出错, 最后又需要前端来协助, 然而前端同样也不熟悉后端模板
- 前端引用的静态资源如果使用相对路径等, 当后端模板需要配置的时候, 需要修改大量的link, src等, 麻烦且容易出错
- 服务器因为要渲染大量的html, 负载会比较大

这些只是众多问题中的一部分

为了解决这些问题, 进来年开始前后端分离, SPA(单页应用)变得流行起来.

## 前端
在前后端分离架构中, 前端注重与页面以及交互逻辑, 数据全部用Ajax向后端获取, 再将获取到的数据与组件什么的渲染(呈现)出来.

前端不再需要将页面交给后端来渲染, 组件的渲染转交给浏览器来实现.

同时前端出现了众多的框架, 比如`Vue`, `AngularJS`, `React`

### Ajax
Ajax全称是`Asynchronous Javascript And XML`（异步JavaScript和XML）

通过在后台与服务器进行少量数据交换，AJAX 可以使网页实现异步更新。这意味着可以在不重新加载整个网页的情况下，对网页的某部分进行更新。


## 后端
后端不再处理模板, 只负责业务处理和数据等, 接受前端的Ajax请求, 处理好之后返回给前端需要的数据.

`flask` 就是后端的一个框架, 除此以外还有`django`等.

Java 常见的框架则比如`Spring`, `Struts2`之类的.


# RESTful API
什么是`API`, `API` 是 __应用程序编程接口__ , 一般简称 __接口__ .

是一组预定义好的函数, 提供应用程序与开发人员访问一些服务/数据的能力.

反映到Web开发当中, API通常就是一些`HTTP URL`, 通过`GET`, `POST` 等方法向这些接口发出请求. 并返回数据.

比如云家园登陆接口为`https://www.ncuos.com/api/user/token`, 向此地址发送合法的数据, 即可登陆(返回token)

而`RESTful API`则是目前比较成熟的API设计理论, 方便规范化接口, 使得不同的前端设备能方便的与后端进行通信.

## 路径
路径表示的是一个API的具体网址(URI), 每一个网址代表一个资源

比如做一个留言板的应用, 一个API提供留言信息, 那么他的路径类似于:

- https://api.example.com/api/comments
- https://api.example.com/api/comments/2

## HTTP动词
HTTP动词也即HTTP方法, 例如`GET`, `POST`.

|动词|操作|说明|
|---|---|---|
|`GET`|`SELECT`|获取资源|
|`POST`|`CREATE`|新建资源|
|`PUT`|`UPDATE`|更新资源(提供完整资源)|
|`PATCH`|`UPDATE`|更新资源(提供改变的属性)|
|`DELETE`|`DELETE`|删除资源|

具体到之前提到的留言板应用:

|操作|说明|
|---|---|
|`GET /api/comments`|获取全部留言|
|`POST /api/comments`|新建一个留言|
|`PUT /api/comments/2`|修改一个留言|
|`DELETE /api/comments/2`|删除一个留言|


## HTTP状态码
状态码是服务器向用户返回的状态码, 常见的状态码有

|状态码|信息|说明|
|---|---|---|
|200|OK|成功返回请求的数据|
|201|CREATED|新建或修改数据成功|
|202|Accepted|请求已进入后排排队|
|400|invalid request|请求有错误, 服务器没有执行|
|401|unauthorized|没有权限, 一般是未登录|
|403|forbidden|通常是已登陆, 但是没有权限操作|
|404|not found|找不到对应的记录|
|500|internal server error|服务器错误, 无法知道请求是否成功|

# JSON
JSON全称是`JavaScript Object Notation`, 是一种轻量级的数据交换格式, 不仅用在JS中, 在其他语言以及数据传输当中都可以使用`JSON`格式.

需要注意的是, __JSON是字符串__.

例如
```json
{
    "name": "John",
    "age": 19,
    "family": [
        {
            "name": "Tom",
            "age": 20
        },
        {
            "name": "Hunter",
            "age": 50
        }
    ],
    "job": {
        "name": "ncuhome",
        "department": "backend"
    }
}
```

在RESTful API中, 数据交换统一使用`JSON`, 前端发送给后端使用`JSON`, 后端返回的数据也用`JSON`, 同时设置HTTP头`Content-Type: application/json`
