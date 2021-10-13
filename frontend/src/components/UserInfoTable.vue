<template>
  <div>
    <div class="custom-navbar">
      <div class="search-bar">
        <form>
          <div class="input-field">
            <input v-model="filterField" id="search" type="search" required />
            <label class="label-icon" for="search"
              ><i class="material-icons">search</i></label
            >
            <i class="material-icons">close</i>
          </div>
        </form>
      </div>
      <div class="queue-bar">
        <div class="queue">
          <select id="select-queue" v-model="selectedGraph" multiple>
            <option value="" disabled selected>
              <p>Выбрать граф из очереди</p>
            </option>
          </select>
        </div>
        <div class="union-graph">
          <ul class="right hide-on-med-and-down">
            <router-link
              :to="{
                name: 'UserUnionGraph',
                params: { queueGraphs: selectedGraph },
              }"
              target="_blank"
            >
              <button
                id="union-graph-but"
                class="btn waves-effect waves-light col"
                type="submit"
                name="action"
                @click="sendGraphsQueue()"
              >
                Объединенный граф
              </button>
            </router-link>
          </ul>
        </div>
      </div>
      <ul id="slide-out" class="sidenav">
        <h2 class="settings-title">Настройки</h2>
        <li>
          <div class="publication-filter"><b>Число публикаций</b></div>
        </li>
        <div class="input-publication-limit">
          <div class="input-publication-field">
            <input
              v-model="publicationLimit"
              placeholder="Введите количество публикаций"
              id="publicationLimit"
              type="text"
            />
          </div>
          <div class="send-button">
            <button
              id="search-button"
              class="btn waves-effect waves-light col"
              type="submit"
              name="action"
            >
              Сбросить
            </button>
          </div>
        </div>
      </ul>
      <div class="active-btn">
        <div class="add-user-btn">
          <a href="#" data-target="modal2" class="modal-trigger"
            ><i class="medium material-icons">add</i></a
          >
        </div>
        <UserAdd @close="closeUserAddModal" />
        <div class="sidenav-btn">
          <a href="#" data-target="slide-out" class="sidenav-trigger"
            ><i class="medium material-icons">filter_list</i></a
          >
        </div>
      </div>
    </div>
    <table class="table highlight">
      <thead>
        <th @click="sort('username')">
          Имя аккаунта <i class="material-icons"> unfold_more </i>
        </th>
        <th @click="sort('full_name')">
          Полное имя <i class="material-icons"> unfold_more </i>
        </th>
        <th @click="sort('media_count')">
          Количество постов <i class="material-icons"> unfold_more </i>
        </th>
        <th @click="sort('follower_count')">
          Количество подписчиков <i class="material-icons"> unfold_more </i>
        </th>
        <th @click="sort('following_count')">
          Количество подписок <i class="material-icons"> unfold_more </i>
        </th>
        <th>Приватность <i class="material-icons"> unfold_more </i></th>
        <th>Фото профиля</th>
        <th>Активность пользователей</th>
      </thead>
      <tbody>
        <tr v-for="user in sortedUsers" :key="user.pk">
          <td>{{ user.username }}</td>
          <td id="full-name" class="user-data">{{ user.full_name }}</td>
          <td id="media-count" class="user-data">{{ user.media_count }}</td>
          <td id="follower-count" class="user-data">
            {{ user.follower_count }}
          </td>
          <td id="following-count" class="user-data">
            {{ user.following_count }}
          </td>
          <td id="is-private" class="user-data">{{ user.is_private }}</td>
          <td>
            <img
              :src="require(`../assets/profile_photos/${user.username}.jpg`)"
              alt=""
              class="circle responsive-img"
            />
          </td>
          <td v-if="user.is_private == false">
            <SelectComponents
              @setSelectedComponent="setComponent"
              :componentsName="componentsName"
            >
            </SelectComponents>
            <button
              v-if="notGraph"
              data-target="modal1"
              class="btn modal-trigger"
              @click.prevent="showComponents(user.username)"
            >
              Старт
            </button>
            <router-link
              v-else
              :to="{
                name: selectedComponent,
                params: { username: user.username },
              }"
              target="_blank"
            >
              <button
                id="union-graph-but"
                class="btn waves-effect waves-light col"
                type="submit"
                name="action"
                @click="showComponents(user.username)"
              >
                Граф
              </button>
            </router-link>
          </td>
          <td v-else> </td>
          <td>
            <i
              class="medium material-icons icon-red"
              @click="deleteUser(user.username)"
              >delete</i
            >
          </td>
        </tr>
        <div v-if="isComponentVisible && notGraph">
          <Modal
            v-show="isComponentVisible"
            v-bind:selectedComponent="selectedComponent"
            @close="closeModal"
            @addUser="closeUserAddModal"
          ></Modal>
        </div>
        <!-- <div v-if="isGraph">
          <router-link
            :to="{
              name: this.selectedComponent,
              params: {username: user.username},  
            }" target="_blank"> </router-link>
        </div> -->
      </tbody>
    </table>
  </div>
