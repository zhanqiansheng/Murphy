<script setup>
import { ref, watch, onMounted, onBeforeMount } from 'vue'
import Recorder from 'recorder-core'
import 'recorder-core/src/engine/mp3'
import 'recorder-core/src/engine/mp3-engine'
import axios from "axios";
import { Microphone, ChatLineRound, WarningFilled, Promotion, MoreFilled } from '@element-plus/icons-vue'

// ----------------------------------------------------------------------------------- 变量定义
const talkAllMessage = ref([])      // 所有对话内容的html代码数组
// const history = ref([]) // 历史记录数组

const messageInput = ref('') // 输入框内容
const message = ref('') // 处理后的输入内容
const rowsNum = ref(1)  // 输入框行数

const ai_response_content = ref('') // ai的单条回复内容
let response_box = ref()   // ai最新答复的聊天框
let talkBody = ref()       // 整体聊天框
let foot_input = ref()       // 输入框
let foot_input_copy = ref()       // 输入框
let talkFoot = ref()       // 底部
let turnVoice = ref(false)

let isBottom = ref(true) // 是否位于底部
let controlable = ref(true)   // 用户是否可输入的状态变量
let socket  // 双向通信通道
let voiceOpen = ref(false) // 是否开启语音播放
let foot_voice = ref()
let foot_voice_copy = ref()
let recording_block = ref() //录音黑背景
let recordingBox = ref() // 录音中提示框
let unRecognizedVoice = ref(false) // 是否未识别到语音
let recordMode = true // 录音模式，true长按 false点按
let popoverVisible = ref(false) // 录音模式选择弹窗

// 大模型选择
const modelValue = ref('1.0')
const modelOptions = ref([{value: '1.0',label: 'Murphy-1.0'},{value: '2.0',label: 'Murphy-2.0'}])
let testURL = ref('u271424-b7ae-37107f92.neimeng.seetacloud.com:6443')
// let testURL = ref('u271424-98ae-ff5ded8d.neimeng.seetacloud.com:6443')

// ---------------------------------------------------- 发送逻辑
// 发送前状态重置
const beforeSendMessage = () => {
  popoverVisible.value=false;
  voiceNum.value = 0
  sentenceTotal.value = 0
  controlable.value = false
  if (audio) audio.pause()
  voiceQueue.clear()
  msgQueue.clear()
  sentence.value = ''
}
const messageIsEmpty = ref(false)
// 发送消息
const sendMessage = async () => {
  // 过滤用户携带的<>括号
  message.value = messageInput.value.replace(/</g, '&lt;').replace(/>/g, '&gt;')
  if (messageInput.value.trim() === '' || controlable.value === false){
    messageIsEmpty.value = true
    setTimeout(()=>{messageIsEmpty.value = false}, 2000)
    return
  }
  beforeSendMessage()
  // 将用户输入上传到页面
  talkAllMessage.value.push({ message: message.value, kind: 'human' })
  // 用户发送消息后1ms，滑动到底部，发送请求
  setTimeout(() => {
    scrollToBottom()
    try {
      // 尝试发送消息
      if (socket.readyState === WebSocket.OPEN) {
        // 语音发送一定要发送两遍，不然没效果
        if(turnVoice.value || unRecognizedVoice.value){
          socket.send(message.value)
        }
        socket.send(message.value)
        unRecognizedVoice.value = false
        times.value = 1
      } else {
        ElMessage({
          message: '未连接服务器!',
          type: 'error',
        })
      }
    } catch (error) {
      // 处理连接错误
      ElMessage({
        message: '连接错误!',
        type: 'error',
      })
    }
    // 清空输入框
    messageInput.value = ''
    foot_input.value.value = ''
    foot_input.value.style.height = 25 + 'px'
    foot_input_copy.value.style.height = 25 + 'px'
  }, 1)

  // AI回复样式框架
  talkAllMessage.value.push({ message: '......', kind: 'machine' })

  // AI回复消息，获取最新回答的聊天框
  setTimeout(() => {
    scrollToBottom()
    const children = talkBody.value.children
    response_box = children[children.length - 1]
  }, 2)
}
// 连接大模型
const connect = () => {
  // 建立双向通信npm
  socket = new WebSocket('wss://' + testURL.value + '/ws/v1/chat/completions')
  // socket = new WebSocket('wss://' + testURL.value + '/ws/v1/code/completions')
  // 连接建立后调用函数
  socket.addEventListener('open', (event) => {
    console.log('连接开启')
    ElMessage({
      message: '连接成功!',
      type: 'success',
    })
    localStorage.setItem('testURL', JSON.stringify(testURL.value))
  })

  let flag = false // 去掉</pre>后的一个换行符
  let isCode = false
  // 处理服务器返回数据
  socket.addEventListener('message', (event) => {
    let temp = event.data.replace(/</g, '&lt;')
    // console.log('--' + temp + '--')
    if (voiceOpen.value) makeQueue(temp) // 制作句子队列，等待转语音
    // 设置聊天框内的文字内容
    const target = response_box.querySelector('.mobile_talk_box')
    if(target.innerHTML === '......') target.innerHTML = ''
    // 传输已结束
    if(temp === '[DONE]'){
      console.log('---传输完毕，请继续输入---')
      sentence.value = ''
      ai_response_content.value = ''
      controlable.value = true
    }
    // 传输文字内容
    else if( isCode === false ) {
      if (event.data === '\n') {
        ai_response_content.value = '<br>'
        if( flag === true ) { // 去掉</pre>后的一个换行符
          ai_response_content.value = ''
          flag = false
        }
      } else if(event.data ===' '){
        ai_response_content.value = '&nbsp;'
      } else if (event.data.substring(0, 3) === '```' || event.data.substring(1, 4) === '```') {
        isCode = true
        ai_response_content.value = '<pre style="display: inline-block;padding: 10px;background-color: black;color: white">########################################################&nbsp;&nbsp;</pre>'
      } else {
        ai_response_content.value = temp
      }
      target.innerHTML += ai_response_content.value
    }
    // 传输代码内容
    else if ( isCode === true ) {
      if (event.data.substring(event.data.length - 3, event.data.length) === '```') {
        isCode = false
        flag = true
        target.innerHTML = target.innerHTML.slice(0, -6) + '########################################################</pre>'
      } else {
        ai_response_content.value = target.innerHTML.slice(0, -6);
        ai_response_content.value += temp + '</pre>' // </code>
        // 将新文本设置回元素
        target.innerHTML = ai_response_content.value;
      }
    }
    scrollToBottom()
  });

  // 连接关闭后调用函数
  socket.addEventListener('close', () => {
    const target = response_box.querySelector('.mobile_talk_box')
    // target.textContent = ai_response_content.value
    target.innerHTML = ai_response_content.value
    ElMessage.error('连接已关闭，请刷新页面')
    ai_response_content.value = ''
    controlable.value = true
  });
}

