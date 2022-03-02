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
      <span>Last update</span>
    </div>
    <UserStatus
      v-for="(user, index) in this.$store.state.getUsers()"
      :name="user.name"
      :location="user.location"
      :status="user.status"
      :scope="user.scope"
      :last_seen="user.time"
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
      needLogin: true,
      isAdmin: false,
    };
  },
  methods: {
    updater() {
      new Promise((resolve) => {
        !this.needLogin
          ? this.$store.state.downloadUpdate()
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
        .get("/auth.api", {
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
