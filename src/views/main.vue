<script setup>
import { ref, watch, onMounted } from 'vue'
import axios from 'axios'
// import ElMessage, {ElMessageBox, ElementPlus} from "element-plus";
const messageInput = ref('')
const message = ref('')
const rowsNum = ref(3)
const answer = ref('')
const talkAllMessage = ref([])
const history = ref([])
let lastChild = ref()
let talkBody = ref()
let buttonText = ref('发送')
// 用户是否可输入
let controlable = ref(true)
const modelValue = ref('1.0')
const modelOptions = ref([{
  value: '1.0',
  label: 'Murphy-1.0'
},{
  value: '2.0',
  label: 'Murphy-2.0'
}])

// 过滤器，过滤用户携带的<>括号
function escapeHtml(value) {
  // 将 < 替换为 &lt;，将 > 替换为 &gt;
  return value.replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
// 发送消息
const sendMessage = async () => {
  message.value = escapeHtml(messageInput.value)
  if (messageInput.value === '' || controlable.value === false) {
    return
  }
  controlable.value = false
  buttonText.value = ''
  let str =
      '<div class="human">' +
      '  <div class="talk_box right">' + message.value + '</div>' +
      '  <div><div class="head_pic human_pic"></div></div>' +
      '</div>'
  talkAllMessage.value.push(str)
  // 用户发送消息，滑动到底部
  setTimeout(() => {
    scrollToBottom()
    const foot_input = document.querySelector('.foot_input')
    // 清空输入框
    messageInput.value = ''
    foot_input.value = ''
    foot_input.style.height = 25 + 'px'
  }, 10)
  // AI回复样式框架
  str = '<div class="machine">' +
        '  <div><div class="head_pic machine_pic"></div></div>' +
        '  <div class="talk_box">......</div>' +
        '</div>'

  // 半秒后显示AI回复的框架
  setTimeout(() => {
    talkAllMessage.value.push(str)
  }, 500)

  // 访问参数
  const data = {
    message: message.value,
    mode: "chat",
    history: history.value
  }

  // AI回复消息，窗口滑动到底部
  setTimeout(() => {
    scrollToBottom()
    const children = talkBody.value.children;
    lastChild = children[children.length - 1];
    connect()
    // const response = axios.post('/api', data );
    // // 询问成功
    // response.then((result) => {
    //   answer.value = result.data.response
    //   history.value.push(result.data.history[result.data.history.length-2])
    //   history.value.push(result.data.history[result.data.history.length-1])
    //   localStorage.setItem('talkHistory', JSON.stringify(history.value))
    //   // AI开始回答，清空省略号，逐字打印
    //   lastChild.querySelector('.talk_box').textContent = ''
    //   printText(0);
    // })
    // // 询问失败
    // .catch((error) => {
    //   console.error("服务错误:", error);
    // });
  }, 550)
}

// 平滑滚动到底部
const scrollToBottom = () => {
  talkBody.value.scrollTo({
    top: talkBody.value.scrollHeight,
    behavior: 'smooth',
  });
}

// 递归实现逐字打印
function printText(index) {
  scrollToBottom()
  const target = lastChild.querySelector('.talk_box')
  if (index < answer.value.length) {
    target.textContent += answer.value.charAt(index);
    setTimeout(function() {
      printText(index + 1);
    }, 1);
  } else {
    controlable.value = true
    buttonText.value = '发送'
  }
}

// 清除历史
const clearHistory = () => {
  ElMessageBox.confirm('是否清空会话历史?当前窗口的数据记录将会丢失!', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
  .then(() => {
    history.value.splice(1, history.value.length - 1)
    localStorage.setItem('talkHistory', JSON.stringify(history.value))
    ElMessage.success('已清空')
  })
  .catch(() => {

  })
}

// 监听输入内容变化
watch(messageInput, () => {
  adjustHeight();
})
// 控制输入框高度
const adjustHeight = () => {
  const foot_input = document.querySelector('.foot_input')
  // console.log('当前滚动高度为：' + foot_input.scrollHeight)
  switch ( foot_input.scrollHeight ) {
    case 35: rowsNum.value = 1;break;
    case 60: rowsNum.value = 2;break;
    case 85: rowsNum.value = 3;break;
    case 110: rowsNum.value = 4;break;
    case 135: rowsNum.value = 5;break;
    default: rowsNum.value = 6;break;
  }
  foot_input.style.height = rowsNum.value * 25 + 'px'
  scrollToBottom()
  // console.log('当前行数：' + rowsNum.value)
};
// 键盘监听事件
document.addEventListener('keydown', function(event) {
  // 判断按下的键是否是删除键
  if (event.key === 'Backspace' || event.key === 'Delete' || (!event.shiftKey && event.key === 'Enter') || (event.ctrlKey && event.key === 'z') ) {
    const foot_input = document.querySelector('.foot_input')
    foot_input.style.height = 25 + 'px'
  }
  // 检测非换行：回车发送
  if (!event.shiftKey && event.key === 'Enter') {
    event.preventDefault();
    sendMessage()
  }
})

const connect = () => {
  console.log('连接开启')
  // 双向通信
  const socket = new WebSocket('ws://localhost:3001');
  lastChild.querySelector('.talk_box').textContent = ''
  socket.addEventListener('message', (event) => {
    answer.value = JSON.parse(event.data);
    // console.log(answer.value)
    // AI开始回答，清空省略号
    scrollToBottom()
    // printText(0)
    const target = lastChild.querySelector('.talk_box')
    target.textContent = answer.value
  });

  socket.addEventListener('close', () => {
    console.log('连接已关闭，请继续输入');
    controlable.value = true
    buttonText.value = '发送'
  });
}

onMounted( () => {
  let str = '<div class="machine">' +
            '  <div>' +
            '    <div class="head_pic machine_pic"></div>' +
            '  </div>' +
            '  <div class="talk_box">欢迎来到超思维智能！</div>' +
            '</div>'
  talkAllMessage.value.push(str)
  talkBody.value = document.querySelector('.talk_body')
  document.querySelector('.foot_input').style.height = '25px'
  if (localStorage.getItem('talkHistory')) {
    history.value = JSON.parse(localStorage.getItem('talkHistory'))
  } else {
    history.value.push({"role": "system","content": "你是一个智能聊天对话助手，你需要尽可能的回答用户的问题，并与对方亲切的交流。"})
    localStorage.setItem('talkHistory', JSON.stringify(history.value))
  }
})
</script>

<template>
  <div class="all">
    <div class="head">
      <div style="height: 100%;display: flex">
        <img src="../assets/logo2.png" class="head_icon">
      </div>
      <div class="head_navigation">
        <div class="navigation_button">首页</div>
        <div class="navigation_button">商城</div>
        <div class="navigation_button">关于</div>
        <div class="navigation_button">联系我们</div>
      </div>
    </div>
    <div class="mainbody">
      <div class="mainbody_talk">
        <div class="talk_head">
          <el-select v-model="modelValue" placeholder="请选择">
            <el-option
                v-for="item in modelOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value">
            </el-option>
          </el-select>
          <div>智能Murphy</div>
<!--          <el-button @click="clearHistory()">清空会话历史</el-button>-->
          <button @click="clearHistory()">清空会话历史</button>
        </div>
        <div class="talk_body">
          <div v-for="item in talkAllMessage" :key="item" v-html="item"/>
        </div>
        <div class="talk_foot">
          <textarea v-model="messageInput" placeholder="请输入内容" class="foot_input" />
          <button @click="sendMessage()" v-if="controlable">发送</button>
          <el-button style="border: 1px solid black;" @click="sendMessage()" disabled loading v-else/>
        </div>
      </div>
      <div class="mainbody_ad"></div>
    </div>
  </div>
</template>

<style>
  .all{
    height: 100vh;
    position: relative;
  }
  /* 头部部分 */
  .head{
    width: 100vw;
    height: 50px;
    min-width: 1000px;
    /*border: 1px solid black;*/
    /*background-color: paleturquoise;*/
    background-color: rgba(0, 212, 255, 0.3);
    margin: auto;
    display: flex;
  }
  .head_icon{
    background-size: cover;
    margin: 5px 20px 5px 20px;
  }
  .head_navigation{
    width: 50vw;
    height: 100%;
    float: right;
    flex: 1;
    box-sizing: border-box;
    display: flex;
    justify-content: flex-end;
  }
  .navigation_button{
    float: right;
    width: 160px;
    height: 100%;
    text-align: center;
    line-height: 50px;
    margin-right: 0;
    box-sizing: border-box;
    cursor: pointer;
    /*border-left: 1px solid black;*/
    font-size: 16px;
    transition: all 0.2s;
  }
  .navigation_button:hover{
    color: #007F99;
    font-size: 18px;
    -webkit-text-stroke: 1px rgba(15, 178, 145, 1);
    text-stroke: 1px rgba(15, 178, 145, 0.7);
    border-bottom: rgba(15, 178, 145, 0.7) solid 5px;
  }
  /* 主体部分 */
  .mainbody{
    width: 100vw;
    min-width: 1000px;
    min-height: 800px;
    box-sizing: border-box;
    display: flex;
    padding: 10px;
    /*高度充满父容器*/
    position: absolute;
    top: 50px;
    bottom: 0;
  }
  .mainbody_talk{
    width: 70vw;
    min-width: 700px;
    height: 96%;
    /*border: 5px solid rgba(0, 212, 255, 1);*/
    border: 7px solid rgba(15, 178, 145, 0.5);
    /*background-color: paleturquoise;*/
    border-radius: 3px;
    margin: auto 20px;
    box-sizing: border-box;
    position: relative;
    display: flex;
    flex-direction: column;
    box-shadow: 15px 15px 10px 0 rgba(0, 0, 0, 0.3);
  }
  .talk_head{
    height: 50px;
    line-height: 50px;
    display: flex;
    background-color: rgb(240, 251, 255);
    position: relative;
  }
  .talk_head .el-select{
    width: 150px;
    position: absolute;
    margin: 9px auto auto 15px;
    border-radius: 5px;
  }
  .talk_head div {
    margin: auto;
  }
  .talk_head button {
    width: 100px;
    height: 80%;
    margin: 5px 15px auto auto;
    position: absolute;
    right: 0;
    border: 1px solid gray;
    color: black;
    border-radius: 5px;
    cursor: pointer;
    background-color: #fff;
  }
  .talk_body{
    width: 100%;
    box-sizing: border-box;
    background-color: #fff;
    border-top: rgba(15, 178, 145, 0.7) 3px solid;
    border-bottom: rgba(15, 178, 145, 0.7) 3px solid;
    flex: 1;
    padding: 10px;
    margin-bottom: 0;
    overflow: auto;
  }
  .talk_body::-webkit-scrollbar {
    width: 0;
  }
  .head_pic{
    width: 60px;
    height: 60px;
    border-radius: 30px;
    border: solid 1px gray;
    margin: 5px;
    background-position: center;
    background-size: cover;
    background-repeat: no-repeat;
  }
  .machine_pic{
    background-image: url('../assets/logo.png');
    background-position: center bottom 5px;
  }
  .human_pic{
    background-image: url('../assets/user.jpg');
  }
  .talk_box{
    min-width: 20px;
    height: auto;
    border-radius: 5px;
    border: 1px solid black;
    margin: 10px;
    padding: 5px 10px;
    /*box-shadow: 5px 5px 13px 0 rgba(0, 0, 0, 0.3);*/
    line-height: 40px;
    overflow-x: auto;
    scrollbar-width: thin;
    scrollbar-color: #ccc #fff; /* 设置滚动条颜色和背景颜色 */
  }
  .talk_box::-webkit-scrollbar {
    height: 10px; /* 设置横向滚动条的高度 */
  }

  .talk_box::-webkit-scrollbar-thumb {
    background-color: #ccc; /* 设置滚动条的颜色为浅灰色 */
    border-radius: 5px;
  }

  .talk_box::-webkit-scrollbar-track {
    background-color: #fff; /* 设置滚动条背景颜色为纯白色 */
    border-radius: 5px;
  }
  .machine{
    display: flex;
    margin: 10px 50px auto auto;
  }
  .human{
    display: flex;
    margin: 10px auto auto 50px;
  }
  .right{
    margin-left: auto;
  }
  .talk_foot{
    width: 100%;
    display: flex;
    margin-top: 0;
    background-color: rgb(240, 251, 255);
  }
  .talk_foot button{
    width: 6vw;
    min-width: 70px;
    height: 38px;
    margin: auto auto 10px auto;
    color: black;
    border: 1px solid black;
    border-radius: 5px;
    cursor: pointer;
    background-color: #fff;
  }
  .talk_foot button:hover, .talk_head button:hover{
    color: #3498db;
    border: 1px solid #3498db;
    background-color: rgb(236, 245, 255);
  }
  .foot_input{
    padding: 5px 10px 5px 10px;
    width: 55vw;
    min-width: 575px;
    resize: none;
    margin: 10px 0 10px 10px;
    border-radius: 5px;
    font-size: 20px;
    transition: border 0.3s;
    border: 2px solid #dddddd;
    line-height: 25px;
  }
  .foot_input:focus {
    outline: none;
    border: 2px solid #3498db;
  }
  /*广告*/
  .mainbody_ad{
    width: 300px;
    border: 1px solid black;
    margin: 50px auto;
    box-sizing: border-box;
    background-image: url('../assets/ad.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    box-shadow: 15px 15px 10px 0 rgba(0, 0, 0, 0.3);
    cursor: pointer;
  }
</style>