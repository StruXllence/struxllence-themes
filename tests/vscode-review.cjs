// Runs only in an isolated VS Code test host; never included in the theme VSIX.
const vscode=require('vscode');
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const out=process.env.STRUX_THEME_QA_OUTPUT;
const delay=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function capture(phase) {
  fs.writeFileSync(path.join(out,'phase.json'),JSON.stringify({phase}));
  for(let i=0;i<600;i++) {
    if(fs.existsSync(path.join(out,phase+'.ack')))return;
    await delay(100);
  }
  throw Error('Review screenshot/check did not acknowledge '+phase);
}
exports.run=async()=>{
  const results=[];
  try {
    const extension=vscode.extensions.getExtension('StruXllence.struxllence-themes');assert.ok(extension);assert.equal(extension.packageJSON.version,'1.0.3');
    await vscode.commands.executeCommand('workbench.action.closeAuxiliaryBar');
    await vscode.commands.executeCommand('notifications.clearAll');
    await vscode.extensions.getExtension('vscode.typescript-language-features').activate();
    const file=vscode.Uri.file(path.join(root,'tests/fixtures/semantic.ts'));
    const document=await vscode.workspace.openTextDocument(file);
    for(const mode of ['dark','light']) {
      await vscode.workspace.getConfiguration('workbench').update('colorTheme',`StruXllence ${mode==='dark'?'Dark':'Light'}`,vscode.ConfigurationTarget.Global);
      await vscode.window.showTextDocument(document,{preview:false});
      let legend,tokens;
      for(let i=0;i<50;i++) {
        legend=await vscode.commands.executeCommand('vscode.provideDocumentSemanticTokensLegend',file);
        tokens=await vscode.commands.executeCommand('vscode.provideDocumentSemanticTokens',file);
        if(legend&&tokens?.data?.length)break;
        await delay(300);
      }
      assert.ok(tokens?.data?.length,'Real TypeScript semantic tokens missing');
      const seen=new Set();for(let i=3;i<tokens.data.length;i+=5)seen.add(legend.tokenTypes[tokens.data[i]]);
      for(const category of ['class','interface','enum','method','parameter','property'])assert.ok(seen.has(category),'Missing TypeScript category '+category);
      let modifiers=0;for(let i=4;i<tokens.data.length;i+=5)modifiers|=tokens.data[i];
      assert.ok(modifiers&(1<<legend.tokenModifiers.indexOf('readonly')),'Read-only TypeScript modifier missing');
      await delay(700);await capture(mode+'-semantic');
      await vscode.commands.executeCommand('vscode.diff',vscode.Uri.file(path.join(root,'tests/fixtures/before.ts')),vscode.Uri.file(path.join(root,'tests/fixtures/after.ts')),'StruXllence diff review',{preview:false});
      await delay(700);await capture(mode+'-diff');
      const writer=new vscode.EventEmitter();
      const terminal=vscode.window.createTerminal({name:'StruXllence ANSI palette',pty:{onDidWrite:writer.event,open(){
        writer.fire('\x1b[2J\x1b[H  STRUXLLENCE - 16 ANSI COLOURS\r\n  NORMAL                         BRIGHT\r\n');
        const labels=['BLACK','RED','GREEN','YELLOW','BLUE','MAGENTA','CYAN','WHITE'];
        for(let i=0;i<8;i++)writer.fire(`  \x1b[${30+i}m${labels[i].padEnd(9)} Example 0123\x1b[0m       \x1b[${90+i}m${labels[i].padEnd(9)} Example 0123\x1b[0m\r\n`);
        writer.fire('  \x1b[32mADDED\x1b[0m  \x1b[31mREMOVED\x1b[0m  \x1b[33mMODIFIED\x1b[0m\r\n');
      },close(){}}});
      terminal.show();await delay(700);await vscode.commands.executeCommand('workbench.action.terminal.focus');await delay(1000);await capture(mode+'-terminal');terminal.dispose();writer.dispose();await vscode.commands.executeCommand('workbench.action.closePanel');
      results.push({mode,semanticTokenCount:tokens.data.length/5,semanticTypes:[...seen].sort(),readonlyModifier:true,diffOpened:true,terminalAnsiSlots:16});
    }
    fs.writeFileSync(path.join(out,'extension-host-results.json'),JSON.stringify({ok:true,vscode:vscode.version,version:'1.0.3',results},null,2));
  }catch(error){fs.writeFileSync(path.join(out,'extension-host-results.json'),JSON.stringify({ok:false,error:error.stack},null,2));throw error;}
};
