const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const read = file => JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'));
const themes = ['dark', 'light'].map(mode => read(`themes/struxllence-${mode}-color-theme.json`));
const standard = ['namespace','type','class','enum','interface','struct','typeParameter','parameter','variable','property','enumMember','decorator','event','function','method','macro','label','comment','string','keyword','number','regexp','operator'];
const ansi = ['Black','Red','Green','Yellow','Blue','Magenta','Cyan','White','BrightBlack','BrightRed','BrightGreen','BrightYellow','BrightBlue','BrightMagenta','BrightCyan','BrightWhite'];
const rgb = hex => [1,3,5].map(i => parseInt(hex.slice(i,i+2),16)/255);
const luminance = hex => rgb(hex).reduce((sum,x,i) => sum + [.2126,.7152,.0722][i]*(x<=.04045 ? x/12.92 : ((x+.055)/1.055)**2.4),0);
const contrast = (a,b) => { const [low,high]=[luminance(a),luminance(b)].sort((x,y)=>x-y);return (high+.05)/(low+.05); };
function composite(overlay, background) {
  const alpha=overlay.length===9 ? parseInt(overlay.slice(7),16)/255 : 1;
  return '#'+rgb(overlay).map((v,i)=>Math.round(255*(v*alpha+rgb(background)[i]*(1-alpha))).toString(16).padStart(2,'0')).join('');
}
const foreground = rule => typeof rule==='string' ? rule : rule.foreground;

test('the pair covers the same workbench keys, semantic selectors and fallback scopes', () => {
  assert.deepEqual(Object.keys(themes[0].colors).sort(),Object.keys(themes[1].colors).sort());
  assert.deepEqual(Object.keys(themes[0].semanticTokenColors).sort(),Object.keys(themes[1].semanticTokenColors).sort());
  assert.deepEqual(themes[0].tokenColors.map(x=>x.scope),themes[1].tokenColors.map(x=>x.scope));
  for (const theme of themes) {
    assert.equal(theme.semanticHighlighting,true);
    for (const type of standard) assert.ok(theme.semanticTokenColors[type],`Missing semantic type ${type}`);
    for (const [key,value] of Object.entries(theme.colors)) assert.match(value,/^#[\da-f]{6}([\da-f]{2})?$/i,key);
    for (const value of Object.values(theme.semanticTokenColors)) if (foreground(value)) assert.match(foreground(value),/^#[\da-f]{6}$/i);
    assert.equal(theme.semanticTokenColors['*.deprecated'].strikethrough,true);
  }
});

for (const theme of themes) {
  test(`${theme.name}: complete ANSI palette, selection and cursor; readable default terminal text`, () => {
    const c=theme.colors;
    assert.equal(Object.keys(c).filter(k=>k.startsWith('terminal.ansi')).length,16);
    for (const name of ansi) {
      const value=c['terminal.ansi'+name];assert.ok(value,name);
      // ANSI black deliberately remains dark in the dark theme for programs using it as a background.
      if (theme.type==='dark' && name==='Black') continue;
      assert.ok(contrast(value,c['terminal.background'])>=4.5,`${name}: ${contrast(value,c['terminal.background']).toFixed(2)}`);
    }
    assert.ok(contrast(c['terminal.foreground'],c['terminal.background'])>=7);
    assert.ok(c['terminalCursor.foreground']);assert.ok(c['terminal.selectionBackground']);assert.ok(c['terminal.inactiveSelectionBackground']);
    assert.ok(contrast(c['terminal.selectionForeground'],composite(c['terminal.selectionBackground'],c['terminal.background']))>=4.5);
  });
  test(`${theme.name}: syntax and semantic foregrounds remain readable over diff overlays`, () => {
    const c=theme.colors;
    const backgrounds=[c['editor.background']];
    for (const kind of ['inserted','removed']) {
      const line=c[`diffEditor.${kind}LineBackground`],text=c[`diffEditor.${kind}TextBackground`];
      for (const fill of [line,text]) assert.ok(parseInt(fill.slice(7),16)>0 && parseInt(fill.slice(7),16)<255,'Diff overlays must be translucent');
      backgrounds.push(composite(line,c['editor.background']),composite(text,c['editor.background']),composite(text,composite(line,c['editor.background'])));
    }
    for (const value of [...theme.tokenColors.map(t=>t.settings.foreground),...Object.values(theme.semanticTokenColors).map(foreground).filter(Boolean)])
      for (const bg of backgrounds) assert.ok(contrast(value,bg)>=4.5,`${value} on ${bg}: ${contrast(value,bg).toFixed(2)}`);
    for (const kind of ['added','modified','deleted']) {
      assert.ok(c[`editorGutter.${kind}Background`]);assert.ok(c[`minimapGutter.${kind}Background`]);assert.ok(c[`editorOverviewRuler.${kind}Foreground`]);
    }
    assert.notEqual(c['diffEditor.insertedTextBackground'],c['diffEditor.removedTextBackground']);
  });
  test(`${theme.name}: semantic categories follow the corresponding TextMate palette`, () => {
    const token=name=>theme.tokenColors.find(x=>x.name===name).settings.foreground;
    for (const [semantic,syntax] of [['class','Types, Classes & Interfaces'],['parameter','Variables & Parameters'],['property','Object & Property Keys'],['method','Functions & Methods'],['keyword','Keywords & Control Flow'],['string','Strings & Characters'],['number','Numbers & Booleans'],['comment','Comments'],['enumMember','Constants & Enums'],['variable.readonly','Constants & Enums'],['property.readonly','Constants & Enums']])
      assert.equal(foreground(theme.semanticTokenColors[semantic]),token(syntax),semantic);
  });
}

test('all contributed resources exist, and the theme extension has no runtime entry point', () => {
  const p=read('package.json');assert.equal(p.version,'1.0.3');assert.equal(p.publisher,'StruXllence');assert.equal(p.name,'struxllence-themes');
  assert.equal(p.main,undefined);assert.equal(p.browser,undefined);assert.equal(p.activationEvents,undefined);
  for (const family of ['themes','iconThemes','productIconThemes']) for (const contribution of p.contributes[family]) {
    assert.ok(fs.existsSync(path.join(root,contribution.path)),contribution.path);
    const document=read(contribution.path);
    if(family==='iconThemes')for(const value of Object.values(document.iconDefinitions)) if(value.iconPath)assert.ok(fs.existsSync(path.resolve(root,path.dirname(contribution.path),value.iconPath)));
    if(family==='productIconThemes')for(const font of document.fonts)for(const source of font.src)assert.ok(fs.existsSync(path.resolve(root,path.dirname(contribution.path),source.path)));
  }
});
