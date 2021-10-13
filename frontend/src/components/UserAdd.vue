<template>
  <div id="modal2" class="modal">
    <div class="modal-content">
      <h3 class="add-user-title">Новый акканут</h3>
      <div class="row">
        <div class="input-field col s6">
          <input
            v-model="newUsername"
            placeholder="Имя пользователя"
            id="first_name"
            type="text"
            class="validate"
          />
          <label for="first_name">Username</label>
          <div class="usernames-num col s2 offset-s11">
            <p>{{ countUsernames }}</p>
          </div>
        </div>
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

<!-- eslint-disable -->
<script>
export default {
  name: "UserAdd",
  data() {
    return {
      newUsername: "",
      usernameNum: 0,
    };
  },
  computed: {
    countUsernames: function () {
      if (this.newUsername === "") {
        this.usernameNum = 0;
        return this.usernameNum;
      } else {
        let usernameData = this.newUsername.split(",");
        this.usernameNum = usernameData.length;
        return this.usernameNum;
      }
    },
  },
  methods: {
    close() {
      let data = {
        username: this.newUsername.split(","),
      };
      const response = fetch("http://localhost:8000/api/v1/user_info/", {
        method: "post",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      this.$emit("close", data);
      this.newUsername = "";
    },
  },
};
</script>

<style scoped>
.add-user-title {
  color: black;
}
</style>