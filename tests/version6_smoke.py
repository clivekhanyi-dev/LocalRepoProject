"""Exact offline V5/V6 bytes; managed Chromium does not allow file URLs."""
from pathlib import Path
import tempfile,json,base64
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];U5='http://127.0.0.1:18191/v5';U6='http://127.0.0.1:18191/v6'
H5=(ROOT/'Automation-Academy-V5.html').read_text();H6=(ROOT/'Automation-Academy-V6.html').read_text();assert '<script src=' not in H6
with tempfile.TemporaryDirectory() as tmp,sync_playwright() as p:
 def launch():
  c=p.chromium.launch_persistent_context(str(Path(tmp)/'profile'),executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'],viewport={'width':1600,'height':1100},accept_downloads=True);c.set_offline(True);c.route(U5,lambda r:r.fulfill(content_type='text/html',body=H5));c.route(U6,lambda r:r.fulfill(content_type='text/html',body=H6));return c
 c=launch();page=c.pages[0];errors=[];requests=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url));page.on('dialog',lambda d:d.accept())
 page.goto(U5);page.evaluate("navigate('learn')");page.locator('#notes').fill('V5 notes remain');page.evaluate("navigate('practical')");page.locator('#v5Notes').fill('Earlier wiring observations');page.evaluate("navigate('projects')");page.locator('#mobileProjectName').fill('V6 practical engineering')
 with page.expect_download() as d:page.locator('#exportBackup').click()
 old=Path(tmp)/'v5.json';d.value.save_as(old)
 page.goto(U6);assert 'Version 6' in page.title();assert page.evaluate("(()=>{const ids=[...document.querySelectorAll('[id]')].map(e=>e.id);return ids.filter((id,i)=>ids.indexOf(id)!==i)})()")==[]
 page.evaluate("navigate('projects')");page.locator('#importBackup').set_input_files(old);page.wait_for_function("project.notes==='V5 notes remain'");assert page.locator('#v5Notes').input_value()=='Earlier wiring observations'
 page.evaluate("navigate('practical');v6Practice.open=true;v6Meter.open=true");page.locator('#v6StartChallenge').click();page.locator('#v6Grade').click();assert 'Missing' in page.locator('#v6PracticeResult').inner_text()
 for _ in range(5):page.locator('#v5Next').click()
 page.locator('#v6Grade').click();assert '6 / 6' in page.locator('#v6PracticeResult').inner_text();assert page.evaluate("!!v6Progress['challenge:direct']");page.locator('#v5Undo').click();assert 'changed since' in page.locator('#v6PracticeResult').inner_text();page.locator('#v5Redo').click();page.locator('#v6Grade').click()
 # Live voltage, sign reversal and resistance interlock via actual controls.
 page.locator('#v5Power').check();page.locator('#v5Start').check();page.locator('#v6Red').select_option('Y1:A1');page.locator('#v6Black').select_option('P:-');page.locator('#v6Measure').click();assert '24.00 V' in page.locator('#v6MeterResult').inner_text()
 page.locator('#v6MeterMode').select_option('resistance');page.locator('#v6Measure').click();assert 'power OFF' in page.locator('#v6MeterResult').inner_text();page.locator('#v5Power').uncheck();page.locator('#v6Black').select_option('Y1:A2');page.locator('#v6Measure').click();assert '240.00 Ω' in page.locator('#v6MeterResult').inner_text()
 # Missing-return case: both coil terminals read positive to 0 V, voltage across coil is zero.
 page.locator('#v6Case').select_option('return');page.locator('#v6LoadCase').click();page.locator('#v5Start').check();page.locator('#v6MeterMode').select_option('voltage');page.locator('#v6Red').select_option('Y1:A2');page.locator('#v6Black').select_option('P:-');page.locator('#v6Measure').click();assert '24.00 V' in page.locator('#v6MeterResult').inner_text();page.locator('#v6Diagnosis').select_option('return');page.locator('#v6SubmitDiagnosis').click();assert 'Correct' in page.locator('#v6PracticeResult').inner_text()
 page.locator('#v6Case').select_option('coil');page.locator('#v6LoadCase').click();page.locator('#v5Power').uncheck();page.locator('#v6MeterMode').select_option('resistance');page.locator('#v6Red').select_option('Y1:A1');page.locator('#v6Black').select_option('Y1:A2');page.locator('#v6Measure').click();assert 'OL' in page.locator('#v6MeterResult').inner_text();page.locator('#v6Diagnosis').select_option('coil');page.locator('#v6SubmitDiagnosis').click();assert 'Correct' in page.locator('#v6PracticeResult').inner_text();page.locator('#v6ExitCase').click();assert page.evaluate('v6Case') is None
 # Fuse voltage-drop and pneumatic-energy cases use the same actual meter/trainer.
 page.locator('#v6Case').select_option('fuse');page.locator('#v6LoadCase').click();page.locator('#v5Start').check();page.locator('#v6MeterMode').select_option('voltage');page.locator('#v6Red').select_option('F:1');page.locator('#v6Black').select_option('F:2');page.locator('#v6Measure').click();assert '24.00 V' in page.locator('#v6MeterResult').inner_text();assert 'OPEN FAULT' not in page.locator('#v5Canvas').text_content();page.locator('#v6Diagnosis').select_option('fuse');page.locator('#v6SubmitDiagnosis').click();assert 'Correct' in page.locator('#v6PracticeResult').inner_text()
 page.locator('#v6Case').select_option('air');page.locator('#v6LoadCase').click();page.locator('#v5Start').check();assert page.evaluate('v5State.outputs[0]') is True;assert page.evaluate('v5State.positions[0]')==0;page.locator('#v6Red').select_option('Y1:A1');page.locator('#v6Black').select_option('Y1:A2');page.locator('#v6Measure').click();assert '24.00 V' in page.locator('#v6MeterResult').inner_text();page.locator('#v6Diagnosis').select_option('air');page.locator('#v6SubmitDiagnosis').click();assert 'Correct' in page.locator('#v6PracticeResult').inner_text();page.locator('#v6ExitCase').click()
 # Three examples remain runnable and challenge checks include relay/PLC behaviour.
 for model in ['relay','plc']:
  page.locator('#v5Model').select_option(model);page.locator('#v5Load').click();page.locator('#v6Grade').click();assert '6 / 6' in page.locator('#v6PracticeResult').inner_text()
 # Motion reacts to opening/load, animates, resets when inputs change.
 page.evaluate("v6Open('motion')");normal=page.evaluate('v6MotionCalc().time');page.locator('#v6Opening').fill('.25');assert page.evaluate('v6MotionCalc().time')>normal;page.locator('#v6RunMotion').click();page.wait_for_function('v6Position>0');page.locator('#v6ResetMotion').click();assert page.evaluate('v6Position')==0;page.locator('#v6StallExample').click();assert 'STALLED' in page.locator('#v6MotionResult').inner_text();page.locator('#v6NormalExample').click();assert 'Estimate:' in page.locator('#v6MotionResult').inner_text();page.locator('#v6Opening').fill('0');assert 'fully closed' in page.locator('#v6MotionResult').inner_text();page.locator('#v6NormalExample').click();page.locator('#v6Direction').select_option('retract');assert page.evaluate("v6Piston.style.transform")=='translateX(250%)';page.locator('#v6Direction').select_option('extend')
 # Configurable functions, spares, zones and unique output schedule.
 page.evaluate("v6Open('terminal')");page.locator('#v6StationCount').fill('5');page.locator('#v6ApplyStations').click();page.locator('[data-v6-station="2"]').select_option('53');page.locator('[data-v6-zone="2"]').select_option('2');assert page.evaluate('v6Stations[1].zone')==2
 with page.expect_download() as d:page.locator('#v6ExportTerminal').click()
 schedule=Path(tmp)/'terminal.txt';d.value.save_as(schedule);assert 'Centre function is unspecified' in schedule.read_text();assert 'zone 2' in schedule.read_text()
 # Photos resize locally; survey report escapes authored text and includes the actual JPEG.
 page.evaluate("v6Open('survey')");page.locator('#v6Site').fill('Customer line <script>unsafe()</script>');page.locator('#v6Nameplate').fill('24 V DC · photo reference pending');page.locator('#v6Unknowns').fill('Confirm mounting pin and bore drawing')
 photo=page.evaluate("(()=>{const c=document.createElement('canvas');c.width=400;c.height=160;const x=c.getContext('2d');x.fillStyle='white';x.fillRect(0,0,400,160);x.fillStyle='black';x.font='28px Arial';x.fillText('TRAINING LABEL 24 V',20,70);return c.toDataURL('image/png').split(',')[1]})()")
 page.locator('#v6PhotoInput').set_input_files({'name':'training-label.png','mimeType':'image/png','buffer':base64.b64decode(photo)});page.wait_for_function('v6Photos.length===1');assert page.locator('.v6-photos img').count()==1
 with page.expect_download() as d:page.locator('#v6ExportSurvey').click()
 survey=Path(tmp)/'survey.html';d.value.save_as(survey);body=survey.read_text();assert '<script>' not in body and '&lt;script&gt;' in body and 'data:image/jpeg;base64,' in body
 # Reopen generated report as offline bytes to verify embedded photo and escaping.
 reportURL='http://127.0.0.1:18191/report';c.route(reportURL,lambda r:r.fulfill(content_type='text/html',body=body));report=c.new_page();report.goto(reportURL);assert report.locator('img').evaluate('(i)=>i.complete&&i.naturalWidth>0');report.close()
 page.evaluate("v6Open('projects')");page.locator('.v6-project summary').first.click();page.locator('[data-v6-evidence="reject:0"]').fill('Requirement, boundaries and energy hazards recorded')
 with page.expect_download() as d:page.locator('#v6ExportPortfolio').click()
 portfolio=Path(tmp)/'portfolio.txt';d.value.save_as(portfolio);assert 'energy hazards recorded' in portfolio.read_text()
 page.evaluate("v6Open('evidence')");page.locator('#v6FestoCode').fill('Exact model pending');page.locator('#v6SourceCheck').click();assert 'not independently verified' in page.locator('#v6SourceStatus').inner_text()
 page.evaluate("navigate('projects')");page.locator('#mobileProjectName').fill('V6 practical engineering')
 with page.expect_download() as d:page.locator('#exportBackup').click()
 backup=Path(tmp)/'v6.json';d.value.save_as(backup);data=json.loads(backup.read_text());assert data['appVersion']=='6.0';assert data['projects'][-1]['project']['masteryV6']['photos'][0]['name']=='training-label.png'
 for width in [360,412,768,1600]:
  page.set_viewport_size({'width':width,'height':1000})
  for section in ['motion','terminal','survey','projects','evidence']:
   page.evaluate('(s)=>v6Open(s)',section);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,section)
  page.evaluate("navigate('practical')");assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,'practical')
 page.set_viewport_size({'width':1600,'height':1100});page.evaluate("navigate('practical');v6Practice.open=true;v6Meter.open=true");page.screenshot(path='/tmp/v6-final.png',full_page=True);page.wait_for_timeout(1700);assert not errors,errors;c.close()
 c=launch();page=c.pages[0];page.on('dialog',lambda d:d.accept());page.on('pageerror',lambda e:errors.append(str(e)));page.goto(U6);page.wait_for_function('v6Photos.length===1');assert page.evaluate('v5State.power') is False;assert page.evaluate('v6Case') is None;assert page.evaluate('v6MotionRunning') is False;assert page.evaluate("v6Progress['reject:0']").startswith('Requirement');assert page.evaluate('v6Stations.length')==5
 page.evaluate('localStorage.clear()');page.reload();page.evaluate("navigate('projects')");page.locator('#importBackup').set_input_files(backup);page.wait_for_function('v6Photos.length===1');assert page.locator('#v6Unknowns').input_value().startswith('Confirm')
 bad=json.loads(backup.read_text());bad['projects'][-1]['project']['masteryV6']['photos'][0]['data']='data:image/svg+xml,<svg onload="x()">';badpath=Path(tmp)/'bad.json';badpath.write_text(json.dumps(bad));page.evaluate("navigate('projects')");page.locator('#importBackup').set_input_files(badpath);page.wait_for_function("document.querySelector('#toast').textContent.includes('Import failed')");assert page.evaluate('v6Photos.length')==1;assert not errors,errors;assert not [u for u in requests if u not in [U5,U6]],requests
 c.close();print('PASS: V5→V6 migration, actual wiring challenges and meter readings/interlock, diagnostic cases, motion/stall, terminal allocation, resized photo/report, portfolio/evidence, persistence/restart/recovery/rejection and phone layouts; no JS errors or external resources')
