import base64
import datetime
import os
import threading
import requests
from selenium import webdriver
import time
import http.cookiejar
import urllib.parse
import re
from urllib.parse import urlparse
import getpass


def get_protocol_and_domain(url):
    parsed_url = urlparse(url)
    protocol = parsed_url.scheme
    domain = parsed_url.netloc
    protocol_and_domain = f"{protocol}://{domain}"
    return protocol_and_domain

def base64_decode(s):
    decoded_bytes = base64.b64decode(s)
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string

def base64url_encode(s):
    encoded_bytes = base64.urlsafe_b64encode(s.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string

def redirect(url):
    if re.search(r'redirectUrl=(\S*)', url):
        all_path = re.search(r'redirectUrl=(\S*)', url).group(1)
        third_path = ''
        if re.search(r'state=(\S*)', url):
            third_path = re.search(r'state=(\S*)', url).group(1)
        elif re.search(r'goto=(\S*)', url):
            third_path = re.search(r'goto=(\S*)', url).group(1)
        else:
            # 处理没有state或goto的情况
            pass
        if third_path:
            decode_third = urllib.parse.unquote(third_path)
            try:
                # 进行解密操作，防止重复加密
                decode_third = base64_decode(decode_third)
            except:
                # 解密失败，不处理
                pass
            # 加密third_path
            encode_third = base64url_encode(decode_third)
            all_path = all_path.replace(third_path, encode_third)
        # 加密redirectUrl
        next_jump = '/nextJump.html?nextJump=' + base64url_encode(all_path)
        return next_jump
    else:
        return '/nextJump.html?nextJump=/'

class SsoLoginUtil:
    def __init__(self,sso_url = None):
        self.browser_type_map = {
            "chrome": self.init_chrome,
            "edge": self.init_edge,
            "firefox": self.init_firefox,
            "safari": self.init_safari,
        }
        self.installed_browser = None
        self.work_folder = ".zpsso"
        # 读取环境变量 ZPSSO_FOLDER_NAME
        self.url =os.getenv("ZPSSO_URL",sso_url)
        self.session = requests.Session() 
        self.get_or_update_version()

    def clearCookie(self):
        self.session.cookies.clear()

    def get_cookie_path(self,type = None):
        cookie_dir = self.get_or_create_work_dir() + "/" +str(type)
        if not os.path.exists(cookie_dir):
            os.makedirs(cookie_dir)
        return cookie_dir + '/cookies.txt'
    
    # 获取pypi最新版本, 如果版本不一致,提示更新
    def get_or_update_version(self):
        version_path = os.path.abspath(self.get_or_create_work_dir() + "/update_failed.log")
        try:
            # 读取更新信息
            version = None
            if os.path.exists(version_path):
                with open(version_path, "r", encoding="utf-8") as fh:
                    version = fh.read()
                    print("package version is : " + version)
            if version is not None:
                # 说明尝试更新失败,不执行更新操作
                print("\033[31m auto update failed , please try update by : pip3 install -i https://pypi.org/simple --upgrade zpassistant")
                return
            import pkg_resources
            for i in range(3):
                version = pkg_resources.get_distribution("zpassistant").version
                # 读取远端版本
                url = "https://pypi.org/pypi/zpassistant/json"
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    latest_version = data["info"]["version"]
                    if latest_version != version:
                        # 使用红色字体打印
                        print("\033[31m latest version is : " + latest_version + ",will update your package: pip3 install -i https://pypi.org/simple --upgrade zpassistant")
                        # 执行安装指令
                        os.system("pip3 install -i https://pypi.org/simple --upgrade zpassistant")
                        # 绿色字体
                        print("\033[32m update success,please retry your cammond")
                    else:
                        break
        except Exception as e:
            print("get or update version failed , ignore")
            # 写入更新失败到文件中
            with open(version_path, "w", encoding="utf-8") as fh:
                fh.write(str(e))

    def base_cookie_check(self,url):
        browser = self.installed_browser
        # 创建LWPCookieJar对象
        base_cookie_jar = http.cookiejar.LWPCookieJar(filename=self.get_cookie_path("base"))
        # 校验是否超时
        if base_cookie_jar.filename is not None and os.path.exists(base_cookie_jar.filename):
            base_cookie_jar.load()
            if not self.check_cookie_jar_expire(base_cookie_jar):
                self.session.cookies = base_cookie_jar
                response = self.session.get(self.url,allow_redirects= True)
                if response.status_code != 200:
                    print("cookie 过期,重新登录")
                    base_cookie_jar.clear()
                else:
                    print("部分cookie过期,重新获取")
                    if browser is None:
                        browser = self.get_installed_browser(True)
                    browser.get(f"{self.url}?service={url}")
                    for cookie in self.session.cookies:
                        browser.add_cookie({
                            "name": cookie.name,
                            "value": cookie.value,
                            "domain": cookie.domain,
                            "path": cookie.path,
                            "expires": cookie.expires,
                        })
            else:
                print("cookie 过期,重新登录")
                base_cookie_jar.clear()
        return (base_cookie_jar,browser)
    
    def session_cookie_expired_check(self,type = None):
        # 创廳new_cookie_jar对象
        session_cookie_jar = http.cookiejar.LWPCookieJar(filename=self.get_cookie_path(type))
        # 校顶是否超时
        if session_cookie_jar.filename is not None and os.path.exists(session_cookie_jar.filename):
            session_cookie_jar.load(ignore_expires=True)
            all_cookies = session_cookie_jar._cookies
            # 遍历 cookie 对象的列表
            for domain in all_cookies:
                for path in all_cookies[domain]:
                    for name in all_cookies[domain][path]:
                        cookie = all_cookies[domain][path][name]
                        # 检查 cookie 是否已过期
                        if cookie.is_expired():
                            return (session_cookie_jar,True)
            return  (session_cookie_jar,False)
        return (session_cookie_jar,True)


    def ssologinByBrowser(self,url, checkFunction,checkCookieFunc = None,type = None):
        # 获取 session cookie
        session_cookie_jar, expire = self.session_cookie_expired_check(type)
        if not expire:
            self.session.cookies = session_cookie_jar
            return self.session

        # 获取基础cookie
        base_cookie_jar, browser = self.base_cookie_check(url)
        auto_login = True
        # 创建一个浏览器实例，这里使用Chrome浏览器作为示例
        if not browser:
            print("正在打开浏览器,请进行单点登录操作,请耐心等待...")
            browser = self.get_installed_browser()
            auto_login = False
        # 打开一个网页
        browser.get(f"{self.url}?service={url}")
        # 等待用户进行操作，例如登录或浏览网页
        count = 0;
        while count <10 or not auto_login:
            time.sleep(1)
            print("等待用户登录...")
            count += 1
            if checkFunction is None :
                for cookie in browser.get_cookies():
                    if cookie.get('name') == "INNER_AUTHENTICATION":
                        break 
            elif checkFunction(browser):
                break
        if count == 10 and auto_login:
            browser.close()
            print("登录超时,请手动登录,正在打开浏览器")
            self.installed_browser =None
            browser = self.get_installed_browser()
            browser.get(f"{self.url}?service={url}")
            while True:
                time.sleep(1)
                print("等待用户登录...")
                count += 1
                if checkFunction(browser):
                    break

        # 获取浏览器中的cookie
        browser_cookies = browser.get_cookies()
        # 将浏览器中的cookie添加到cookie_jar中
        expiration_time = datetime.datetime.now() + datetime.timedelta(days=20)
        session_cookie_jar =  http.cookiejar.LWPCookieJar(filename=self.get_cookie_path(type))
        for cookie in browser_cookies:
            cookie_dict = {
                "version": 0,
                "name": cookie['name'],
                "value": cookie['value'],
                "port": None,
                "port_specified": False,
                "domain": cookie['domain'],
                "domain_specified": True,
                "domain_initial_dot": False,
                "path": cookie['path'],
                "path_specified": True,
                "secure": False,
                "expires":  cookie.get('expiry',expiration_time.timestamp()),
                "discard": False,
                "comment": None,
                "comment_url": None,
                "rfc2109": False,
                "rest": {'HttpOnly': None}
            }
            if cookie["name"] in ["INNER_AUTHENTICATION"]:
                base_cookie_jar.set_cookie(http.cookiejar.Cookie(**cookie_dict))
            if cookie["name"] in ["INNER_AUTH_PATH"]:
                continue
            session_cookie_jar.set_cookie(http.cookiejar.Cookie(**cookie_dict))
        
        # 保存cookie_jar到指定文件
        base_cookie_jar.save()
        session_cookie_jar.save()

        # 关闭浏览器
        browser.quit()
        self.session.cookies = session_cookie_jar
        return self.session

    def get_or_create_work_dir(self):
        user_home = os.path.expanduser("~")
        folder_name = self.work_folder
        config_path = os.path.join(user_home, folder_name)
        if not os.path.exists(config_path):
            os.makedirs(config_path)
            print(f"文件夹 '{folder_name}' 已创建在用户主目录下。")
        return os.path.abspath(config_path)


    def check_cookie_jar_expire(self,cookie_jar,checkCookieFunc = None):
        if checkCookieFunc is not None:
            return checkCookieFunc(cookie_jar)
        for cookie in cookie_jar:
            if cookie.name == "INNER_AUTHENTICATION":
                return False
        return True

    def login(self,url,checkFunction = None, userName = None, password=None,type = None,checkCookieFunc = None):
        # 获取 session cookie
        session_cookie_jar, expire = self.session_cookie_expired_check(type)
        if not expire:
            self.session.cookies = session_cookie_jar
            return self.session
        if userName is not None and password is not None:
            return self.ssoLoginByUserNamePassword(url=url,userName=userName,password=password,type=type)
        else:
            if self.is_chrome_installed():
                return self.ssologinByBrowser(url,checkFunction=checkFunction,checkCookieFunc=checkCookieFunc,type=type)
            else:
                self.ssoLoginByUserNamePassword(url=url,userName=userName,password=password,type=type)

    def ssoLoginByUserNamePassword(self,url, userName = None, password=None,type = None):
        if userName is None:
            userName = input("请输入ERP用户名: ")
        if password is None:
            password = getpass.getpass("请输入ERP密码：")
        # 密码去除前后空格,base64加密
        password = password.strip()
        password = base64.b64encode(str(password).encode("utf-8")).decode()
        portal_address = urllib.parse.quote(url)
        headers = {
            'Referer': self.url,
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "content-type": "application/x-www-form-urlencoded",
        }
        session = requests.Session()
        session.cookies = http.cookiejar.LWPCookieJar(filename=self.get_cookie_path(type=type))
        data = f"path={portal_address}&username={userName}&password={password}&hideDing=true&loginthrid=&ct="
        response = session.post(self.url, data=data, headers=headers, allow_redirects=True)
        if response.status_code == 200:
            headers = {
                'Referer': response.url,
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            }
            response = session.get(get_protocol_and_domain(response.url) +  redirect(response.url), allow_redirects=True,headers= headers)
            if response.status_code == 200:
                session.cookies.save()
                return session
        raise Exception("登录失败" + response.text)

    def is_chrome_installed(self):
        try:
            # 读取浏览器类型
            type = None
            typePath = os.path.abspath(self.get_or_create_work_dir() + "/browser")
            if os.path.exists(typePath):
                with open(typePath, 'r', encoding="utf-8") as f:
                    type = f.read().strip()
            if type:
                if type not in self.browser_type_map:
                    return False
                else:
                    return True
            if self.get_installed_browser() is not None:
                return True
            return False
        except :
            return False

    def init_chrome(self,option = None):
        # 尝试检测Chrome浏览器
        try:
            if option is not None:
                from selenium.webdriver.chrome.options import Options
                option = Options()
                option.add_argument("--headless")
                option.add_argument("--log-level=4")
            browser =  webdriver.Chrome(options = option)
            self.installed_browser = browser
        except Exception as e:
            print("try open chrome failed:" ,e)
            pass


    def init_edge(self,option = None):
        # 尝试检测Edge浏览器
        try:
            if option is not None:
                from selenium.webdriver.edge.options import Options
                option = Options()
                option.add_argument("--headless")
                option.add_argument("--log-level=WARNING")
            browser =  webdriver.Edge( options= option)
            self.installed_browser = browser
        except Exception as e:
            print("try open edge failed:" ,e)
            pass


    def init_firefox(self,option = None):
        # 尝试检测Firefox浏览器
        try:
            if option is not None:
                from selenium.webdriver.firefox.options import Options
                option = Options()
                option.add_argument("--headless")
                option.add_argument("--log-level=4")
            browser =  webdriver.Firefox( options= option)
            self.installed_browser = browser
        except Exception as e:
            print("try open firefox failed:" ,e)
            pass


    def init_safari(self,option = None):
        # 尝试检测Safari浏览器 (需要Safari驱动程序)
        try:
            from selenium.webdriver.safari.service import Service as SafariService
            if option is not None:
                from selenium.webdriver.safari.options import Options
                option = Options()
                option.add_argument("--headless")
                option.add_argument("--log-level=4")
            browser =  webdriver.Safari( options= option)
            self.installed_browser = browser
        except Exception as e:
            print("try open safari failed:" ,e)
            pass


    def get_installed_browser(self,options= None):
        if self.installed_browser is not None:
            return self.installed_browser
        # 读取浏览器类型
        typePath = os.path.abspath(self.get_or_create_work_dir() + "/browser")
        if os.path.exists(typePath):
            with open(typePath, 'r', encoding="utf-8") as f:
                typePath = f.read()
        if typePath:
            type = typePath.strip()
            if type in self.browser_type_map:
                self.browser_type_map[type](options)
                if self.installed_browser is not None:
                    return self.installed_browser
        else:
            return None
        for browser_type in self.browser_type_map:
            args = []
            if options is not None:
                args.append(options)
            open_browser_thread = threading.Thread(target=self.browser_type_map[browser_type],args=args)
            open_browser_thread.start()
            open_browser_thread.join(timeout=20)
            if self.installed_browser is not None:
                with open(typePath, 'w', encoding="utf-8") as f:
                    f.write(browser_type)
                return self.installed_browser
        raise Exception("启动浏览器失败....")

if (__name__ == "__main__"):
    def checkSsoLogin(browser):
        if browser.title == '工作台 [Jenkins]':
            print("login success ,closing browser")
            return True
        return False
    session = SsoLoginUtil("https://zpsso.zhaopin.com/login").login("https://jenkins.dev.zhaopin.com:443/securityRealm/commenceLogin?from=/",checkFunction=checkSsoLogin)
    response = session.get("https://jenkins.dev.zhaopin.com")
    print(response.text)