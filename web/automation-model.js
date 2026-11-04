/* Deterministic educational ladder runtime. No eval or native-machine connection. */
(function(root){
function parse(expression){
 if(typeof expression!=='string'||expression.length>1500)throw Error('Expression must be under 1500 characters.');
 const tokens=expression.match(/[A-Za-z_][A-Za-z0-9_.]*|[()]|\S/g)||[];let i=0;
 function atom(){const t=tokens[i++];if(t==='NOT')return {op:'not',a:atom()};if(t==='('){const a=or();if(tokens[i++]!==')')throw Error('Missing closing parenthesis');return a;}if(!t||!/^[A-Za-z_][A-Za-z0-9_]*(\.Q)?$/.test(t)||['AND','OR'].includes(t))throw Error('Expected a tag or parenthesised expression');return {op:'tag',name:t};}
 function and(){let a=atom();while(tokens[i]==='AND'){i++;a={op:'and',a,b:atom()}}return a;}
 function or(){let a=and();while(tokens[i]==='OR'){i++;a={op:'or',a,b:and()}}return a;}
 const ast=or();if(i!==tokens.length)throw Error('Use AND, OR, NOT and parentheses only');return ast;
}
function evaluate(ast,tags){if(ast.op==='tag'){if(ast.name==='TRUE')return true;if(ast.name==='FALSE')return false;if(!Object.hasOwn(tags,ast.name))throw Error('Unknown tag: '+ast.name);return !!tags[ast.name];}if(ast.op==='not')return !evaluate(ast.a,tags);const a=evaluate(ast.a,tags),b=evaluate(ast.b,tags);return ast.op==='and'?a&&b:a||b;}
const inputDefaults={Start:false,StopHealthy:true,OverloadHealthy:true,Reset:false,Extended:false,Retracted:true,PressureOK:true,PartPresent:false,Reverse:false};
function compile(program){
 if(!Array.isArray(program)||program.length<1||program.length>16)throw Error('Use 1–16 rungs');
 const inputs=Object.keys(inputDefaults),seen=new Set(),timers=new Set();
 const parsed=program.map((r,i)=>{
  if(!r||typeof r.tag!=='string'||! /^[A-Za-z_][A-Za-z0-9_]{0,31}$/.test(r.tag)||inputs.includes(r.tag)||['TRUE','FALSE','AND','OR','NOT','__proto__','constructor','prototype'].includes(r.tag))throw Error('Rung '+(i+1)+': invalid output tag');
  if(!['COIL','SET','RESET','TON'].includes(r.action))throw Error('Invalid rung action');
  if(r.action==='TON'){if(!Number.isFinite(+r.preset)||+r.preset<0||+r.preset>3600000)throw Error('TON preset must be 0–3600000 ms');if(seen.has(r.tag))throw Error('Timer requires a unique instance name');timers.add(r.tag)}
  if(seen.has(r.tag)&&r.action!=='SET'&&r.action!=='RESET')throw Error('Duplicate output writer: '+r.tag);
  seen.add(r.tag);return {...r,ast:parse(r.expression)};
 });
 for(const r of parsed){if(timers.has(r.tag)&&r.action!=='TON')throw Error('A timer instance cannot also be a coil');}
 const tags={...inputDefaults};for(const r of parsed)tags[r.action==='TON'?r.tag+'.Q':r.tag]=false;
 for(const r of parsed)evaluate(r.ast,tags);
 return parsed;
}
function scan(program,state,inputs,dt){
 if(!Number.isFinite(dt)||dt<=0||dt>1000)throw Error('Scan interval must be 1–1000 ms');
 const parsed=compile(program),tags={...inputDefaults,...state.tags,...inputs},timers={};
 for(const r of parsed)if(r.action==='TON')tags[r.tag+'.Q']??=false;else tags[r.tag]??=false;
 const trace=[];
 for(const r of parsed){const before={...tags},powered=evaluate(r.ast,tags);
  if(r.action==='TON'){const old=state.timers?.[r.tag]?.elapsed||0;const elapsed=powered?(state.timers?.[r.tag]?.active?Math.min(+r.preset,old+dt):0):0;timers[r.tag]={elapsed,preset:+r.preset,active:powered};tags[r.tag+'.Q']=powered&&elapsed>=+r.preset;}
  else if(r.action==='COIL')tags[r.tag]=powered;
  else if(powered)tags[r.tag]=r.action==='SET';
  trace.push({tag:r.tag,powered,before,value:!!tags[r.action==='TON'?r.tag+'.Q':r.tag]});
 }
 return {tags,timers,trace,elapsed:(state.elapsed||0)+dt};
}
function hydraulic(p,q,bore,rod,efficiency){if(![p,q,bore,rod,efficiency].every(Number.isFinite)||p<0||q<=0||bore<=0||rod<0||rod>=bore||efficiency<=0||efficiency>1)return null;const a=Math.PI*bore*bore/4,ar=Math.PI*(bore*bore-rod*rod)/4;return {force:p*.1*a,retractForce:p*.1*ar,extendSpeed:q*1e6/60/a,retractSpeed:q*1e6/60/ar,fluidPower:p*q/600,inputPower:p*q/600/efficiency,returnOnRetract:q*a/ar,returnOnExtend:q*ar/a};}
function motor(voltage,power,pf,efficiency){if(![voltage,power,pf,efficiency].every(Number.isFinite)||voltage<=0||power<=0||pf<=0||pf>1||efficiency<=0||efficiency>1)return null;return {current:power*1000/(Math.sqrt(3)*voltage*pf*efficiency),inputPower:power/efficiency};}
const api={parse,evaluate,compile,scan,hydraulic,motor,inputDefaults};if(typeof module!=='undefined')module.exports=api;else root.Automation=api;
})(globalThis);
