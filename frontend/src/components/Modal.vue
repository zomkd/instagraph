<template>
  <div id="modal1" class="modal">
    <a
      href=""
      id="close-btn"
      class="modal-close waves-effect waves-green btn-flat"
      @click.prevent="close"
      >close</a
    >
    <div class="modal-content">
      <component :is="selectedComponent" @addNewUser="addUser"></component>
    </div>
  </div>
</template>

<script>
// import UserGraph from "./UserGraph";
// import UserCommonFollowingsGraph from "./UserCommonFollowingsGraph";
import UserLikersTable from "./UserLikersTable";
import UserReverseActivity from "./UserReverseActivity";
import UserUnionGraph from "./UserUnionGraph";
import UserFollowings from "./UserFollowings";
import CSVWriter from "./CSVWriter";
import Map from "./Map";
import M from "materialize-css/dist/js/materialize.min";

export default {
  name: "Modal",
  data() {
    return {
      modalInstance: null,
      componentState: {
        selectedComponent: "",
        isVisible: false,
      },
    };
  },
  props: ["selectedComponent"],
  components: {
    // UserGraph,
    // UserCommonFollowingsGraph,
    UserLikersTable,
    UserReverseActivity,
    UserUnionGraph,
    UserFollowings,
    CSVWriter,
    Map,
  },
  mounted() {
    const elemsModal = document.querySelectorAll(".modal");
    this.modalInstance = M.Modal.init(elemsModal, { dismissible: false });
  },
  methods: {
    close() {
      document.getElementById("select-actions").selectedIndex = 0;
      this.componentState["selectedComponent"] = this.selectedComponent;
      this.modalInstance.destroy;
      this.$emit("close", this.componentState);
      // this.modalInstance[0].close();
    },
    addUser(username) {
            let data = {
        username: username,
      };
      const response = fetch("http://localhost:8000/api/v1/user_info/", {
        method: "post",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      this.$emit("addUser", data);
      console.log(response)
    },
  },
};
</script>

<style scoped>
#close-btn {
  height: 2rem;
  float: right;
}

#modal1 {
  /* position: relative; */
  height: 90%;
  max-height: 100%;
  max-width: 90%;
  width: 80%;
}
.modal-content {
  /* position: absolute; */
  height: 100%;
  width: 100%;
  z-index: 1003;
  display: block;
  opacity: 1;
  transform: scaleX(1) scaleY(1);
  /* top: 10%; */
}
</style>