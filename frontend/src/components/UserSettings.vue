<template>
  <div id="modal1" class="modal">
    <div class="modal-content">
      <h1 class="settings-title">Настройки</h1>
      <div class="row">
        <div class="input-field col s6">
          <input
            v-model="botUsername"
            placeholder="Имя пользователя-бота для поиска"
            id="first_name"
            type="text"
            class="validate"
          />
          <label for="first_name">Username</label>
        </div>
      </div>
      <div class="input-field col s12">
        <input
          v-model="botPassword"
          id="password"
          type="password"
          class="validate"
        />
        <label for="password">Password</label>
      </div>
    </div>
    <div class="modal-footer">
      <a
        href=""
        class="modal-close waves-effect waves-green btn-flat"
        @click.prevent="close"
        >Save</a
      >
    </div>
  </div>
</template>


<script>
export default {
  name: "UserSettings",
  data() {
    return {
      botSettingsChild: [],
      botUsername: "",
      botPassword: "",
    };
  },
  mounted() {
    if (localStorage.botUsername) this.botUsername = localStorage.botUsername;
    if (localStorage.botPassword) this.botPassword = localStorage.botPassword;
    this.botSettingsChild.push(this.botUsername);
    this.botSettingsChild.push(this.botPassword);
    this.$emit("setBotSettings", this.botSettingsChild);
  },
  methods: {
    close() {
      localStorage.botUsername = this.botUsername;
      localStorage.botPassword = this.botPassword;
      this.botSettingsChild.push(this.botUsername);
      this.botSettingsChild.push(this.botPassword);
      this.$emit("close", this.botSettingsChild);
    },
  },
};
</script>

<style scoped>
.settings-title {
  color: black;
}
</style>