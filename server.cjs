const WebSocket = require('ws');
const fs = require('fs');

const wss = new WebSocket.Server({ port: 8080 });

wss.on('connection', (ws) => {
    console.log('Client connected');

    // 发送文本消息
    ws.send('1Hello1,1 W1ebSo1cke1t![DONE]');

    // 发送语音数据
    const audioFile1 = './src/assets/murphy.wav';
    const audioFile2 = './src/assets/murphy.wav';
    const audioData1 = fs.readFileSync(audioFile1);
    const audioData2 = fs.readFileSync(audioFile2);
    ws.send(audioData1);
    ws.send(audioData2);
    setTimeout(()=>{
        ws.send(audioData2);
    }, 20)

    // 监听消息
    ws.on('message', (message) => {
        console.log('Received message:', message);
    });

    // 监听关闭事件
    ws.on('close', () => {
        console.log('Client disconnected');
    });
});
