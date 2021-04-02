from threading import Thread
from Assets.database import DB
import time
from Assets.others import *

class Task(Thread):
    def __init__(self, account, type=None, link=None, delay=None, text='No', exist=0, stop=True):
        Thread.__init__(self)
        self.stop_flag = stop
        self.start_time = time.time()
        self.db = DB()
        self.account = account
        self.type = type
        self.link = link
        self.delay = delay * 60
        self.text = text
        self.EndPoint = lambda: print('EndPoint')
        self.MiddlePoint = lambda: print('MiddlePoint')
        self.WaitingTrigger = lambda x: print('WaitingTrigger', x)


    def setEndPoint(self, f):
        self.EndPoint = f

    def setMiddlePoint(self, f):
        self.MiddlePoint = f

    def setWaitingTrigger(self, f):
        self.WaitingTrigger = f

    def stop(self):
        try:
            self.browser.close()
            self.browser.quit()
        except:
            pass
        self.stop_flag = False
        self.EndPoint()


    def run(self):
        while self.stop_flag:
            if time.time() - self.start_time >= self.delay - 30:
                self.browser = start_vk(proxy=self.account.get_proxy())
                self.start_task()
                self.stop()
                break
            n = int(self.start_time + self.delay - time.time())
            h = str(n // 3600)
            m = str((n // 60) % 60)
            s = str(n % 60)
            self.WaitingTrigger(h + ':' + m + ':' + s)
            time.sleep(1)

    def start_task(self):
        self.MiddlePoint()
        url1 = self.browser.current_url
        for i in range(5):
            vklogin = self.account.get_login()
            vkpassword = self.account.get_password()
            try:

                self.browser.find_element_by_xpath('//*[@id="index_email"]').send_keys(vklogin)

                self.browser.find_element_by_xpath('//*[@id="index_pass"]').send_keys(vkpassword)

                self.browser.find_element_by_xpath('//*[@id="index_login_button"]').click()

                time.sleep(2)
            except:
                self.stop()
                print("Ошибка при входе")
            time.sleep(2)
            url2 = self.browser.current_url
            recaptcha = False
            try:
                print(self.browser.find_elements_by_css_selector('.g-recaptcha'))
                recaptcha = True
            except:
                pass
            try:
                if url1 == url2 and recaptcha:
                    print(self.browser.find_element_by_css_selector('.g-recaptcha'))
                    WebDriverWait(self.browser, 120).until(lambda x: x.find_element_by_css_selector('.antigate_solver'))
            except:
                pass
            if url1 != url2:
                break
            time.sleep(2)
        self.browser.get(self.link)
        time.sleep(2)
        try:
            if (self.browser.find_element_by_class_name('popup_box_container')):
                self.browser.find_element_by_class_name('box_x_button').click()
                self.browser.get(self.link)
                time.sleep(3)
        except Exception as e:
            print(e)

        if self.type == 'Лайк':
            self.like()
        elif self.type == 'Коментарий':
            self.comment()
        elif self.type == 'Оба':
            self.like()
            self.comment()
        time.sleep(4)
        self.stop()

    def get_id(self):
        return self.id

    def like(self):
        self.browser.find_element_by_xpath('//*[@id="wl_post_actions_wrap"]/div/div/div[1]/a[1]/div[1]').click()

    def comment(self):
        print(self.browser.find_element_by_class_name("submit_post_field"))
        time.sleep(4)
        self.browser.execute_script(" document.getElementById('wl_post_body_wrap').style.display = 'none'; ")
        self.browser.find_element_by_css_selector('#wl_head_wrap').click()
        time.sleep(1)
        self.browser.find_element_by_css_selector('body').send_keys(Keys.DOWN)
        time.sleep(2)
        self.browser.find_element_by_css_selector(".reply_field").send_keys(self.text)
        time.sleep(2)
        self.browser.find_element_by_css_selector(".reply_send_button:not(.reply_send_disabled)").click()