// ---------------------------------------------------- 语音逻辑
// 开启/关闭语音
const openVoice = () => {
  voiceOpen.value = !voiceOpen.value
  if(voiceOpen.value){
    ElMessage.success('声音已开启')
  }else {
    if(audio) audio.pause()
    ElMessage.info('声音已关闭')
  }
}
// 队列封装
function createQueue() {
  const items = [];

  // 入队操作
  function inqueue(element) {
    items.push(element);
  }

  // 出队操作
  function outqueue() {
    if (isEmpty()) {
      return null;
    }
    return items.shift();
  }

  // 查看队头元素
  function front() {
    if (isEmpty()) {
      return null;
    }
    return items[0];
  }

  // 检查队列是否为空
  function isEmpty() {
    return items.length === 0;
  }

  // 获取队列长度
  function size() {
    return items.length;
  }

  // 清空队列
  function clear() {
    items.length = 0;
  }

  // 返回队列对象
  return {
    inqueue,
    outqueue,
    front,
    isEmpty,
    size,
    clear
  };
}
// 语音播放条数
const voiceNum = ref(0)
// 句子总数
const sentenceTotal = ref(0)
// 第times次语音请求
const times = ref(1)
// 待转换队列
const msgQueue = createQueue()
// 语音队列
const voiceQueue = createQueue()
// 获取一句句子
const sentence = ref('')
// 制作句子队列，等待转语音
const makeQueue = async(temp) => {
  if (onlyMark(temp.trim())) {  // 若遇到标点符号，分割，赋值句子
    if (sentence.value !== '') {  // 不为空才将句子压入队列，等待进行语音转换
      msgQueue.inqueue(sentence.value)
      sentenceTotal.value++
      sentence.value = ''
      // 只在前若干次次执行的时候在这里进行请求，请求前几句
      if(times.value > 0) {
        // 只在第一次时在这里播放，此后都是在音频播放判断结束后进行播放
        times.value--
        await sendMessageToMicrosoft(msgQueue.front())
        if(times.value === 0){
          playAudio()
        }
      }
    }
  } else {
    sentence.value += temp
  }
}

