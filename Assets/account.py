from Assets.database import DB

class Account:
    def auth(self, id):
        self.id = id
        self.db = DB()
        sql = f"SELECT id, login, password, name, proxy, proxy_login, proxy_pass FROM accounts WHERE id = {self.id}"
        res = self.db.query(sql).fetchall()
        self.login = res[0][1]
        self.id = res[0][0]
        self.password = res[0][2]
        self.name = res[0][3]
        self.proxy = res[0][4]
        self.proxy_login = res[0][5]
        self.proxy_pass = res[0][6]
        self.db.close()

    def __init__(self, login, password=None, name=None, proxy=None, proxy_login=None, proxy_pass=None):
        if password is None:
            self.auth(login)
        else:
            self.db = DB()
            sql = f"INSERT INTO accounts (id, login, password, name, proxy, proxy_login, proxy_pass) VALUES" \
                  f" (NULL, '{login}', '{password}', '{name}', '{proxy}', '{proxy_login}', '{proxy_pass}')"
            self.login = login
            self.proxy = proxy
            self.proxy_pass = proxy_pass
            self.proxy_login = proxy_login
            self.password = password
            self.name = name
            self.db.query(sql)
            self.db.close()
            sql = "SELECT id FROM accounts ORDER BY ID DESC LIMIT 1"
            res = self.db.query(sql).fetchall()[0]
            self.db.close()
            self.id = res[0]

    def get_proxy(self):
        return (self.proxy, self.proxy_login, self.proxy_pass)

    def get_id(self):
        return self.id

    def get_login(self):
        return self.login

    def get_password(self):
        return self.password

    def get_name(self):
        return self.name

