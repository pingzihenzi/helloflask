# HelloFlask

HelloFlask 的 Meta 仓库，包含 HelloFlask 相关文档和示例程序。


## Links

- 文档：<https://docs.helloflask.com>
- 主站：<https://helloflask.com>
- 论坛：<https://discuss.helloflask.com>


## Books

- Flask Web 开发实战：<https://helloflask.com/book/1>
- Python Web API 设计与开发：<https://helloflask.com/book/2>
- Flask 入门教程：<https://helloflask.com/book/3>
- Flask Web 开发实战（第 2 版）：<https://helloflask.com/book/4>


## Feedbacks

- 勘误和建议：创建 [issue](https://github.com/greyli/helloflask/issues) 或发送邮件到 withlihui@gmail.com
- 问题求助 & 讨论：在[论坛](https://discuss.helloflask.com)、[GitHub Discussion](https://github.com/greyli/helloflask/discussions) 或[群聊](https://helloflask.com#discuss)创建讨论


## Docs

一些快速链接：

- [《Flask Web 开发实战》示例程序索引](https://docs.helloflask.com/examples/)
- [《Flask Web 开发实战》勘误](https://docs.helloflask.com/book/1/errata/)
- [《Flask Web 开发实战（第 2 版）》代码片段](https://docs.helloflask.com/book/4/snippets/)

## 学习笔记

- 如果使用text/xml，xml内容中的version只能是1.0或1.1，因为1.1使用的不多，常用的version是1.0
- pipenv shell进入虚拟环境，flask run启动服务
- routes中带参数时，给出默认值使用defaults={"key":"value"}方式
- 开放重定向漏洞，校验url的netloc是否相同，协议是否相同
- jinja2的escape()方法可以将输入内容转义成文本，防止XSS注入攻击
- 局部模板通常以下划线开头
- 子模板的第一个标签必须是extends