let loopId
let loopendId // 语音播放条数是否匹配
let audio
// 播放语音
const playAudio = () => {
  audio = voiceQueue.front()
  audio.muted = true;
  audio.play();
  audio.muted = false;
  voiceNum.value++
  console.log('当前语音是第' + voiceNum.value + '条, sentenceTotal的值为' + sentenceTotal.value)
  let flag = 0

  // 添加timeupdate事件监听器
  audio.addEventListener('timeupdate', () => {
    const currentTime = audio.currentTime
    const duration = audio.duration
    // 如果当前时间距离结束不足5秒
    if (duration - currentTime < 8) {
      if (flag === 0) {
        flag = 1
        // 还不能发送，代表第二句还没生成完，执行循环
        if(msgQueue.size()===0 && controlable.value === false) {
          loopId = setInterval(()=>{
            if(msgQueue.size()>0){
              sendMessageToMicrosoft(msgQueue.front())
              clearInterval(loopId)
            }
          }, 1000) // 每1秒执行一次判断
        } else if(msgQueue.size()>0){
          sendMessageToMicrosoft(msgQueue.front())
        }
      }
    }
  })

  // 在音频播放结束时执行函数
  audio.addEventListener('ended', () => {
    voiceQueue.outqueue() // 当前语音出列
    if (!voiceQueue.isEmpty()) { // voiceQueue不为空，继续播放
      playAudio()
    }
    else if(voiceNum.value !== sentenceTotal.value) { // 语音与总句子数不匹配，进入等待
      loopendId = setInterval(()=>{
        if (!voiceQueue.isEmpty()) { // voiceQueue不为空，表示已请求到语音继续播放
          playAudio()
          clearInterval(loopendId)
        }
      }, 1000)
    }
    else if (voiceNum.value === sentenceTotal.value ){
      console.log('所有语音播放完毕')
      // ElMessage.success('播放完毕')
    }
  })
}

// 向微软发送请求语音合成api请求，将
const sendMessageToMicrosoft = async(msg) => {
  msgQueue.outqueue()
  console.log('发送语音请求中，内容：' + msg)
  const subscriptionKey = '854b68902a2d42f39acb0b8fb789342d';
  const region = 'japaneast';
  const aiName = 'zh-CN-XiaoxiaoNeural'
  const str = '<speak version="1.0" xml:lang="en-us"><voice xml:lang="en-US" name="' + aiName + '">' + msg + '</voice></speak>'
  const tokenResponse = await fetch(`https://${region}.api.cognitive.microsoft.com/sts/v1.0/issuetoken`, {
    method: 'POST',
    headers: {
      'Ocp-Apim-Subscription-Key': subscriptionKey
    }
  });
  if (tokenResponse.ok) {
    const accessToken = await tokenResponse.text()
    const synthesisResponse = await fetch(`https://${region}.tts.speech.microsoft.com/cognitiveservices/v1`, {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + accessToken,
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
        'User-Agent': 'YOUR_RESOURCE_NAME'
      },
      body: str,
    });
    if (synthesisResponse.ok) {
      const audioBlob = await synthesisResponse.blob()
      const audioUrl = URL.createObjectURL(audioBlob)
      const audio = new Audio();
      audio.src = audioUrl;
      audio.type = 'audio/wav';
      // 将获取到的语音压入队列
      voiceQueue.inqueue(audio)
      console.log('---请求音频完成, 请求内容：---\n' +  msg)
    } else {
      console.error('api访问错误:', synthesisResponse.body);
    }
  } else {
    console.log('token访问失败!访问次数过于频繁，请稍后重试')
    ElMessage.error('语音访问过于频繁，请稍后重试')
  }
}
// 包含以下标点符号的字符串
const onlyMark = (temp) => {
  const mark = ["。", "！", "？", "!", ".", "?", "：", "**"]
  return mark.includes(temp)
}

// 中止回答
const stopConnection = async () => {
  await axios.post('https://' + testURL.value + '/stop-processing')
  ai_response_content.value = ''
  controlable.value = true
}

// 点击滚动到底部按钮
const clickToBottom = () => {
  talkBody.value.scrollTo({
    top: talkBody.value.scrollHeight,
    // behavior: 'smooth',
  });
}
// 平滑滚动到底部
const scrollToBottom = () => {
  if(isBottom.value){
    talkBody.value.scrollTo({
      top: talkBody.value.scrollHeight,
      // behavior: 'smooth',
    });
  }
}

// ---------------------------------------------------- 录音逻辑
let rec
let recBlob
let isFirstTimeOpenWeb = 1 //第一次打开网页
const recording = ref(false) //是否正在录音
let timeCounter = 0 // 记录录音时长

