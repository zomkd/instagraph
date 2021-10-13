<template>
  <div class="main-page">
    <nav>
      <div class="nav-wrapper">
        <a href="" class="brand-logo">InstaGraph</a>
        <ul class="right hide-on-med-and-down">
          <li>
            <button
              data-target="modal1"
              class="btn modal-trigger"
              @click.prevent="showSettings"
            >
              Настройки
            </button>
          </li>
        </ul>
      </div>
      <UserSettings @setBotSettings="setSettings"  @close="closeSettings" />
    </nav>
    <div class="row">
      <div class="input-username col s12">
        <div class="input-field col s2 offset-s5">
          <input
            v-model="username"
            placeholder="username1, username2"
            id="username"
            type="text"
          />
          <label class="active" for="username">Usernames</label>
          <div class="usernames-num col s2 offset-s11">
            <p>{{ countUsernames }}</p>
          </div>
        </div>
        <div class="send-button col s3 offset-s5">
          <keep-alive include="UserSettings">
            <router-link to="/user_info">
              <button
                id="search-button"
                class="btn waves-effect waves-light col"
                type="submit"
                name="action"
                v-on:click="setUsername(username)"
              >
                Submit
              </button>
            </router-link>
          </keep-alive>
        </div>
      </div>
    </div>
  </div>
</template>

<!-- eslint-disable -->
<script>
import UserSettings from "./UserSettings";
import M from "materialize-css/dist/js/materialize.min";

export default {
  name: "UsernameForm",
  components: {
    UserSettings,
  },
  data() {
    return {
      username: "",
      settingsInstance: null,
      isSettingsVisible: false,
      botSettings: [],
      usernameNum: 0,
    };
  },
  mounted() {
    const elems = document.querySelectorAll(".modal");
    this.settingsInstance = M.Modal.init(elems);
  },

  computed: {
    countUsernames: function () {
      if (this.username === "") {
        this.usernameNum = 0;
        return this.usernameNum;
      } else {
        let usernameData = this.username.split(",");
        this.usernameNum = usernameData.length;
        return this.usernameNum;
      }
    },
  },
  methods: {
    async setUsername(username) {
      const fetch = require("node-fetch");
      let usernameData = username.split(",");
      this.botSettings = this.botSettings.slice(-2)
      let data_to_django = {
        username: usernameData,
        botUsername: this.botSettings[0],
        botPassword: this.botSettings[1],
      };
      console.log(data_to_django);

      const response = await fetch("http://localhost:8000/api/v1/username/", {
        method: "post",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data_to_django),
      });
      this.username = "";
      this.proxy_address = "";
      console.log(response);
    },
    showSettings() {
      console.log(this.settingsInstance);
    },
    closeSettings(botSettings) {
      this.botSettings = botSettings;
    },
    setSettings(settings) {
      this.botSettings = settings;
    }
  },
};
</script>

<style>
nav .brand-logo {
  padding-left: 10px;
}
.btn {
  margin-right: 10px;
}
.row {
  margin-top: 10%;
  
}

</style>