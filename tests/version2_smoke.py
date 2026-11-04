"""Offline V2 bundle/migration tests. File:// is blocked by managed-browser policy.
Routes fulfil only bundled document bytes in memory; there is no app server."""
from pathlib import Path
import tempfile,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
URL1='http://127.0.0.1:18182/Automation-Academy-V1.html'
URL2='http://127.0.0.1:18182/Automation-Academy-V2.html'
HTML1=(ROOT/'Automation-Academy-V1.html').read_text();HTML2=(ROOT/'Automation-Academy-V2.html').read_text()
assert '<script src=' not in HTML2 and 'href="style.css"' not in HTML2
with tempfile.TemporaryDirectory() as tmp,sync_playwright() as p:
 def launch():
  ctx=p.chromium.launch_persistent_context(str(Path(tmp)/'profile'),executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'],viewport={'width':1280,'height':900},accept_downloads=True)
  ctx.set_offline(True);ctx.route(URL1,lambda r:r.fulfill(status=200,content_type='text/html',body=HTML1));ctx.route(URL2,lambda r:r.fulfill(status=200,content_type='text/html',body=HTML2))
  return ctx
 ctx=launch();page=ctx.pages[0];errors=[];requests=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url));page.on('dialog',lambda d:d.accept())
 # Export actual V1 data and use it unchanged in V2.
 page.goto(URL1);page.evaluate("navigate('learn')");page.locator('#notes').fill('My V1 notes survive V2')
 page.locator('#advancedNotes').fill('Original commissioning record');page.evaluate("navigate('projects')");page.locator('#mobileProjectName').fill('Legacy V1 project');page.locator('#projectSave').click()
 with page.expect_download() as d:page.locator('#exportBackup').click()
 backup=Path(tmp)/'v1.json';d.value.save_as(backup)
 page.goto(URL2);assert 'Version 2' in page.title();assert page.locator('#notes').input_value()==''
 page.evaluate("navigate('projects')");page.locator('#importBackup').set_input_files(backup)
 page.wait_for_function("project.notes==='My V1 notes survive V2'")
 assert page.locator('#advancedNotes').input_value()=='Original commissioning record'
 assert page.evaluate("JSON.parse(localStorage.getItem('automation-academy-v1')).projects.length")==1
 page.evaluate("navigate('sizing')")
 assert '50 mm' in page.locator('#sizeResult').inner_text()
 assert '290.25 N' in page.locator('#loadResult').inner_text()
 page.locator('#sizeLoad').fill('1000');page.locator('#sizeDir').select_option('retract');assert '1500.0 N' in page.locator('#sizeResult').inner_text()
 page.locator('#useBore').click();assert page.locator('#airBore').input_value()=='80'
 page.locator('#airCycles').fill('40');assert 'INCONSISTENT CYCLE' in page.locator('#airResult').inner_text()
 page.locator('#airCycles').fill('10');page.locator('#airStroke').fill('150');page.locator('#sizingNotes').fill('Measured load case, confirm rod buckling')
 page.evaluate("navigate('panels')");assert '2.313 A' in page.locator('#panelResult').inner_text()
 assert 'FITS' in page.locator('#layoutResult').inner_text()
 page.locator('#layoutD').fill('100');assert 'DOES NOT FIT' in page.locator('#layoutResult').inner_text()
 page.locator('#layoutD').fill('250');page.locator('#panelNotes').fill('Protection coordination pending');page.locator('#panelCheck0').check()
 with page.expect_download() as d:page.locator('#designReport').click()
 report=Path(tmp)/'report.txt';d.value.save_as(report);assert 'Measured load case' in report.read_text()
 page.evaluate("navigate('calculators')");assert '11.78 L/min' in page.locator('#hydFlowResult').inner_text()
 page.locator('#hydFlowSide').select_option('retract');assert '8.84 L/min' in page.locator('#hydFlowResult').inner_text()
 page.evaluate("navigate('symbols')");assert page.locator('#symbolLibrary svg').count()==36
 for example in ['ep-hold','ep-auto','hydraulic-unit','motor-starter']:
  page.evaluate("navigate('circuits')");page.locator('#circuitSelect').select_option(example)
  assert page.locator('#circuitDrawing > svg').count()==1
  assert page.locator('#circuitDetails tr').count()==4
 page.locator('#circuitSelect').select_option('ep-auto');page.locator('#circuitNotes').fill('Validate port assignments before hardware')
 page.locator('#circuitPlc').click()
 assert page.locator('.rung-row').count()==15
 assert page.locator('#plcRetracted').is_checked()
 page.locator('#plcStart').check();page.locator('#scanPlc').click();assert page.evaluate('labState.tags.Y1') is True
 page.locator('#plcStart').uncheck();page.locator('#plcRetracted').uncheck();page.locator('#scanPlc').click()
 page.locator('#plcExtended').check();page.locator('#scanPlc').click();assert page.evaluate('labState.tags.Y2') is True;assert page.evaluate('labState.tags.Y1') is False
 page.locator('#plcExtended').uncheck();page.locator('#scanPlc').click();page.locator('#plcRetracted').check();page.locator('#scanPlc').click();assert page.evaluate('labState.tags.Y2') is False
 page.evaluate("navigate('projects')");page.locator('#projectSave').click()
 with page.expect_download() as d:page.locator('#exportBackup').click()
 v2backup=Path(tmp)/'v2.json';d.value.save_as(v2backup);value=json.loads(v2backup.read_text());assert value['version']==1 and value['appVersion']=='2.0'
 assert value['projects'][0]['project']['designV2']['sizingNotes']=='Measured load case, confirm rod buckling'
 page.wait_for_function("JSON.parse(localStorage.getItem('automation-academy-v2')).draft?.project.designV2.panelCheck0===true")
 assert not errors,errors
 ctx.close()
 ctx=launch();page=ctx.pages[0];page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept());page.goto(URL2)
 assert page.locator('#sizingNotes').input_value()=='Measured load case, confirm rod buckling'
 assert page.locator('#panelCheck0').is_checked();assert page.locator('#panelNotes').input_value()=='Protection coordination pending'
 assert page.locator('#circuitSelect').input_value()=='ep-auto';assert page.locator('.rung-row').count()==15
 assert page.locator('#notes').input_value()=='My V1 notes survive V2'
 # Stored outputs must not auto-resume; a saved program and inputs do not imply running machinery.
 assert not page.evaluate('labState.tags.Y1 || labState.tags.Y2 || false')
 # Core backup format survives a clean V2 local store as well as draft restoration.
 page.evaluate("localStorage.removeItem('automation-academy-v2')");page.reload();page.evaluate("navigate('projects')")
 page.locator('#importBackup').set_input_files(v2backup);page.wait_for_function("project.designV2?.panelCheck0===true")
 assert page.locator('#sizingNotes').input_value()=='Measured load case, confirm rod buckling'
 assert page.locator('#airStroke').input_value()=='150'
 # Selectors and wide diagrams must stay inside scroll containers, including phone widths.
 for width in [360,412,768,1280]:
  page.set_viewport_size({'width':width,'height':900})
  for tab in ['dashboard','sizing','panels','circuits','plc','symbols','learn','projects']:
   page.evaluate('(t)=>navigate(t)',tab)
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,tab,'page overflow')
 # Offline ST reference download is embedded, not a network request.
 page.evaluate("navigate('plc')");page.locator('#plcExamplesHost > details > summary').click()
 page.locator('#codesysExample').select_option('1')
 with page.expect_download() as d:page.locator('#downloadST').click()
 st=Path(tmp)/'reference.st';d.value.save_as(st);assert 'CASE Step OF' in st.read_text()
 page.locator('#plcExtended').check();page.locator('#resetPlc').click()
 assert not page.locator('#plcExtended').is_checked() and page.locator('#plcRetracted').is_checked()
 assert page.locator('.rung-row').count()==4
 assert not errors,errors
 assert not [r for r in requests if r not in [URL1,URL2]],requests
 ctx.close()
 print('PASS: V1→V2 migration, sizing/flow/panel worksheets, 36 symbols, four circuits, 15-rung cylinder cycle, reports, ST download, persistent V2 fields, backup recovery, phone layouts; no external resources or JS errors')
