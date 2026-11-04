/* V3 checks cover entered geometry and evidence completeness, never conformity. */
(function(root){
const statuses=['not-started','needs-work','evidence-recorded','not-applicable'];
function validatePlan(plan){
 if(!plan||typeof plan!=='object'||!plan.spec||!Array.isArray(plan.devices)||plan.devices.length>60)throw Error('Use a panel specification and at most 60 devices.');
 const s=plan.spec;for(const k of ['width','height','depth'])if(!Number.isFinite(s[k])||s[k]<100||s[k]>5000)throw Error('Available width/height/depth must be 100–5000 mm.');
 if(!Number.isFinite(s.wiringDepth)||s.wiringDepth<0||s.wiringDepth>1000)throw Error('Enter a valid additional wiring-depth allowance.');
 const ids=new Set();for(const d of plan.devices){
  if(!d||typeof d.id!=='string'||! /^[A-Za-z][A-Za-z0-9_.-]{0,39}$/.test(d.id)||ids.has(d.id)||typeof d.label!=='string'||d.label.length>120)throw Error('Device IDs must be unique with valid labels.');ids.add(d.id);
  for(const k of ['x','y','width','height','depth','clearance','dcWatts','heat'])if(!Number.isFinite(d[k])||d[k]<0||d[k]>10000)throw Error('Device dimensions, location and loads must be finite nonnegative values.');
  if(d.rotation!==undefined&&![0,90,180,270].includes(d.rotation))throw Error('Invalid device orientation.');
  if(d.width<5||d.height<5||d.depth<1)throw Error('Enter positive physical dimensions for each device.');
 }
 return plan;
}
function checkPlan(plan){
 validatePlan(plan);const findings=[];const s=plan.spec;
 for(const d of plan.devices){
  if(d.x-d.clearance<0||d.y-d.clearance<0||d.x+d.width+d.clearance>s.width||d.y+d.height+d.clearance>s.height)findings.push({type:'boundary',ids:[d.id],message:d.id+': device/entered clearance extends outside available backplate.'});
  if(d.depth+s.wiringDepth>s.depth)findings.push({type:'depth',ids:[d.id],message:d.id+': device depth plus entered wiring allowance exceeds available depth.'});
  if(!(d.sourceVerified===true&&typeof d.source==='string'&&d.source.trim().length>=8))findings.push({type:'data',ids:[d.id],message:d.id+': dimensions/losses/clearance need a datasheet reference and review.'});
 }
 for(let i=0;i<plan.devices.length;i++)for(let j=i+1;j<plan.devices.length;j++){
  const a=plan.devices[i],b=plan.devices[j];
  if(a.x-a.clearance<b.x+b.width+b.clearance&&a.x+a.width+a.clearance>b.x-b.clearance&&a.y-a.clearance<b.y+b.height+b.clearance&&a.y+a.height+a.clearance>b.y-b.clearance)findings.push({type:'overlap',ids:[a.id,b.id],message:a.id+' / '+b.id+': physical rectangles or their reserved clearance areas overlap.'});
 }
 return {findings,geometryIssues:findings.filter(f=>f.type!=='data').length,unverifiedDevices:findings.filter(f=>f.type==='data').length,dcWatts:plan.devices.reduce((a,d)=>a+d.dcWatts,0),heat:plan.devices.reduce((a,d)=>a+d.heat,0)};
}
function evidenceSummary(checks,records,currentRevision){
 let recorded=0,excluded=0;const open=[];
 for(const c of checks){const r=records?.[c.id]||{},status=statuses.includes(r.status)?r.status:'not-started';
  const explanation=typeof r.evidence==='string'&&r.evidence.trim().length>=12;
  const owner=typeof r.reviewer==='string'&&r.reviewer.trim().length>=2;const current=currentRevision===undefined||r.revision===currentRevision;
  if(status==='evidence-recorded'&&explanation&&owner&&current)recorded++;
  else if(status==='not-applicable'&&explanation&&owner&&current)excluded++;
  else open.push(c.id);
 }
 return {recorded,excluded,open,total:checks.length,label:'Evidence inventory only — compliance and safety performance not assessed'};
}
function standardsSummary(refs,records){const open=[];for(const r of refs){const a=records?.[r.id];if(!a||a.applicability==='undetermined'||!['applicable','not-applicable'].includes(a.applicability)||typeof a.source!=='string'||a.source.trim().length<8||typeof a.rationale!=='string'||a.rationale.trim().length<12||(a.applicability==='applicable'&&(typeof a.edition!=='string'||a.edition.trim().length<3)))open.push(r.id);}return {entered:refs.length-open.length,open,label:'User-entered scope records, not verified editions or conformity'};}
function nextPractice(skills,records){
 const complete=id=>{const r=records?.[id];return r&&Number.isInteger(r.level)&&r.level>=3&&typeof r.evidence==='string'&&r.evidence.trim().length>=20};
 const candidates=skills.filter(s=>!complete(s.id)&&s.requires.every(complete));
 return candidates[0]?.id||skills.find(s=>!complete(s.id))?.id||null;
}
function validateDesign(value){
 if(!value||typeof value!=='object')throw Error('Invalid V3 design.');
 validatePlan(value.plan);
 if(!Number.isInteger(value.revision)||value.revision<1)throw Error('Invalid panel draft revision.');
 for(const key of ['reviews','learning','faultAnswers','standards'])if(value[key]!==undefined&&(!value[key]||typeof value[key]!=='object'||Array.isArray(value[key])))throw Error('Invalid V3 record collection.');
 if(value.standards)for(const a of Object.values(value.standards))if(!a||!['undetermined','applicable','not-applicable'].includes(a.applicability)||typeof a.edition!=='string'||typeof a.source!=='string'||typeof a.rationale!=='string')throw Error('Invalid standard applicability record.');
 if(value.reviews)for(const r of Object.values(value.reviews))if(!r||!statuses.includes(r.status)||typeof r.evidence!=='string'||typeof r.reviewer!=='string')throw Error('Invalid review evidence.');
 if(value.learning)for(const r of Object.values(value.learning))if(!r||!Number.isInteger(r.level)||r.level<0||r.level>4||typeof r.evidence!=='string'||typeof r.feedback!=='string')throw Error('Invalid learning record.');
 for(const k of ['risk','editionNotes','designNotes'])if(value[k]!==undefined&&typeof value[k]!=='string')throw Error('Invalid V3 notes.');
 return value;
}
const api={validatePlan,checkPlan,evidenceSummary,standardsSummary,nextPractice,validateDesign,statuses};if(typeof module!=='undefined')module.exports=api;else root.PanelDesign=api;
})(globalThis);
