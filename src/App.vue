<script setup>
</script>

<template>
  <router-view/>
</template>

<style>
  body{
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
  }
  .body::-webkit-scrollbar {
    width:0;
  }
</style>
