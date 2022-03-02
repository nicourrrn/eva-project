import { createStore } from "vuex";
import axios from "axios";

export default createStore({
  state: {
    users: [],
  },
  getters: {
    getUsers(state) {
      return state.users
    }
  },
  mutations: {
    setUsers(state, newUsers) {
      state.users = newUsers;
    },
  },
  actions: {
    async downloadUpdate(context) {
      let users = await axios
        .get(`/get_users.api`, {
          headers: { "Access-Token": localStorage.getItem("Access-Token") },
        })
        .then((response) => response.data)
        .catch((error) => {
          console.log(error);
          this.needLogin = true;
        });
      for (let i = 0; i < users.length; i++) {
        users[i].time = new Date(users[i].time).toLocaleString();
      }
      context.commit("setUsers", users);
    },
  },
});
