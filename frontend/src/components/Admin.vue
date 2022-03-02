<template>
  <div class="admin">
      <div class="texts">
          <input type="text" placeholder="Name" v-model="actualUser.name" />
          <input type="text" placeholder="Location" v-model="actualUser.location" />
          <input type="text" placeholder="Username" v-model="actualUser.username" />
      </div>
      <input class="submit" type="button" @click="sendData" value="Send data" />
  </div>

</template>

<script>
import axios from "axios";

export default {
  name: "Admin",
  data() {
    return {
      actualUser: {
        name: "",
        location: "",
        username: "",
      },
    };
  },
    methods: {
      sendData(){
          axios.post("/new_user.api", this.actualUser, {
              headers: { "Access-Token": localStorage.getItem("Access-Token") },
          }).then(response => console.log(response.data))
          .catch(error => console.log(`Error!!! ${error}`))
          this.actualUser.name = ""
          this.actualUser.location = ""
          this.actualUser.username = ""
      }
    }
};
</script>

<style scoped lang="sass">
.admin
    display: flex
    flex-direction: column
    align-items: center
    margin-bottom: 20px
    padding: 0 10vw

.texts
    display: flex
    justify-content: center
    margin-bottom: 10px
    input
        margin: 0 10px
.submit
    width: 100px

</style>