// 语音与文字模式切换
const turnVoiceOrText = () => {
  turnVoice.value = !turnVoice.value
  popoverVisible.value = false
  // 第一次时请求录音权限
  if(turnVoice.value && isFirstTimeOpenWeb){
    giveRecordPermission()
    isFirstTimeOpenWeb = 0
  }
  adjustRecordHintBox()
  adjustHeight(turnVoice.value)
}
// 开启录音权限
const giveRecordPermission = () => {
  rec=null
  recBlob=null
  //mp3格式, 指定采样率hz, 比特率kbps
  let newRec = Recorder({
    type:"mp3",sampleRate:16000,bitRate:16
  })
  //打开麦克风授权获得相关资源
  newRec.open(function(){
    rec = newRec
  },function(){
    ElMessage.error('未检测到麦克风设备/用户未授权')
  })
}
let recordingHintId
// 开始录音
const recordStart = () => {
  popoverVisible.value = false
  if(!rec){
    giveRecordPermission()
    return
  }
  if(rec && Recorder.IsOpen()){
    recBlob=null;
    rec.start();
    setTimeout(()=>{recording.value = true}, 0)
    console.log('开始录音...')
    timeCounter = Date.now()
    foot_voice.value.innerHTML = '录制中...'
    foot_voice_copy.value.innerHTML = '录制中...'
    adjustRecordHintBox()
    // 录音开始时打断AI的语音播报
    if (audio) audio.pause()
    voiceQueue.clear()
    msgQueue.clear()
    const hint = document.querySelector('.mobile_recording div')
    let i = 0
    recordingHintId = setInterval(()=>{
      i === 3 ? i = 1 : i++
      switch (i){
        case 1: hint.innerHTML = '录制中.';break;
        case 2: hint.innerHTML = '录制中..';break;
        case 3: hint.innerHTML = '录制中...';break;
      }
    },500)
  }else{
    ElMessage.error('未检测到麦克风设备/用户未授权')
  }
}
// 结束录音
const recordStop = () => {
  if(!(rec&&Recorder.IsOpen())){
    return
  }
  rec.stop(async (blob) => {
    recBlob=blob
    recording.value = false
    clearTimeout(recordingHintId)
    if (Date.now() - timeCounter < 1000) { // 提示录音时间过短
      foot_voice.value.innerHTML = '按住 说话'
      foot_voice_copy.value.innerHTML = '单击开始录制'
      ElMessage.error('录音时间过短!')
      return
    }
    console.log("录制完毕")
    // 停止AI文字回复
    await stopConnection()
    await stopConnection()
    talkAllMessage.value.push({ message: '......', kind: 'human' })
    setTimeout(()=>{scrollToBottom()}, 10)
    foot_voice.value.innerHTML = '按住 说话'
    foot_voice_copy.value.innerHTML = '单击开始录制'
    const audioFile = new File([recBlob], 'recorded.wav', { type: 'audio/wav' });
    // 获取文件输入元素
    const fileInput = document.querySelector('input[name="mobile_file"]');
    // 创建一个 DataTransfer 对象
    const dataTransfer = new DataTransfer();
    // 将新文件对象添加到 DataTransfer
    dataTransfer.items.add(audioFile);
    // 将 DataTransfer 对象赋值给文件输入元素
    fileInput.files = dataTransfer.files;

    let formData = new FormData(mobile_uploadForm)
    formData.append('file', audioFile, 'recorded.wav');

    const children = talkBody.value.children
    let targetChild = children[children.length - 1].querySelector('.mobile_talk_box')
    setTimeout(()=>{
      targetChild = children[children.length - 1].querySelector('.mobile_talk_box')
    }, 10)

    fetch('https://' + testURL.value + '/transcribe/', {
      method: 'POST',
      body: formData
    })
        .then(response => response.json())
        .then(async (result) =>  {
          if(result.text === ''){
            targetChild.innerHTML = '(未识别到文字)'
            targetChild.style.color = 'red'
            unRecognizedVoice.value = true
          } else {
            messageInput.value = result.text
            talkAllMessage.value.pop()
            await sendMessage()
          }
        })
        .catch(() => {
          targetChild.innerHTML = '转录失败...请检查与服务器之间的链接'
          targetChild.style.color = 'red'
        })
  },function(msg){
    console.log('录制失败' + msg)
  })
}
// 注册按钮事件，长按/点按 - 开始/结束录音
const recordButtonRegister = () => {
  // 长按模式
  let touchTimeout;
  foot_voice.value.addEventListener('touchstart', () => {
    touchTimeout = setTimeout(() => {
      if (recording.value === false) {
        recordStart();
      }
    }, 50);
  });
  foot_voice.value.addEventListener('touchend', () => {
    clearTimeout(touchTimeout); // 清除长按的计时器
    if (recording.value) {
      recordStop();
    }
  });
  // 点按模式
  foot_voice_copy.value.addEventListener('click', () => {
    if (recording.value === false) {
      recordStart()
    } else if (recording.value) {
      recordStop()
    }
  })
}
// ---------------------------------------------------- 输入框逻辑
// 监听输入内容变化
watch(messageInput, () => {
  adjustHeight()
})

