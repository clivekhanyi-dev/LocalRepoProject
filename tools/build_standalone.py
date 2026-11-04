"""Bundle the existing frontend into one offline HTML. No third-party packages."""
from pathlib import Path
import re
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]
web=ROOT/'web'
s=(web/'index.html').read_text()
s=s.replace('<title>Automation Engineering Academy</title>','<title>Automation Engineering Academy — Version 6</title>')
s=s.replace('<link rel="stylesheet" href="style.css">','<style>\n'+(web/'style.css').read_text()+'\n</style>')
a=s.index('<section id="profile"');b=s.index('</section>',a)+len('</section>')
s=s[:a]+'''<section id="profile" class="tab" hidden><div class="panel"><span class="eyebrow">VERSION 6.0 · OFFLINE EDITION</span><h2>Your local profile</h2><p id="profileEmail"></p><p id="serverAddress"></p><p id="connectionStatus" role="status"></p><button id="profileLogin" hidden>Local mode</button><button id="logout" hidden>Local mode</button><label>Display name<input id="localName" maxlength="100"></label><button id="renameProfile">Save display name</button><p>This file runs on your computer. There are no passwords, server accounts or cloud synchronisation. Anyone using this browser profile may access these local projects.</p><p>Browser storage belongs to this browser and file location. Clearing browser data, using private browsing, moving the HTML or changing browsers can make it unavailable. Use Projects → Export backup regularly. An export is a separate JSON file you can keep and later import into an updated version.</p><p>Existing Python-server accounts and projects are unchanged. To transfer projects, use Export backup in the updated server app while signed in, then Import backup here. SQLite databases cannot be imported directly into this browser app.</p></div></section>'''+s[b:]
s=s.replace('<div class="intro">','<div class="version-banner"><strong>Automation Engineering Academy · Version 6.0</strong><p>Offline desktop edition. Open this HTML in Chrome or Edge. No Python, VS Code or installation needed.</p><span id="draftStatus" role="status">Local saving initialising…</span></div><div class="intro">')
s=s.replace('Saving includes your circuit, lesson progress, notes, calculator values and product evidence.', 'Local saving includes your circuit, lesson progress, notes, calculator values, PLC program and product evidence. Export a backup before moving this file or clearing browser data.')
s=s.replace('AUTOMATION / ENGINEERING</span>','VERSION 6.0 / OFFLINE</span>')
s=s.replace('href="examples/AutomationCell.st"','href="data:text/plain;charset=utf-8,'+quote((web/'examples/AutomationCell.st').read_text(),safe='')+'"')
def inline(m):
 name=m.group(1)
 code=(web/name).read_text()
 return '<script>\n'+re.sub(r'</script',r'<\\/script',code,flags=re.I)+'\n</script>'
s=re.sub(r'<script src="([^"]+)"></script>',inline,s)
# Install the local persistence adapter before the existing application starts.
store="window.AppEdition={major:6,version:'6.0'};\n"+(web/'standalone-store.js').read_text()
s=s.replace('<script>','<script>\n'+store+'\n</script><script>',1)
output=ROOT/'Automation-Academy-V6.html'
output.write_text(s,encoding='utf-8')
print(f'Built {output.name}: {output.stat().st_size:,} bytes')
