<template>
  <div class="about">
  <h2>This is an login page</h2>
  <div class="container">
  <div class="row">
  <div class="col-sm"></div>
  <div class="col-sm">
  <form @submit.prevent="login">
  <div class="form-group">
  <label for="exampleInputEmail1">Email</label>
  <input type="email" v-model="email" class="form-control"
  id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter
  email"  autocomplete="email"/>
  <small id="emailHelp" class="form-text text-muted" >We'll
  never share your email with anyone else.</small>
  </div>
  <div class="form-group">
  <label for="exampleInputPassword2">Password</label>
  <input type="password" v-model="password" class="form-control"
  id="exampleInputPassword1" placeholder="Password"  autocomplete="current-password"/>
  </div>
  <button style="background-color:#71CFF2; color: black"  type="submit" class="btn btn-primary" >Login</button> <br><br>
  <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>
  </form>
  
  </div>
  <div class="col-sm"></div>
  </div>
  </div>
  </div>
 
  </template>

<script>

export default {
  data() {
    return {
      email: '',
      password: '',
      errorMessage: '',
            
      
    };
  },
  methods: {
    async login() {
       if (!this.email || !this.password){
        this.errorMessage = "Unesite email i lozinku";
        return;
       }
       const loginData = {
        username: this.email,
        password: this.password
       };
       try{
        const response = await fetch ("http://localhost:8000/login", {
          method: "POST",
          headers:{
            "Content-Type": "application/json"
          },
          body: JSON.stringify(loginData)
        });
        if (!response.ok){
          const errorData = await response.json();
          throw new Error(errorData.detail || "Greška prilikom prijave");
        }
        const data = await response.json();
          console.log('Uspješna prijava', data.message);
          localStorage.setItem("authToken", data.token || "");
          this.$router.replace({name:'home'});
        } catch(error) {
          this.errorMessage = error.message || "Greška prilikom prijave, pokušajte ponovo";
          }
        }
      },
      
  };
</script>