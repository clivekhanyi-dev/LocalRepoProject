(function(root){
function validate(p){
 const issues=[]; const nodes=p.nodes||[], wires=p.wires||[];
 const byKind=k=>nodes.filter(n=>n.kind===k);
 for(const k of ['supply','valve','cylinder']) if(byKind(k).length!==1) issues.push(`Use exactly one ${k} in this foundation circuit.`);
 if(issues.length)return issues;
 const port=(k,s)=>byKind(k)[0].id+':'+s;
 const has=(a,b)=>wires.some(w=>(w[0]===a&&w[1]===b)||(w[1]===a&&w[0]===b));
 for(const [a,b,msg] of [[port('supply','out'),port('valve','1'),'Connect the air supply to valve port 1.'],[port('valve','2'),port('cylinder','cap'),'Connect valve port 2 to the cap end.'],[port('valve','4'),port('cylinder','rod'),'Connect valve port 4 to the rod end.']])if(!has(a,b))issues.push(msg);
 if(wires.length!==3)issues.push('This example needs exactly three hoses; ports 3 and 5 exhaust to atmosphere.');
 return issues;
}
function forces(bar,bore,rod){if(![bar,bore,rod].every(Number.isFinite)||bar<0||bore<=0||rod<0||rod>=bore)return null;return {extend:bar*.1*Math.PI*bore*bore/4,retract:bar*.1*Math.PI*(bore*bore-rod*rod)/4};}
function advance(position,coil){return Math.max(0,Math.min(1,position+(coil?-.1:.1)));}
function compare(a,b){
 const missing=Array.from({length:11},(_,j)=>j).filter(j=>!a[j]||!b[j]);
 const different=Array.from({length:9},(_,j)=>j+1).filter(j=>a[j]&&b[j]&&a[j].toLowerCase()!==b[j].toLowerCase());
 return {missing,different,status:missing.length?'Insufficient evidence':different.includes(1)?'Unsuitable on entered function':different.length?'Partial match — technical review required':'Candidate alternative — user-entered fields match'};
}
const api={validate,forces,advance,compare};if(typeof module!=='undefined')module.exports=api;else root.Model=api;
})(globalThis);
