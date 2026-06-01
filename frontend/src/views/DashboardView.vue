<script setup>

import { ref, watch } from "vue"

import api from "../api/analytics"
import { VueDatePicker } from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'
import { es } from "date-fns/locale"

import UploadExcel from "../components/UploadExcel.vue"
import FiltersBar from "../components/FiltersBar.vue"
import PivotTable from "../components/PivotTable.vue"
import SummaryCards from "../components/SummaryCards.vue"
import ClientSummaryCards from "../components/ClientSummaryCards.vue"
import LineChart from "../components/LineChart.vue"

const tableData = ref([])
const clients = ref([])
const datasetLoaded = ref(false)
const summary = ref({})
const selectedClientSummary = ref({})
const selectedClient = ref("")
const lineChartData = ref(null)
const selectedProduct = ref("")
const productFilter = ref("")
const globalYear = ref("")
const currentFilters = ref({})
const truckChartData = ref(null)

const fetchTruckChart = async (filters) => {
  if (!filters.client) {
    return
  }

  try {
    const response = await api.get("/analytics/truck-chart",
      {
        params: {
          client: filters.client,
          year: globalYear.value || undefined,
          month: filters.month
        }
      }
    )

    truckChartData.value = {
      labels: response.data.map(
        item => item.fecha
      ),

      datasets: [
        {
          label: "Despachos",

          data: response.data.map(
            item => item.despachos
          ),

          borderColor: "#22c55e",

          backgroundColor:
            "rgba(34,197,94,0.2)",

          tension: 0.4,

          fill: true
        }
      ]
    }
  } catch (error) {
    console.log(error)
  }
}


const fetchSummary = async () => {

  const response = await api.get(
    "/analytics/summary",
    {
      params: {
        year: globalYear.value || undefined
      }
    }
  )

  summary.value = response.data
}

const fetchClientSummary = async () => {

  if (!selectedClient.value) {
    selectedClientSummary.value = {}
    return
  }

  const response = await api.get(
    "/analytics/summary",
    {
      params: {
        client: selectedClient.value,
        year: globalYear.value || undefined
      }
    }
  )

  selectedClientSummary.value = response.data
}

const handleUploadSuccess = async (uploadedClients) => {

  datasetLoaded.value = true

  clients.value = uploadedClients

  await fetchSummary()
}


const fetchClientData = async (filters) => {

  selectedClient.value = filters.client
  currentFilters.value = filters
  await fetchLineChart(filters)
  await fetchTruckChart(filters)

  if (!filters.client) {
    tableData.value = []
    return
  }

  try {

    const response = await api.get(
      "/analytics/client-table",
      {
        params: {
          client: filters.client,
          year:
            globalYear.value || undefined,
          month: filters.month || undefined,
          day: filters.day || undefined,
          turno: filters.turno || undefined
        }
      }
    )

    tableData.value = response.data

  } catch (error) {

    console.error(error)

  }

}

const fetchLineChart = async (filters) => {

  if (!filters.client)
    return

  try {

    const response = await api.get(
      "/analytics/line-chart",
      {
        params: {
          client: filters.client,
          product: productFilter.value,
          year:
            globalYear.value || undefined,
          month: filters.month
        }
      }
    )

    lineChartData.value = {

      labels: response.data.map(
        item => item.fecha
      ),

      datasets: [
        {
          label: productFilter.value || "Sacos",

          data: response.data.map(
            item => item.cantidad
          ),

          borderColor: "#a855f7",

          backgroundColor: "rgba(168,85,247,0.2)",

          tension: 0.4,

          fill: true
        }
      ]
    }

    selectedProduct.value =
      productFilter.value

  } catch (error) {

    console.error(error)

  }

}

watch(selectedClient, () => {
  fetchClientSummary(
    currentFilters.value
  )
})

watch(productFilter, async () => {

  await fetchLineChart(
    currentFilters.value
  )

})

watch(globalYear, async () => {

  await fetchSummary()

  if (selectedClient.value) {

    await fetchClientSummary()

    await fetchClientData(
      currentFilters.value
    )

  }
  else {
    tableData.value = []
  }

})


</script>

<template>

  <div class="
      min-h-screen
      bg-gray-950
      text-white
      flex
      justify-center
      items-start
      p-10
    ">

    <div class="
        w-full
        max-w-7xl
        bg-gray-900
        rounded-3xl
        border
        border-gray-800
        shadow-2xl
        p-10
      ">

      <h1 class="
          text-4xl
          font-bold
          text-purple-400
          mb-10
          text-center
        ">
        Dashboard de Productos
      </h1>

      <div class="
    flex
    justify-center
    items-center
    gap-4
    mb-8
">

        <p class="
            text-gray-300
            font-medium
        ">
          Filtrar año global:
        </p>

        <VueDatePicker v-model="globalYear" :locale="es" year-picker dark placeholder="Año" :year-range="[2020, 2030]"
          :start-date="new Date()" auto-apply />

      </div>




      <SummaryCards :summary="summary" />

      <Transition name="fade-slide">
        <ClientSummaryCards v-if="selectedClient" :summary="selectedClientSummary" :client="selectedClient" />
      </Transition>
      <div class="
          flex
          flex-col
          gap-6
          mb-10
          items-center
          justify-center
        ">

        <UploadExcel @upload-success="handleUploadSuccess" />

        <FiltersBar :enabled="datasetLoaded" :clients="clients" @filters-changed="fetchClientData" />

      </div>

      <PivotTable :rows="tableData" />

      <div class="
    flex
    items-center
    gap-4
    mt-8
">

        <p class="
      text-gray-300
      font-medium
  ">
          Seleccionar producto:
        </p>

        <select v-model="productFilter" class="
      bg-gray-800
      border
      border-gray-700
      rounded-xl
      px-4
      py-2
      text-white
      focus:outline-none
      focus:ring-2
      focus:ring-purple-500
    ">

          <option value="">
            Todos
          </option>

          <option value="SACOS">
            SACOS
          </option>

          <option value="MAXISACOS">
            MAXISACOS
          </option>

        </select>

      </div>
      <LineChart v-if="lineChartData" :chartData="lineChartData" :selectedProduct="selectedProduct" />
      <LineChart v-if="truckChartData" :chartData="truckChartData" selectedProduct="Despachos" />

    </div>

  </div>

</template>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.35s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>