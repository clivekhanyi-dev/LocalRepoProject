const defaultProgram=()=>[
 {tag:'Run',action:'COIL',expression:'StopHealthy AND OverloadHealthy AND (Start OR Run)',preset:0},
 {tag:'T1',action:'TON',expression:'Run',preset:1500},
 {tag:'Motor',action:'COIL',expression:'Run AND T1.Q',preset:0},
 {tag:'Fault',action:'COIL',expression:'NOT StopHealthy OR NOT OverloadHealthy',preset:0}
];
let labProgram=defaultProgram(),labState={tags:{},timers:{},elapsed:0},labRunning=false,labDirty=false;
const inputIds=['hydP','hydQ','hydB','hydR','hydE','motorV','motorP','motorPf','motorE'];
function el(tag,text,parent){const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(parent)parent.append(e);return e;}
function advancedProgress(){const completed=(project.advancedCompleted||[]).filter(id=>AdvancedLessons.some(l=>l.id===id));$('advancedProgress').textContent=`${completed.length} / ${AdvancedLessons.length} advanced modules reviewed`;$('progressCount').textContent=`${project.completed.length} / 5 foundations · ${completed.length} / ${AdvancedLessons.length} advanced`;}
function renderAdvancedLessons(){
 const host=$('advancedLessons');host.replaceChildren();
 for(const lesson of AdvancedLessons.filter(l=>$('lessonTrack').value==='All disciplines'||l.track===$('lessonTrack').value)){
  const d=el('details',undefined,host);d.className='advanced-lesson';el('summary',lesson.track+' · '+lesson.title,d);
  lesson.body.forEach(p=>el('p',p,d));
  const task=el('div',undefined,d);task.className='lesson-assessment';el('strong','Engineering challenge',task);el('p',lesson.challenge,task);
  const label=el('label','Your calculation / reasoning',task),answer=el('textarea',undefined,label);answer.value=project.advancedAnswers?.[lesson.id]||'';answer.oninput=()=>{project.advancedAnswers??={};project.advancedAnswers[lesson.id]=answer.value};
  const solution=el('details',undefined,task);el('summary','Review the worked answer',solution);el('p',lesson.answer,solution);
  const complete=el('label',undefined,d);complete.className='lab-inputs';const check=el('input',undefined,complete);check.type='checkbox';check.checked=(project.advancedCompleted||[]).includes(lesson.id);complete.append(document.createTextNode('I have reviewed the worked answer and can explain the assumptions'));
  check.onchange=()=>{project.advancedCompleted=(project.advancedCompleted||[]).filter(id=>id!==lesson.id);if(check.checked)project.advancedCompleted.push(lesson.id);advancedProgress()};
 }
 advancedProgress();
}
$('lessonTrack').onchange=renderAdvancedLessons;
function renderSymbols(){
 $('symbolLibrary').replaceChildren();const q=$('symbolSearch').value.toLowerCase();
 for(const s of EngineeringSymbols.filter(s=>(s.name+' '+s.domain+' '+s.detail).toLowerCase().includes(q))){const card=el('article',undefined,$('symbolLibrary'));card.className='symbol-card';card.innerHTML=symbolMarkup(s.kind);el('h3',s.name,card);el('small',s.domain+' · '+s.ref,card);el('p',s.detail,card)}
}
$('symbolSearch').oninput=renderSymbols;
function advancedCalculations(){
 const values=inputIds.map(id=>$(id).value.trim()===''?NaN:Number($(id).value));
 const h=Automation.hydraulic(...values.slice(0,5));$('hydResult').textContent=h?`Ideal extension: ${h.force.toFixed(1)} N\nIdeal retraction: ${h.retractForce.toFixed(1)} N\nExtension speed: ${h.extendSpeed.toFixed(1)} mm/s\nRetraction speed: ${h.retractSpeed.toFixed(1)} mm/s\nFluid power: ${h.fluidPower.toFixed(2)} kW\nEstimated shaft input: ${h.inputPower.toFixed(2)} kW`:'Enter valid positive flow and dimensions, pressure ≥ 0, rod < bore, and efficiency in (0, 1].';
 const m=Automation.motor(...values.slice(5));$('motorResult').textContent=m?`Estimated line current: ${m.current.toFixed(2)} A\nElectrical input: ${m.inputPower.toFixed(2)} kW`:'Enter positive voltage/power, and power factor and efficiency in (0, 1].';
}
inputIds.forEach(id=>$(id).oninput=advancedCalculations);
function markDirty(){$('plcError').style.color='#a63f28';labDirty=true;pausePLCLab();$('plcError').textContent='Program edited. Compile to validate and reset runtime before scanning.';}
function renderEditor(){
 $('rungEditor').replaceChildren();labProgram.forEach((r,i)=>{const row=el('div',undefined,$('rungEditor'));row.className='rung-row';
  const remove=el('button','Delete '+(i+1),row);remove.onclick=()=>{labProgram=readProgram();if(labProgram.length===1)return toast('Keep at least one rung.');labProgram.splice(i,1);markDirty();renderEditor()};
  const actionLabel=el('label','Instruction',row),action=el('select',undefined,actionLabel);action.className='rung-action';for(const a of ['COIL','SET','RESET','TON']){const opt=el('option',a,action);opt.value=a}action.value=r.action;
  for(const [name,cls,value]of [['Output / instance','rung-tag',r.tag],['Boolean expression','rung-expression',r.expression],['TON PT (ms)','rung-preset',r.preset]]){const label=el('label',name,row),input=el('input',undefined,label);input.className=cls;input.value=value;input.oninput=markDirty;if(cls==='rung-preset'){input.type='number';input.min=0;input.max=3600000}}
  action.onchange=markDirty;
 });
}
function readProgram(){return [...document.querySelectorAll('.rung-row')].map(r=>({tag:r.querySelector('.rung-tag').value.trim(),action:r.querySelector('.rung-action').value,expression:r.querySelector('.rung-expression').value.trim(),preset:Number(r.querySelector('.rung-preset').value)}))}
function plcInputs(){return {Start:$('plcStart').checked,StopHealthy:$('plcStop').checked,OverloadHealthy:$('plcOverload').checked};}
function compileLab(){
 pausePLCLab();try{const p=readProgram();Automation.compile(p);labProgram=p;labState={tags:{},timers:{},elapsed:0};labDirty=false;$('plcError').style.color='#447a23';$('plcError').textContent='Compiled. Runtime reset; press Single scan or Run scans.';renderLab();return true}catch(e){$('plcError').style.color='#a63f28';labDirty=true;labState={tags:{},timers:{},elapsed:0};$('plcError').textContent=e.message;$('ladder').replaceChildren();$('plcTrace').replaceChildren();$('stCode').textContent='Fix the program and compile before generating Structured Text.';return false}
}
function scanLab(){if(labDirty){pausePLCLab();return toast('Compile the edited program first.')}try{labState=Automation.scan(labProgram,labState,plcInputs(),Number($('scanMs').value));$('plcError').textContent='';renderLab()}catch(e){pausePLCLab();$('plcError').textContent=e.message}}
function pausePLCLab(){labRunning=false;$('runPlc').textContent='Run scans';}
window.pausePLCLab=pausePLCLab;
$('compilePlc').onclick=compileLab;$('scanPlc').onclick=scanLab;$('runPlc').onclick=()=>{if(labDirty)return toast('Compile the edited program first.');labRunning=!labRunning;$('runPlc').textContent=labRunning?'Pause scans':'Run scans'};
setInterval(()=>{if(labRunning)scanLab()},100);
$('addRung').onclick=()=>{labProgram=readProgram();if(labProgram.length>=16)return toast('This lab supports up to 16 rungs.');labProgram.push({tag:'Output'+(labProgram.length+1),action:'COIL',expression:'FALSE',preset:0});markDirty();renderEditor()};
$('resetPlc').onclick=()=>{labProgram=defaultProgram();$('plcStart').checked=false;$('plcStop').checked=true;$('plcOverload').checked=true;renderEditor();compileLab()};
function stProgram(){
 const declarations=['    Start : BOOL;','    StopHealthy : BOOL := TRUE;','    OverloadHealthy : BOOL := TRUE;'],seen=new Set();
 for(const r of labProgram)if(!seen.has(r.tag)){seen.add(r.tag);declarations.push('    '+r.tag+' : '+(r.action==='TON'?'TON':'BOOL')+';')}
 const lines=labProgram.map(r=>r.action==='TON'?`${r.tag}(IN := ${r.expression}, PT := T#${r.preset}ms);`:r.action==='COIL'?`${r.tag} := ${r.expression};`:`IF ${r.expression} THEN ${r.tag} := ${r.action==='SET'?'TRUE':'FALSE'}; END_IF;`);
 return 'PROGRAM PLC_PRG\nVAR\n'+declarations.join('\n')+'\nEND_VAR\n\n(* Implementation; standard TON library and task configuration required. *)\n'+lines.join('\n');
}
function drawLadder(){
 const host=$('ladder');host.replaceChildren();
 const make=(tag,attrs,text)=>{const e=document.createElementNS(NS,tag);for(const[k,v]of Object.entries(attrs))e.setAttribute(k,v);if(text!==undefined)e.textContent=text;host.append(e);return e};
 let tags={Start:false,StopHealthy:true,OverloadHealthy:true,...labState.tags,...plcInputs()};for(const r of labProgram)tags[r.action==='TON'?r.tag+'.Q':r.tag]??=false;
 const sizes=a=>a.op==='and'?{w:sizes(a.a).w+sizes(a.b).w,h:Math.max(sizes(a.a).h,sizes(a.b).h)}:a.op==='or'?{w:Math.max(sizes(a.a).w,sizes(a.b).w)+50,h:sizes(a.a).h+sizes(a.b).h}:a.op==='not'&&a.a.op!=='tag'?{w:sizes(a.a).w+30,h:sizes(a.a).h+24}:{w:140,h:75};
 const wire=(d,on=false)=>make('path',{d,fill:'none',stroke:on?'#538d29':'#50675b','stroke-width':2});
 function draw(a,x,y,w){const size=sizes(a);let on=false;try{on=Automation.evaluate(a,tags)}catch(e){};
  if(a.op==='and'){const wa=sizes(a.a).w;draw(a.a,x,y,wa);draw(a.b,x+wa,y,w-wa);return}
  if(a.op==='or'){const y2=y+sizes(a.a).h;wire(`M${x} ${y}V${y2} M${x+w} ${y}V${y2}`,on);draw(a.a,x+25,y,w-50);draw(a.b,x+25,y2,w-50);wire(`M${x} ${y}h25 M${x+w-25} ${y}h25 M${x} ${y2}h25 M${x+w-25} ${y2}h25`,on);return}
  if(a.op==='not'&&a.a.op!=='tag'){wire(`M${x} ${y}h${w}`);make('rect',{x:x+5,y:y-18,width:w-10,height:36,fill:'#fff',stroke:'#50675b'});make('text',{x:x+12,y:y+5,'font-size':12},'NOT (group)');return}
  const mid=x+w/2;wire(`M${x} ${y}H${mid-12} M${mid-12} ${y-14}V${y+14} M${mid+12} ${y-14}V${y+14} M${mid+12} ${y}H${x+w}`,on);
  if(a.op==='not')wire(`M${mid-18} ${y+19}L${mid+18} ${y-19}`,on);
  make('text',{x:mid,y:y-25,'text-anchor':'middle',fill:on?'#447a23':'#193332'},a.op==='not'?a.a.name:a.name);
 }
 let y=60,maxWidth=760;const parsed=labProgram.map(r=>{try{return Automation.parse(r.expression)}catch(e){return null}});
 maxWidth=Math.max(760,...parsed.filter(Boolean).map(a=>sizes(a).w+240));
 for(let i=0;i<labProgram.length;i++){const r=labProgram[i],a=parsed[i];if(!a)continue;if(labState.trace?.[i]?.before)tags=labState.trace[i].before;const size=sizes(a),width=maxWidth;maxWidth=Math.max(maxWidth,width);make('text',{x:7,y:y-20},String(i+1));wire(`M35 ${y-35}V${y+size.h-20}`);wire(`M35 ${y}H60`);draw(a,60,y,size.w);wire(`M${60+size.w} ${y}H${width-130}`);const powered=labState.trace?.[i]?.value;
  if(r.action==='TON'){make('rect',{x:width-130,y:y-22,width:105,height:44,fill:powered?'#d9edb7':'#fff',stroke:'#50675b'});make('text',{x:width-78,y:y-4,'text-anchor':'middle'},r.tag);make('text',{x:width-78,y:y+13,'text-anchor':'middle'},`TON ${r.preset}ms`);}else{wire(`M${width-130} ${y}H${width-105} M${width-105} ${y-18}Q${width-125} ${y} ${width-105} ${y+18} M${width-55} ${y-18}Q${width-35} ${y} ${width-55} ${y+18} M${width-55} ${y}H${width-25}`,powered);make('text',{x:width-80,y:y-25,'text-anchor':'middle'},r.tag);if(r.action!=='COIL')make('text',{x:width-80,y:y+5,'text-anchor':'middle'},r.action==='SET'?'S':'R');}wire(`M${width-25} ${y}H${width-10}V${y-35}`);y+=size.h+35;
 }
 wire(`M35 25V${y-25} M${maxWidth-10} 25V${y-25}`);
 host.setAttribute('viewBox',`0 0 ${maxWidth} ${Math.max(y,250)}`);host.style.width=maxWidth+'px';host.style.height=Math.max(y,250)+'px';
}
function renderLab(){drawLadder();$('stCode').textContent=stProgram();const trace=$('plcTrace');trace.replaceChildren();el('h3',`Runtime · ${labState.elapsed||0} ms simulated · fixed ${$('scanMs').value} ms per scan`,trace);const table=el('table',undefined,trace);const head=el('tr',undefined,table);['Rung','Tag','Rung result','Output','Timer ET / PT'].forEach(t=>el('th',t,head));labProgram.forEach((r,i)=>{const row=el('tr',undefined,table),t=labState.trace?.[i],timer=labState.timers?.[r.tag];[i+1,r.tag,t?String(t.powered):'Not scanned',t?String(t.value):'Not scanned',timer?`${timer.elapsed} / ${timer.preset} ms`:'—'].forEach(v=>el('td',String(v),row))})}
for(const id of ['plcStart','plcStop','plcOverload'])$(id).onchange=drawLadder;
window.saveAdvanced=function(){project.advancedNotes=$('advancedNotes').value;project.engineeringInputs=Object.fromEntries(inputIds.map(id=>[id,$(id).value]));project.plc={program:readProgram(),inputs:plcInputs(),scanMs:$('scanMs').value};};
window.loadAdvanced=function(){
 pausePLCLab();project.advancedCompleted??=[];project.advancedAnswers??={};$('advancedNotes').value=project.advancedNotes||'';
 for(const id of inputIds)if(project.engineeringInputs?.[id]!==undefined)$(id).value=project.engineeringInputs[id];
 labProgram=project.plc?.program||defaultProgram();$('scanMs').value=project.plc?.scanMs||100;const inputs=project.plc?.inputs||{Start:false,StopHealthy:true,OverloadHealthy:true};$('plcStart').checked=inputs.Start;$('plcStop').checked=inputs.StopHealthy;$('plcOverload').checked=inputs.OverloadHealthy;
 renderEditor();compileLab();renderAdvancedLessons();advancedCalculations();
};
loadAdvanced();renderSymbols();
