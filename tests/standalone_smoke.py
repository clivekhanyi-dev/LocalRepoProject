"""Test exact bundled HTML offline. Managed browser blocks file://; route the bytes in memory."""
from pathlib import Path
import json,tempfile
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
URL='http://127.0.0.1:18181/Automation-Academy-V1.html'
HTML=(ROOT/'Automation-Academy-V1.html').read_text()
assert '<script src=' not in HTML and 'href="style.css"' not in HTML
def serve(context):
 context.route(URL,lambda route:route.fulfill(status=200,content_type='text/html',body=HTML))
with tempfile.TemporaryDirectory() as tmp, sync_playwright() as p:
 userdir=Path(tmp)/'profile'
 def launch():
  context=p.chromium.launch_persistent_context(str(userdir),executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'],viewport={'width':1280,'height':900},accept_downloads=True)
  context.set_offline(True)
  serve(context)
  return context
 context=launch();page=context.pages[0];errors=[];requests=[]
 page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url));page.on('dialog',lambda d:d.accept())
 page.goto(URL)
 page.get_by_role('heading',name='Build confidence.').wait_for()
 assert 'Version 1' in page.title()
 page.locator('[data-tab="learn"]').click();page.locator('#notes').fill('Offline commissioning notebook')
 page.locator('#advancedNotes').fill('Retain my hydraulic calculations')
 page.locator('#lessonTrack').select_option('PLC / CODESYS')
 page.locator('#advancedLessons > details > summary').first.click()
 page.locator('#advancedLessons textarea').first.fill('Later rungs see earlier assignments')
 page.locator('#advancedLessons input[type=checkbox]').first.check()
 page.evaluate("navigate('plc')");page.locator('.rung-preset').nth(1).fill('200');page.locator('#compilePlc').click()
 page.locator('#plcStart').check();page.locator('#scanPlc').click();page.locator('#plcStart').uncheck();page.locator('#scanPlc').click();page.locator('#scanPlc').click()
 assert page.evaluate('labState.tags.Motor') is True
 page.locator('[data-tab="profile"]').click();page.locator('#localName').fill('Clive');page.locator('#renameProfile').click()
 page.locator('[data-tab="projects"]').click();page.locator('#mobileProjectName').fill('Version 1 offline project');page.locator('#projectSave').click()
 page.get_by_text('Project, notes and progress saved.',exact=True).wait_for()
 with page.expect_download() as info:page.locator('#exportBackup').click()
 backup=Path(tmp)/'backup.json';info.value.save_as(backup)
 value=json.loads(backup.read_text());assert value['format']=='automation-academy-backup';assert value['profile']=='Clive';assert len(value['projects'])==1
 assert value['projects'][0]['project']['notes']=='Offline commissioning notebook'
 page.wait_for_function("localStorage.getItem('automation-academy-v1').includes('Version 1 offline project')")
 page.wait_for_function("JSON.parse(localStorage.getItem('automation-academy-v1')).draft?.project.notes === 'Offline commissioning notebook'")
 assert not errors,errors
 context.close()
 # Reopen the file in a new browser process using the same local profile.
 context=launch();page=context.pages[0];page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept())
 page.goto(URL)
 assert page.locator('#notes').input_value()=='Offline commissioning notebook'
 assert page.locator('#advancedNotes').input_value()=='Retain my hydraulic calculations'
 assert page.evaluate('labProgram[1].preset')==200
 assert page.evaluate('labState.tags.Motor || false') is False  # Do not resume machine commands.
 assert page.evaluate('StandaloneStore.profile()')=='Clive'
 # Clear browser data, then recover by importing the downloaded backup.
 page.evaluate("localStorage.clear()");page.reload()
 page.locator('[data-tab="projects"]').click();page.locator('#importBackup').set_input_files(backup)
 page.wait_for_function("project.notes==='Offline commissioning notebook'")
 assert page.evaluate('(project.advancedCompleted||[]).includes("plc-scan")')
 assert page.locator('#advancedNotes').input_value()=='Retain my hydraulic calculations'
 assert page.evaluate('labProgram[1].preset')==200
 page.evaluate("navigate('symbols')");assert page.locator('#symbolLibrary svg').count()==15
 page.evaluate("navigate('calculators')");assert '14.67 A' in page.locator('#motorResult').inner_text();assert '5.00 kW' in page.locator('#hydResult').inner_text()
 # Reject malformed backup before replacing any saved data.
 page.evaluate("navigate('projects')")
 page.locator('#importBackup').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':b'{"format":"automation-academy-backup","version":1,"projects":[{"name":"Bad","project":{"nodes":[{"kind":"unknown"}],"wires":[]}}]}'})
 page.wait_for_function("document.getElementById('toast').textContent.includes('Import failed')")
 assert page.evaluate('StandaloneStore.request("projects").then(r=>r.projects.length)')==1
 # An unfinished PLC expression is a recoverable draft, not a reason to discard notes.
 page.evaluate("navigate('plc')");page.locator('.rung-expression').first.fill('MissingTag');page.locator('#compilePlc').click()
 page.wait_for_function("JSON.parse(localStorage.getItem('automation-academy-v1')).draft?.project.plc.program[0].expression==='MissingTag'")
 page.reload()
 assert 'Unknown tag' in page.locator('#plcError').inner_text()
 assert page.locator('#notes').input_value()=='Offline commissioning notebook'
 assert not errors,errors
 assert not [r for r in requests if r.startswith(('http:','https:')) and r!=URL],requests
 context.close()
 # Storage blocked: tools and export remain usable; a save must not claim success.
 context=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']).new_context(accept_downloads=True)
 context.set_offline(True)
 serve(context)
 context.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('Storage blocked')}})")
 page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(URL);page.evaluate("navigate('projects')")
 page.locator('#projectSave').click();assert 'storage is unavailable' in page.locator('#toast').inner_text()
 with page.expect_download() as d:page.locator('#exportBackup').click()
 assert d.value.suggested_filename=='automation-academy-backup.json'
 assert not errors,errors
 context.browser.close()
 print('PASS: bundled HTML offline launch (loopback route; file:// blocked by managed-browser policy), PLC, local saving, autosave, browser restart, backup export/import, invalid backup rejection, calculators/symbols and storage-blocked recovery; no HTTP dependencies or JS errors')