// 控制输入框高度
const adjustHeight = (flag) => {
  if (flag) {
    setTimeout(()=>{
      talkFoot.value.style.height = '60px'
    }, 0)
  } else {
    setTimeout(()=>{
      switch ( foot_input_copy.value.scrollHeight ) {
        case 38: rowsNum.value = 1; talkFoot.value.style.height = '60px' ;break;
        case 50: rowsNum.value = 2; talkFoot.value.style.height = '66px' ;break;
        case 75: rowsNum.value = 3; talkFoot.value.style.height = '91px';break;
        default: rowsNum.value = 4; talkFoot.value.style.height = '116px';break;
      }
      if (messageInput.value===''){
        rowsNum.value = 1; talkFoot.value.style.height = '60px'
      }
      if (rowsNum.value === 1){
        foot_input.value.style.margin = 'auto'
      } else {
        foot_input.value.style.margin = '5px auto'
      }
      const toBottomButton = document.querySelector('.mobile_to_bottom_button')
      if (toBottomButton) {
        toBottomButton.style.bottom = 80 + (rowsNum.value - 1) * 25 + 'px'
      }
      foot_input.value.style.height = rowsNum.value * 25 + 'px'
      foot_input_copy.value.style.height = rowsNum.value * 25 + 'px'
      scrollToBottom()
    }, 0)
  }

  setTimeout(()=>{
    talkBody.value.style.bottom = talkFoot.value.style.height
  }, 0)
}

// 控制录音提示的位置
const adjustRecordHintBox = () => {
  if (recordingBox.value) {
    setTimeout(()=>{
      recordingBox.value.style.bottom = (window.visualViewport.height - 130) / 2 - 30  + 'px'
      recordingBox.value.style.left = recording_block.value.clientWidth/ 2 - recordingBox.value.clientWidth / 2 + 'px'
    }, 0)
  }
}
// 键盘监听事件
document.addEventListener('keydown', function(event) {
  // 判断按下的键是否是删除键，del键，回车发送键，撤回键
  if (event.key === 'Backspace' || event.key === 'Delete' || (!event.shiftKey && event.key === 'Enter') || (event.ctrlKey && event.key === 'z') ) {
    foot_input_copy.value.style.height = 25 + 'px'
    setTimeout(()=>{
      adjustHeight()
    }, 0)
  }
  // 检测非shift+enter换行：回车发送
  if (!event.shiftKey && event.key === 'Enter') {
    event.preventDefault()
    sendMessage()
  }
})

// ---------------------------------------------------- 其他逻辑


// window.addEventListener('scroll', () => {
// })

// 鼠标滚轮滑动事件
const mousewheel = (event) => {
  // 向上滚动，取消自动滑动
  if (event.deltaY < 0) {
    isBottom.value = false
  }
  // 设置若上滑超过5 则可以滚动到底部
  isBottom.value = talkBody.value.scrollHeight - talkBody.value.scrollTop <= talkBody.value.clientHeight + 5;
  // 同时按下ctrl键，页面大小变化
  if (event.ctrlKey){
    adChange()
    adjustRecordHintBox()
  }
}
// 禁用双指缩放
document.documentElement.addEventListener('touchstart', function (event) {
  if (event.touches.length > 1) {
    event.preventDefault();
  }
}, false);
// 禁用手指双击缩放
let lastTouchEnd = 0;
document.documentElement.addEventListener('touchend', function (event) {
  let now = Date.now();
  if (now - lastTouchEnd <= 300) {
    event.preventDefault();
  }
  lastTouchEnd = now;
})
onMounted( () => {
  // 如果有缓存链接
  // if(localStorage.getItem('testURL')){
  //   testURL.value = JSON.parse(localStorage.getItem('testURL'))
  //   connect()
  // }
  // let document.querySelector('.mobile_talk_body').style.height
  connect()
  talkBody.value = document.querySelector('.mobile_talk_body')
  talkFoot.value = document.querySelector('.mobile_talk_foot')
  foot_input.value = document.querySelector('.mobile_foot_input')
  foot_input_copy.value = document.getElementById('mobile_foot_input_copy')
  recording_block.value = document.querySelector('.recording_block')
  recordingBox.value = document.querySelector('.mobile_recording')
  foot_voice.value = document.getElementById('mobile_foot_voice')
  foot_voice_copy.value = document.getElementById('mobile_foot_voice_copy')
  // let str = '<div class="mobile_machine">' +
  //           '  <div>' +
  //           '    <div class="mobile_head_pic mobile_machine_pic"></div>' +
  //           '  </div>' +
  //           '  <div class="mobile_talk_box">欢迎来到超思维智能!<br>(测试阶段，效果以正式上线为准)<br>当前为手机端界面</div>' +
  //           '</div>'
  // talkAllMessage.value.push(str)

  talkAllMessage.value.push({ message: '欢迎来到超思维智能!<br>(测试阶段，效果以正式上线为准)<br>当前为PC端页面', kind: 'machine' })
  foot_input.value.style.height = '25px'
  foot_input_copy.value.style.height = '25px'
  recordButtonRegister()
})