</template>

<!-- eslint-disable -->
<script>
import M from "materialize-css/dist/js/materialize.min";
import Modal from "./Modal";
import SelectComponents from "./SelectComponents";
import UserAdd from "./UserAdd";

export default {
  name: "UserInfoTable",
  props: ["userData"],
  components: {
    Modal,
    SelectComponents,
    UserAdd,
  },
  data() {
    return {
      users: this.userData,
      publicationLimit: 0,
      selectedGraph: [],
      selectedComponent: "",
      componentsName: [
        {
          vueName: "UserGraph",
          forUser: "Граф лайкнувших пользователей",
        },
        {
          vueName: "UserCommonFollowingsGraph",
          forUser: "Граф общих подписчиков",
        },
        {
          vueName: "UserLikersTable",
          forUser: "Таблица лайкнувших пользователей",
        },
        {
          vueName: "UserReverseActivity",
          forUser: "Таблица обратной активаности пользователя",
        },
        {
          vueName: "UserFollowings",
          forUser: "Таблица подписчиков пользователя",
        },
        {
          vueName: "CSVWriter",
          forUser: "Запись лайкнувших пользователей в CSV",
        },
        {
          vueName: "Map",
          forUser: "Геопозиция публикаций пользователя",
        },
      ],
      queue: [],
      sidebarInstance: null,
      modalInstance: null,
      settingsInstance: null,
      isComponentVisible: false,
      isQueueVisible: false,
      currentSort: "username",
      currentSortDir: "asc",
      filterField: "",
      notGraph: true,
    };
  },
  mounted() {
    const elems = document.querySelectorAll(".modal");
    this.modalInstance = M.Modal.init(elems);
    const elemsSelect = document.querySelectorAll(".sidenav");
    // const elemsModal = document.querySelectorAll(".modal");
    this.selectingInstance = M.Sidenav.init(elemsSelect, { edge: "right" });
    // this.settingsInstance = M.Modal.init(elemsModal);
  },
  computed: {
    filteredUsers() {
      return this.users.filter((c) => {
        if (this.filterField == "") return true;
        return (
          c.full_name.toLowerCase().indexOf(this.filterField.toLowerCase()) >= 0
        );
      });
    },
    sortedUsers() {
      return this.filteredUsers.sort((a, b) => {
        let modifier = 1;
        if (this.currentSortDir === "desc") modifier = -1;
        if (a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
        if (a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
        return 0;
      });
    },
  },
  methods: {
    sendGraphsQueue() {
      const fetch = require("node-fetch");
      let graphData = this.getGraphName(this.selectedGraph);
      let data = {
        graphsQueue: graphData,
      };
      console.log(data);
      const response = fetch("http://localhost:8000/api/v1/user_union_graph/", {
        method: "post",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      console.log(response + " ok");
      console.log(data);
    },
    getGraphName(selectedGraph) {
      let dataResponse = [];
      for (let i = 0; i < selectedGraph.length; ++i) {
        let splittedSelectedGraph = selectedGraph[i].split(" ");
        console.log(splittedSelectedGraph);
        let username = splittedSelectedGraph.pop();
        let forUser = splittedSelectedGraph.join(" ");
        console.log(forUser);
        let vueName = this.componentsName.find(
          (elem) => elem["forUser"] === forUser
        );
        console.log(vueName);
        vueName = vueName["vueName"];
        let graphData = vueName + " " + username;
        dataResponse.push(graphData);
      }
      return dataResponse;
    },
    removeDublicates(dublicates) {
      const noDublicates = [
        ...new Map(
          dublicates.map((item) => [JSON.stringify(item), item])
        ).values(),
      ];
      return noDublicates;
    },
    destroyOldSelect() {
      let selectList = document.getElementById("select-queue");
      for (var i = selectList.length - 1; 0 < i; i--)
        if (selectList[i] && selectList[i].parentElement)
          selectList[i].parentElement.removeChild(selectList[i]);
    },
    addNewSelect() {
      let selectList = document.getElementById("select-queue");
      for (let i = 0; i < this.queue.length; ++i) {
        let selectobject = document.createElement("option");
        selectobject.text =
          this.queue[i]["graphNameForUser"] + " " + this.queue[i]["usernames"];
        let selectList = document.getElementById("select-queue");
        selectList.appendChild(selectobject);
      }
      M.FormSelect.init(selectList);
    },
    showComponents(username) {
      let user = username.split(",");
      let graphQueue = {};
      let data = {
        username: user,
        limits: { publicationLimit: parseInt(this.publicationLimit) },
      };
      if (this.selectedComponent === "UserLikersTable") {
        const response = fetch("http://localhost:8000/api/v1/user_likers/", {
          method: "post",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });
        console.log(data);
      }
      if (this.selectedComponent === "Map") {
        const response = fetch("http://localhost:8000/api/v1/post_location/", {
          method: "post",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });
      }
      if (this.selectedComponent === "CSVWriter") {
        const response = fetch(
          "http://localhost:8000/api/v1/user_csv_writer/",
          {
            method: "post",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
          }
        );
      }
      if (this.selectedComponent === "UserFollowings") {
        const response = fetch(
          "http://localhost:8000/api/v1/user_followings/",
          {
            method: "post",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
          }
        );
      }
      if (this.selectedComponent === "UserReverseActivity") {
        const response = fetch(
          "http://localhost:8000/api/v1/user_reverse_activity/",
          {
            method: "post",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
          }
        );
      }
      if (this.selectedComponent === "UserGraph") {
        const response = fetch(
          "http://localhost:8000/api/v1/user_likers_graph/",
          {
            method: "post",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
          }
        );
        console.log(username);
        let selectedGraph = this.componentsName.find(
          (elem) => elem["vueName"] === this.selectedComponent
        );
        graphQueue = {
          graphName: selectedGraph["vueName"],
          graphNameForUser: selectedGraph["forUser"],
          usernames: username,
        };
        this.queue.push(graphQueue);
        this.queue = this.removeDublicates(this.queue);
        this.destroyOldSelect();
        this.addNewSelect();

        // let routeData = this.$router.resolve({ name: 'UserGraph', params: { username: username } })
        // window.open(routeData.href, '_blank');
      }
      if (this.selectedComponent === "UserCommonFollowingsGraph") {
        // let names = [];
        // for (let i = 0; i < this.users.length; ++i) {
        //   names.push(this.users[i]["username"]);
        // }
        // let data = {
        //   username: names,
        // };
        const response = fetch(
          "http://localhost:8000/api/v1/user_common_followings_graph/",
          {
            method: "post",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
          }
        );
        console.log(username);
        let selectedGraph = this.componentsName.find(
          (elem) => elem["vueName"] === this.selectedComponent
        );
        graphQueue = {
          graphName: selectedGraph["vueName"],
          graphNameForUser: selectedGraph["forUser"],
          usernames: username,
        };
        this.queue.push(graphQueue);
        this.queue = this.removeDublicates(this.queue);
        this.destroyOldSelect();
        this.addNewSelect();
      }
      this.isComponentVisible = true;
    },
    showQueue() {
      this.isQueueVisible = !this.isQueueVisible;
    },
    setComponent(component) {
      this.selectedComponent = component;
      if (this.selectedComponent.endsWith("Graph")) {
        this.notGraph = false;
      } else {
        this.notGraph = true;
      }
    },
    closeModal(selectedState) {
      console.log(selectedState);
      this.selectedComponent = selectedState["selectedComponent"];
      this.isComponentVisible = selectedState["isVisible"];
    },
    sort(s) {
      //if s == current sort, reverse
      if (s === this.currentSort) {
        this.currentSortDir = this.currentSortDir === "asc" ? "desc" : "asc";
      }
      this.currentSort = s;
    },
    filterByName(user) {
      // no search, don't filter :
      if (this.searchName.length === 0) {
        return true;
      }
      return (
        user.full_name.toLowerCase().indexOf(this.searchName.toLowerCase()) > -1
      );
    },
    async closeUserAddModal(data) {
      let response = await fetch("http://localhost:8000/api/v1/user_info/");
      const seen = new Set();
      let userData = await response.json();
      this.users = this.users.concat(userData);
      this.users = this.users.filter((el) => {
        const duplicate = seen.has(el.pk);
        seen.add(el.pk);
        return !duplicate;
      });

      console.log(userData);
      this.$emit("closeUserAddModal", this.users);
    },
    deleteUser(username) {
      let data = {
        username: username,
      };
      const response = fetch("http://localhost:8000/api/v1/user_delete/", {
        method: "post",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      this.users = this.users.filter((x) => x.username !== username);
      this.$emit("deleteUser", "");
    },
  },
};
</script>

<style scoped>

.input-field {
  padding-bottom: .9rem;
}

img {
  display: block;
  margin: 0 auto;
}
td {
  font-size: 1.4em;
}
th {
  font-size: 1.5em;
  cursor: pointer;
}
.user-data {
  text-align: center;
}
.input-publication-field {
  margin-left: 1rem;
  margin-right: 2rem;
  padding-top: 0;
}
.custom-navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #d3d1eb;
}
.queue-bar {
  display: flex;
}
.active-btn {
  display: flex;
}
.sidenav-btn {
  margin-right: 2rem;
  margin-left: 2rem;
}
.queue {
  width: 500px;
  margin-right: 2rem;
}
.send-button {
  padding: 2rem 1.3rem 2rem 2rem;
  float: right;
}
.settings-title {
  text-align: center;
}
.publication-filter {
  margin-left: 1rem;
  font-size: 20px;
}
#search {
  margin-left: 1rem;
  width: 30rem;
  max-height: 55px;
}
i.icon-red {
  color: red;
}
</style>