import hashlib, hmac, json, os, secrets, sqlite3, time
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).parent
DB = os.environ.get('ACADEMY_DB', str(ROOT / 'academy.sqlite3'))

def connect():
    db = sqlite3.connect(DB)
    db.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE, salt TEXT, password TEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS sessions (token TEXT PRIMARY KEY, user INTEGER, expires REAL)')
    db.execute('CREATE TABLE IF NOT EXISTS projects (user INTEGER, name TEXT, data TEXT, PRIMARY KEY(user,name))')
    return db

def password_hash(password, salt):
    return hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), n=16384, r=8, p=1).hex()

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / 'web'), **kwargs)

    def reply(self, status, data, cookie=None):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        if cookie: self.send_header('Set-Cookie', cookie)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith('/api/'): return self.api({})
        return super().do_GET()

    def do_POST(self):
        origin = self.headers.get('Origin')
        if origin and origin not in ('http://' + self.headers.get('Host',''), 'https://' + self.headers.get('Host','')):
            return self.reply(403, {'error': 'Origin rejected'})
        try:
            size = int(self.headers.get('Content-Length', 0))
            if size > 2_000_000: return self.reply(413, {'error': 'Request too large'})
            data = json.loads(self.rfile.read(size))
            if not isinstance(data, dict): raise ValueError()
        except (ValueError, TypeError): return self.reply(400, {'error': 'Invalid JSON'})
        self.api(data)

    def api(self, data):
        with connect() as db:
            route = self.path
            if route in ('/api/register','/api/login') and self.command == 'POST':
                email, password = data.get('email',''), data.get('password','')
                if not isinstance(email,str) or not isinstance(password,str) or '@' not in email or len(email)>254 or not 12 <= len(password) <= 256:
                    return self.reply(400, {'error': 'Use an email and a password of 12–256 characters.'})
                email = email.strip().lower()
                if route.endswith('register'):
                    salt = secrets.token_hex(16)
                    try: db.execute('INSERT INTO users(email,salt,password) VALUES(?,?,?)',(email,salt,password_hash(password,salt)))
                    except sqlite3.IntegrityError: return self.reply(409, {'error': 'Account unavailable; try signing in.'})
                user = db.execute('SELECT id,salt,password FROM users WHERE email=?',(email,)).fetchone()
                salt = user[1] if user else '00'*16
                computed = password_hash(password,salt)
                if not user or not hmac.compare_digest(computed,user[2]): return self.reply(401, {'error': 'Invalid credentials'})
                token = secrets.token_hex(32)
                db.execute('INSERT INTO sessions VALUES(?,?,?)',(token,user[0],time.time()+86400))
                secure = '; Secure' if os.environ.get('ACADEMY_SECURE_COOKIE') == '1' else ''
                return self.reply(200, {'email':email}, f'session={token}; HttpOnly; SameSite=Strict; Path=/; Max-Age=86400{secure}')
            from http.cookies import SimpleCookie
            cookie = SimpleCookie()
            try: cookie.load(self.headers.get('Cookie',''))
            except Exception: pass
            token = cookie['session'].value if 'session' in cookie else ''
            user = db.execute('SELECT users.id,email FROM sessions JOIN users ON users.id=sessions.user WHERE token=? AND expires>?',(token,time.time())).fetchone()
            if not user: return self.reply(401, {'error':'Sign in to save and load projects.'})
            if route == '/api/me': return self.reply(200, {'email': user[1]})
            if route == '/api/logout' and self.command == 'POST':
                db.execute('DELETE FROM sessions WHERE token=?',(token,))
                return self.reply(200, {}, 'session=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0')
            if route == '/api/projects':
                if self.command == 'POST':
                    name, project = data.get('name'), data.get('project')
                    if not isinstance(name,str) or not 1 <= len(name.strip()) <= 100 or not isinstance(project,dict):
                        return self.reply(400, {'error':'Invalid project'})
                    db.execute('INSERT OR REPLACE INTO projects VALUES(?,?,?)',(user[0],name.strip(),json.dumps(project)))
                rows = db.execute('SELECT name,data FROM projects WHERE user=?',(user[0],)).fetchall()
                return self.reply(200, {'projects':[{'name':n,'project':json.loads(d)} for n,d in rows]})
            return self.reply(404, {'error':'Not found'})

if __name__ == '__main__':
    connect().close()
    ThreadingHTTPServer((os.environ.get('HOST','127.0.0.1'), int(os.environ.get('PORT','8000'))), Handler).serve_forever()
