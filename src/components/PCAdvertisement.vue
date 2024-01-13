<script setup>
import { ref, onMounted } from 'vue'
// ---------------------------------------------------- 广告逻辑
// 广告图片数组
const imgList = ref(['ad1', 'ad2', 'ad3'])
import ad1 from '/src/assets/ad1.png'
import ad2 from '/src/assets/ad2.png'
import ad3 from '/src/assets/ad3.png'
let intervalId = ref()  // 广告轮播计时器id
const adIndex = ref(0) // 广告页数下标
let imgWidth = ref(0) // 广告图片宽度
// 广告自动滚动
const adChange = () => {
  const adimg = document.querySelector('.mainbody_ad img')
  imgWidth.value = parseFloat(window.getComputedStyle(adimg).width)
  const pointList = document.querySelector('.pointList')
  const imgList = document.querySelector('.mainbody_ad .img-container')
  for (let i = 0; i < pointList.children.length; i++) {
    imgList.children[i].style.transform = 'translateX(' + -imgWidth.value * adIndex.value + 'px)'
    pointList.children[i].style.backgroundColor = 'gray'
  }
  const point = pointList.children[adIndex.value]
  point.style.backgroundColor = 'white'
}
// 广告手动翻页
const adIndexChange = (value) => {
  adIndex.value += value
  if(adIndex.value === -1){
    adIndex.value = imgList.value.length - 1
  } else if(adIndex.value === imgList.value.length) {
    adIndex.value = 0
  }
  adChange()
}
// 开启定时器
const startTimer = () => {
  adChange()
  // 每三秒进行一次滚动
  intervalId.value = setInterval(()=>{
    adIndex.value++
    if (adIndex.value >= imgList.value.length) {
      adIndex.value = 0
    }
    adChange()
  }, 3000)
}
// 点击广告的下标圆点
const adChoice = (index) => {
  adIndex.value = index
  adChange()
}
// 获取海报图片路径
const getImagePath = (imageName) => {
  if (imageName === 'ad1') return ad1
  if (imageName === 'ad2') return ad2
  if (imageName === 'ad3') return ad3
}
// 注册广告按钮点击事件
const computerAdButtonRegister = () => {
  setTimeout(()=>{
    const ad = document.querySelector('.mainbody_ad')
    ad.style.transform = "translateY(0)";
    ad.style.opacity = "1";
  }, 10)

  const imgList = document.querySelector('.mainbody_ad .img-container');
  const arrowContainer = document.querySelector('.mainbody_ad .arrow-container');
  const arrowleft = document.querySelector('.arrow-container .arrowleft');
  const arrowright = document.querySelector('.arrow-container .arrowright');
  imgList.addEventListener('mouseenter', function() {
    clearInterval(intervalId.value);
    arrowleft.style.display = 'block'
    arrowright.style.display = 'block'
  })
  imgList.addEventListener('mouseleave', function() {
    startTimer()
    arrowleft.style.display = 'none'
    arrowright.style.display = 'none'
  })
  arrowContainer.addEventListener('mouseover', function() {
    clearInterval(intervalId.value);
    arrowleft.style.display = 'block'
    arrowright.style.display = 'block'
  })
  arrowContainer.addEventListener('mouseout', function() {
    arrowleft.style.display = 'none'
    arrowright.style.display = 'none'
  })
  startTimer()
}

onMounted( () => {
  computerAdButtonRegister()
})
</script>

<template>
  <div class="mainbody_ad">
    <div class="img-container" style="display: flex">
      <img v-for="item in imgList" :key="item" :src="getImagePath(item)">
    </div>
    <div class="arrow-container">
      <div class="arrowleft" @click="adIndexChange(-1)">&lt;</div>
      <div class="arrowright" @click="adIndexChange(1)">></div>
    </div>
    <div class="pointList">
      <div class="point" v-for="(item, index) in imgList.length" :key="item"  @click="adChoice(index)"></div>
    </div>
  </div>
</template>

<style>

/*广告*/
.mainbody_ad {
  width: 20%;
  height: auto; /* 高度自适应，保持原始宽高比 */
  max-width: 400px; /* 设置最大宽度，以防止图像放大过多 */
  max-height: 800px; /* 设置最大高度 */
  min-width: 200px;
  min-height: 400px;
  border: 1px solid black;
  margin: 50px auto auto 5%;
  box-sizing: border-box;
  border-radius: 5px;
  overflow: hidden;
  box-shadow: 15px 15px 10px 0 rgba(0, 0, 0, 0.3);
  cursor: pointer;
  position: relative;
  transition: all 1s;
  opacity: 0.5;
  transform: translateY(50px); /* 初始时从下往上偏移 */
}

.mainbody_ad img {
  max-width: 100%;
  height: auto;
  object-fit: contain;
  transition: all 0.5s;
}

.arrow-container {
  position: absolute;
  width: 100%;
  height: 40px;
  bottom: 50%;
  display: flex;
}

.arrowleft {
  width: 30px;
  height: 40px;
  background-color: rgba(0, 0, 0, 0.3);
  border-bottom-right-radius: 20px;
  border-top-right-radius: 20px;
  color: white;
  font-size: 30px;
  line-height: 37px;
  display: none;
}

.arrowright {
  width: 30px;
  height: 40px;
  margin-left: auto;
  background-color: rgba(0, 0, 0, 0.5);
  border-bottom-left-radius: 20px;
  border-top-left-radius: 20px;
  color: white;
  font-size: 30px;
  line-height: 37px;
  text-indent: 6px;
  display: none;
}

.pointList {
  position: absolute;
  height: 30px;
  background-color: rgba(0, 0, 0, 0.6);
  border-radius: 20px;
  line-height: 30px;
  bottom: 3%;
  display: flex;
  margin: auto;
  left: 50%;
  transform: translateX(-50%);
}

.point {
  width: 10px;
  height: 10px;
  border-radius: 10px;
  background-color: white;
  border: 2px solid black;
  margin: 9px 10px 10px 10px;
}
</style>