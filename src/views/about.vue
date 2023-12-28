<script setup>
import { ref, onMounted } from 'vue'

const clickit = () => {
}
onMounted(()=>{
  setTimeout(()=>{
    const loader = document.querySelector('.c1')
    loader.style.transform = "translateX(0)";
  }, 1000)
})
</script>

<template>
  <div>关于</div>
  <div class="c1" @click="clickit">1Hello, this is an animated component!</div>
  <div class="c2" @click="clickit">2Hello, this is an animated component!</div>
</template>

<style scoped>
.c1, .c2{
  transition: all 2s;
  width: 600px;
  height: 200px;
  background-color:paleturquoise;
  margin: 100px;
  cursor:pointer;

  transform: translateX(-100px); /* 初始时从左往右偏移 */
}
</style>
