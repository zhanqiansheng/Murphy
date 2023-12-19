<script setup>
import { ref, onMounted } from 'vue'

onMounted(() => {
  setTimeout(()=>{
    const c1 = document.querySelector('.c1')
    const c2 = document.querySelector('.c2')
    c1.style.opacity = "1";
    c2.style.opacity = "1";
    c1.style.transform = "translateX(0)";
    c2.style.transform = "translateX(0)";
  }, 10)
})
</script>

<template>
  <div class="shopBackground">
    <div class="cardBody c1">
      <img src="/src/assets/good1.png" class="card">
    </div>
    <div class="cardBody c2">
      <img src="/src/assets/good2.png" class="card">
    </div>
  </div>
</template>

<style scoped>
.cardBody{
  margin: auto;
  transition: all 0.8s;
  opacity: 0.5;
}
.c1{
  transform: translateX(-100px); /* 初始时从左往右偏移 */
}
.c2{
  transform: translateX(100px); /* 初始时从左往右偏移 */
}
.card{
  box-sizing: border-box;
  width: 100vw;
  margin: auto;
  cursor: pointer;
}
</style>