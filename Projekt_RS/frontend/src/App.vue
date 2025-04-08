<template>
<div id="app">
    <nav class="navbar navbar-expand-lg navbar-light">
      <div class="container-fluid">
        <div class="container-fluid navbar-grid">
      <div class="logo-search">
    <div class="navbar-brand">
      <img src="@/assets/Logo kuce za odmor.png" alt="Logo" 
       height="40"
       class="d-inline-block align-text-top">
    
  </div>
    <form class="d-flex" role="search">
      <input v-model="$store.state.searchTerm" class="form-control me-2" type="search" placeholder="Search" aria-label="Search" @input="updateSearchTerm">
    </form>
  </div>


  <div class="navbar-links">
      <ul class="  navbar-nav d-flex justify-content-center mb-0 ">
        <li class="nav-item">
          <router-link to="/" class="nav-link btn mx-4" style="background-color:#71CFF2; color: black" > Home</router-link> 
        </li>
        <li v-if = "!store.currentUser"  class="nav-item">
          <router-link to="/login" class="nav-link btn mx-4" style="background-color:#71CFF2; color: black" >Login</router-link>
        </li>
        <li v-if = "!store.currentUser" class="nav-item">
           <router-link to="/signup" class="nav-link btn mx-4" style="background-color:#71CFF2; color: black">Signup</router-link>
        </li>
        <li v-if = "currentUser" class="nav-item">
           <a href="#" v-on:click.prevent="logout" class="nav-link btn mx-4" style="background-color:#71CFF2; color: black">Logout</a>
        </li>
      </ul>
    </div>
  </div>  
</div> 
  </nav> 
  <div class="container">
  <router-view/>
</div>
  </div>

</template>

<script> 
import store from "@/store";
import router from '@/router';
import komentar from '@/views/Komentar.vue';


export default {
  name: "App",
  data(){
   return {
      store, 
      currentUser: null,
      searchTerm: ''
    };
  },
  methods:{
    logout() {
      try{
        localStorage.removeItem("authToken");
        console.log('Korisnik odjavljen');
        this.currentUser = null;
        this.$store.commit('setUser', null);
        this.$router.push({ name: 'home' });
      } catch(error) {
        console.error('Greška prilikom odjave: ', error.message);
      }
    },
  
  updateSearchTerm(event){
    const searchTerm = event.target.value;
    this.$store.commit('setSearchTerm', event.target.value);
    this.updateFilteredCards();
  }
},
  created(){
    const authToken = localStorage.getItem("authToken");
    if (authToken){
      try{
        this.$store.dispatch('fetchCurrentUser', authToken);
        console.log('Korisnik prijavljen');
      } catch (error){
        console.error("Greška prilikom dohvaćanja korisnika", error.message);
        localStorage.removeItem("authToken");
      }
    } else {
      console.log ('Nema prijavljenog korisnika');
      this.currentUser = null;
      this.$store.commit('setUser', null);
    }
  }
};


 

   
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
  background-color: #c7f97c !important;
.navbar-nav{
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
.navbar-grid{
  display: grid;
  grid-template-rows: auto auto;
  gap: 10px;
}
.logo-search{
  display:flex;
  justify-content: space-between;
  align-items: center;
}
.navbar-nav-container{
  margin-top:10px;
}
 
  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
