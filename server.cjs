const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 3001 });

wss.on('connection', (ws) => {
    console.log('连接已开启');
    const answer = '勇士總管小鄧里維15日親自說明這次「追夢」卓雷蒙格林無限期禁賽內幕，除了強調這是他跟追夢團隊、聯盟三方共同討論出來的決定，更表明追夢自己也同意了，願意接受這種不知何時才可上場打球的禁賽模式。「比起卓雷蒙格林的無限期禁賽，勇士未來15到20場比賽如何調整將是關鍵，沒有追夢的勇士表現如何，比起他被禁賽多久更重要。」小鄧里維說。小鄧里維表示，儘管無法保證卓雷蒙格林禁賽後就會改變自己行為，但勇士仍會信任與支持他，所以在他禁賽期間，他會留在球隊周圍，「最健康方式就是把他留在球隊，也許不是每天，我們總不可能把他丟在某個地方。」「很多人把這件事情當作一個問題，但我們希望轉化成為一個積極因素，」小鄧里維說，「在卓雷蒙格林的職業生涯與生活中，他正處在一個迷惘階段，也許他需要這樣的刺激，我認為這是非常積極、非常樂觀的做法。」勇士本季只拿10勝14敗，排名落到西區第11，本季更有不少比賽慘遭對方上演逆轉秀，證明球隊狀態確實到了一個需要改革階段，不僅卓雷蒙格林，威金斯與克雷湯普生的低迷與失常，更是勇士迫切需要解決的問題。'
    let index = 0
    let currentMessage = ''
    // 模拟定时发送更新的字符串
    setInterval(() => {
        if(index<answer.length){
            currentMessage += `${answer[index++]}`;
            ws.send(JSON.stringify(currentMessage));
        } else {
            ws.close();
        }
    }, 10);

    ws.on('close', () => {
        console.log('连接关闭');
    });
});
