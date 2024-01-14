<script setup>
import { ref } from 'vue'
import { CopyDocument, Check } from '@element-plus/icons-vue'
const props = defineProps({
  message: String,
  kind: String
})
let copyOK = ref(false)
let machineTalkBox = ref()
// 复制文本函数
const mobile_copyContent = () => {
  copyOK.value = true
  navigator.clipboard.writeText(machineTalkBox.value.innerText)
  setTimeout(() => {
    copyOK.value = false
  }, 2000)
}
</script>

<template>
  <!--  AI区域-->
  <div class="mobile_machine" v-if="props.kind==='machine'">
    <div>
      <div class="mobile_head_pic mobile_machine_pic"></div>
    </div>

    <div class="mobile_talk_box" v-html="message" ref="machineTalkBox"/>

    <div style="position: relative;flex: 1;min-width: 3rem">
      <el-icon v-show="!copyOK" class="mobile_content_copy" @click="mobile_copyContent"><CopyDocument /></el-icon>
      <el-icon v-show="copyOK" class="mobile_content_copy_ok"><Check /></el-icon>
    </div>
  </div>

  <!--  用户区域-->
  <div class="mobile_human" v-if="props.kind==='human'">
    <div class="mobile_talk_box" style="margin-left: auto;">
      {{message}}
    </div>
    <div>
      <div class="mobile_head_pic mobile_human_pic"/>
    </div>
  </div>
</template>

<style>
.mobile_machine {
  display: flex;
  margin: 5px 0 10px auto;
}
.mobile_human {
  display: flex;
  margin: 0 auto auto 3rem;
}
.mobile_head_pic {
  width: 2.4rem;
  height: 2.4rem;
  border-radius: 0.4rem;
  border: solid 1px gray;
  margin: 3px;
  background-position: center;
  background-size: cover;
  background-repeat: no-repeat;
}
.mobile_machine_pic {
  background-image: url('/src/assets/logo.png');
  background-position: center bottom 2px;
}
.mobile_human_pic {
  background-image: url('/src/assets/user.jpg');
}

/*手机端对话框内容*/
.mobile_talk_box {
  min-width: 20px;
  height: auto;
  border-radius: 5px;
  border: 1px solid black;
  margin: 3px 0 auto 2px;
  padding: 8px 6px;
  overflow-x: auto;
  scrollbar-width: thin;
  font-size: 1rem;
  line-height: 1.4rem;
}
.mobile_talk_box::-webkit-scrollbar {
  height: 5px; /* 设置横向滚动条的高度 */
}
.mobile_talk_box::-webkit-scrollbar-thumb {
  background-color: #ccc; /* 设置滚动条的颜色为浅灰色 */
  border-radius: 5px;
}
.mobile_talk_box::-webkit-scrollbar-track {
  background-color: #fff; /* 设置滚动条背景颜色为纯白色 */
  border-radius: 5px;
}
/*.mobile_right {*/
/*  margin: 3px 2px auto auto;*/
/*  padding: 8px 8px;*/
/*  min-width: 10px;*/
/*}*/
.mobile_content_copy{
  height: 20px;
  width: 20px;
  position: absolute;
  bottom: 0;
  margin: auto auto 0 3px;
  cursor: pointer;
  font-size: 18px;
}
.mobile_content_copy_ok{
  height: 20px;
  width: 20px;
  position: absolute;
  bottom: 0;
  margin: auto auto 0 3px;
  cursor: pointer;
  font-size: 22px;
}
.mobile_hint{
  height: 20px;
  position: absolute;
  bottom: 0;
  margin: auto auto 0 25px;
  font-size: 13px;
  line-height: 19px;
  color: rgba(0, 0, 0, 0.9);
}
</style>