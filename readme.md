# 简介

通过爬虫对wenku8网站的请求封装成api，由flask提供支持

# 已实现接口

- [x] 用户注册
- [x] 用户登录
- [x] 获取小说信息
- [ ] 。。。

# 运行

python库

```
requests
bs4
flask
```

运行main.py

# 实体

## novel

```
novel: json{	小说信息
		author: str			作者
		catalog: list,		目录
		description: str,	小说简介
		id: int,			小说id
		name: str,			小说名
		pic_url: str		小说封面
}

catalog: list[	目录列表
	json{
		volume: str		卷名
		chapter: list	章节名
	}
]

chapter: list[	章节列表
	json{
		name: str		章节名
		novel_id: int	小说id
		chapter_id: int	章节id
	}
]
```

# 接口请求

## 用户注册

```
url: localhost:5000/register/
method: post
data: 表单{
	username: str 用户名
	password: str 密码
	email: str 邮箱
}

return: json{
	status: bool 是否成功
	info: str 描述
}
```

## 用户登录

```
url: localhost:5000/login/
method: post
data: 表单{
	username: str 用户名
	password: str 密码
}

return: json{
	status: bool 是否成功
	info: str 描述
	cookie: json 用户信息
}
```

# 获取小说信息

### 不含目录

```
url: localhost:5000/book/小说id/
method: get

return: json{
	status: bool	是否成功
	info: str		描述
	novel: json		小说实体
}
```

### 含目录

```
url: localhost:5000/book/catalog/小说id/
method: get

return: json{
	status: bool	是否成功
	info: str		描述
	novel: json		小说实体
}
```

