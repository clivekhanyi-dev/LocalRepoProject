/* File-based edition: local data, not server authentication. Never stores passwords. */
(function(){
 const key='automation-academy-v'+(window.AppEdition?.major||1);let available=true,data={version:1,profile:'Local learner',projects:[],draft:null};
 try{const test=key+'-check';localStorage.setItem(test,'1');localStorage.removeItem(test);const raw=localStorage.getItem(key);if(raw){const saved=JSON.parse(raw);if(saved.version!==1||!Array.isArray(saved.projects))throw Error('Invalid local data');data=saved;}}
 catch(e){available=false;}
 function persist(next){if(!available)throw Error('Browser storage is unavailable. Use Export backup to keep your work as a file.');try{localStorage.setItem(key,JSON.stringify(next));data=next;}catch(e){throw Error('Browser storage is full or blocked. Export a backup now; this change was not saved.')}}
 window.StandaloneStore={
  profile:()=>data.profile||'Local learner',
  status:()=>available?'Offline mode · projects stored in this browser. Export backups regularly.':'Browser storage unavailable · use Export backup before closing.',
  async request(path,body){
   if(path==='me')return {email:this.profile()};
   if(path==='projects'){
    if(body){const name=body.name?.trim();if(!name||name.length>100||!body.project)throw Error('Enter a project name of 1–100 characters.');const next=JSON.parse(JSON.stringify(data));next.projects=next.projects.filter(p=>p.name!==name);next.projects.push({name,project:body.project});persist(next);}
    return {projects:JSON.parse(JSON.stringify(data.projects))};
   }
   throw Error('This edition uses a local profile, not server accounts.');
  },
  rename(name){if(typeof name!=='string'||!name.trim()||name.length>100)throw Error('Enter a display name of 1–100 characters.');persist({...data,profile:name.trim()});},
  saveDraft(draft){persist({...data,draft});},
  draft:()=>data.draft?JSON.parse(JSON.stringify(data.draft)):null,
  merge(projects,profile){const next=JSON.parse(JSON.stringify(data));for(const p of projects){next.projects=next.projects.filter(old=>old.name!==p.name);next.projects.push(p)}if(profile)next.profile=profile;persist(next);}
 };
})();
