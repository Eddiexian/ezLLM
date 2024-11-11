<template>
    <div class="container-fluid" style="height:100vh;">
        
        
            <div class="edit-panel" style="width:10%;">
                <ComArea @addElement="addToDisplayList" @itemSelected="addNewItem" />
            </div>
         

        <div class="ui-panel" style="width:90%">
                <SelectedComArea :displayList="displayList" @deleteElement="deleteElement" />
            </div>

    </div>
</template>

<script setup>
import { ref } from 'vue';
import SelectedComArea from '../components/SelectedComArea.vue';
import ComArea from '../components/ComArea.vue';
import Vue3DraggableResizable from 'vue3-draggable-resizable'
//default styles
import 'vue3-draggable-resizable/dist/Vue3DraggableResizable.css'
const displayList = ref([]);
const active = ref(100);
const addToDisplayList = (newElement) => {
    displayList.value.push(newElement); // 添加新元素到 displayList
};

const deleteElement = (index) => {
    if (index > -1 && index < displayList.value.length) {
        displayList.value.splice(index, 1); // 移除指定索引的元素

    } else {
        console.error("Invalid index:", index);
    }
}

const addNewItem = (item) => {

    displayList.value.push(
        {
            "type": item, 
            'x': 100,
            'y': 100,
            'h': 100,
            'w': 100,
            'active': true,
            'sizeChangeMonitor': false,
            'dataSourceType':'API',
            'dataAPI':'http://tw100043626.corpnet.auo.com:3066/MFG_WEB/Api/TestC2/GetLineTrend',
            'dataRefreshTime':300000,
            'chartData':null,
            'chartOption':null,
            
        })

}
</script>

<style scoped>
body {
    margin: 0;
    animation: backgroundAnimation 10s ease infinite;
    /* 背景動畫效果 */
    background: linear-gradient(270deg, rgba(0, 0, 0, 0.9), rgba(10, 10, 10, 0.9), rgba(0, 0, 0, 0.9));
    background-size: 400% 400%;
    /* 調整背景大小以增加動畫效果 */
}

@keyframes backgroundAnimation {
    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}

.edit-panel {
    background: rgba(30, 30, 30, 0.9);
    /* 較不透明的透明黑色 */
    border-right: 2px solid rgba(0, 255, 255, 0.5);
    /* 發光的邊框 */
    height: 100px;
    text-align: center;
    /* 文字居中 */
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.7);
    /* 增加光暈效果 */
    border-radius: 0;
    /* 去掉圓角 */
    opacity: 0;
    /* 初始透明度 */
    animation: fadeIn 1s forwards;
    /* 淡入動畫 */
    padding: 20px;
    /* 內邊距 */
    color: #FFFFFF;
    /* 文字顏色 */
}

@keyframes fadeIn {
    to {
        opacity: 1;
    }
}

.ui-panel {
    background: rgba(40, 40, 40, 0.8);
    /* 更透明的透明黑色，提供層次感 */
    height: 100%;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.7);
    /* 增加光暈效果 */
    border-radius: 0;
    /* 去掉圓角 */
    padding: 20px;
    /* 內邊距 */
    color: #FFFFFF;
    /* 文字顏色 */
    transition: transform 0.3s;
    /* 懸停縮放效果 */
}

/* 光標閃爍效果 */
.caret {
    display: inline-block;
    border-right: 3px solid rgba(0, 255, 255, 0.7);
    /* 光標效果 */
    animation: blink-caret 0.75s step-end infinite;
    /* 使用光標閃爍動畫 */
    margin-left: 3px;
    /* 確保光標與文本之間有間隔 */
}

/* 光標閃爍動畫 */
@keyframes blink-caret {
    50% {
        border-color: transparent;
        /* 光標閃爍效果 */
    }
}

/* 調整標題和其他元素 */
h4 {
    text-shadow: 0 0 10px rgba(0, 255, 255, 0.7);
    /* 標題發光效果 */
    display: inline;
    /* 讓標題行內顯示以便光標顯示在右側 */
    margin: 0;
    /* 去掉標題的預設外邊距 */
}

hr {
    margin: 10px 0;
    border: none;
    /* 去掉默認邊框 */
    background-color: rgba(0, 255, 255, 0.5);
    /* 使用發光顏色 */
}

.parent {
    width: 200px;
    height: 200px;
    position: absolute;
    top: 100px;
    left: 100px;
    border: 1px solid #000;
    user-select: none;
}
</style>
