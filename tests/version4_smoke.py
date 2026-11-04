"""Broad circuit/easy-panel workflows using exact offline bundles. File URLs are policy-blocked here."""
from pathlib import Path
import tempfile,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
URL3='http://127.0.0.1:18186/Automation-Academy-V3.html';URL4='http://127.0.0.1:18186/Automation-Academy-V4.html'
H3=(ROOT/'Automation-Academy-V3.html').read_text();H4=(ROOT/'Automation-Academy-V4.html').read_text()
assert '<script src=' not in H4
with tempfile.TemporaryDirectory() as tmp,sync_playwright() as p:
 def launch():
  c=p.chromium.launch_persistent_context(str(Path(tmp)/'profile'),executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'],viewport={'width':1600,'height':1100},accept_downloads=True);c.set_offline(True);c.route(URL3,lambda r:r.fulfill(status=200,content_type='text/html',body=H3));c.route(URL4,lambda r:r.fulfill(status=200,content_type='text/html',body=H4));return c
 c=launch();page=c.pages[0];errors=[];requests=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url));page.on('dialog',lambda d:d.accept())
 page.goto(URL3);page.evaluate("navigate('learn')");page.locator('#notes').fill('Earlier lessons remain intact');page.evaluate("navigate('paneldesign')");page.locator('#v3DesignNotes').fill('Keep the V3 engineering review basis');page.evaluate("navigate('projects')");page.locator('#mobileProjectName').fill('My broad circuit and panel')
 with page.expect_download() as d:page.locator('#exportBackup').click()
 old=Path(tmp)/'v3.json';d.value.save_as(old)
 page.goto(URL4);assert 'Version 4' in page.title();page.evaluate("navigate('projects')");page.locator('#importBackup').set_input_files(old);page.wait_for_function("project.notes==='Earlier lessons remain intact'");assert page.locator('#v3DesignNotes').input_value()=='Keep the V3 engineering review basis'
 page.evaluate("navigate('studio')");assert page.locator('#studioParts button').count()>=40
 page.locator('#studioStarter').select_option('prepared');page.locator('#loadStudioStarter').click();assert page.evaluate('project.nodes.length')==8
 for _ in range(5):page.locator('#step').click()
 assert page.evaluate('b4Positions.c')>0
 before=page.evaluate('b4Positions.c');page.locator('#coil').check();page.locator('#step').click();assert page.evaluate('b4Positions.c')<before
 # All seven starter families, including clearly non-simulated drawing modes.
 for starter in ['basic','prepared','spring','two','oil','relay','electropneumatic']:
  page.locator('#studioStarter').select_option(starter);page.locator('#loadStudioStarter').click()
  assert page.evaluate('CircuitBuilder.inspect(project).errors.length')==0
  assert page.locator('#play').is_disabled()==(starter in ['oil','relay','electropneumatic'])
 page.locator('#studioStarter').select_option('two');page.locator('#loadStudioStarter').click()
 page.locator('#studioPartSelect').select_option('v1');page.locator('#coil').check();assert page.evaluate('CircuitBuilder.airState(project,b4Controls).cylinders.map(c=>c.target)')==[0,1]
 page.locator('#studioPartSelect').select_option('v2');assert not page.locator('#coil').is_checked()
 page.locator('#studioSearch').fill('5/3');page.locator('#studioParts [data-kind="air-v53"]').click();assert page.locator('#coil').is_disabled();page.locator('#studioUndo').click()
 # Build a spring-cylinder circuit from the toolbox and actual dot clicks.
 page.locator('#clear').click()
 for query,kind in [('3/2','air-v32'),('single-acting','air-single'),('compressed-air','supply')]:
  page.locator('#studioSearch').fill(query);page.locator(f'#studioParts [data-kind="{kind}"]').click()
 assert page.evaluate('project.nodes.length')==3
 for a,b in [('part3:out','part1:1'),('part1:2','part2:A')]:
  page.locator(f'#canvas [data-port="{a}"]').click();page.locator(f'#canvas [data-port="{b}"]').click()
 assert page.evaluate('project.wires.length')==2
 page.locator('#coil').check();page.locator('#step').click();assert page.evaluate('b4Positions.part2')>0
 page.locator('#studioUndo').click();assert page.evaluate('project.wires.length')==1
 page.locator('#studioRedo').click();assert page.evaluate('project.wires.length')==2
 page.locator('#canvas [data-part="part2"]').click();page.locator('#studioRotate').click();assert page.evaluate('project.nodes.find(n=>n.id==="part2").angle')==90
 page.locator('#studioDuplicate').click();assert page.evaluate('project.nodes.length')==4;page.locator('#studioUndo').click();assert page.evaluate('project.nodes.length')==3
 with page.expect_download() as d:page.locator('#studioExportSvg').click()
 circuit_svg=Path(tmp)/'circuit.svg';d.value.save_as(circuit_svg);assert 'http://www.w3.org/2000/svg' in circuit_svg.read_text() and '<script' not in circuit_svg.read_text()
 # Easy panel: select/illustrate parts, blank starter, wire matching functions, rotate and undo.
 page.evaluate("navigate('assembly')");assert page.locator('#easyPanelParts button').count()>=14
 page.locator('#easyPowerLinks').click();assert page.evaluate('b4PanelWires.length')>0;assert page.evaluate('PanelAssembly.inspect(v3.plan,b4PanelWires,PanelFunctionPorts).length')==0
 page.locator('#easyUndo').click();assert page.evaluate('b4PanelWires.length')==0
 page.locator('#easyPanelStarter').select_option('blank');page.locator('#easyLoadPanel').click();assert page.evaluate('v3.plan.devices.length')==0
 for query,kind in [('supply','psu'),('PLC','plc')]:
  page.locator('#easyPanelSearch').fill(query);page.locator(f'#easyPanelParts [data-type="{kind}"]').click()
 assert page.evaluate('v3.plan.devices.length')==2
 page.locator('#easyPanelSelect').select_option('D1');page.locator('[data-easy-port="D1:+24"]').click();page.locator('#easyPanelSelect').select_option('D2');page.locator('[data-easy-port="D2:+24"]').click();assert page.evaluate('b4PanelWires.length')==1
 page.locator('#easyPanelSelect').select_option('D1');page.locator('[data-easy-port="D1:0V"]').click();page.locator('#easyPanelSelect').select_option('D2');page.locator('[data-easy-port="D2:+24"]').click();assert page.evaluate('b4PanelWires.length')==1;assert 'do not match' in page.locator('#toast').inner_text()
 page.evaluate('b4PanelPending=null;b4RenderPanel()')
 dims=page.evaluate('[v3.plan.devices[1].width,v3.plan.devices[1].height]');page.locator('#easyRotate').click();assert page.evaluate('[v3.plan.devices[1].width,v3.plan.devices[1].height]')==dims[::-1]
 page.locator('#easyUndo').click();assert page.evaluate('[v3.plan.devices[1].width,v3.plan.devices[1].height]')==dims
 page.locator('#easyPanelNotes').fill('Place the PLC on a row and verify actual terminal data')
 with page.expect_download() as d:page.locator('#easyExportSvg').click()
 panel_svg=Path(tmp)/'panel.svg';d.value.save_as(panel_svg);assert 'http://www.w3.org/2000/svg' in panel_svg.read_text() and '<script' not in panel_svg.read_text()
 # Real pointer drag on an illustrated housing; fit scale maps movement into mm.
 body=page.locator('#easyPanelCanvas [data-panel-device="D2"] rect').first;body.scroll_into_view_if_needed();r=body.bounding_box();page.mouse.move(r['x']+r['width']*.5,r['y']+r['height']*.5);page.mouse.down();page.mouse.move(r['x']+r['width']*.5+70,r['y']+r['height']*.5-50,steps=4);page.mouse.up();assert page.evaluate('v3.plan.devices[1].x')!=40
 page.evaluate("navigate('paneldesign')");assert page.evaluate('document.querySelector("#v3Canvas [data-device=D2]")!==null')
 page.evaluate("navigate('projects')");page.locator('#projectSave').click()
 with page.expect_download() as d:page.locator('#exportBackup').click()
 backup=Path(tmp)/'v4.json';d.value.save_as(backup);data=json.loads(backup.read_text());assert data['appVersion']=='4.0';saved=data['projects'][0]['project'];assert len(saved['buildV4']['panelWires'])==1;assert saved['notes']=='Earlier lessons remain intact';assert len(saved['nodes'])==3
 page.wait_for_function("JSON.parse(localStorage.getItem('automation-academy-v4')).draft?.project.buildV4.panelWires.length===1")
 assert not errors,errors;c.close()
 c=launch();page=c.pages[0];page.on('pageerror',lambda e:errors.append(str(e)));page.on('dialog',lambda d:d.accept());page.goto(URL4)
 assert page.evaluate('project.nodes.find(n=>n.id==="part2").angle')==90;assert page.evaluate('b4PanelWires.length')==1
 assert page.locator('#easyPanelNotes').input_value().startswith('Place the PLC')
 page.evaluate("localStorage.removeItem('automation-academy-v4')");page.reload();page.evaluate("navigate('projects')");page.locator('#importBackup').set_input_files(backup);page.wait_for_function('project.buildV4?.panelWires.length===1');assert page.evaluate('project.nodes.length')==3
 # Invalid connection references cannot replace the imported project.
 bad=json.loads(backup.read_text());bad['projects'][0]['project']['buildV4']['panelWires']=[['missing:port','D2:+24']]
 page.evaluate("navigate('projects')");page.locator('#importBackup').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':json.dumps(bad).encode()});page.wait_for_function("document.getElementById('toast').textContent.includes('Import failed')");assert page.evaluate('b4PanelWires.length')==1
 for width in [360,412,768,1600]:
  page.set_viewport_size({'width':width,'height':1000})
  for tab in ['dashboard','studio','assembly','paneldesign','standards','projects']:
   page.evaluate('(t)=>navigate(t)',tab);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,tab,'overflow')
 assert not errors,errors;assert not [r for r in requests if r not in [URL3,URL4]],requests;c.close()
 print('PASS: V3→V4 offline migration, seven starters, broad parts, dot connections, air motion, undo/redo/rotation/duplication, easy-panel functions and pointer placement, type rejection, restart/backups and phone layouts; no external resources or JS errors')
