<template>
    <div class="about">
    <h2>Kontakt obrazac</h2>
    <div class="container">
    <div class="row">
    <div class="col-sm"></div>
    <div class="col-sm">
      <div v-if = "isAuthenticated">
    <form @submit.prevent="submitContactForm">
       <div class="form-group">
    <label for="NameAndSurname">Name and surname</label>
    <input type="text" v-model= "nameAndSurname" class="form-control"
    id="NameAndSurname" placeholder="Enter your name and surname" />
    <small id="emailHelp" class="form-text text-muted" >We'll
    never share your email with anyone else.</small>
    </div>
    <div class="form-group">
    <label for="exampleInputEmail1">Email</label>
    <input type="email" v-model="email" class="form-control"
    id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email" />
    <small id="emailHelp" class="form-text text-muted" >We'll
    never share your email with anyone else.</small>
    </div>
    <div class="mb-3">
  <label for="exampleFormControlTextarea1" class="form-label">Vaša poruka</label>
  <textarea class="form-control" v-model="message" id="exampleFormControlTextarea1" rows="3"></textarea>
</div>
    <button style="background-color:#71CFF2; color: black" type="submit" class="btn btn-primary">Pošalji</button>
    <button style="background-color:#71CFF2; color: black" @click.prevent="clearForm" class="btn btn-primary">Očisti</button>
    </form>
    <p v-if="successMessage" class="text-success">{{ successMessage }}</p>
    <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>
    </div>
    <div v-else><router-link to="/login"></router-link></div>
    </div>
    <div class="col-sm"></div>
    </div>
    </div>
    </div>
    
</template>

<script>

import store from '@/store.js';

export default {
      name: "kontakt",
data() {
return {
nameAndSurname: "",
email: "",
message: "",
houseId: "",
successMessage: "",
errorMessage: ""
};
},
computed: {
  isAuthenticated(){
    return this.$store.getters.isAuthenticated;
  },
},
beforeRouteEnter(to, from, next){
  const isAuthenticated = store.getters.isAuthenticated;
  if (!isAuthenticated){
    next ({name: 'login'});
  
  }else{
    next();
  }
},

methods: {
  
    async submitContactForm(){
        if (!this.nameAndSurname || !this.email || !this.message){
            this.errorMessage = "Sva polja moraju biti popunjena!";
            return;
        }
        const contactData = {
          house_name: this.$route.query.houseName || "",
          sender_email: this.email,
          message: this.message
        };
       
    try {
      const response = await fetch('http://localhost:8000/send}',{
                  method: "POST",
                  headers:{
                    "Content-Type": "application/json",
                    "Authorization": 'Bearer ${localStorage.getItem("authToken")}'
                  },
                  body: JSON.stringify(contactData)
                  
                });
                if (!response.ok){
                    throw new Error("Greška prilikom slanja poruke");
                }
                const responseData = await response.json();
                this.successMessage = responseData.message;
                this.clearForm();
              } catch (error){
                  this.errorMessage = `Greška prilikom slanja poruke: ${error.message}`;
              }
            },
            clearForm(){
            this.nameAndSurname="";
            this.email = "";
            this.message = "";
            }
          }
            
        };
        
    
    </script>
