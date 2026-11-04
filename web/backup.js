function restoreWorkspace(name,data){
 running=false;project=JSON.parse(JSON.stringify(data));project.completed??=[];project.products??=[];project.wires??=[];
 $('projectName').value=name;$('notes').value=project.notes||'';
 for(const[k,v]of Object.entries(project.calculator||{}))if($(k))$(k).value=v;
 position=0;coil=false;portStart=null;selected=null;$('coil').checked=false;
 render();renderLessons();renderProducts();force();if(window.loadAdvanced)loadAdvanced();$('comparison').replaceChildren();navigate('studio');
}
function validateBackup(value){
 if(!value||value.format!=='automation-academy-backup'||value.version!==1||!Array.isArray(value.projects)||value.projects.length>100)throw Error('Select a Version 1 Automation Academy backup (maximum 100 projects).');
 const names=new Set();
 for(const p of value.projects){
  if(!p||typeof p.name!=='string'||!p.name.trim()||p.name.length>100||names.has(p.name))throw Error('Backup contains invalid or duplicate project names.');names.add(p.name);
  const d=p.project;if(!d||!Array.isArray(d.nodes)||!Array.isArray(d.wires)||d.nodes.length>100||d.wires.length>200)throw Error('Invalid circuit in backup.');
  const nodes=new Map();for(const n of d.nodes){if(!n||typeof n.id!=='string'||!n.id||n.id.includes(':')||nodes.has(n.id)||!Object.hasOwn(ports,n.kind)||!Number.isFinite(n.x)||!Number.isFinite(n.y))throw Error('Invalid circuit component.');nodes.set(n.id,n);}
  for(const w of d.wires){if(!Array.isArray(w)||w.length!==2)throw Error('Invalid hose.');for(const end of w){if(typeof end!=='string')throw Error('Invalid port.');const[id,port]=end.split(':');if(!nodes.has(id)||!Object.hasOwn(ports[nodes.get(id).kind],port))throw Error('Unknown circuit port.');}}
  if(d.completed!==undefined&&(!Array.isArray(d.completed)||!d.completed.every(i=>Number.isInteger(i)&&i>=0&&i<5)))throw Error('Invalid foundation progress.');
  if(d.products!==undefined&&(!Array.isArray(d.products)||d.products.length>2))throw Error('Invalid product evidence.');
  if(d.advancedCompleted!==undefined&&(!Array.isArray(d.advancedCompleted)||!d.advancedCompleted.every(i=>typeof i==='string')))throw Error('Invalid advanced progress.');
  if(d.designV3&&window.PanelDesign)PanelDesign.validateDesign(d.designV3);
  if(d.plc){if(!Array.isArray(d.plc.program)||d.plc.program.length<1||d.plc.program.length>16)throw Error('Invalid PLC program.');for(const r of d.plc.program)if(!r||typeof r.tag!=='string'||typeof r.expression!=='string'||r.expression.length>1500||!['COIL','SET','RESET','TON'].includes(r.action)||!Number.isFinite(Number(r.preset)))throw Error('Invalid PLC rung.');}
 }
 return value.projects;
}
function downloadData(name,body,type){const url=URL.createObjectURL(new Blob([body],{type}));const a=document.createElement('a');a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),10000);}
$('exportBackup').onclick=async()=>{
 try{let saved=[];let warning='';try{saved=(await api('projects')).projects}catch(e){warning=' Only the current workspace was included.';}
 const name=$('projectName').value.trim()||'My workspace',current=JSON.parse(JSON.stringify(collect()));
 const projects=saved.filter(p=>p.name!==name);projects.push({name,project:current});
 const backup={format:'automation-academy-backup',version:1,appVersion:window.AppEdition?.version||'server',exportedAt:new Date().toISOString(),profile:window.StandaloneStore?StandaloneStore.profile():undefined,projects,current:name};
 downloadData('automation-academy-backup.json',JSON.stringify(backup,null,2),'application/json');toast('Backup downloaded.'+warning);
 }catch(e){toast('Export failed: '+e.message)}
};
$('importBackup').onchange=async e=>{
 const file=e.target.files[0];if(!file)return;
 try{if(file.size>20*1024*1024)throw Error('Backup must be under 20 MB.');const value=JSON.parse(await file.text()),projects=validateBackup(value);
 if(!confirm(`Import ${projects.length} projects? Saved projects with the same names will be replaced. Export a backup first if you want to keep both versions.`))return;
 if(window.StandaloneStore)StandaloneStore.merge(projects,typeof value.profile==='string'?value.profile.slice(0,100):undefined);
 else{let count=0;try{for(const p of projects){await api('projects',p);count++;}}catch(err){throw Error(`${count} projects imported before the server error: ${err.message}`)}}
 const current=projects.find(p=>p.name===value.current)||projects[0];if(current)restoreWorkspace(current.name,current.project);
 toast('Backup imported. Projects and notes are available in Open saved project.');
 }catch(err){toast('Import failed: '+err.message)}finally{e.target.value='';}
};
if(window.StandaloneStore){
 $('renameProfile').onclick=()=>{try{StandaloneStore.rename($('localName').value);refreshProfile();toast('Local profile saved.')}catch(e){toast(e.message)}};
 $('localName').value=StandaloneStore.profile();
 const draft=StandaloneStore.draft();if(draft){try{validateBackup({format:'automation-academy-backup',version:1,projects:[draft]});restoreWorkspace(draft.name,draft.project);toast('Your last local workspace was restored.')}catch(e){toast('Last workspace could not be restored. Import a backup to recover it.')}}
 let lastDraft='';const saveDraft=()=>{try{const draft={name:$('projectName').value.trim()||'My workspace',project:collect()},json=JSON.stringify(draft);if(json!==lastDraft){StandaloneStore.saveDraft(draft);lastDraft=json;$('draftStatus').textContent='Workspace autosaved in this browser · '+new Date().toLocaleTimeString();}}catch(e){$('draftStatus').textContent=e.message;}};
 setInterval(saveDraft,1500);window.addEventListener('pagehide',saveDraft);
}
