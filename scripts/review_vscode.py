"""Exercise the theme in an isolated VS Code test host and capture cursor-free evidence."""
from pathlib import Path
import argparse,json,os,socket,subprocess,time
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--insiders',action='store_true');args=parser.parse_args()
channel='insiders' if args.insiders else 'stable';out=root/'.qa'/f'{channel}-{int(time.time())}';out.mkdir(parents=True,exist_ok=False)
for phase in ['dark-semantic','dark-diff','dark-terminal','light-semantic','light-diff','light-terminal']:
    assert not (out/(phase+'.ack')).exists(),'Use a fresh review output directory'
app=Path(os.environ['LOCALAPPDATA'])/'Programs'/('Microsoft VS Code Insiders' if args.insiders else 'Microsoft VS Code')/('Code - Insiders.exe' if args.insiders else 'Code.exe')
settings={'telemetry.telemetryLevel':'off','update.mode':'none','extensions.autoUpdate':False,'extensions.autoCheckUpdates':False,'security.workspace.trust.enabled':False,'workbench.startupEditor':'none','workbench.enableExperiments':False,'workbench.tips.enabled':False,'workbench.colorTheme':'StruXllence Dark','window.zoomLevel':0,'window.newWindowDimensions':'maximized','editor.fontSize':16,'editor.minimap.enabled':False,'editor.semanticHighlighting.enabled':'configuredByTheme','editor.stickyScroll.enabled':False,'editor.guides.indentation':False,'terminal.integrated.fontSize':16,'terminal.integrated.gpuAcceleration':'off','terminal.integrated.minimumContrastRatio':1,'diffEditor.renderSideBySide':True,'workbench.editor.enablePreview':False,'typescript.check.npmIsInstalled':False,'chat.disableAIFeatures':True,'git.enabled':False,'git.openRepositoryInParentFolders':'never','workbench.secondarySideBar.defaultVisibility':'hidden'}
user=out/'user';(user/'User').mkdir(parents=True,exist_ok=True);(user/'User/settings.json').write_text(json.dumps(settings),encoding='utf-8');(out/'extensions').mkdir(exist_ok=True)
with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
env={**os.environ,'STRUX_THEME_QA_OUTPUT':str(out)};env.pop('ELECTRON_RUN_AS_NODE',None)
flags=[str(app),'--user-data-dir='+str(user),'--extensions-dir='+str(out/'extensions'),'--extensionDevelopmentPath='+str(root),'--extensionTestsPath='+str(root/'tests/vscode-review.cjs'),'--skip-welcome','--skip-release-notes','--disable-workspace-trust','--disable-updates','--disable-telemetry','--disable-gpu','--remote-debugging-port='+str(port),'--remote-debugging-address=127.0.0.1','--new-window',str(root/'tests/fixtures')]
startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
records=[];process=None;browser=None
try:
    with (out/'host.log').open('w',encoding='utf-8') as log,sync_playwright() as p:
        process=subprocess.Popen(flags,env=env,stdout=log,stderr=log,startupinfo=startup)
        deadline=time.monotonic()+120
        while time.monotonic()<deadline:
            try:
                browser=p.chromium.connect_over_cdp(f'http://127.0.0.1:{port}',timeout=1000);break
            except Exception:time.sleep(.3)
        assert browser,'Isolated VS Code debugging connection unavailable'
        captured=set();deadline=time.monotonic()+240
        while time.monotonic()<deadline:
            result=out/'extension-host-results.json'
            if result.exists():
                final=json.loads(result.read_text());assert final['ok'],final;break
            phase_file=out/'phase.json'
            if phase_file.exists():
                phase=json.loads(phase_file.read_text())['phase']
                if phase not in captured:
                    pages=[page for context in browser.contexts for page in context.pages if 'workbench' in page.url]
                    assert pages,'VS Code workbench not found';page=pages[0];page.wait_for_timeout(300)
                    mode=phase.split('-')[0];theme=json.loads((root/f'themes/struxllence-{mode}-color-theme.json').read_text())
                    # Read the actual registered workbench variables, rather than a mock theme renderer.
                    keys=[k for k in theme['colors'] if k.startswith(('terminal','diffEditor'))]+['editor.background','editorGutter.addedBackground']
                    resolved=page.evaluate("keys=>{const s=getComputedStyle(document.querySelector('.monaco-workbench'));return Object.fromEntries(keys.map(k=>[k,s.getPropertyValue('--vscode-'+k.replaceAll('.','-')).trim()]));}",keys)
                    for key in keys:assert resolved[key],f'Colour not registered in {channel}: {key}'
                    def rgba(color):
                        if color.startswith('#'):
                            raw=color[1:];return tuple(int(raw[i:i+2],16) for i in (0,2,4))+(round(int(raw[6:8],16)/255,3) if len(raw)==8 else 1,)
                        import re
                        numbers=re.findall(r'[\d.]+',color);return tuple(map(int,numbers[:3]))+(round(float(numbers[3]),3) if len(numbers)>3 else 1,)
                    for key in keys:
                        actual=rgba(resolved[key]);expected=rgba(theme['colors'][key]);assert actual[:3]==expected[:3] and abs(actual[3]-expected[3])<=.006,f'Colour override/drift: {key} {resolved[key]}'
                    if phase.endswith('-diff'):assert page.locator('.monaco-diff-editor').count()>0,'Real diff editor not open'
                    terminal_colours=[]
                    if phase.endswith('-terminal'):
                        assert page.locator('.xterm').count()>0,'Integrated terminal not open'
                        names=['Black','Red','Green','Yellow','Blue','Magenta','Cyan','White','BrightBlack','BrightRed','BrightGreen','BrightYellow','BrightBlue','BrightMagenta','BrightCyan','BrightWhite']
                        for index,name in enumerate(names):
                            rendered=page.locator(f'.xterm-rows .xterm-fg-{index}').first
                            assert rendered.count(),f'ANSI slot not visible: {name}'
                            colour=rendered.evaluate('(e)=>getComputedStyle(e).color');assert rgba(colour)==rgba(theme['colors']['terminal.ansi'+name]),f'ANSI renderer drift: {name} {colour}'
                            terminal_colours.append({'slot':name,'rendered':colour})
                    semantic=[]
                    if phase.endswith('-semantic'):
                        semantic=page.locator('.view-lines span').evaluate_all("nodes=>nodes.filter(e=>['Structure','calculate','load','stiffness'].includes(e.textContent)).map(e=>({text:e.textContent,color:getComputedStyle(e).color}))")
                        assert semantic,'Semantic sample not rendered'
                        expected={'Structure':'class','calculate':'method','load':'parameter','stiffness':'property'}
                        for name,token in expected.items():
                            rule=theme['semanticTokenColors'][token];colour=rule if isinstance(rule,str) else rule['foreground'];matches=[x for x in semantic if x['text']==name];assert matches,f'Missing rendered {name}'
                            assert any(rgba(x['color'])==rgba(colour) for x in matches),f'Actual semantic rendering drift: {name}: {matches}'
                    page.screenshot(path=str(out/(phase+'.png')),animations='disabled',caret='hide')
                    records.append({'phase':phase,'registered_colours_checked':len(keys),'semantic_rendered_samples':semantic,'terminal_rendered_colours':terminal_colours});captured.add(phase);(out/(phase+'.ack')).write_text('verified',encoding='utf-8')
            time.sleep(.15)
        else:raise AssertionError('Timed out waiting for isolated theme checks')
        process.wait(timeout=30)
        assert len(records)==6,records
        (out/'render-results.json').write_text(json.dumps({'channel':channel,'records':records,'terminalMinimumContrastRatio':1,'user_profile_modified':False},indent=2),encoding='utf-8')
        print(json.dumps({'channel':channel,'phases':len(records),'extension_host':final,'registered_colours_verified':True,'actual_semantic_rendering_verified':True}))
finally:
    if browser:
        try:browser.close()
        except Exception:pass
    if process and process.poll() is None:process.terminate();process.wait(timeout=15)
