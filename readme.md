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

## User

```
user: json{		用户信息
	id: int				用户id
    username: str		用户名
    password: str		密码
    email: str			邮箱
    cookie: dict		用户凭证
    promotion_link: str	推广链接
    nick: str			昵称
    gender_type: list['保密', '男', '女']	固定的
    gender_id: int		通过 gender_id 选择 gender_type
}
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
	user: json 用户信息
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

## 小说列表

### 获取书籍列表类型

```
url: localhost:5000/toplist/type/
method: get

return: {
    "info": "获取成功",
    "list_type": [
        "总排行榜",
        "总推荐榜",
        "月排行榜",
        "月推荐榜",
        "周排行榜",
        "周推荐榜",
        "日排行榜",
        "日推荐榜",
        "最新入库",
        "最近更新",
        "总收藏榜",
        "字数排行"
    ],
    "status": true
}
```

### 获取书籍列表

```
url: localhost:5000/book/toplist/
method: post
data: json{
	cookie: json 		来自user.cookie
	type_id: int 		获取书籍列表类型返回的list_type里的类型的下标
	request_page: int	请求的书籍列表是第几页
}

return: json{
	{
    "info": "获取小说列表成功",		请求信息
    "status": true,				 请求状态
    "toplist": json{				小说列表（json）
        "novel_list": list[			list 里面包含novel_id(int)
            2966,
            3589,
        ],
        "request_page": 2,			请求的是第几页
        "total_page": "38",			请求的列表的总页数
        "type_id": 3,				请求的列表的类型
        "type_name": "月推荐榜"		类型的名字
    }
}
}
```

