<script setup>

import { ref } from "vue"

import api from "../api/analytics"

import UploadExcel from "../components/UploadExcel.vue"
import FiltersBar from "../components/FiltersBar.vue"
import PivotTable from "../components/PivotTable.vue"
import SummaryCards from "../components/SummaryCards.vue"

const tableData = ref([])
const clients = ref([])
const datasetLoaded = ref(false)
const summary = ref({})

const fetchSummary = async () => {
  const response = await api.get("/analytics/summary")

  summary.value = response.data
}

const handleUploadSuccess = async (uploadedClients) => {

  datasetLoaded.value = true

  clients.value = uploadedClients

  await fetchSummary()
}

const fetchClientData = async (filters) => {

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
          year: filters.year || undefined,
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
        Dashboard de Turnos
      </h1>


      <SummaryCards :summary="summary"/>
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

    </div>

  </div>

</template>