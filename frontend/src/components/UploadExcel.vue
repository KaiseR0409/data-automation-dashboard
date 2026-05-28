<script setup>

import { ref } from "vue"
import api from "../api/analytics"
import { toast } from "vue-sonner"

const file = ref(null)

const emit = defineEmits([
  "upload-success"
])
const handleFileChange = (event) => {
  file.value = event.target.files[0]
}

const uploadFile = async () => {

  if (!file.value) return

  const formData = new FormData()

  formData.append("file", file.value)

  try {

    const response = await api.post(
      "/upload",
      formData,
      {
        headers: {
          "Content-Type":"multipart/form-data"
        }
      }
    )
    emit(
      "upload-success",
      response.data.clients
    )
    toast.success("Excel cargado correctamente")
    

  } catch (error) {
    toast.error("Error al subir el archivo excel")
  }
}

</script>

<template>

  <div class="flex gap-4 items-center">

    <input
      type="file"
      @change="handleFileChange"
      class="
        bg-gray-800
        border
        border-gray-700
        rounded-xl
        px-4
        py-3
      "
    />

    <button
      @click="uploadFile"
      class="
        bg-purple-600
        hover:bg-purple-500
        transition
        px-6
        py-3
        rounded-xl
        font-semibold
      "
    >
      Subir Excel
    </button>

  </div>

</template>