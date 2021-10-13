<template>
  <div class="input-field col s12">
    <select v-model="selectedComponent" id="select-actions" @change="onChange()">
      <option value="" disabled selected>Выберите действие</option>
      <option v-for="name in componentsName" v-bind:key="name.id">
        {{ name.forUser }}
      </option>
    </select>
  </div>
</template>

<script>
import M from "materialize-css/dist/js/materialize.min";
export default {
  name: "SelectComponents",
  props: ["componentsName"],
  data() {
    return {
      selectedComponent: null,
      selectingInstance: null,
    };
  },
  mounted() {
    const elemsSelect = document.querySelectorAll("select");
    // const elemsModal = document.querySelectorAll(".modal");
    this.selectingInstance = M.FormSelect.init(elemsSelect);
    // this.settingsInstance = M.Modal.init(elemsModal);
  },
  methods: {
    onChange() {
      const selected_obj = this.componentsName.find((e) => e.forUser === this.selectedComponent)
      const vueName = selected_obj['vueName']
      this.$emit("setSelectedComponent", vueName);
      
    },
  },
};
</script>

<style >
</style>