# 简介

通过爬虫对wenku8网站的请求封装成api，由flask提供支持

# 已实现接口

- [x] 用户注册
- [x] 用户登录
- [ ] 。。。

# 接口请求

## 用户注册

```
url: localhost:5000/register/
method: post
data: 通过表单形式提供

return: json{
	status: bool 是否成功
	info: 描述
}
```

## 用户登录

```
url: localhost:5000/login/
method: post
data: 通过表单形式提供

return: json{
	status: bool 是否成功
	info: str 描述
	cookie: json 用户信息
}
```

