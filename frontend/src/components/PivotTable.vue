<script setup>

defineProps({
  rows: Array
})

</script>

<template>

  <div
    class="
      overflow-x-auto
      rounded-2xl
      border
      border-gray-800
    "
  >

    <table
      class="
        w-full
        border-collapse
      "
    >

      <thead
        class="
          bg-gray-800
          text-purple-300
        "
      >

        <tr>

          <th class="p-4 text-left">
            Fecha
          </th>

          <th class="p-4 text-left">
            Día
          </th>

          <th class="p-4 text-left">
            Turno
          </th>

          <th class="p-4 text-left">
            SACOS
          </th>

          <th class="p-4 text-left">
            MAXISACOS
          </th>

        </tr>

      </thead>

      <tbody>

        <tr
          v-for="(row, index) in rows"
          :key="index"
          class="
            border-t
            border-gray-800
            hover:bg-gray-800
            transition
          "
        >

          <td class="p-4">
            {{ row.Fecha }}
          </td>

          <td class="p-4">
            {{ row["Dia Semana"] }}
          </td>

          <td class="p-4">
            {{ row.Turno }}
          </td>

          <td class="p-4">
            {{ row.SACOS || 0 }}
          </td>

          <td class="p-4">
            {{ row.MAXISACOS || 0 }}
          </td>

        </tr>

      </tbody>

    </table>

  </div>

</template>