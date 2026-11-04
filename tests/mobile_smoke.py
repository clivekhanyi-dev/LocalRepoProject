"""Requires Playwright and Chromium; runs against an isolated temporary server/database."""
import os, subprocess, tempfile, time, socket
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as tmp:
 with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
 env={**os.environ,'PORT':str(port),'ACADEMY_DB':tmp+'/db.sqlite3'}
 process=subprocess.Popen(['python3','server.py'],cwd=ROOT,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 try:
  with sync_playwright() as p:
   browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
   page=browser.new_page(viewport={'width':360,'height':800},is_mobile=True,has_touch=True)
   errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   for _ in range(50):
    try:page.goto(f'http://127.0.0.1:{port}');break
    except Exception:time.sleep(.1)
   page.get_by_role('heading',name='Build confidence.').wait_for()
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'Page overflow'
   page.locator('[data-tab="learn"]').click()
   assert page.get_by_text('PLC foundations',exact=False).count()
   page.locator('#lessons input').first.check()
   page.locator('#notes').fill('Samsung test notes')
   page.locator('[data-tab="calculators"]').click()
   page.locator('#bore').fill('40')
   assert '754.0' in page.locator('#force').inner_text()
   page.locator('[data-tab="compare"]').click()
   page.locator('.product input[type=file]').first.set_input_files({'name':'datasheet.txt','mimeType':'text/plain','buffer':b'Source excerpt for a test valve.'})
   assert page.locator('#excerpt0').input_value()=='Source excerpt for a test valve.'
   page.locator('#compareBtn').click()
   assert page.get_by_text('Insufficient evidence',exact=True).is_visible()
   page.locator('[data-tab="profile"]').click()
   page.locator('#profileLogin').click()
   page.locator('#email').fill('mobile@example.com');page.locator('#password').fill('mobile-test-password')
   page.locator('#register').click();page.locator('#auth').wait_for(state='hidden')
   page.locator('[data-tab="projects"]').click()
   page.locator('#mobileProjectName').fill('Mobile project')
   page.locator('#projectSave').click()
   page.get_by_text('Project, notes and progress saved.',exact=True).wait_for()
   page.reload();page.locator('#projectOpen').click()
   page.get_by_role('button',name='Mobile project',exact=True).click()
   assert page.locator('#studio').is_visible()
   assert page.locator('#excerpt0').input_value()=='Source excerpt for a test valve.'
   page.locator('#coil').check();page.locator('#step').click()
   assert 'Cylinder retracts' in page.locator('#feedback').inner_text()
   page.locator('[data-tab="learn"]').click()
   assert page.locator('#notes').input_value()=='Samsung test notes'
   assert page.locator('#lessons input').first.is_checked()
   page.locator('[data-tab="calculators"]').click()
   assert page.locator('#bore').input_value()=='40'
   page.locator('[data-tab="dashboard"]').click()
   assert '1 / 5' in page.locator('#progressCount').inner_text()
   page.locator('#toast').evaluate('(e)=>e.style.display="none"')
   page.screenshot(path=str(ROOT/'docs/mobile-dashboard.png'),full_page=True)
   for width in [360,412,768,1280]:
    page.set_viewport_size({'width':width,'height':900})
    for tab in ['dashboard','learn','calculators','compare','projects','profile','studio']:
     page.evaluate('(tab)=>navigate(tab)',tab)
     assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (width,tab,'overflow')
   assert not errors,errors
   print('PASS: mobile dashboard/navigation, registration, save/reload, notes, lessons, calculator, coil, comparison, and responsive widths 360/412/768/1280; no JS errors')
   browser.close()
 finally:process.terminate();process.wait()
