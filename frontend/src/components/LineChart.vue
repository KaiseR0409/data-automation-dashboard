<script setup>

import {
    Line
} from "vue-chartjs"

import {
    Chart,
    Title,
    Tooltip,
    Legend,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement
} from "chart.js"

Chart.register(
    Title,
    Tooltip,
    Legend,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement
)

defineProps({
    chartData: Object,
    selectedProduct: String
})

const chartOptions = {

    responsive: true,

    maintainAspectRatio: false,

    plugins: {

        legend: {
            labels: {
                color: "white"
            }
        }

    },

    scales: {

        x: {
            ticks: {
                color: "white"
            },
            grid: {
                color: "rgba(255,255,255,0.05)"
            }
        },

        y: {
            ticks: {
                color: "white"
            },
            grid: {
                color: "rgba(255,255,255,0.05)"
            }
        }

    }

}

</script>

<template>

    <div class="
      bg-white/5
      border
      border-white/10
      rounded-3xl
      p-6
      mt-10
      h-[500px]
  ">

        <h2 class="
        text-2xl
        font-bold
        text-white
        mb-6
    ">

            Evolución de
            {{ selectedProduct || "Productos" }}

        </h2>

        <Line :data="chartData" :options="chartOptions" />

    </div>

</template>