</script>

<template>
  <!--手机端界面-->
  <div class="mobilebody">
    <div class="mobilebody_ad"></div>
    <div class="mobile_mainbody_talk">
      <div class="mobile_talk_head">
        <div style="margin: auto;">智能Murphy</div>
      </div>
      <div class="mobile_talk_body" @scroll="mousewheel">
        <div class="recording_block" v-show="recording"/>
        <form id="mobile_uploadForm" enctype="multipart/form-data" style="display: none">
          <input type="file" name="mobile_file" accept="audio/*">
          <button type="submit">上传并转录</button>
        </form>
        <div v-show="recording" class="mobile_recording">
          <el-icon style="padding: 10px 20px 0;font-size: 60px;margin-left: auto; color: white;"><Microphone /></el-icon>
          <div style="font-size: 14px;color: white;text-align: center">录制中...</div>
        </div>
<!--        <div v-for="item in talkAllMessage" :key="item" v-html="item"/>-->
        <MobileResponseBox v-for="(item, index) in talkAllMessage" :key="index" :message="item.message" :kind="item.kind"></MobileResponseBox>
      </div>
      <div class="mobile_talk_foot">
        <div v-if="!isBottom" class="mobile_to_bottom_button" @click="clickToBottom">↓</div>
        <el-icon class="mobile_button_turn" @click="turnVoiceOrText()" v-if="!turnVoice"><Microphone /></el-icon>
        <el-icon class="mobile_button_turn" @click="turnVoiceOrText()" v-if="turnVoice"><ChatLineRound /></el-icon>
        <textarea v-model="messageInput" class="mobile_foot_input" v-show="!turnVoice"/>
        <textarea v-model="messageInput" class="mobile_foot_input_copy" v-show="!turnVoice" id="mobile_foot_input_copy"/>
        <div class="mobile_foot_voice" v-show="recordMode  && turnVoice" id="mobile_foot_voice">按住 说话</div>
        <div class="mobile_foot_voice" v-show="!recordMode && turnVoice" id="mobile_foot_voice_copy">单击开始录制</div>

        <el-popover :visible="messageIsEmpty && controlable" placement="top-end" :width="150" content="请勿发送空内容!" popper-style="box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);height: 30px;line-height: 5px;font-size: 15px">
          <template #reference>
            <el-button style="opacity: 0;height: 1px;position: absolute;right: 8px;" disabled/>
          </template>
        </el-popover>
        <el-icon class="mobile_button_turn" @click="sendMessage()" v-if="controlable" v-show="!turnVoice"><Promotion /></el-icon>
        <div class="mobile_button_turn mobile_button_stop" @click="stopConnection()" v-else>■</div>

        <el-popover placement="top-end" :width="150" popper-style="margin-bottom: 8px;box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);" :visible="popoverVisible && controlable && turnVoice">
          <el-button class="mobile_mode_choice" @click="popoverVisible=false;recordMode = true;foot_voice.innerHTML = '按住 说话';foot_voice.style.display = 'block';foot_voice_copy.style.display = 'none'">长按录音模式</el-button><br>
          <el-button class="mobile_mode_choice" @click="popoverVisible=false;recordMode = false;foot_voice_copy.innerHTML = '单击开始录制';foot_voice.style.display = 'none';foot_voice_copy.style.display = 'block'">单击录音模式</el-button>
          <template #reference>
            <el-icon class="mobile_button_turn" @click="popoverVisible=!popoverVisible;" v-if="turnVoice && controlable"><MoreFilled /></el-icon>
          </template>
        </el-popover>
      </div>
    </div>
  </div>

  <!--  <div class="mobile_beian" v-if="isMobile">-->
  <!--    <div class="mobile_beian_pic"/>-->
  <!--    <div style="border-left: 2px solid gray;"></div>-->
  <!--    <div>-->
  <!--      <div style="height: 30px">-->
  <!--        <div class="mobile_beian_other">联系我们：1************@supermurphy.com</div>-->
  <!--        <div class="mobile_beian_other">电话：1****************</div>-->
  <!--      </div>-->
  <!--      <div style="display: flex;height: 20px">-->
  <!--        <div style="margin-top: 0"><a href="https://beian.miit.gov.cn/" class="mobile_icp">粤ICP备2023152770号</a></div>-->
  <!--        <div class="mobile_gwab">&nbsp;/&nbsp;粤公网安备11***********号</div>-->
  <!--      </div>-->
  <!--    </div>-->
  <!--  </div>-->
