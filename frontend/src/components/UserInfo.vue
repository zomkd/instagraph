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
      <h5>Загрузка общей информации о пользователе...</h5>
    </div>
    <section v-else>
      <div
        class="info-table"
        v-if="this.userData['error_message'] === undefined"
      >
        <UserInfoTable :userData="userData" @closeUserAddModal="close" @deleteUser="deleteUser">
        </UserInfoTable>
      </div>
      <div v-else>
        <h3>{{ this.userData["error_message"] }}</h3>
      </div>
    </section>
  </div>
</template>

<script>
import UserInfoTable from "./UserInfoTable";

export default {
  name: "UserInfo",
  data() {
    return {
      userData: [],
      loading: true,
    };
  },
  components: { UserInfoTable },
  async created() {
      let response = await fetch("http://localhost:8000/api/v1/username/");
      this.userData = await response.json();
    
    // else {
    //   let response = await fetch("http://localhost:8000/api/v1/user_info/");
    //   this.userData = await response.json();
    // }
    // this.userData = [{username: 'DFSuser',
    // full_name: 'asdfull',
    // media_count: 23,
    // follower_count:1,
    // following_count:4,
    // is_private: true}, {username: 'CVuser',
    // full_name: 'xcxcfull',
    // media_count: 33,
    // follower_count:1,
    // following_count:4,
    // is_private: true},{username: 'SDuser',
    // full_name: 'fcvull',
    // media_count: 331,
    // follower_count:1,
    // following_count:4,
    // is_private: true},{username: 'Auser',
    // full_name: 'xfxvcull',
    // media_count: 43,
    // follower_count:1,
    // following_count:4,
    // is_private: true},{username: 'Xuser',
    // full_name: 'bvfull',
    // media_count: 321,
    // follower_count:1,
    // following_count:4,
    // is_private: true},{username: 'cvuser',
    // full_name: 'mnbvfull',
    // media_count: 35,
    // follower_count:1,
    // following_count:4,
    // is_private: true}],
    console.log(this.userData);
    this.loading = false;
  },
  methods: {
    close(data) {
      this.userData = data;
    },
    async deleteUser() {
      let response = await fetch("http://localhost:8000/api/v1/user_delete/");
      this.userData = await response.json();
    },
  },
};
</script>

<style>
.loading {
  text-align: center;
  margin-top: 20%;
}
.preloader-wrapper.big {
  width: 200px;
  height: 200px;
}
</style>