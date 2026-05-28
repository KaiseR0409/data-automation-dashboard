<script setup>

import { reactive, watch } from "vue"
import { VueDatePicker } from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'
import { es } from 'date-fns/locale'



const props = defineProps({
  enabled: Boolean,
  clients: Array
})

const emit = defineEmits([
  "filters-changed"
])

const filters = reactive({
  client: "",
  year: null,
  month: null,
  day: null,
  turno: ""
})

watch(
  filters,
  () => {

    emit(
      "filters-changed",
      {
        client: filters.client,

        year: filters.year || undefined,

        month: filters.month
          ? filters.month.month + 1
          : undefined,

        day: filters.day
          ? filters.day.getDate()
          : undefined,

        turno: filters.turno

      }
    )

  },
  { deep: true }
)

</script>

<template>

  <div class="
    flex
    flex-wrap
    gap-4
    justify-center
    items-center
  ">

    <!-- CLIENTE -->

    <select v-model="filters.client" :disabled="!enabled"  class="
        bg-gray-800
        border
        border-gray-700
        rounded-xl
        px-4
        py-3
        text-white
        disabled:opacity-50
        disabled:cursor-not-allowed
      disabled:bg-gray-700
      ">
      <option value="">
        Seleccione un cliente
      </option>

      <option v-for="client in clients" :key="client" :value="client">
        {{ client }}
      </option>
    </select>

    <!-- AÑO -->

    <VueDatePicker v-model="filters.year" :disabled="!enabled" :locale="es" year-picker dark placeholder="Año" :year-range="[2020, 2030]" :start-date="new Date()" auto-apply />

    <!-- MES -->

    <VueDatePicker v-model="filters.month" :disabled="!enabled" :locale="es" month-picker dark placeholder="Mes" auto-apply disable-year-select />


    <!-- TURNO -->

    <select v-model="filters.turno" :disabled="!enabled" class="
        bg-gray-800
        border
        border-gray-700
        rounded-xl
        px-4
        py-3
        text-white
        disabled:opacity-50
        disabled:cursor-not-allowed
        disabled:bg-gray-700
      ">

      <option value="">
        Seleccione Turno
      </option>

      <option  value="Primer">
        Primer
      </option>

      <option  value="Segundo">
        Segundo
      </option>

      <option  value="Tercero">
        Tercero
      </option>

    </select>

  </div>

</template>