</template>

<style>
.mobile_beian{
  width: 100%;
  height: 50px;
  background-color: #EFF4F9;
  position: absolute;
  bottom: -60px;
  display: flex;
  padding-top: 5px;
  padding-bottom: 5px;
  justify-content: space-around;
}
.mobile_beian_pic{
  width: 50px;
  height: 50px;
  background-image: url('../assets/logo3.png');
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}
.mobile_beian_other{
  color: #6A7176;
  font-size: 13px;
  line-height: 17px;
  margin: auto;
}
.mobile_icp{
  font-size: 13px;
  color: #999AAA;
  cursor: pointer;
  text-decoration: none;
}
.mobile_gwab {
  font-size: 12px;
  color: #6A7176;
  margin-top: 4px;
}
/* 手机部分样式 */
.mobilebody{
  width: 100vw;
  position: fixed;
  top: 40px;
  bottom: 0;
  box-sizing: border-box;
}
.mobilebody::-webkit-scrollbar {
  width: 0;
}
.mobile_mainbody_talk {
  width: 100vw;
  border: 2px solid rgba(15, 178, 145, 0.5);
  border-radius: 5px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  position: absolute;
  top: 60px;
}
.mobile_talk_head{
  height: 30px;
  line-height: 30px;
  display: flex;
  background-color: rgb(240, 251, 255);
  border-radius: 5px;
}
.mobile_voiceButton {
  width: 2rem;
  height: 2rem;
  border-radius: 2rem;
  position: absolute;
  top: 4px;
  left: 0.5rem;
  cursor: pointer;
  border: 1px solid red;
  /*box-sizing: border-box;*/
  background-image: url("/src/assets/novoice.jpg");
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}
.mobile_talk_body {
  width: 100%;
  box-sizing: border-box;
  background-color: #fff;
  border-top: rgba(15, 178, 145, 0.7) 3px solid;
  margin-bottom: 0;
  overflow: auto;
  position: fixed;
  bottom: 60px;
  top: 130px;
  border-left: rgba(15, 178, 145, 0.7) 1px solid;
  border-right: rgba(15, 178, 145, 0.7) 1px solid;
  left: 0;
  transition: all 0.3s;
}

.mobile_talk_body::-webkit-scrollbar {
  width: 0;
}
.mobile_talk_body::-webkit-scrollbar-thumb {
  background-color: #bbb; /* 设置滚动条的颜色为浅灰色 */
}
.mobile_talk_body::-webkit-scrollbar-track {
  background-color: #fff; /* 设置滚动条背景颜色为纯白色 */
}
.recording_block{
  position: fixed;
  top: 132px;
  bottom: 60px;
  left: 2px;
  right: 2px;
  background-color: rgba(0, 0, 0, 0.6);
  z-index: 1;
}
/*.mobile_machine {*/
/*  display: flex;*/
/*  margin: 5px 3rem 10px auto;*/
/*}*/
/*.mobile_human {*/
/*  display: flex;*/
/*  margin: 0 auto auto 3rem;*/
/*}*/
/*.mobile_head_pic {*/
/*  width: 2.4rem;*/
/*  height: 2.4rem;*/
/*  border-radius: 0.4rem;*/
/*  border: solid 1px gray;*/
/*  margin: 3px;*/
/*  background-position: center;*/
/*  background-size: cover;*/
/*  background-repeat: no-repeat;*/
/*}*/
/*.mobile_machine_pic {*/
/*  background-image: url('/src/assets/logo.png');*/
/*  background-position: center bottom 2px;*/
/*}*/
/*.mobile_human_pic {*/
/*  background-image: url('/src/assets/user.jpg');*/
/*}*/

