<template>
    <div class="login">
        <input class="token-input" type="text" placeholder="Token" v-model="token"/>
        <input @click="checkData" type="button" value="Load data"/>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "Login",
    data() {
        return {
            token: "",
        }
    },
    methods: {
        async checkData() {
            let response = await axios.get("http://localhost:8080/auth.api", {
                headers: {"Access-Token": this.token}
            }).catch(error => alert(error))

            if (response.data["Access"] === "OK") {
                localStorage.setItem("Access-Token", this.token)
                this.$emit("access-loaded", response.data["Admin"])
            } else {
                console.log(response)
            }
        },
    }
}
</script>

<style scoped lang="sass">

.login
    display: flex
    justify-content: center
    input
        margin: 0 10px
    .token-input
        width: 50vw

</style>