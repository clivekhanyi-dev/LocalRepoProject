"""Exact standalone V3 bytes tested offline; managed-browser policy blocks file://."""
from pathlib import Path
import tempfile,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
URL2='http://127.0.0.1:18184/Automation-Academy-V2.html';URL3='http://127.0.0.1:18184/Automation-Academy-V3.html'
HTML2=(ROOT/'Automation-Academy-V2.html').read_text();HTML3=(ROOT/'Automation-Academy-V3.html').read_text()
assert '<script src=' not in HTML3 and 'href="style.css"' not in HTML3
with tempfile.TemporaryDirectory() as tmp,sync_playwright() as p:
 def launch():
  c=p.chromium.launch_persistent_context(str(Path(tmp)/'profile'),executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'],viewport={'width':1500,'height':1000},accept_downloads=True)
  c.set_offline(True);c.route(URL2,lambda r:r.fulfill(status=200,content_type='text/html',body=HTML2));c.route(URL3,lambda r:r.fulfill(status=200,content_type='text/html',body=HTML3));return c
 ctx=launch();page=ctx.pages[0];errors=[];requests=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url));page.on('dialog',lambda d:d.accept())
 page.goto(URL2);page.evaluate("navigate('learn')");page.locator('#notes').fill('My earlier V2 learning notes');page.evaluate("navigate('sizing')");page.locator('#sizingNotes').fill('Keep my V2 load and rod review');page.evaluate("navigate('projects')");page.locator('#mobileProjectName').fill('Integrated V3 project')
 with page.expect_download() as d:page.locator('#exportBackup').click()
 old=Path(tmp)/'v2.json';d.value.save_as(old)
 page.goto(URL3);assert 'Version 3' in page.title();page.evaluate("navigate('projects')");page.locator('#importBackup').set_input_files(old);page.wait_for_function("project.notes==='My earlier V2 learning notes'")
 assert page.locator('#sizingNotes').input_value()=='Keep my V2 load and rod review'
 page.evaluate("navigate('paneldesign')");assert page.evaluate('v3.jurisdiction')=='ZA'
 for case in ['transfer','clamp','drive','clamp']:
  page.locator('#v3Template').select_option(case);page.locator('#v3LoadTemplate').click();assert page.evaluate('PanelDesign.checkPlan(v3.plan).geometryIssues')==0
  assert page.locator('#v3Package table').count()>=5
 page.locator('#v3PanDown').click();assert page.evaluate('document.querySelector(".v3-board-scroll").scrollTop')>0
 page.locator('#v3SelectDevice').select_option('G1');assert 'G1' in page.locator('#v3DeviceEditor').inner_text()
 page.locator('#v3PanUp').click()
 # Selecting a device must not falsely invalidate review revisions.
 revision=page.evaluate('v3.revision');page.locator('#v3Canvas [data-device="Q0"]').click();assert page.evaluate('v3.revision')==revision
 source=page.locator('#v3DeviceEditor textarea');source.fill('Actual installation manual revision B, pages 14–16')
 page.locator('#v3DeviceEditor input[type=checkbox]').check();assert page.evaluate('PanelDesign.checkPlan(v3.plan).unverifiedDevices')==page.evaluate('v3.plan.devices.length-1')
 # Real pointer drag, then keyboard/numeric placement.
 r=page.locator('#v3Canvas [data-device="Q0"] rect').nth(1).bounding_box();page.mouse.move(r['x']+20,r['y']+20);page.mouse.down();page.mouse.move(r['x']+60,r['y']+30,steps=4);page.mouse.up();assert page.evaluate('v3.plan.devices.find(d=>d.id==="Q0").x')!=40
 for key,value in [('x','40'),('y','45')]:
  i=page.locator(f'#v3DeviceEditor input[data-property="{key}"]');i.fill(value);i.press('Tab')
 assert page.evaluate('PanelDesign.checkPlan(v3.plan).geometryIssues')==0
 x=page.locator('#v3DeviceEditor input[data-property="x"]');x.fill('0');x.press('Tab');assert 'outside available backplate' in page.locator('#v3Findings').inner_text();x=page.locator('#v3DeviceEditor input[data-property="x"]');x.fill('40');x.press('Tab')
 # Evidence requires fields, explicit draft attribution and becomes stale on a plan edit.
 page.evaluate("navigate('standards')");assert 'SANS 10142-1' in page.locator('#v3Context').inner_text();assert 'not been verified' in page.locator('#v3Context').inner_text()
 review=page.locator('#v3Reviews [data-review="scope"]');review.locator('summary').click();review.locator('button').click();assert page.evaluate('PanelDesign.evidenceSummary(PanelReviews,v3.reviews,v3.revision).recorded')==0
 review.locator('select').select_option('evidence-recorded');review.locator('input').fill('Clive — learning record');review.locator('textarea').fill('Scope review draft A, applicability decisions and open-edition check recorded.')
 review.locator('button').click();assert page.evaluate('PanelDesign.evidenceSummary(PanelReviews,v3.reviews,v3.revision).recorded')==1
 page.evaluate("navigate('paneldesign')");x=page.locator('#v3DeviceEditor input[data-property="x"]');x.fill('45');x.press('Tab');assert page.evaluate('PanelDesign.evidenceSummary(PanelReviews,v3.reviews,v3.revision).recorded')==0
 page.locator('#v3DesignNotes').fill('Keep device measurements and outstanding coordination checks')
 fault=page.locator('#v3Package > details').filter(has=page.get_by_text('Clamp position is reached but the part slips during processing.',exact=True));fault.locator('summary').first.click();fault.locator('textarea').fill('Compare actual clamp pressure, force and fixture geometry.')
 page.evaluate("navigate('standards')");page.locator('#v3Risk').fill('Risk assessment draft: <img src=x onerror=alert(1)> is literal text, not markup.')
 page.locator('#v3EditionNotes').fill('SANS adoption/edition to confirm in SABS catalogue; reviewer scope decision pending.')
 standard=page.locator('#v3StandardRecords [data-standard="machine-electrical"]');standard.locator('summary').click();standard.locator('select').select_option('applicable');standard.locator('input').nth(0).fill('Exact adopted designation/edition review pending');standard.locator('input').nth(1).fill('SABS catalogue lookup recorded as pending');standard.locator('textarea').fill('Machine electrical equipment scope intended; adopted edition and installation interface need review.')
 assert page.evaluate('v3.standards["machine-electrical"].applicability')=='applicable'
 page.evaluate("navigate('growth')");assert 'customer problem' in page.locator('#v3NextPractice').inner_text()
 skill=page.locator('#v3Skills [data-skill="requirements"]');skill.locator('summary').click();skill.locator('select').select_option('3');skill.locator('textarea').first.fill('Requirements and acceptance matrix revision A with measured cycle-time targets.');skill.locator('textarea').nth(1).fill('Mentor asked for a measurable restart acceptance test.');assert 'physical process' in page.locator('#v3NextPractice').inner_text()
 page.evaluate("navigate('paneldesign')")
 with page.expect_download() as d:page.locator('#v3Report').click()
 report=Path(tmp)/'report.html';d.value.save_as(report);report_text=report.read_text();assert '&lt;img src=x' in report_text and '<img src=x' not in report_text;assert 'not a compliance certificate' in report_text.lower() and '<script' not in report_text.lower()
 assert 'My earlier V2 learning notes' not in report_text  # Report is the panel/evidence package; project backup holds all lessons.
 page.evaluate("navigate('projects')");page.locator('#projectSave').click()
 with page.expect_download() as d:page.locator('#exportBackup').click()
 backup=Path(tmp)/'v3.json';d.value.save_as(backup);value=json.loads(backup.read_text());assert value['appVersion']=='3.0';saved=value['projects'][0]['project'];assert saved['designV3']['plan']['devices'][0]['x']==45;assert saved['notes']=='My earlier V2 learning notes';assert saved['designV2']['sizingNotes']=='Keep my V2 load and rod review'
 page.wait_for_function("JSON.parse(localStorage.getItem('automation-academy-v3')).draft?.project.designV3.learning.requirements.level===3")
 assert not errors,errors;ctx.close()
 ctx=launch();page=ctx.pages[0];page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept());page.goto(URL3)
 assert page.locator('#notes').input_value()=='My earlier V2 learning notes';assert page.evaluate('v3.plan.devices[0].x')==45;assert page.evaluate('v3.learning.requirements.level')==3;assert page.evaluate('v3.standards["machine-electrical"].applicability')=='applicable';assert 'outstanding coordination' in page.locator('#v3DesignNotes').input_value();assert page.evaluate('v3.faultAnswers["clamp:clamp"]').startswith('Compare actual clamp')
 # Clean-store import restores the whole plan without claiming review currency.
 page.evaluate("localStorage.removeItem('automation-academy-v3')");page.reload();page.evaluate("navigate('projects')");page.locator('#importBackup').set_input_files(backup);page.wait_for_function('project.designV3?.learning.requirements.level===3');assert page.evaluate('v3.plan.devices[0].x')==45
 bad=json.loads(backup.read_text());bad['projects'][0]['project']['designV3']['plan']['spec']['width']=0
 page.evaluate("navigate('projects')");page.locator('#importBackup').set_input_files({'name':'bad-v3.json','mimeType':'application/json','buffer':json.dumps(bad).encode()});page.wait_for_function("document.getElementById('toast').textContent.includes('Import failed')");assert page.evaluate('v3.plan.spec.width')==800
 for width in [360,412,768,1500]:
  page.set_viewport_size({'width':width,'height':950})
  for tab in ['dashboard','paneldesign','standards','growth','panels','plc','circuits']:
   page.evaluate('(t)=>navigate(t)',tab);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,tab,'overflow')
 assert not errors,errors;assert not [r for r in requests if r not in [URL2,URL3]],requests;ctx.close()
 print('PASS: V2→V3 offline migration, three integrated packages, pointer/numeric layout, data references, evidence attribution/staleness, SA context, development path, escaped report, restart/backups, invalid import rejection and phone layouts; no external resources/JS errors')
