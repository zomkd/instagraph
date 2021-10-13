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
      <h5>Загрузка объединенного графа пользователей...</h5>
    </div>
    <section v-else>
      <div
        class="info-table"
        v-if="this.unionData['error_message'] === undefined"
      >
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
        <h2>{{ this.unionData["error_message"] }}</h2>
      </div>
    </section>
  </div>
</template>

<script>
import Network from "vue-network-d3";

export default {
  name: "UserUnionGraph",
  components: {
    Network,
  },
  data() {
    return {
      nodes: [],
      links: [],
      loading: true,
      unionData: [],
    };
  },
  async created() {
    let response = await fetch(
            "http://localhost:8000/api/v1/user_union_graph/"
    );
    this.unionData = await response.json();
    this.nodes = this.unionData[0];
    this.links = this.unionData[1];
    this.loading = false;
  },
};
</script>
 
<style>
body {
  margin: 0;
}
</style>
