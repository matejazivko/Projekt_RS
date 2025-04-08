<template>
    <div class="container">
    <h2 align="left">Interijer kuće</h2>
    <div class="d-grid gap-2 d-md-flex justify-content-md-end">
        <button @click="toggleForm" class="btn btn-primary">Dodaj slike</button>
        </div>
        <form v-if="showForm && isAuthenticated" @submit.prevent="uploadImage" class="form-inline mb-5">
          <img v-if="imageSrc" :src="imageSrc" alt="Slika interijera" class="preview-image"/>
          <input type="file" @change="onFileChange"/>
        <button type="submit" class="btn btn-success mt-3">Dodaj sliku</button>
        </form>
        <div class="row">
            <div v-for="card in filteredCards" :key="card.houseId" class="col-md">
                <div class="card">
                    <img :src="card.url" class="card-img-top" alt="Interijer kuće"/>
                </div>
            </div>
        </div>
   </div>
</template>

<script>

export default {
   name: 'Slike',
   data() {
     return {
      selectedHouseId: this.$route.query.houseId,
      filteredCards:[],
      imageSrc:"",
      showForm: false,
    };
   },
computed:{
    isAuthenticated(){
        return this.$store.getters.isAuthenticated;
    }
},
mounted(){
    this.getImages();
},
methods:{
    toggleForm(){
        if(this.isAuthenticated){
            this.showForm = !this.showForm;
        } else{
            alert('Prijavite se kako biste mogli dodati slike');
        }
    },
    async getImages(){
        try{
            const response = await fetch ("http://localhost:8000/houses", {
          method: "GET",
          headers:{
            "Content-Type": "application/json"
          }
        });
        if (!response.ok){
          throw new Error("Greška prilikom dodavanja slika");
        }
        const data = await response.json();
        this.filteredCards= data.filter(house => house.house_id === this.selectedHouseId)
        .map(house => ({
            url: house.image,
            houseId: house.houseId,
        }));                  
              
        } catch (error){
            console.error('Greška prilikom učitavanja slike', error);
        }
    },
    onFileChange(event){
        const file = event.target.files[0];
        if(file && file.type.startsWith('image/')){
            const reader = new FileReader();
            reader.onload = (error) => {
                this.imageSrc = error.target.result;
            };
            reader.readAsDataURL(file);
        }else{
            alert ('Odaberite ispravnu sliku');
        }
    },
    async uploadImage(){
        if(this.imageSrc && this.selectedHouseId){
            const formData = new FormData();
            formData.append("houseId", this.selectedHouseId);
            formData.append("image", this.imageFile);
            try{
                const reponse = await fetch ("http://localhost:8000/add_images",{
                    method: "POST",
                    body: formData
                });
                if (!response.ok){
                    throw new Error ("Greška prilikom dodavanja slike");
                }
                const result = await response.json();
                this.filteredCards.push({
                    url: result.image_path,
                    houseId: this.selectedHouseId
                });
                          
                this.imageSrc="";
                this.showForm = false;
            } catch (error){
                console.error ('Greška prilikom dodavanja slike', error);
            }
        }else {
            alert ('Odaberite sliku');
        }
    }
} 
};
</script> 

<style scoped>
.btn {
    background-color: gainsboro;
    color:black;
    border: none;
}

</style>