<template>
    <div class="form-group">
      <p><strong>Step:</strong> {{ step.description }}</p>
  
      <label>Status</label>
      <select v-model="result.status" class="form-control" required>
        <option value="Passed">Passed</option>
        <option value="Failed">Failed</option>
      </select>
  
      <label>Comments</label>
      <textarea v-model="result.comments" class="form-control"></textarea>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      step: Object,
      modelValue: Object
    },
    computed: {
      result: {
        get() {
          return this.modelValue || { status: "", comments: "" };
        },
        set(value) {
          this.$emit("update:modelValue", value);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .form-group {
    margin-bottom: 15px;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    background: #f9f9f9;
  }
  </style>
  