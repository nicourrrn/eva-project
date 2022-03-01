<template>
  <h2 class="page-name">User status</h2>
  <Admin v-if="isAdmin"></Admin>
  <Login
    v-if="needLogin"
    class="login-form"
    @access-loaded="
      (Admin) => {
        this.needLogin = false;
        this.isAdmin = Admin;
      }
    "
  ></Login>
  <div v-else class="users-status">
    <div class="column-name">
      <div>Name</div>
      <span>Location</span>
      <span>Status</span>
      <span>Score</span>
    </div>
    <UserStatus
      v-for="(user, index) in this.users"
      :name="user.name"
      :location="user.location"
      :status="user.status"
      :scope="user.scope"
      :key="index"
    ></UserStatus>
  </div>
</template>

<script>
import UserStatus from "@/components/UserStatus";
import Login from "@/components/Login";
import Admin from "@/components/Admin";
import axios from "axios";

export default {
  name: "App",
  components: {
    Admin,
    UserStatus,
    Login,
  },
  data() {
    return {
      users: [],
      needLogin: true,
      isAdmin: false,
    };
  },
  methods: {
    downloadUpdate() {
      axios
        .get(`http://localhost:8080/get_users.api`, {
          headers: { "Access-Token": localStorage.getItem("Access-Token") },
        })
        .then((response) => (this.users = response.data))
        .catch((error) => {
          console.log(error);
          this.needLogin = true;
        });
    },
    updater() {
      new Promise((resolve) => {
        !this.needLogin
          ? this.downloadUpdate()
          : console.log("Token not found");
        setTimeout(() => resolve(), 1000);
      }).then(this.updater);
    },
  },
  mounted() {
    let token = localStorage.getItem("Access-Token");
    this.needLogin = token === null || token === "undefined";
    if (!this.needLogin) {
      axios
        .get("http://localhost:8080/auth.api", {
          headers: { "Access-Token": this.token },
        })
        .then((response) => (this.isAdmin = response.data["Admin"]));
    }
    this.updater();
  },
};
</script>

<style lang="sass">
#app
  font-family: Avenir, Helvetica, Arial, sans-serif
  -webkit-font-smoothing: antialiased
  -moz-osx-font-smoothing: grayscale

.page-name
  text-align: center

.users-status
  display: flex
  flex-direction: column

.column-name
  margin: 0 20vw 10px
  display: flex
  justify-content: space-between
</style>
