<template>
    <div class="border">

        <div class="btn-container">
            
            <button @click="selectItem('Bar')" style="height:40px;width:100%">Bar</button>
            <button  @click="selectItem('Line')" style="height:40px;width:100%">Line</button>

               
        </div>
    </div>
</template>

<script setup>
import { reactive, defineProps, defineEmits } from 'vue';
import draggable from 'vuedraggable';
import BarChart from '../components/BarChart.vue';
import LineChart from '../components/LineChart.vue';




const emit = defineEmits(['itemSelected']);


const selectItem = (item) =>
{

    emit('itemSelected',item); // 发出删除事件，并传递 id

}

const state = reactive({
    list: [
        {
            id:0,
            elementType: 'BarChart',
            
        },
        {
            id:1,
            elementType: 'LineChart',
            
        },
        {
            id:2,
            elementType: 'Text',
            
        }
    ]
});




// const emit = defineEmits(['activeImage']);


</script>

<style scoped>

.btn-container{
    display: flex; /* 使用弹性盒布局 */
    gap: 10px; /* 按钮之间的间距 */
}

.photoArea {
    margin-bottom: 1.5rem;
    /* 6 */
    border: 1px solid #ccc;
    /* 添加边框 */
    padding: 1rem;
    /* 4 */
}

.barchart-container {
    height: 100%;
    /* 设定图表的高度 */
    width: 100%;
    padding: 0.5rem;
    /* 2 */
}

.flex {
    display: flex;
    flex-wrap: wrap;
}

.w-1_3 {
    width: 33.3333%;
    /* 每个图表占据 1/3 的宽度 */
}

.mb-6 {
    margin-bottom: 1.5rem;
    /* 相当于 6 */
}
</style>
