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
data: 表单{
	username: 用户名
	password: 密码
	email: 邮箱
}

return: json{
	status: bool 是否成功
	info: 描述
}
```

## 用户登录

```
url: localhost:5000/login/
method: post
data: 表单{
	username: 用户名
	password: 密码
}

return: json{
	status: bool 是否成功
	info: str 描述
	cookie: json 用户信息
}
```

