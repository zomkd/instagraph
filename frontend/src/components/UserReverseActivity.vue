<template>
  <div>
    <div class="loading" v-if="loading">
      <div class="preloader-wrapper big active">
        <div class="spinner-layer spinner-blue-only">
          <div class="circle-clipper left">
            <div class="circle"></div>
          </div>
          <div class="gap-patch">
            <div class="circle"></div>
          </div>
          <div class="circle-clipper right">
            <div class="circle"></div>
          </div>
        </div>
      </div>
    </div>
    <section v-else>
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
      <div
        class="info-table"
        v-if="this.userLikersData['error_message'] === undefined"
      >
        <table class="table">
          <thead>
            <th>ID</th>
            <th>Имя пользователя</th>
            <th>Количество лайков</th>
          </thead>
          <tbody>
            <tr v-for="user in sortedUsers" :key="user.pk">
              <td>{{ user.pk }}</td>
              <th @click="sort('username')">
                Имя аккаунта <i class="material-icons"> unfold_more </i>
              </th>
              <th @click="sort('like_count')">
                Количество лайков <i class="material-icons"> unfold_more </i>
              </th>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <h2>{{ this.userLikersData["error_message"] }}</h2>
      </div>
    </section>
  </div>
</template>


<!-- eslint-disable -->
<script>
export default {
  name: "UserReverseActivity",
  props: ["username"],
  data() {
    return {
      userLikersData: [],
      loading: true,
      currentSort: "username",
      currentSortDir: "asc",
      filterField: "",
    };
  },
  async created() {
    let response = await fetch(
      "http://localhost:8000/api/v1/user_reverse_activity/"
    );
    this.userLikersData = await response.json();
    console.log(this.userLikersData);
    this.loading = false;
  },
  computed: {
    filteredUsers() {
      return this.userLikersData.filter((c) => {
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
  },
};
</script>


<style>
.loading {
  position: center;
}
</style>