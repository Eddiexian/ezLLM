<template>
    <div ref="chartRef" style="width: 100%; height: 400px;"></div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, onUnmounted, watch } from 'vue';
import * as echarts from 'echarts';

export default defineComponent({
    name: 'LineChart',
    props: {
        title: {
            type: String,
            required: false,
            default: () => (
                "Line Chart"
            )
        },
        chartData: {
            type: Array as () => { name: string; value: number }[],
            required: false,
            default: () => (
                [
                    { name: 'A', value: 10 },
                    { name: 'B', value: 20 },
                    { name: 'C', value: 30 },
                    { name: 'E', value: 20 },
                    { name: 'E', value: 50 },
                ]
            )
        },

        updateListner: {
            required: false,
        }
    },
    setup(props) {
        const chartRef = ref<HTMLDivElement | null>(null);
        let chartInstance: echarts.ECharts | null = null;

        const initChart = () => {
            if (chartRef.value) {
                chartInstance = echarts.init(chartRef.value);
                const option = {
                    textStyle: {
                        color: '#ffffff', // 全局文本颜色设置为白色
                    },
                    title: {
                        text: props.title,
                        textStyle: {
                            color: '#ffffff', // 设置标题文字颜色为白色
                        },
                    },
                    tooltip: {},
                    xAxis: {
                        type: 'category',
                        data: props.chartData.map(item => item.name),
                    },
                    yAxis: {
                        type: 'value',
                    },
                    series: [{
                        name: '值',
                        type: 'line',
                        data: props.chartData.map(item => item.value),
                    }],
                };

                chartInstance.setOption(option);
            }
        };

        // 監視 updateListner 的變化
        watch(() => props.chartData, (newVal, oldVal) => {
            console.log('updateListner updated:', newVal);
            // 你可以在這裡執行根據 updateListner 更新圖表的邏輯
            // 例如刷新圖表數據
            initChart();
            window.addEventListener('resize', resizeChart);
        });


        // 監視 updateListner 的變化
        watch(() => props.updateListner, (newVal, oldVal) => {
            console.log('updateListner updated:', newVal);
            // 你可以在這裡執行根據 updateListner 更新圖表的邏輯
            // 例如刷新圖表數據
            resizeChart();
        });


        const resizeChart = () => {
            if (chartInstance) {
                chartInstance.resize();
            }
        };

        // onMounted(() => {
        //     initChart();
        //     window.addEventListener('resize', resizeChart);
        // });

        onUnmounted(() => {
            if (chartInstance) {
                chartInstance.dispose();
            }
            window.removeEventListener('resize', resizeChart);
        });

        return {
            chartRef,
        };
    },
});
</script>

<style scoped></style>
