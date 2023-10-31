"""
└── django // 根目录
    ├── apps
    ├── conf
    ├── contrib
    ├── core
    ├── db
    ├── dispatch
    ├── forms
    ├── http
    ├── middleware
    ├── template
    ├── templatetags
    ├── test
    ├── urls
    ├── utils
    └── views
apps：与 Django 中定义的 app 相关的逻辑，Django中app即是在settings文件中配置的 INSTALLED_APPS。
conf：公共配置信息相关的目录，存放一些模版文件与 settings默认配置。
contrib：是 Django 内置的强大的功能包，相当于 Django 中的各种子模块，里面有大量额外提供的、或者增加 Django 功能的库及函数，比如 contrib 目录下的 auth 模块提供了与Django的用户验证相关的框架，admin模块提供了与自动化站点管理相关的后台功能。
core：Django的核心功能目录，核心的功能都位于这个目录下， Django 下各种命令的使用如 django startproject && python manage.py xxx 等核心命令的使用都在此目录下。
db：数据库连接、模型Model定义以及 ORM 相关的逻辑。Django可以兼容很多数据库，包括MySQL、Oracle，PgSql等等，通过这个模块可以屏蔽不同数据库之间底层的差异，实现统一接口。
dispatch：处理信号相关的模块，在 Django 中很多地方都有用到信号，比如生成数据库迁移文件时。
forms：表单处理，主要用于与前端表单组件交互的封装。
http：Http请求和应答等与网络请求相关的模块。
middleware：内置的中间件模块，有很多方便可直接使用的中间件。
Template&&Templatetags：Django的模版引擎。
test：单元测试相关的模块。
urls：处理路由相关的模块。
utils：提供了很多使用的小工具类，比如懒加载类就在这个目录下。
views：视图处理的模块

"""