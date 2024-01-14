<script setup>
import { ref, onMounted} from 'vue'
import { CopyDocument, Check } from '@element-plus/icons-vue'
const props = defineProps({
  message: String,
  kind: String
})
let showCopy = ref(false)
let copyOK = ref(false)
let machineTalkBox = ref()
let copyArea = ref()
// 复制文本函数
const copyContent = () => {
  copyOK.value = true
  navigator.clipboard.writeText(machineTalkBox.value.innerText)
  setTimeout(() => {
    copyOK.value = false
    showCopy.value = false
  }, 2000)
}
const copyAlready = () => {
  if(!copyOK.value){
    showCopy.value = false
  }
}
const showCopyArea = () => {
  copyArea.value.style.opacity = '1'
  showCopy.value = true
}
onMounted(()=>{

})
</script>

<template>
<!--  AI区域-->
  <div class="machine" v-if="props.kind==='machine'" @mouseenter="showCopyArea()" @mouseleave="copyAlready">
    <div>
      <div class="head_pic machine_pic"></div>
    </div>

    <div class="talk_box" v-html="message" ref="machineTalkBox"/>

    <div style="position: relative;flex: 1;min-width: 75px;opacity: 0;" ref="copyArea">
      <el-icon v-show="showCopy && !copyOK" class="content_copy" @click="copyContent"><CopyDocument /></el-icon>
      <el-icon v-show="showCopy && copyOK" class="content_copy_ok"><Check /></el-icon>
      <div v-show="showCopy && copyOK" class="hint">已复制</div>
    </div>
  </div>

<!--  用户区域-->
  <div class="human" v-if="props.kind==='human'">
    <div class="talk_box" style="margin-left: auto;">
      {{message}}
    </div>
    <div>
      <div class="head_pic human_pic"/>
    </div>
  </div>
</template>

<style>

.machine {
  display: flex;
  margin: 0 0 0 5px;
}
.head_pic {
  width: 60px;
  height: 60px;
  border-radius: 30px;
  border: solid 1px gray;
  margin: 5px;
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}

.machine_pic {
  background-image: url('/src/assets/logo.png');
  background-position: center bottom 5px;
}
.human {
  display: flex;
  margin: 0 5px 0 75px;
  height: auto;
}
.human_pic {
  background-image: url('/src/assets/user.jpg');
}
/*对话框内容*/
.talk_box {
  min-width: 20px;
  height: auto;
  border-radius: 5px;
  border: 1px solid black;
  padding: 7px 10px 7px 10px;
  /*box-shadow: 5px 5px 13px 0 rgba(0, 0, 0, 0.3);*/
  overflow-x: auto;
  scrollbar-width: thin;
  scrollbar-color: #ccc #fff; /* 设置滚动条颜色和背景颜色 */
  font-size: 15px;
  line-height: 45px;
  margin: 5px;
}
.talk_box_adjust{
  line-height: 30px;
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
.content_copy{
  height: 20px;
  width: 20px;
  position: absolute;
  bottom: 0;
  margin: auto auto 5px 0;
  cursor: pointer;
  font-size: 18px;
}
.content_copy_ok{
  height: 20px;
  width: 20px;
  position: absolute;
  bottom: 0;
  margin: auto auto 5px 0;
  cursor: pointer;
  font-size: 22px;
}
.hint{
  height: 20px;
  position: absolute;
  bottom: 0;
  margin: auto auto 5px 22px;
  font-size: 13px;
  line-height: 19px;
  color: rgba(0, 0, 0, 0.9);
}
</style>