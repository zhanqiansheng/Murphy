import { exec } from 'child_process'
console.log('开启语音功能')
const pythonPath = "D:\\vue\\Murphy\\src\\py\\.venv\\Scripts\\python.exe";
const scriptPath = "D:\\vue\\Murphy\\src\\py\\TTSSample.py";

exec(`${pythonPath} ${scriptPath}`, (err, stdout, stderr) => {
  if (err) {
    console.error(`执行出错: ${stderr}`);
    return;
  }
  console.log(stdout);
})