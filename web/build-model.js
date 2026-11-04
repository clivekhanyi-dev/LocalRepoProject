/* V4: broad drawing catalogue, typed connections and explicitly limited ideal-air tracing. */
(function(root){
const p=(x,y,ax=x,ay=y,medium='air',direction='pass')=>({x,y,ax,ay,medium,direction});
const side=(medium='air')=>({IN:p(0,50,14,50,medium),OUT:p(140,50,126,50,medium)});
const c=Object.create(null);
function part(kind,name,category,symbol,ports,sim,help){c[kind]={kind,name,category,symbol,ports,sim,help:help||'Drawing component. Use actual device data and the matching learning tools for detailed design.'};}
part('supply','Compressed-air supply','Pneumatics','supply',{out:p(70,100,70,78)},'source','Supplies ideal air connectivity in the teaching simulator. This does not predict pressure, flow or force.');
part('valve','5/2 solenoid / spring valve','Pneumatics','valve',{'1':p(70,100,53.9,78),'2':p(25,0,45.5,18.5),'4':p(115,0,63,18.5),'3':p(25,100,45.5,78),'5':p(115,100,63,78)},'v52','OFF: 1→2 and 4→5. ON: 1→4 and 2→3. Click Operate or select this valve and use the energise switch.');
part('cylinder','Double-acting air cylinder','Pneumatics','cylinder',{cap:p(35,100,35,81.5),rod:p(86,100,86.1,81.5)},'double','Both a pressure path and an opposite-chamber exhaust path are required for the ideal motion preview. Use the sizing worksheet for force/flow estimates.');
part('air-filter','Air filter','Pneumatics','filter',side(),'pass','Ideal pass-through in the air preview. Actual filtration pressure loss and efficiency are not modelled.');
part('air-regulator','Pressure regulator','Pneumatics','regulator',side(),'forward','Ideal forward connectivity only. Regulation, reverse flow and relieving characteristics need the actual valve data.');
part('air-flow','Adjustable flow control','Pneumatics','restrictor',side(),'pass','Draws a restriction; motion speed is illustrative and is not calculated from this setting.');
part('air-check','One-way check valve','Pneumatics','check',side(),'forward','Ideal IN→OUT flow only. Reverse flow is blocked in the air connectivity preview.');
part('air-gauge','Pressure gauge','Pneumatics','gauge',{P:p(70,100,70,85)},'gauge','Shows a measurement point; no quantitative gauge pressure is solved by the simulator.');
part('air-tee','Air junction / tee','Pneumatics','junction',{L:p(0,50,14,50),R:p(140,50,126,50),T:p(70,0,70,18.5),B:p(70,100,70,81.5)},'junction','All four ports communicate. Use junctions to make a branching drawing easy to read.');
part('air-silencer','Exhaust / silencer','Pneumatics',null,{IN:p(70,0,70,30)},'vent','An ideal atmospheric exhaust. Real back pressure, noise and silencer sizing are not modelled.');
part('air-single','Single-acting spring cylinder','Pneumatics','single-cylinder',{A:p(35,100,35,81.5)},'single','Pressure extends; an open exhaust path permits spring return in the unloaded teaching model. Spring force and external load are not solved.');
part('air-v32','3/2 normally-closed valve','Pneumatics','valve32',{'1':p(30,100,45.5,81.5),'2':p(70,0,53.9,18.5),'3':p(115,100,63,81.5)},'v32','OFF: work port 2 exhausts through 3; supply 1 is blocked. ON: 1→2; exhaust is blocked.');
part('air-v22','2/2 shut-off valve','Pneumatics','valve22',{'1':p(70,100,53.9,78),'2':p(70,0,53.9,18.5)},'v22','OFF blocks both ports. ON provides ideal bidirectional continuity. Actual isolation/bleed functions must be selected separately.');
part('air-v53','5/3 closed-centre valve','Pneumatics','valve53',{'1':p(70,100,66.5,78),'2':p(25,0,59.5,18.5),'4':p(115,0,73.5,18.5),'3':p(20,100,58.1,78),'5':p(120,100,74.9,78)},'v53','Operate cycles centre → left → right. Centre blocks ports. This is not a load-holding/safety claim; trapped compressed air and leakage require real analysis.');
part('air-shuttle','Pneumatic OR / shuttle','Pneumatics','shuttle',{A:p(0,50,7,50),B:p(140,50,133,50),OUT:p(70,0,70,15)},null,'Available for drawing; shuttle dynamics are not simulated.');
part('oil-pump','Hydraulic pump','Hydraulics','pump',{IN:p(70,100,70,85,'oil'),OUT:p(70,0,70,15,'oil')},null);
part('oil-tank','Hydraulic reservoir','Hydraulics','tank',{T:p(70,0,70,15,'oil')},null);
part('oil-cylinder','Hydraulic cylinder','Hydraulics','cylinder',{A:p(35,100,35,81.5,'oil'),B:p(86,100,86.1,81.5,'oil')},null);
part('oil-v43','4/3 closed-centre valve','Hydraulics','valve43',{P:p(30,100,59.5,74.5,'oil'),T:p(110,100,73.5,74.5,'oil'),A:p(25,0,59.5,18.5,'oil'),B:p(115,0,73.5,18.5,'oil')},null);
part('oil-relief','Pressure-relief valve','Hydraulics','relief',{P:p(70,100,70,85,'oil'),T:p(70,0,70,15,'oil')},null);
part('oil-filter','Hydraulic filter','Hydraulics','filter',side('oil'),null);
part('oil-check','Hydraulic check valve','Hydraulics','check',side('oil'),null);
part('oil-pilot-check','Pilot-operated check','Hydraulics','pilot-check',{...side('oil'),X:p(70,100,66.5,85,'oil')},null);
part('oil-accumulator','Gas-charged accumulator','Hydraulics','accumulator',{P:p(70,100,70,88.5,'oil')},null);
part('oil-gauge','Hydraulic gauge','Hydraulics','gauge',{P:p(70,100,70,85,'oil')},null);
part('oil-tee','Oil junction / tee','Hydraulics','junction',{L:p(0,50,14,50,'oil'),R:p(140,50,126,50,'oil'),T:p(70,0,70,18.5,'oil'),B:p(70,100,70,81.5,'oil')},null);
const e=(medium='24V')=>side(medium);
part('dc-source','24 V DC source','Electrical',null,{'+24':p(140,30,120,30,'24V','out'),'0V':p(140,80,120,80,'0V','out')},null,'Functional 24 V DC training supply, not a particular product or physical pinout.');
part('dc-fuse','Control-circuit fuse','Electrical','fuse',e(),null);
part('contact-no','Normally-open contact','Electrical','no',e(),null);
part('contact-nc','Normally-closed contact','Electrical','nc',e(),null);
part('pushbutton','Start pushbutton','Electrical','pushbutton',e(),null);
part('relay-coil','24 V relay / contactor coil','Electrical','coil',{A1:p(0,50,14,50,'24V','in'),A2:p(140,50,126,50,'0V','in')},null,'Functional 24 V DC coil terminals. Actual ratings, polarity/suppression and terminal allocation require the real device instructions.');
part('dc-terminal','24 V junction / terminal','Electrical','terminal',e(),null);
part('zero-terminal','0 V junction / terminal','Electrical','terminal',e('0V'),null);
part('pe-terminal','Protective earth point','Electrical','earth',{PE:p(70,0,70,18.5,'PE')},null);
part('motor','Three-phase motor','Electrical','motor',{U:p(30,0,56,13.6,'AC'),V:p(70,0,70,13.6,'AC'),W:p(110,0,84,13.6,'AC'),PE:p(70,100,70,78,'PE')},null,'A symbolic three-phase motor. AC power circuits are drawing-only and require actual protection, wiring and manufacturer data.');
part('plc','PLC / I/O interface','PLC / Sensors',null,{'+24':p(0,20,20,20,'24V','in'),'0V':p(0,80,20,80,'0V','in'),DI:p(140,25,120,25,'24V','in'),DO:p(140,80,120,80,'24V','out')},null,'A functional PNP/24 V I/O interface. Not a device-specific module pinout or a safety PLC implementation.');
part('sensor','PNP position sensor','PLC / Sensors',null,{'+24':p(0,20,20,20,'24V','in'),'0V':p(0,80,20,80,'0V','in'),Q:p(140,50,120,50,'24V','out')},null,'Generic PNP signal allocation. Confirm sensor/module type, ratings and actual wiring.');
part('pressure-switch','Pressure switch / signal','PLC / Sensors','pressure-switch',{P:p(38.5,100,38.5,85,'air'),Q:p(140,40,133,46.5,'24V','out')},null,'Cross-domain functional drawing; pressure/electrical switch behaviour is not simulated.');
part('electrical-resistor','Resistor','Electrical','resistor',e(),null);
part('electrical-capacitor','Capacitor','Electrical','capacitor',e(),null);
part('ac-source','Three-phase AC supply','Electrical',null,{L1:p(20,100,20,80,'AC','out'),L2:p(70,100,70,80,'AC','out'),L3:p(120,100,120,80,'AC','out'),PE:p(140,30,120,30,'PE','out')},null,'Functional power source only; no supply/protection/safety design is validated.');
part('ac-fuse','AC protective element (one pole)','Electrical','fuse',side('AC'),null,'A drawing allocation, not a selected protective-device rating or coordination result.');
part('power-contactor','3-pole contactor interface','Electrical',null,{L1:p(20,0,20,20,'AC'),L2:p(70,0,70,20,'AC'),L3:p(120,0,120,20,'AC'),T1:p(20,100,20,80,'AC'),T2:p(70,100,70,80,'AC'),T3:p(120,100,120,80,'AC'),A1:p(0,30,20,30,'24V','in'),A2:p(0,80,20,80,'0V','in')},null,'Functional contactor power/coil interface. Verify physical poles, terminal names, ratings, suppression and actual device diagrams.');
part('limit-switch','Mechanical position switch','PLC / Sensors','pushbutton',side(),null,'An illustrative 24 V control contact. Physical switch type and PLC TRUE/FALSE instruction are different concepts.');
part('oil-motor','Hydraulic motor','Hydraulics','hydmotor',{IN:p(70,0,70,15,'oil'),OUT:p(70,100,70,85,'oil')},null,'Hydraulic motor drawing; torque, leakage and dynamic behaviour are not solved.');
part('oil-flow','Hydraulic flow restriction','Hydraulics','restrictor',side('oil'),null,'Draw a variable restriction; calculate actual flow/pressure loss using the selected equipment data.');
part('transformer','Two-winding transformer','Electrical','transformer',{P1:p(0,25,21,22,'AC'),P2:p(0,80,21,78,'AC'),S1:p(140,25,119,22,'AC'),S2:p(140,80,119,78,'AC')},null,'Functional winding references, not actual pinouts. Turns ratio, protection, insulation and electrical operation are not modelled.');
function portMap(){return Object.fromEntries(Object.entries(c).map(([k,d])=>[k,Object.fromEntries(Object.entries(d.ports).map(([n,p])=>[n,[p.x,p.y]]))]));}
function point(node,port){const d=c[node.kind]?.ports[port];if(!d)return null;const a=(node.angle||0)*Math.PI/180,x=d.x-70,y=d.y-50;return [node.x+70+x*Math.cos(a)-y*Math.sin(a),node.y+50+x*Math.sin(a)+y*Math.cos(a)];}
function wireRoute(project,a,b){
 const ra=resolve(project,a),rb=resolve(project,b);if(!ra||!rb)return null;
 const pa=point(ra.node,ra.name),pb=point(rb.node,rb.name);
 function stub(r,pt){const p=r.port;let dx=p.x<=0?-1:p.x>=140?1:0,dy=p.y<=0?-1:p.y>=100?1:0;if(!dx&&!dy)dy=p.y>=50?1:-1;const angle=(r.node.angle||0)*Math.PI/180;return [Math.max(5,Math.min(1195,pt[0]+40*(dx*Math.cos(angle)-dy*Math.sin(angle)))),Math.max(5,Math.min(795,pt[1]+40*(dx*Math.sin(angle)+dy*Math.cos(angle))))];}
 const sa=stub(ra,pa),sb=stub(rb,pb),start=[Math.round(sa[0]/20),Math.round(sa[1]/20)],end=[Math.round(sb[0]/20),Math.round(sb[1]/20)],key=(x,y)=>x+','+y;
 const rects=project.nodes.map(n=>{const angle=(n.angle||0)*Math.PI/180,corners=[[0,0],[140,0],[0,100],[140,100]].map(([x,y])=>[n.x+70+(x-70)*Math.cos(angle)-(y-50)*Math.sin(angle),n.y+50+(x-70)*Math.sin(angle)+(y-50)*Math.cos(angle)]);return {l:Math.min(...corners.map(p=>p[0]))-18,r:Math.max(...corners.map(p=>p[0]))+18,t:Math.min(...corners.map(p=>p[1]))-18,b:Math.max(...corners.map(p=>p[1]))+18};});
  const betweenClear=(vertical)=>rects.every((r,i)=>{const n=project.nodes[i];if(n.id===ra.node.id||n.id===rb.node.id)return true;return vertical?!(pa[0]>r.l&&pa[0]<r.r&&Math.max(pa[1],pb[1])>r.t&&Math.min(pa[1],pb[1])<r.b):!(pa[1]>r.t&&pa[1]<r.b&&Math.max(pa[0],pb[0])>r.l&&Math.min(pa[0],pb[0])<r.r)});
 const da=[sa[0]-pa[0],sa[1]-pa[1]],db=[sb[0]-pb[0],sb[1]-pb[1]],vertical=Math.abs(da[0])<.001&&Math.abs(db[0])<.001&&Math.sign(da[1])===Math.sign(pb[1]-pa[1])&&Math.sign(db[1])===Math.sign(pa[1]-pb[1]),horizontal=Math.abs(da[1])<.001&&Math.abs(db[1])<.001&&Math.sign(da[0])===Math.sign(pb[0]-pa[0])&&Math.sign(db[0])===Math.sign(pa[0]-pb[0]);
 if((vertical&&Math.abs(pa[0]-pb[0])<.001&&betweenClear(true))||(horizontal&&Math.abs(pa[1]-pb[1])<.001&&betweenClear(false)))return {d:'M'+pa.join(',')+' L'+pb.join(','),routed:true,points:[pa,pb]};
const blocked=(x,y)=>rects.some(r=>x*20>r.l&&x*20<r.r&&y*20>r.t&&y*20<r.b),queue=[start],prev=new Map([[key(...start),null]]);let found=false;
 for(let i=0;i<queue.length;i++){const cur=queue[i];if(cur[0]===end[0]&&cur[1]===end[1]){found=true;break}for(const[dx,dy]of [[1,0],[-1,0],[0,1],[0,-1]]){const x=cur[0]+dx,y=cur[1]+dy,k=key(x,y);if(x<0||x>60||y<0||y>40||prev.has(k))continue;if(blocked(x,y)&&!(x===end[0]&&y===end[1]))continue;prev.set(k,cur);queue.push([x,y]);}}
 let path=[];if(found){let at=end;while(at){path.push([at[0]*20,at[1]*20]);at=prev.get(key(...at));}path.reverse();}else path=[[sa[0],sb[1]]];
 const points=found?[pa,sa,[start[0]*20,sa[1]],...path,[end[0]*20,sb[1]],sb,pb]:[pa,sa,[sa[0],sb[1]],sb,pb],simple=[];for(const p of points){while(simple.length>=2){const x=simple.at(-2),y=simple.at(-1);if((Math.abs(x[0]-y[0])<.001&&Math.abs(y[0]-p[0])<.001)||(Math.abs(x[1]-y[1])<.001&&Math.abs(y[1]-p[1])<.001))simple.pop();else break}simple.push(p)}
 return {d:simple.map((p,i)=>(i?'L':'M')+p.join(',')).join(' '),routed:found,points:simple};
}
function resolve(project,key){const at=key.lastIndexOf(':');if(at<1)return null;const id=key.slice(0,at),name=key.slice(at+1),node=project.nodes.find(n=>n.id===id),port=node&&c[node.kind]?.ports[name];return port?{node,name,port}:null;}
function connection(project,a,b){const x=resolve(project,a),y=resolve(project,b);if(!x||!y)return 'Choose two existing connection dots.';if(a===b||x.node.id===y.node.id)return 'Choose dots on two different parts.';if(x.port.medium!==y.port.medium)return 'These connections do not match: '+x.port.medium+' / '+y.port.medium+'.';if(x.port.direction==='out'&&y.port.direction==='out')return 'Do not connect two outputs or supply sources together.';if(project.wires.some(w=>w.includes(a)&&w.includes(b)))return 'These dots are already connected.';return null;}
function inspect(project){const errors=[],warnings=[];const seen=new Set();if(!Array.isArray(project.nodes)||!Array.isArray(project.wires))return {errors:['Invalid workspace.'],warnings:[],simulated:false};for(const n of project.nodes){if(!c[n.kind]||seen.has(n.id))errors.push('Unknown or duplicate component.');seen.add(n.id)}for(const w of project.wires){const x=resolve(project,w[0]),y=resolve(project,w[1]);if(!x||!y)errors.push('A wire refers to a removed/unknown dot.');else if(x.port.medium!==y.port.medium)errors.push('Mixed connection types: '+x.port.medium+' / '+y.port.medium);else if(x.port.direction==='out'&&y.port.direction==='out')errors.push('Two output/source dots are joined.');}
 const unsupported=project.nodes.filter(n=>!c[n.kind]?.sim).map(n=>c[n.kind]?.name||n.kind);if(!project.nodes.length)warnings.push('Add parts or choose a starter.');
 const open=project.nodes.flatMap(n=>Object.keys(c[n.kind]?.ports||{}).filter(p=>!project.wires.some(w=>w.includes(n.id+':'+p))).map(p=>n.id+':'+p));if(open.length)warnings.push(open.length+' unconnected dots (some exhaust/test/unused ports may intentionally remain open).');
 return {errors,warnings,unsupported,simulated:project.nodes.length>0&&!errors.length&&!unsupported.length};}
function airState(project,controls={}){
 const check=inspect(project);if(!check.simulated)return {supported:false,...check,cylinders:[],pressure:[]};
 const graph=new Map(),add=(a,b,both=false)=>{if(!graph.has(a))graph.set(a,new Set());graph.get(a).add(b);if(both)add(b,a)};
 for(const w of project.wires)add(w[0],w[1],true);
 const sources=[],vents=[];
 for(const n of project.nodes){const d=c[n.kind],key=p=>n.id+':'+p,s=controls[n.id]||0,link=(a,b,both=true)=>add(key(a),key(b),both);
  if(d.sim==='source'&&controls[n.id]!==false)sources.push(key('out'));
  if(d.sim==='vent')vents.push(key('IN'));
  if(d.sim==='pass')link('IN','OUT');if(d.sim==='forward')link('IN','OUT',false);
  if(d.sim==='junction'){const names=Object.keys(d.ports);names.slice(1).forEach(p=>link(names[0],p));}
  if(d.sim==='v52'){link('1',s?'4':'2');link(s?'2':'4',s?'3':'5');}
  if(d.sim==='v32'){if(s)link('1','2');else link('2','3');}
  if(d.sim==='v22'&&s)link('1','2');
  if(d.sim==='v53'&&s){link('1',s===1?'2':'4');link(s===1?'4':'2',s===1?'5':'3');}
  for(const p of ['3','5'])if(d.ports[p]&&!project.wires.some(w=>w.includes(key(p))))vents.push(key(p));
 }
 function reachable(starts){const found=new Set(starts),queue=[...starts];for(let i=0;i<queue.length;i++)for(const b of graph.get(queue[i])||[])if(!found.has(b)){found.add(b);queue.push(b)}return found}
 const pressure=reachable(sources),ventSet=new Set(vents),vented=key=>[...reachable([key])].some(k=>ventSet.has(k));const supplyToExhaust=vents.some(v=>pressure.has(v));const cylinders=[];
 for(const n of project.nodes){const d=c[n.kind];if(!['single','double'].includes(d.sim))continue;let target=null,reason='No complete pressure/exhaust path.';
  if(d.sim==='single'){const k=n.id+':A';if(pressure.has(k)){target=1;reason='Pressure extends the spring cylinder.'}else if(vented(k)){target=0;reason='Exhaust permits spring return.'}}
  else{const cap=n.id+':cap',rod=n.id+':rod',a=pressure.has(cap),b=pressure.has(rod);if(a&&b)reason='Both chambers have a pressure path; no net force is calculated.';else if(a&&vented(rod)){target=1;reason='Cylinder extends: cap supplied, rod side exhausts.'}else if(b&&vented(cap)){target=0;reason='Cylinder retracts: rod side supplied, cap side exhausts.'}else if(a||b)reason='The opposite chamber has no exhaust path.';}
  if(supplyToExhaust){target=null;reason='Supply reaches exhaust; chamber pressure is indeterminate, so motion preview is withheld.';}cylinders.push({id:n.id,target,reason});
 }
 return {supported:true,...check,cylinders,pressure:[...pressure],vents,supplyToExhaust};
}
function validateDrawing(project){if(!project||!Array.isArray(project.nodes)||!Array.isArray(project.wires)||project.nodes.length>100||project.wires.length>200)throw Error('Use at most 100 components / 200 connections.');const ids=new Set();for(const n of project.nodes){if(!n||typeof n.id!=='string'||!n.id||n.id.includes(':')||ids.has(n.id)||!c[n.kind]||!Number.isFinite(n.x)||!Number.isFinite(n.y)||Math.abs(n.x)>10000||Math.abs(n.y)>10000||!([0,90,180,270].includes(n.angle||0)))throw Error('Invalid circuit component.');ids.add(n.id)}for(const w of project.wires)if(!Array.isArray(w)||w.length!==2||w.some(k=>typeof k!=='string'||!resolve(project,k)))throw Error('Invalid circuit connection.');return project;}
const api={catalog:c,portMap,point,wireRoute,resolve,connection,inspect,airState,validateDrawing};if(typeof module!=='undefined')module.exports=api;else root.CircuitBuilder=api;
})(globalThis);
