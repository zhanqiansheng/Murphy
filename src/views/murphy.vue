<script setup>
import {onBeforeMount, ref} from 'vue'
import { useRouter } from 'vue-router';

const router = useRouter();
// 获取当前路由路径
const currentPath = router.currentRoute.value;

const isActive = (value) => {
  return currentPath.path === value
}
const handleNavigationClick = (event) => {
    const targetLink = event.target
    // 移除所有带有 'active' 类的子组件的 'active' 类
    const links = document.querySelectorAll('.' + mobile + 'navigation_button')
    links.forEach(link => {
      if (link.classList.contains(mobile + 'active')) {
        link.classList.remove(mobile + 'active')
      }
    })
    // 给当前点击的导航链接加上 'active' 类
    targetLink.classList.add(mobile + 'active')
}

let mobile = ''
const isMobile = ref(false) // 通过屏幕比例判断样式启用类型为电脑/手机// 计算屏幕的宽高比
const checkScreen = () => {
  const temp = window.innerWidth / window.innerHeight
  isMobile.value = temp <= 1
  if(isMobile.value) {
    mobile = 'mobile_'
  } else {
    mobile = ''
  }
}
// 监听窗口大小变化，设置界面样式
window.addEventListener('resize', () => {
  checkScreen()
});
onBeforeMount(() => {
  checkScreen()
})
</script>

<template>
  <div class="all">
    <div class="head" v-if="!isMobile">
      <div style="height: 100%;display: flex">
        <img src="../assets/logo2.png" class="head_icon">
      </div>
      <div class="head_navigation" @click="handleNavigationClick">
        <router-link :class="{'navigation_button':1, 'active': isActive('/main')}" to="/main">首页</router-link>
        <router-link :class="{'navigation_button':1, 'active': isActive('/shop')}" to="/shop">商城</router-link>
        <router-link :class="{'navigation_button':1, 'active': isActive('/about')}" to="/about">测试</router-link>
        <router-link :class="{'navigation_button':1, 'active': isActive('/contact')}" to="/contact">测试</router-link>
      </div>
    </div>
    <div class="mobile_head" v-if="isMobile">
      <div style="height: 40px;display: flex">
        <img src="../assets/logo2.png" class="mobile_head_icon">
      </div>
      <div class="mobile_head_navigation" @click="handleNavigationClick">
        <router-link :class="{'mobile_navigation_button':1, 'mobile_active': isActive('/main')}" to="/main">首页</router-link>
        <router-link :class="{'mobile_navigation_button':1, 'mobile_active': isActive('/shop')}" to="/shop">商城</router-link>
        <router-link :class="{'mobile_navigation_button':1, 'mobile_active': isActive('/about')}" to="/about">关于</router-link>
        <router-link :class="{'mobile_navigation_button':1, 'mobile_active': isActive('/contact')}" to="/contact">联系</router-link>
      </div>
    </div>
    <router-view/>
  </div>
</template>


<style scoped>
  .all {
    width: 100vw;
    height: 100vh;
    position: relative;
  }

  .mobile_head{
    width: 100%;
    height: 40px;
    background-color: #CCF6FF;
    margin: auto;
    display: flex;
    position: fixed;
    /*bottom: 60px;*/
    top: 0;
    left: 0;
    z-index: 1;
  }
  .mobile_head_icon{
    max-width: 126px;
    background-size: cover;
    margin: 5px;
  }
  .mobile_head_navigation {
    width: 200px;
    height: 100%;
    /*float: right;*/
    margin-left: auto;
    box-sizing: border-box;
    display: flex;
  }
  .mobile_navigation_button {
    color: black;
    text-decoration: none;
    float: right;
    min-width: 50px;
    height: 100%;
    text-align: center;
    line-height: 40px;
    margin-right: 0;
    box-sizing: border-box;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
  }
  .mobile_active {
    color: #007F99;
    font-size: 16px;
    -webkit-text-stroke: 1px rgba(15, 178, 145, 1);
    text-stroke: 1px rgba(15, 178, 145, 0.5);
    border-bottom: rgba(15, 178, 145, 0.5) solid 5px;
    border-bottom: none;
  }


  /* 头部部分 */
  .head {
    width: 100vw;
    height: 50px;
    min-width: 1000px;
    /*border: 1px solid black;*/
    /*background-color: paleturquoise;*/
    background-color: rgba(0, 212, 255, 0.2);
    margin: auto;
    display: flex;
  }

  .head_icon {
    background-size: cover;
    margin: 5px 20px 5px 20px;
  }

  .head_navigation {
    width: 60vw;
    height: 100%;
    float: right;
    flex: 1;
    box-sizing: border-box;
    display: flex;
    justify-content: flex-end;
  }

  .navigation_button {
    color: black;
    text-decoration: none;
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

  .active, .navigation_button:hover {
    color: #007F99;
    font-size: 18px;
    -webkit-text-stroke: 1px rgba(15, 178, 145, 1);
    text-stroke: 1px rgba(15, 178, 145, 0.7);
    border-bottom: rgba(15, 178, 145, 0.7) solid 5px;
  }

  .active {
    border-bottom: none;
  }

  .shopBackground {
    box-sizing: border-box;
    position: absolute;
    margin-top: 50px;
    top: 0;
    bottom: 0;
    display: flex;
    flex-direction: column; /* 垂直排布 */
    align-items: center; /* 水平居中对齐 */
  }
</style>