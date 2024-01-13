<script setup>
import { ref, onMounted, onBeforeMount } from 'vue'
// import Recorder from 'recorder-core'
// import 'recorder-core/src/engine/mp3'
// import 'recorder-core/src/engine/mp3-engine'
import axios from "axios";

// ---------------------------------------------------- 屏幕逻辑
const isMobile = ref(false) // 通过屏幕比例判断样式启用类型为电脑/手机
// 计算屏幕的宽高比
const checkScreen = () => {
  isMobile.value = window.innerWidth < 1000
}
onBeforeMount(() => {
  checkScreen()
})
onMounted( () => {

})

</script>

<template>
  <!--手机端界面-->
  <MobileMainBody v-if="isMobile"/>
  <!--电脑端界面-->
  <PCMainBody v-else/>

</template>

<style>
</style>