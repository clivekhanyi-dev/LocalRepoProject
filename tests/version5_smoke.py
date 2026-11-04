"""Exact offline bundle; file URLs are blocked by managed Chromium policy."""
from pathlib import Path
import tempfile,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
U4='http://127.0.0.1:18188/v4';U5='http://127.0.0.1:18188/v5'
H4=(ROOT/'Automation-Academy-V4.html').read_text();H5=(ROOT/'Automation-Academy-V5.html').read_text()
assert '<script src=' not in H5
with tempfile.TemporaryDirectory() as tmp,sync_playwright() as p:
 def launch():
  c=p.chromium.launch_persistent_context(str(Path(tmp)/'profile'),executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'],viewport={'width':1600,'height':1100},accept_downloads=True);c.set_offline(True);c.route(U4,lambda r:r.fulfill(content_type='text/html',body=H4));c.route(U5,lambda r:r.fulfill(content_type='text/html',body=H5));return c
 c=launch();page=c.pages[0];errors=[];requests=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url));page.on('dialog',lambda d:d.accept())
 page.goto(U4);page.evaluate("navigate('learn')");page.locator('#notes').fill('Keep earlier learning and notes');page.evaluate("navigate('paneldesign')");page.locator('#v3DesignNotes').fill('Keep SANS review');page.evaluate("navigate('projects')");page.locator('#mobileProjectName').fill('V5 practical build')
 with page.expect_download() as d:page.locator('#exportBackup').click()
 old=Path(tmp)/'v4.json';d.value.save_as(old)
 page.goto(U5);assert 'Version 5' in page.title();assert page.evaluate("(()=>{const ids=[...document.querySelectorAll('[id]')].map(e=>e.id);return ids.filter((id,i)=>ids.indexOf(id)!==i)})()")==[];page.evaluate("navigate('projects')");page.locator('#importBackup').set_input_files(old);page.wait_for_function("project.notes==='Keep earlier learning and notes'");assert page.locator('#v3DesignNotes').input_value()=='Keep SANS review'
 page.evaluate("navigate('practical')");assert page.locator('#v5Canvas').is_visible();assert page.locator('#v5Canvas [data-v5-device]').count()==5
 page.locator('#v5Power').check();page.locator('#v5Start').check();page.locator('#v5Run').click();page.wait_for_function('v5State.positions[0]>.1');page.locator('#v5Run').click();assert page.evaluate('v5State.outputs[0]');page.locator('#v5Start').uncheck();assert not page.evaluate('v5State.outputs[0]')
 # Guide a blank panel, dot and selector connections, trace and undo/redo.
 page.locator('#v5Blank').click();assert page.evaluate('v5Wires.length')==0
 page.locator('[data-v5-port="P:+"]').click();page.locator('[data-v5-port="F:1"]').click();assert page.evaluate('v5Wires.length')==1
 page.locator('#v5Undo').click();assert page.evaluate('v5Wires.length')==0;page.locator('#v5Redo').click();assert page.evaluate('v5Wires.length')==1
 page.locator('#v5From').select_option('P:+');page.locator('#v5To').select_option('P:-');page.locator('#v5Connect').click();assert page.evaluate('v5Wires.length')==1
 for _ in range(4):page.locator('#v5Next').click()
 assert page.locator('#v5Next').is_disabled();assert page.evaluate('PracticalLab.check(PracticalLab.models.direct,v5Wires).length')==0
 page.locator('#v5Trace').select_option('3');assert 'Start' in page.locator('#v5Trace').input_value() or page.evaluate('v5Trace')==3
 # Real missing return prevents coil current, while replacement restores it.
 page.locator('#v5Power').check();page.locator('#v5Start').check();assert page.evaluate('v5State.outputs[0]')
 page.get_by_text('Connection schedule — every wire explained',exact=True).click();page.locator('[data-remove-v5="4"]').click();page.locator('#v5Power').check();page.locator('#v5Start').check();assert not page.evaluate('v5State.outputs[0]');page.locator('#v5Next').click()
 # Relay seal-in and drop-out through actual UI.
 page.locator('#v5Model').select_option('relay');page.locator('#v5Load').click();page.locator('#v5Power').check();page.locator('#v5Start').check();page.locator('#v5Start').uncheck();assert page.evaluate('v5State.relay');page.locator('#v5Stop').check();assert not page.evaluate('v5State.relay')
 # Two-station sequence and air-loss timeout, deterministic steps instead of waiting 10 seconds.
 page.locator('#v5Model').select_option('plc');page.locator('#v5Load').click();page.locator('#v5Power').check();page.locator('#v5Start').check();assert page.evaluate('v5State.stage')=='A+';page.locator('#v5Start').uncheck()
 stages=page.evaluate("(()=>{const stages=new Set();for(let i=0;i<120;i++){v5Step();stages.add(v5State.stage);}return [...stages]})()");assert stages==['A+','B+','B-','A-','idle'],stages
 page.locator('#v5Air').uncheck();page.locator('#v5Start').check();page.locator('#v5Start').uncheck();page.evaluate('for(let i=0;i<110;i++)v5Step()');assert 'timeout' in page.locator('#v5Status').inner_text();page.locator('#v5Reset').click();assert page.evaluate('v5State.fault')==''
 page.locator('#v5Notes').fill('Checked two-station wiring and fault timeout')
 with page.expect_download() as d:page.locator('#v5Export').click()
 report=Path(tmp)/'guide.txt';d.value.save_as(report);assert 'Q0 -> Y1:A1' in report.read_text()
 # Site unknown bore is not converted from outside diameter; worked dimensions and portable RFQ.
 page.evaluate("navigate('practicalsize')");assert 'UNKNOWN' in page.locator('#v5CylinderResult').inner_text();page.locator('#v5Barrel').fill('65');assert 'UNKNOWN' in page.locator('#v5CylinderResult').inner_text();page.locator('#v5MeasureExample').click();assert '200.0' in page.locator('#v5CylinderResult').inner_text();page.locator('#v5Tag').fill('Customer clamp A');page.locator('#v5CopyMeasures').click();assert page.locator('#v5TubeBore').input_value()=='50';assert page.locator('#v5TubeResult table tbody tr').count()==6
 page.locator('#v5Stations').fill('2');assert '329.9' in page.locator('#v5TubeResult').inner_text();page.locator('#v5DcVolts').fill('12');assert 'DOES NOT match' in page.locator('#v5ValveResult').inner_text();page.locator('#v5DcVolts').fill('24');page.locator('#v5ValveSource').fill('Customer datasheet pending verification')
 with page.expect_download() as d:page.locator('#v5Rfq').click()
 rfq=Path(tmp)/'rfq.txt';d.value.save_as(rfq);assert 'Customer clamp A' in rfq.read_text();assert '200.0' in rfq.read_text()
 page.locator('#v5Extended').fill('30');assert 'Enter valid' in page.locator('#v5CylinderResult').inner_text();page.locator('#v5Extended').fill('240')
 # New parts can be added in Circuit Builder and saved without breaking import validation.
 page.evaluate("navigate('studio')");assert page.locator('#studioParts button').count()==55
 for kind in ['pneumatic-terminal','hydraulic-terminal','solenoid-coil','indicator-lamp','flyback-diode','air-meter-out','air-quick-exhaust']:
  page.locator(f'#studioParts [data-kind="{kind}"]').click()
 assert page.locator('#play').is_disabled()
 page.evaluate("navigate('assembly')");page.locator('#easyParts [data-type="hydraulicbank"]').click() if page.locator('#easyParts').count() else page.locator('[data-type="hydraulicbank"]').click()
 assert page.evaluate("v3.plan.devices.some(d=>d.type==='hydraulicbank')")
 assert page.evaluate('PracticalLab.validate(collect().practicalV5).model')=='plc'
 page.evaluate("navigate('projects')");page.locator('#mobileProjectName').fill('V5 practical build')
 with page.expect_download() as d:page.locator('#exportBackup').click()
 backup=Path(tmp)/'v5.json';d.value.save_as(backup);data=json.loads(backup.read_text());assert data['appVersion']=='5.0';assert data['projects'][-1]['project']['practicalV5']['notes'].startswith('Checked')
 for width in [360,412,768,1600]:
  page.set_viewport_size({'width':width,'height':1000})
  for tab in ['dashboard','practical','practicalsize','studio','assembly']:
   page.evaluate('tab=>navigate(tab)',tab);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),(width,tab)
 page.set_viewport_size({'width':1600,'height':1100});page.evaluate("navigate('practical')");page.screenshot(path='/tmp/v5-panel.png',full_page=True)
 page.wait_for_timeout(1700);assert not errors,errors;c.close()
 c=launch();page=c.pages[0];page.on('dialog',lambda d:d.accept());page.on('pageerror',lambda e:errors.append(str(e)));page.goto(U5);page.wait_for_function("v5Model==='plc'");assert page.locator('#v5Notes').input_value().startswith('Checked');assert page.locator('#v5Tag').input_value()=='Customer clamp A';assert page.evaluate('v5State.power') is False;assert page.evaluate('v5State.outputs')==[False,False]
 page.evaluate('localStorage.clear()');page.reload();page.evaluate("navigate('projects')");page.locator('#importBackup').set_input_files(backup);page.wait_for_function("v5Model==='plc'");assert page.locator('#v5Tag').input_value()=='Customer clamp A'
 bad=json.loads(backup.read_text());bad['projects'][-1]['project']['practicalV5']['wires'].append(['P:+','P:-']);badfile=Path(tmp)/'bad.json';badfile.write_text(json.dumps(bad));page.evaluate("navigate('projects')");page.locator('#importBackup').set_input_files(badfile);page.wait_for_function("document.querySelector('#toast').textContent.includes('Import failed')");assert page.evaluate('v5Model')=='plc';assert not errors,errors;assert not [u for u in requests if u not in [U4,U5]],requests
 c.close();print('PASS: V4→V5 migration, actual guided wiring/trace/history, direct/relay/PLC simulation and faults, site measurements/tubing/RFQ, new parts, persistence/backup rejection and responsive layouts; no JS errors or external resources')
