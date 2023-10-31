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
import pickle


def get_protocol_and_domain(url):
    parsed_url = urlparse(url)
    protocol = parsed_url.scheme
    domain = parsed_url.netloc
    protocol_and_domain = f"{protocol}://{domain}"
    return protocol_and_domain
def get_domain(url):
    parsed_url = urlparse(url).netloc
    if ":" in parsed_url:
        return parsed_url.split(":")[0]
    return parsed_url

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
        self.login_page_inited= False
        self.work_folder = ".zpsso"
        self.session_cookie_jar =  http.cookiejar.LWPCookieJar(filename=self.get_cookie_path())
        if os.path.exists(self.get_cookie_path()):
            self.session_cookie_jar.load()
        self.key_cookie_names =  ["INNER_AUTHENTICATION","crosgwusercred"]
        self.browser_options = None
        self.installed_browser = None
        # 读取环境变量 ZPSSO_FOLDER_NAME
        self.url =os.getenv("ZPSSO_URL",sso_url)
        self.session = requests.Session() 
        self.session.cookies = self.session_cookie_jar
        self.get_or_update_version()

    def clearCookie(self):
        self.session.cookies.clear()

    def get_cookie_path(self):
        cookie_dir = self.get_or_create_work_dir()
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
    def init_login_page(self,url):
        self.login_page_inited = False
        browser = self.get_installed_browser()
        browser.get(f"{self.url}?service={url}")
        self.login_page_inited = True

    def ssologinByBrowser(self,url,username = None, password = None, type = None):
        # 打开浏览器并且打开登录页面
        threading.Thread(target=self.init_login_page,args=[url]).start()
        # 等待用户进行操作，例如登录或浏览网页
        def login_wait(username,password):
            while True:
                if username is None:
                    username = input("请输入ERP用户名: ")
                if password is None:
                    password = getpass.getpass("请输入ERP密码: ")
                print("等待登录网页中...")
                while not self.login_page_inited :
                    time.sleep(0.1)
                browser = self.get_installed_browser()
                try:
                    browser.find_element(value = "sel_account").click()
                    time.sleep(0.1)
                    browser.find_element(value = "username").clear()
                    browser.find_element(value = "username").send_keys(username)
                    browser.find_element(value = "password").send_keys(password)
                    time.sleep(0.1)
                    browser.find_element(value = "login").click()
                    print("正在登录,请稍后....")
                    while True:
                        if get_domain(url) == get_domain(browser.current_url):
                            break
                        try:
                            text = browser.find_element(value = "username").get_attribute('innerText') 
                            if text != username:
                                break
                        except:
                            pass
                        time.sleep(0.1)
                    break
                except:
                    time.sleep(1)
            for cookie_name in self.key_cookie_names:
                cookie = browser.get_cookie(cookie_name)
                if cookie is None:
                    print("用户密码可能错了,请重新输入...")
                    login_wait(None,None)
                    break
            browser.quit()
            print("login success")
           
        login_wait(username,password)            
        # 获取浏览器中的cookie
        #browser_cookies = browser.get_cookies()
        expiration_time = datetime.datetime.now() + datetime.timedelta(days=20)

        def add_cookie(cookie):
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
                "secure": cookie.get('secure',False),
                "expires": expiration_time.timestamp(),
                "discard": False,
                "comment": None,
                "comment_url": None,
                "rfc2109": False,
                "rest": {'HttpOnly': cookie.get("httpOnly",None),"sameSite":cookie.get("sameSite",None)}
            }
            self.session_cookie_jar.set_cookie(http.cookiejar.Cookie(**cookie_dict))
        # 将浏览器中的cookie添加到cookie_jar中
        browser = self.get_installed_browser()
        for cookie_name in self.key_cookie_names:
            cookie = browser.get_cookie(cookie_name)
            if cookie is not None:
                add_cookie(cookie)
        
        # 保存cookie_jar到指定文件
        self.session_cookie_jar.save(ignore_expires=True)
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

    def login(self,url,userName = None, password=None,type = ModuleNotFoundError):
        response = self.session.get(url)
        # 相互包含
        if get_domain(response.url) == get_domain(url):
            return self.session
        print("开始执行浏览器登录逻辑...")
        session = self.ssologinByBrowser(url,type=type)
        self.session.get(url)
        return session

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
    def init_options(self,option):
        #option.add_argument("--headless")
        option.add_argument("--log-level=4")
        option.add_argument('window-size=1920x1080')
        option.add_argument('--start-maximized') 
        option.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
        option.add_argument("disable-cache")#禁用缓存
        option.add_experimental_option("excludeSwitches",['enable-automation','enable-logging'])


        self.browser_options = option

    def init_chrome(self,option = None):
        # 尝试检测Chrome浏览器
        try:
            if option is None:
                from selenium.webdriver.chrome.options import Options
                option = Options()
                self.init_options(option)
            browser =  webdriver.Chrome(options = option)
            self.installed_browser = browser
        except Exception as e:
            print("try open chrome failed:" ,e)
            pass


    def init_edge(self,option = None):
        # 尝试检测Edge浏览器
        try:
            if option is None:
                from selenium.webdriver.edge.options import Options
                option = Options()
                self.init_options(option)
            browser =  webdriver.Edge( options= option)
            self.installed_browser = browser
        except Exception as e:
            print("try open edge failed:" ,e)
            pass


    def init_firefox(self,option = None):
        # 尝试检测Firefox浏览器
        try:
            if option is None:
                from selenium.webdriver.firefox.options import Options
                option = Options()
                self.init_options(option)
            browser =  webdriver.Firefox( options= option)
            self.installed_browser = browser
        except Exception as e:
            print("try open firefox failed:" ,e)
            pass


    def init_safari(self,option = None):
        # 尝试检测Safari浏览器 (需要Safari驱动程序)
        try:
            from selenium.webdriver.safari.service import Service as SafariService
            if option is None:
                from selenium.webdriver.safari.options import Options
                option = Options()
                self.init_options(option)
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
    #session = SsoLoginUtil("https://zpsso.zhaopin.com/login").login("https://apollo.dev.zhaopin.com/")
    #response = session.get("https://apollo.dev.zhaopin.com/user")
    #print(response.text)
    #print("finished")
    session = SsoLoginUtil("https://zpsso.zhaopin.com/login").login("https://jenkins.dev.zhaopin.com:443/securityRealm/commenceLogin?from=/")
    response = session.get("https://jenkins.dev.zhaopin.com:443/securityRealm/commenceLogin?from=/")
    print(response.text)
    print("finished")
    
            