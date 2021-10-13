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
      <h5>Запись лайкнувших пользователей в CSV...</h5>
    </div>
    <section v-else>
      <div class="status-info">
        <p>{{ csvWriterStatus }}</p>
      </div>
    </section>
  </div>
</template>
<script>
export default {
  name: "CSVWriter",
  data() {
    return {
      csvWriterStatus: "",
      loading: true,
    };
  },
  async created() {
    let response = await fetch("http://localhost:8000/api/v1/user_csv_writer/");
    this.csvWriterStatus = await response.json();
    console.log(this.userLikersData);
    this.loading = false;
  },
};
</script>

<style>
.status-info {
  text-align: center;
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