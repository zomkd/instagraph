<template>
  <div id="graph">
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
      <h5>Загрузка графа пользователей оценивших публикацию...</h5>
    </div>
    <section v-else>
      <div
        class="info-table"
        v-if="this.userLikersData['error_message'] === undefined"
      >
        <div class="title">
          <form action="#">
            <div
              class="checkbox"
              v-for="(mode, index) in modes"
              :key="mode.index"
            >
              <label>
                <input
                  type="checkbox"
                  :value="index"
                  v-model="selectedMode"
                  :disabled="
                    selectedMode.length >= max &&
                    selectedMode.indexOf(index) == -1
                  "
                />
                <span>{{ mode }}</span>
              </label>
            </div>
            <p class="range-field">
              <label> Количество лайков </label>
              <input
                type="range"
                id="test5"
                min="1"
                max="100"
                v-model="likeNum"
                @change="likersFilter(selectedMode)"
              />
              {{ likeNum }}
            </p>
          </form>
        </div>
        <network
          :nodeList="nodes"
          :linkList="links"
          showLinkText="true"
          nodeSize="9"
          linkDistance="450"
        >
        </network>
      </div>
      <div v-else>
        <h2>{{ this.userLikersData["error_message"] }}</h2>
      </div>
    </section>
  </div>
</template>

<script>
import Network from "vue-network-d3";

export default {
  name: "UserGraph",
  components: {
    Network,
  },
  data() {
    return {
      nodes: [],
      links: [],
      likeNum: 1,
      loading: true,
      getNodes: [],
      getLinks: [],
      userLikersData: [],
      modes: ["Больше или равно", "Меньше или равно", "Равно"],
      selectedMode: [0],
      max: 1,
    };
  },
  async created() {
    let response = await fetch(
      "http://localhost:8000/api/v1/user_likers_graph/"
    );
    this.userLikersData = await response.json();
    this.nodes = this.userLikersData[0];
    this.links = this.userLikersData[1];
    this.getNodes = this.userLikersData[0];
    this.getLinks = this.userLikersData[1];
    this.loading = false;
  },
  methods: {
    likersFilter: function (selectedMode) {
      let filterNodes = [];
      let filterLinks = [];
      filterNodes.push(this.getNodes[0]);
      if (selectedMode[0] === 0 || selectedMode.length === 0) {
        this.nodes = filterNodes.concat(
          this.getNodes
            .slice(1)
            .filter((el) => el["like_count"] >= this.likeNum)
        );
        this.links = filterLinks.concat(
          this.getLinks.filter((el) => el["like_count"] >= this.likeNum)
        );
      }
      if (selectedMode[0] === 1) {
        this.nodes = filterNodes.concat(
          this.getNodes
            .slice(1)
            .filter((el) => el["like_count"] <= this.likeNum)
        );
        this.links = filterLinks.concat(
          this.getLinks.filter((el) => el["like_count"] <= this.likeNum)
        );
      }
      if (selectedMode[0] === 2) {
        this.nodes = filterNodes.concat(
          this.getNodes
            .slice(1)
            .filter((el) => el["like_count"] == this.likeNum)
        );
        this.links = filterLinks.concat(
          this.getLinks.filter((el) => el["like_count"] == this.likeNum)
        );
      }
    },
  },
};
</script>
 
<style>
body {
  margin: 0;
}
</style>
