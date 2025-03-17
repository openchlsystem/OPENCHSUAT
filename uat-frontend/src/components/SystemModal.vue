<template>
    <div class="modal-overlay">
      <div class="modal">
        <h3>{{ system?.id ? "Edit System" : "Add New System" }}</h3>
        <input type="text" v-model="formData.name" placeholder="System Name" />
        <textarea v-model="formData.description" placeholder="Description"></textarea>
        <button @click="save">Save</button>
        <button @click="$emit('close')">Cancel</button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, watch } from "vue";
  
  const props = defineProps(["system"]);
  const emit = defineEmits(["save", "close"]);
  
  const formData = ref({ id: null, name: "", description: "" });
  
  watch(
    () => props.system,
    (newVal) => {
      formData.value = newVal ? { ...newVal } : { id: null, name: "", description: "" };
    },
    { immediate: true }
  );
  
  const save = () => {
    emit("save", formData.value);
  };
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .modal {
    background: white;
    padding: 20px;
    border-radius: 5px;
  }
  </style>
  