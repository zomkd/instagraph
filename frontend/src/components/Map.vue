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
      <h5>Загрузка информации о местоположении публикаций пользователя...</h5>
    </div>
    <section v-else>
      <div
        class="info-table"
        v-if="this.markers['error_message'] === undefined"
      >
        <div class="body">
          <gmap-map
            :center="center"
            :zoom="5"
            map-type-id="terrain"
            style="width: 1900px; height: 800px"
          >
            <gmap-info-window
              :options="infoOptions"
              :position="infoWindowPos"
              :opened="infoWinOpen"
              @closeclick="infoWinOpen = false"
            >
            </gmap-info-window>
            <gmap-marker
              :key="index"
              v-for="(m, index) in filterdMarkers"
              :position="m.position"
              :clickable="true"
              :draggable="true"
              @click="toggleInfoWindow(m, index)"
            />
          </gmap-map>
          <div class="posts-list">
            <h5>
              {{ filterdMarkers.length }} / {{ this.markers.length }} публикаций
              с геопозцией
            </h5>
            <div v-for="post in filterdMarkers" :key="post.index">
              <h5>{{ filterdMarkers.indexOf(post) + 1 }}.</h5>
              <div @click="center = post.position" class="description">
                <p >{{ post.taken_at }}</p>
                <div class="photo" v-if="post['media_pk'] != undefined">
                  <img
                    :src="
                      require(`../assets/${post.username}/${post.username}_${post.media_pk}.jpg`)
                    "
                    alt=""
                    width="100"
                    height="100"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <h2>{{ this.markers["error_message"] }}</h2>
      </div>
    </section>
  </div>
</template>


<script>
export default {
  name: "Map",
  data() {
    return {
      center: { lat: 56.08434, lng: 37.45028 },
      markers: [],
      statusText: "",
      infoWindowPos: null,
      infoWinOpen: false,
      currentMidx: null,
      infoOptions: {
        content: "",
        //optional: offset infowindow so it visually sits nicely on top of our marker
        pixelOffset: {
          width: 0,
          height: -35,
        },
      },
      loading: true,
    };
  },
  async created() {
    let response = await fetch("http://localhost:8000/api/v1/post_location/");
    this.markers = await response.json();
    this.loading = false;
  },
  computed: {
    filterdMarkers() {
      return this.markers.filter((marker) => {
        if (marker.position != undefined) {
          return marker;
        }
      });
    },
  },
  methods: {
    toggleInfoWindow: function (marker, idx) {
      this.infoWindowPos = marker.position;
      this.infoOptions.content = idx.toString() +
        ". <b>Расположение: </b>" +
        marker.name +
        "<br/>" +
        "<b>Описание: </b>" +
        marker.caption_text +
        "<br/>" +
        marker.taken_at +
        '<img :src="require(`../assets/profile_photos/sany.aaa_.jpg`)" alt="" />';
      console.log(idx)
      //check if its the same marker that was selected if yes toggle
      if (this.currentMidx == idx) {
        this.infoWinOpen = !this.infoWinOpen;
      }

      //if different marker set infowindow to open and reset current marker index
      else {
        this.infoWinOpen = true;
        this.currentMidx = idx;
      }
    },
  },
};
</script>


<style scoped>
.photo {
  text-align: center;
}
.body {
  display: flex;
}

.description {
  cursor: pointer;
}
.posts-list {
  margin-left: 1rem;
}
.loading {
  text-align: center;
  margin-top: 20%;
}
.preloader-wrapper.big {
  width: 200px;
  height: 200px;
}
</style>