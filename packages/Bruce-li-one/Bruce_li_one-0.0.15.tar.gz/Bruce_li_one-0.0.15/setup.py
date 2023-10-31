import setuptools


description="""
武器库
"""
requirements = [
    "python-snap7==1.3",
    "docker==6.0.1",
    "modbus_tk==1.1.2",
    "pyModbusTCP==0.2.0",
    "pyinstaller==5.7.0",   #将 Python 程序转换成独立的执行文件（跨平台）
    "sqlalchemy==2.0.4",    #python SQL 工具以及对象关系映射工具
    "pony==0.7.16",         #提供面向生成器的 SQL 接口的 ORM
    "gitpython==3.1.30",
    "requests==2.28.2",
    "pymysql==1.0.2",
    "redis==4.5.1",
    "pywin32==305",         # 针对 Windows 的Python 扩展
    "rpyc==5.3.1",           #RPC 服务器
    "paho-mqtt==1.6.1",      #MQTT协议通讯
    "websocket==0.2.1",         #websocket协议
    "websocket-client==1.6.4" #websocket协议
    # "ftplib",               #FTP协议
    # "pika==1.3.1",          #RabbitMQ
    # "alembic==1.9.4",        #数据迁移
    # "matplotlib==3.4.3"
    #xlwt / xlrd     读写 Excel 文件的数据和格式信息
    #BeautifulSoup   以 Python 风格的方式来对 HTML 或 XML 进行迭代，搜索和修改
    #envoy           比 Python subprocess 模块更人性化。
    #NumPy           进行科学计算的基础包
    #Pandas          提供高性能，易用的数据结构和数据分析工具
    #matplotlib      一个 Python 2D 绘图库
    #psutil          一个跨平台进程和系统工具模块
    #WinPython       Windows 7/8 系统下便携式开发环境
    #Six             Python 2 和 3 的兼容性工具
    #celery  一个异步任务队列/作业队列，基于分布式消息传递

]       # 自定义工具中需要的依赖包
 
setuptools.setup(
    name="Bruce_li_one",       # 自定义工具包的名字
    version="0.0.15",             # 版本号
    author="Bruce_li123",           # 作者名字
    author_email="lws__xinlang@sina.com",  # 作者邮箱
    description=description, # 自定义工具包的简介
    license='MIT-0',           # 许可协议
    url="",              # 项目开源地址
    packages=setuptools.find_packages(),  # 自动发现自定义工具包中的所有包和子包
    install_requires=requirements,  # 安装自定义工具包需要依赖的包
    python_requires='>=3.5',         # 自定义工具包对于python版本的要求
    # 项目相关额外连接，如代码仓库，文档地址等
    project_urls = {
       "Documentation": "https://bruce-li-one-docs.readthedocs.io/en/latest/Cpp/index.html",
    }
)