/*!*手机端对话框内容*!*/
/*.mobile_talk_box {*/
/*  min-width: 20px;*/
/*  height: auto;*/
/*  border-radius: 5px;*/
/*  border: 1px solid black;*/
/*  margin: 3px auto auto 2px;*/
/*  padding: 8px 6px;*/
/*  overflow-x: auto;*/
/*  scrollbar-width: thin;*/
/*  font-size: 1rem;*/
/*  line-height: 1.4rem;*/
/*}*/
/*.mobile_talk_box::-webkit-scrollbar {*/
/*  height: 5px; !* 设置横向滚动条的高度 *!*/
/*}*/
/*.mobile_talk_box::-webkit-scrollbar-thumb {*/
/*  background-color: #ccc; !* 设置滚动条的颜色为浅灰色 *!*/
/*  border-radius: 5px;*/
/*}*/
/*.mobile_talk_box::-webkit-scrollbar-track {*/
/*  background-color: #fff; !* 设置滚动条背景颜色为纯白色 *!*/
/*  border-radius: 5px;*/
/*}*/
/*.mobile_right {*/
/*  margin: 3px 2px auto auto;*/
/*  padding: 8px 8px;*/
/*  min-width: 10px;*/
/*}*/
.mobile_talk_foot {
  width: 100%;
  height: 60px;
  display: flex;
  margin-top: 0;
  box-sizing: border-box;
  background-color: rgb(240, 251, 255);
  border: rgba(15, 178, 145, 0.7) 2px solid;
  border-top: rgba(15, 178, 145, 0.7) 3px solid;
  position: fixed;
  bottom: 0;
  left: 0;
}
.mobile_mode_choice{
  width: 100%;
  margin: auto;
  /*border: 1px solid red;*/
  text-align: center;
}
.mobile_button_turn {
  border: 2px solid black;
  width: 2rem;
  min-width: 2rem;
  height: 2rem;
  border-radius: 2rem;
  margin: auto 8px;
  color: black;
  box-sizing: border-box;
  transition: border 0.1s;
  font-size: 20px;
  cursor: pointer;
  /* 禁止选中，禁用高亮效果 */
  user-select: none;
  -webkit-tap-highlight-color: transparent;
}
.mobile_button_turn:hover {
  color: #3498db;
  border: 2px solid #3498db;
  background-color: rgb(226, 245, 255);
}
.mobile_button_stop{
  color: red;
  border-radius: 0.5rem;
  text-align: center;
  line-height: 1.5rem;
  border: 2px solid red;
}
.mobile_foot_input {
  padding: 0 2px;
  resize: none;
  margin: auto;
  border-radius: 5px;
  font-size: 1rem;
  transition: border 0.3s;
  border: 2px solid #dddddd;
  line-height: 25px;
  min-height: 2.4rem;
  flex: 1;
}
.mobile_foot_input:focus {
  outline: none;
  border: 2px solid #3498db;
}
.mobile_foot_input_copy{
  padding: 0 2px;
  resize: none;
  margin: auto;
  border-radius: 5px;
  font-size: 1rem;
  transition: border 0.3s;
  border: 2px solid #dddddd;
  line-height: 25px;
  min-height: 2.4rem;
  flex: 1;

  position: fixed;
  bottom: 10px;
  left: 49px;
  right: 50px;
  z-index: -1;
  opacity: 0;
}

.mobile_foot_input::-webkit-scrollbar, .mobile_foot_input_copy::-webkit-scrollbar {
  width: 0;
}

.mobile_foot_voice {
  margin: auto 5px;
  border-radius: 5px;
  font-size: 1rem;
  line-height: 2.1rem;
  text-align: center;
  cursor: pointer;
  min-height: 2.1rem;
  color: #fff;
  text-decoration: none;
  background-color: #80CCBD;
  border-bottom: 5px solid #66A397;
  -webkit-transition: all 0.05s;
  flex: 1;
  /* 禁止选中，禁用高亮效果 */
  user-select: none;
  -webkit-tap-highlight-color: transparent;
}
.mobile_foot_voice:active {
  transform: translate(0px,3px);
  border-bottom: 2px solid #2ecc71;
}
.mobile_recording {
  width: 100px;
  height: 100px;
  color: white;
  position: fixed;
  background-color: rgba(0, 0, 0, 0.7);
  border-radius: 10px;
}
.mobile_to_bottom_button {
  width: 40px;
  height: 40px;
  position: absolute;
  right: 40px;
  bottom: 80px;
  border-radius: 20px;
  border: 2px solid black;
  box-sizing: border-box;
  background-color: #eee;
  text-align: center;
  line-height: 40px;
  cursor: pointer;
  z-index: 1;
  /* 禁止选中，禁用高亮效果 */
  user-select: none;
  -webkit-tap-highlight-color: transparent;
}
.mobilebody_ad{
  height: 60px;
  border: 1px solid black;
  box-sizing: border-box;
  margin: 0 auto;
  background-image: url('/src/assets/mobile_ad1.png');
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}
</style>