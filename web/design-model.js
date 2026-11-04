/* V2 engineering estimates: explicit units and assumptions, no catalogue claims. */
(function(root){
function loadCase(mass,acceleration,processForce,friction,orientation){if(![mass,acceleration,processForce,friction].every(Number.isFinite)||mass<=0||[acceleration,processForce,friction].some(n=>n<0)||!['horizontal','lift'].includes(orientation))return null;return mass*acceleration+processForce+friction+(orientation==='lift'?mass*9.81:0);}
const bores=[8,10,12,16,20,25,32,40,50,63,80,100,125,160,200,250,320];
function sizeCylinder({load,margin,pressure,backPressure,efficiency,rod,direction}){
 if(![load,margin,pressure,backPressure,efficiency,rod].every(Number.isFinite)||load<=0||margin<1||pressure<=backPressure||backPressure<0||efficiency<=0||efficiency>1||rod<0||!['extend','retract'].includes(direction))return null;
 const required=load*margin,ar=Math.PI*rod*rod/4,delta=.1*(pressure-backPressure);
 const area=Math.max(0,(required/efficiency+(direction==='retract'?pressure*.1*ar:-backPressure*.1*ar))/delta);
 const minBore=Math.max(rod,Math.sqrt(4*area/Math.PI)),candidate=bores.find(b=>b>rod&&Math.PI*b*b/4>=area)||null;
 const force=b=>{const a=Math.PI*b*b/4,annulus=a-ar;return efficiency*.1*(direction==='retract'?pressure*annulus-backPressure*a:pressure*a-backPressure*annulus)};
 return {required,minBore,candidate,available:candidate?force(candidate):null};
}
function airDemand({bore,rod,stroke,extraStroke,extendTime,retractTime,cycles,pressure,referencePressure,ambientPressure,temperature,referenceTemperature,deadVolume,reserve}){
 const values=[bore,rod,stroke,extraStroke,extendTime,retractTime,cycles,pressure,referencePressure,ambientPressure,temperature,referenceTemperature,deadVolume,reserve];
 if(!values.every(Number.isFinite)||bore<=0||rod<0||rod>=bore||stroke<=0||extraStroke<0||extendTime<=0||retractTime<=0||cycles<0||pressure<0||referencePressure<=0||ambientPressure<=0||temperature<=-273.15||referenceTemperature<=-273.15||deadVolume<0||reserve<0)return null;
 const travel=stroke+extraStroke,a=Math.PI*bore*bore/4,annulus=Math.PI*(bore*bore-rod*rod)/4;
 const capLitres=a*travel/1e6,rodLitres=annulus*travel/1e6,ratio=(pressure+ambientPressure)/referencePressure*(referenceTemperature+273.15)/(temperature+273.15);
 const deadReference=deadVolume*pressure/referencePressure*(referenceTemperature+273.15)/(temperature+273.15);
 const cycle=(capLitres+rodLitres)*ratio+deadReference;
 return {travel,capLitres,rodLitres,ratio,deadReference,cycle,average:cycle*cycles,withReserve:cycle*cycles*(1+reserve/100),extendActual:capLitres*60/extendTime,retractActual:rodLitres*60/retractTime,extendReference:capLitres*60/extendTime*ratio,retractReference:rodLitres*60/retractTime*ratio,minimumMotionPeriod:extendTime+retractTime,overlap:cycles>0&&60/cycles<extendTime+retractTime};
}
function hydraulicMotion(bore,rod,speed,direction){if(![bore,rod,speed].every(Number.isFinite)||bore<=0||rod<0||rod>=bore||speed<=0||!['extend','retract'].includes(direction))return null;const a=Math.PI*bore*bore/4,annulus=Math.PI*(bore*bore-rod*rod)/4;return {supply:(direction==='extend'?a:annulus)*speed*60/1e6,returnFlow:(direction==='extend'?annulus:a)*speed*60/1e6};}
function tubeDiameter(actualFlow,velocity){if(![actualFlow,velocity].every(Number.isFinite)||actualFlow<=0||velocity<=0)return null;return Math.sqrt(4*(actualFlow/60000)/(Math.PI*velocity))*1000;}
function panelLoads({plcW,ioA,sensors,sensorMA,coils,coilW,otherW,voltage,reserve,heat,ambient,internal}){
 if(![plcW,ioA,sensors,sensorMA,coils,coilW,otherW,voltage,reserve,heat,ambient,internal].every(Number.isFinite)||[plcW,ioA,sensors,sensorMA,coils,coilW,otherW,reserve,heat].some(v=>v<0)||!Number.isInteger(sensors)||!Number.isInteger(coils)||voltage<=0||internal<=ambient)return null;
 const watts=plcW+ioA*voltage+sensors*sensorMA/1000*voltage+coils*coilW+otherW,current=watts/voltage;
 return {watts,current,designCurrent:current*(1+reserve/100),idealAirflow:3600*heat/(1.2*1005*(internal-ambient)),deltaT:internal-ambient};
}
function layout({width,height,depth,edge,duct,railGap,componentWidth,componentHeight,componentDepth,count}){
 if(![width,height,depth,edge,duct,railGap,componentWidth,componentHeight,componentDepth,count].every(Number.isFinite)||[width,height,depth,componentWidth,componentHeight,componentDepth].some(v=>v<=0)||[edge,duct,railGap].some(v=>v<0)||count<1||!Number.isInteger(count))return null;
 const usableW=Math.max(0,width-2*edge-2*duct),usableH=Math.max(0,height-2*edge),columns=Math.floor(usableW/(componentWidth+10)),rows=columns?Math.ceil(count/columns):0,requiredH=rows*(componentHeight+railGap);
 return {usableW,usableH,columns,rows,requiredH,minimumWidth:componentWidth+10+2*edge+2*duct,minimumHeight:requiredH+2*edge,minimumDepth:componentDepth+50,fits:columns>0&&requiredH<=usableH&&componentDepth+50<=depth};
}
const api={loadCase,sizeCylinder,airDemand,hydraulicMotion,tubeDiameter,panelLoads,layout};if(typeof module!=='undefined')module.exports=api;else root.Design=api;
})(globalThis);
