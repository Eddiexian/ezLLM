<template>
    <div class="container-fluid  p-4" style="height:100%">
        <!-- {{ displayList }} -->

        <DraggableContainer>


            <Vue3DraggableResizable v-for="item in displayList" :initW="400" :initH="300" v-model:x="item.x"
                v-model:y="item.y" v-model:w="item.w" v-model:h="item.h" v-model:active="item.active" :draggable="true"
                :resizable="true" @resize-end="EventSizeChanged(item)">
                <BarChart v-if="item.type == 'Bar'" style="height:100%;" :chartData="item.chartData"
                    :updateListner="item.sizeChangeMonitor" />

                <LineChart v-if="item.type == 'Line'" style="height:100%;" :chartData="item.chartData"
                    :updateListner="item.sizeChangeMonitor" />
                
            </Vue3DraggableResizable>





        </DraggableContainer>




    </div>
</template>

<script setup>

import { ref, onMounted, onUnmounted, defineProps, watch } from 'vue';
import BarChart from '../components/BarChart.vue';
import LineChart from '../components/LineChart.vue';
import Vue3DraggableResizable from 'vue3-draggable-resizable'
//需引入默认样式
import 'vue3-draggable-resizable/dist/Vue3DraggableResizable.css'
import { DraggableContainer } from 'vue3-draggable-resizable'
import axios from 'axios';
const props = defineProps({
    displayList: Array
});

const emit = defineEmits(['inactiveImage', 'openLightBox', 'deleteElement']);



const EventSizeChanged = (item) => {

    item.sizeChangeMonitor = !item.sizeChangeMonitor;

};



// 監聽 displayList 的變化
watch(
    () => props.displayList.length,
    (newVal, oldVal) => {
        startFetching(); // 當 displayList 變化時重新啟動請求
    },
    { deep: true }, // 深度監聽，以便監測物件中的變化
    console.log("change!"),
);



const fetchData = (item) => {
    if (item.active) {
        axios.post(item.dataAPI,{Model: "M270QAN06"})
            .then(response => {
                console.log(`Fetched data for ${item.type}:`, response.data);

                const formattedData = response.data.map(entry => {
                    return { name: entry.Test_Week, value: entry.Total };
                });

                console.log(formattedData)
                item.chartData = formattedData; // 更新 chartData
            })
            .catch(error => {
                console.error(`Error fetching data for ${item.type}:`, error);
            });
    }
};

const timers = ref([]);

const startFetching = () => {
    props.displayList.forEach(item => {
        if (item.dataSourceType == 'API') {
            fetchData(item); // 初次呼叫
            const timer = setInterval(() => {
                fetchData(item); // 定時呼叫
            }, item.dataRefreshTime);
            timers.value.push(timer); // 保存定時器，以便於釋放
        }
    });
};


onUnmounted(() => {
    // 清除所有定時器
    timers.value.forEach(timer => clearInterval(timer));
});

const deleteElement = (index) => {
    console.log(index)
    emit('deleteElement', index); // 发出删除事件，并传递 id
};




</script>

<style scoped></style>
