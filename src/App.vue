<script setup>
</script>

<template>
  <router-view/>
</template>

<style>
  html{
    /*scroll-padding-top: 100vh*/
  }
  body{
    width: 100vw;
    margin: 0;
    padding: 0;
    border: 0;
    font: inherit;
    vertical-align: baseline;
    /*min-width: 1000px;*/
    overflow-x: hidden;
    background-color: #fff;
    /*touch-action: none; !* 禁止触摸操作 *!*/
    /*position: fixed; !* 固定位置 *!*/
    /*position: sticky;*/
    /*bottom: 0;*/
    /*height: calc(100vh + 60px);*/
    height: 100vh;
  }
  .body::-webkit-scrollbar {
    width:0;
  }
</style>
