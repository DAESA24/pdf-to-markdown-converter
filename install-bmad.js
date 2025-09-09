const { spawn } = require('child_process');
const path = require('path');

// Path where BMad should be installed
const projectPath = 'C:\\Users\\drewa\\Claude Code\\python-projects\\pdf-to-markdown-github';

// Run the installer
const installer = spawn('npx', ['bmad-method', 'install'], {
  stdio: 'pipe',
  shell: true
});

let step = 0;

installer.stdout.on('data', (data) => {
  const output = data.toString();
  console.log(output);
  
  // When asked for path, provide it
  if (output.includes('Enter the full path') && step === 0) {
    step = 1;
    installer.stdin.write(projectPath + '\n');
  }
  // When asked what to install, just press enter (keep default selection)
  else if (output.includes('Select what to install') && step === 1) {
    step = 2;
    // Just press enter to keep the default selection (BMad Core)
    installer.stdin.write('\n');
  }
});

installer.stderr.on('data', (data) => {
  console.error(`Error: ${data}`);
});

installer.on('close', (code) => {
  console.log(`Installation completed with code ${code}`);
  process.exit(code);
});