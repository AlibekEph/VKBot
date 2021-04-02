from selenium import webdriver
from Assets.database import DB
from Assets.task import Task
from Assets.account import Account
import time
import os



def autolike():
    global stop
    while stop:
        db = DB()
        sql = "SELECT id, name, link, last_post FROM publics"
        res = db.query(sql).fetchall()
        options = webdriver.ChromeOptions()
        browser = webdriver.Chrome(executable_path=os.path.abspath('chromedriver.exe'), options=options)
        need_to_like = []
        for pub in res:
            browser.get(pub[2])
            last_post = browser.find_elements_by_css_selector('#page_wall_posts .post')[0].get_attribute('id')

            posts = browser.find_element_by_id('page_wall_posts')
            posts = posts.find_elements_by_class_name('post')
            for i in posts:
                if i.get_attribute('id') == pub[3]:
                    break
                else:
                    link = i.find_element_by_class_name('post_link').get_attribute('href')[1:]
                    link = pub[2] + '?w=' + link[14:]
                    print(link)
                    need_to_like.append(link)
            sql = f"UPDATE publics SET last_post = '{last_post}' WHERE id = {pub[0]}"
            db.query(sql)
            db.close()
        browser.quit()
        sql = "SELECT id FROM accounts"
        res = db.query(sql).fetchall()
        db.close()
        delay = 0
        for i in need_to_like:
            for j in res:
                task = Task(Account(j[0]), 'Лайк', i, delay)
                task.start()
                delay += 0.5
        time.sleep(3600)
    print('Stop')

