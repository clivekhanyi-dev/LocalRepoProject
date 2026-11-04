"""Requires Playwright and Chromium; runs against an isolated temporary server/database."""
import os, subprocess, tempfile, time, socket, json
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
   page.get_by_text('Foundation refresher (existing lessons)',exact=True).click()
   page.locator('#lessons input').first.check()
   page.locator('#notes').fill('Samsung test notes')
   page.locator('[data-tab="calculators"]').click()
   page.locator('#bore').fill('40')
   assert '754.0' in page.locator('#force').inner_text()
   page.locator('[data-tab="compare"]').click()
   page.locator('.product input[type=file]').first.set_input_files({'name':'datasheet.txt','mimeType':'text/plain','buffer':b'Source excerpt for a test valve.'})
   page.wait_for_function("document.getElementById('excerpt0').value==='Source excerpt for a test valve.'")
   page.locator('#compareBtn').click()
   assert page.get_by_text('Insufficient evidence',exact=True).is_visible()
   page.evaluate("navigate('learn')")
   page.locator('#lessonTrack').select_option('Hydraulics')
   page.locator('#advancedLessons > details > summary').first.click()
   page.locator('#advancedLessons textarea').first.fill('Fluid power = 5 kW; shaft input = 5.88 kW')
   page.locator('#advancedLessons input[type=checkbox]').first.check()
   page.locator('#advancedNotes').fill('Capstone design notes')
   page.evaluate("navigate('calculators')")
   assert '5.00 kW' in page.locator('#hydResult').inner_text()
   assert '14.67 A' in page.locator('#motorResult').inner_text()
   page.evaluate("navigate('symbols')")
   page.locator('#symbolSearch').fill('hydraulic')
   assert page.locator('#symbolLibrary svg').count() >= 3
   page.evaluate("navigate('plc')")
   page.locator('.rung-preset').nth(1).fill('200')
   page.locator('#compilePlc').click()
   page.locator('#plcStart').check();page.locator('#scanPlc').click()
   assert page.evaluate('labState.tags.Run') is True
   page.locator('#plcStart').uncheck()
   page.locator('#scanPlc').click();page.locator('#scanPlc').click()
   assert page.evaluate('labState.tags.Motor') is True
   page.locator('#plcStop').uncheck();page.locator('#scanPlc').click()
   assert page.evaluate('labState.tags.Motor') is False
   assert page.evaluate('labState.tags.Fault') is True
   page.locator('.rung-expression').first.fill('UnknownTag')
   page.locator('#compilePlc').click()
   assert 'Unknown tag' in page.locator('#plcError').inner_text()
   page.locator('.rung-expression').first.fill('StopHealthy AND OverloadHealthy AND (Start OR Run)')
   page.locator('#compilePlc').click()
   page.locator('[data-tab="profile"]').click()
   page.locator('#profileLogin').click()
   page.locator('#email').fill('mobile@example.com');page.locator('#password').fill('mobile-test-password')
   page.locator('#register').click();page.locator('#auth').wait_for(state='hidden')
   page.locator('[data-tab="projects"]').click()
   page.locator('#mobileProjectName').fill('Mobile project')
   page.locator('#projectSave').click()
   page.get_by_text('Project, notes and progress saved.',exact=True).wait_for()
   with page.expect_download() as exported:page.locator('#exportBackup').click()
   backup=Path(tmp)/'server-backup.json';exported.value.save_as(backup)
   data=json.loads(backup.read_text());assert data['format']=='automation-academy-backup'
   assert data['projects'][0]['project']['advancedNotes']=='Capstone design notes'
   page.reload();page.locator('#projectOpen').click()
   page.get_by_role('button',name='Mobile project',exact=True).click()
   assert page.locator('#studio').is_visible()
   page.wait_for_function("document.getElementById('excerpt0').value==='Source excerpt for a test valve.'")
   page.locator('#coil').check();page.locator('#step').click()
   assert 'Cylinder retracts' in page.locator('#feedback').inner_text()
   page.locator('[data-tab="learn"]').click()
   assert page.locator('#notes').input_value()=='Samsung test notes'
   assert page.locator('#advancedNotes').input_value()=='Capstone design notes'
   assert page.evaluate('project.advancedCompleted.includes("hyd-power")')
   assert page.evaluate('project.advancedAnswers["hyd-power"]')=='Fluid power = 5 kW; shaft input = 5.88 kW'
   assert page.evaluate('labProgram[1].preset')==200
   assert page.locator('#lessons input').first.is_checked()
   page.locator('[data-tab="calculators"]').click()
   assert page.locator('#bore').input_value()=='40'
   page.locator('[data-tab="dashboard"]').click()
   assert '1 / 5' in page.locator('#progressCount').inner_text()
   page.locator('#toast').evaluate('(e)=>e.style.display="none"')
   page.screenshot(path=str(ROOT/'docs/mobile-dashboard.png'),full_page=True)
   for width in [360,412,768,1280]:
    page.set_viewport_size({'width':width,'height':900})
    for tab in ['dashboard','learn','calculators','compare','projects','profile','studio','plc','symbols']:
     page.evaluate('(tab)=>navigate(tab)',tab)
     assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (width,tab,'overflow')
   assert not errors,errors
   print('PASS: mobile dashboard/navigation, registration, save/reload, notes, lessons, calculator, coil, comparison, advanced curriculum persistence, PLC timer/stop/compiler, symbols, hydraulic/electrical sizing, and responsive widths 360/412/768/1280; no JS errors')
   browser.close()
 finally:process.terminate();process.wait()
