import sys, tempfile, threading, unittest, json, urllib.request, urllib.error, http.cookiejar
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import server
class Integration(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.temp=tempfile.TemporaryDirectory();server.DB=cls.temp.name+'/test.sqlite3'
  cls.http=server.ThreadingHTTPServer(('127.0.0.1',0),server.Handler)
  cls.url='http://127.0.0.1:'+str(cls.http.server_port)
  threading.Thread(target=cls.http.serve_forever,daemon=True).start()
 @classmethod
 def tearDownClass(cls):cls.http.shutdown();cls.http.server_close();cls.temp.cleanup()
 def test_accounts_save_reload_and_isolation(self):
  a=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
  b=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
  def request(client,path,data=None):
   req=urllib.request.Request(self.url+path,data=json.dumps(data).encode() if data is not None else None,headers={'Content-Type':'application/json'})
   with client.open(req) as r:return json.load(r)
  with self.assertRaises(urllib.error.HTTPError) as e:request(a,'/api/projects')
  self.assertEqual(e.exception.code,401)
  for c,email in [(a,'a@example.com'),(b,'b@example.com')]:request(c,'/api/register',{'email':email,'password':'a-long-test-password'})
  project={'nodes':[{'id':'v','kind':'valve'}],'wires':[],'notes':'test','completed':[0]}
  request(a,'/api/projects',{'name':'Circuit A','project':project})
  self.assertEqual(request(a,'/api/projects')['projects'][0]['project'],project)
  self.assertEqual(request(b,'/api/projects')['projects'],[])
  request(a,'/api/logout',{})
  with self.assertRaises(urllib.error.HTTPError):request(a,'/api/projects')
  request(a,'/api/login',{'email':'a@example.com','password':'a-long-test-password'})
  self.assertEqual(len(request(a,'/api/projects')['projects']),1)
  with a.open(self.url+'/') as r:self.assertIn(b'Automation Engineering Academy',r.read())
if __name__=='__main__':unittest.main()
