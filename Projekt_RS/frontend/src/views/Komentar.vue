<template>
    <div class="about">
        <h2 align="left">Komentari</h2>
        <div class="container">
            <div class="row">
                <div class="col-sm"></div>
                <div class="col-sm">
                   
                    <form v-if="isAuthenticated" @submit.prevent="addComment">
                        <div class="mb-3">
                            <label for="exampleFormControlTextarea1" class="form-label">Vaša poruka</label>
                            <textarea v-model="commentText" class="form-control" id="exampleFormControlTextarea1" rows="3"></textarea>
                        </div>
                        <button style="background-color:#71CFF2; color: black" type="button" class="btn btn-primary" @click="addComment">Dodaj komentar</button>
                        <button style="background-color:#71CFF2; color: black" type="button" class="btn btn-primary" @click="editComment" >Izmjeni komentar</button>
                        <button style="background-color:#71CFF2; color: black" type="button" class="btn btn-primary" @click="deleteComment">Obriši komentar</button><br><br>
                     </form>
                    <p v-if="successMessage" class="text-success">{{ successMessage }}</p>
                    <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>
                    <div v-if="comments.length > 0">
                    <div v-for="(comment, index) in comments" :key = "index" class="comment-box">
                        <p>Kuća: {{ comment.houseName }}</p>  
                        <p class="comment-text">{{ comment.text }}</p>
                         <button class="btn-izmjeni" v-if="isAuthenticated && comment.userId === $store.state.userId" @click = "selectedCommentToEdit(comment)">Izmjeni</button>
                        </div>
                    </div>
                </div>
                  </div>
                <div class="col-sm"></div>
            </div>
         </div>
         
    
</template>
    
<script>

export default{
    name: "komentar",
    data(){
        return{
            commentText: "",
            houses: [],
            selectedComment: null,
            selectedHouseName: "",
            selectedHouseId: null,
            successMessage: "",
            errorMessage: "",
        };
    },
    computed: {
        isAuthenticated(){
            return this.$store.getters.isAuthenticated;
        },
        comments(){
            return this.$store.state.comments || [];
        }
       
    },
     mounted(){
        console.log("Selected House Name:", this.$route.query.houseName);
        console.log("Selected House ID:", this.$route.query.houseId);
            if(!this.$route.query.houseId){
                console.error("Nedostaju podaci o kući");
                alert ("Kuća nije pronađena");
                return;
            }
            this.selectedHouseId = this.$route.query.houseId;
            this.selectedHouseName = this.$route.query.houseName;
            this.fetchComments();
       
        
    },

    methods: {
        async fetchComments(){
            if (!this.selectedHouseId){
                console.error("Id nije definiran");
                return;
            }
            try{
                const response = await fetch('http://localhost:8000/comments?houseId=${this.selectedHouseId}',{
                  method: "GET",
                  headers:{
                    "Content-Type": "application/json",
                    "Authorization": 'Bearer ${localStorage.getItem("authToken")}'
                  }  
                });
                if (!response.ok){
                    throw new Error("Greška u dohvaćanju komentara");
                }
                    const fetchedComments = await response.json();
                    this.$store.commit('setComments', fetchedComments);
                    console.log("Filtrirani komentari:", fetchedComments); 
                } catch(error){
                this.errorMessage = "Pogreška prilikom učitavanja kuće!";
                console.error(error);
            }
        },
    
        async addComment(){
            if(!this.commentText){
                this.errorMessage = "Komentar ne može biti prazan";
                return;
            }
            if(!this.selectedHouseName || !this.selectedHouseId){
                this.errorMessage = "Nedostaju podaci";
                return;
                
            }
            const newComment = {
                text: this.commentText,
                houseName: this.selectedHouseName,
                houseId: this.selectedHouseId,
                userId: this.$store.state.userId,
            };
            try{
                const response = await fetch ("http://localhost:8000/comments",{
                    method: "POST",
                    headers:{
                        "Content-Type": "application/json",
                        "Authorization": 'Bearer ${localStorage.getItem("authToken")}'
                    },
                    body:JSON.stringify(newComment)
                });
                if (!response.ok){
                    throw new Error("Greška u dodavanju komentara");
                }
                this.commentText ='';
                this.successMessage = "Komentar je uspješno dodan";
                this.fetchComments();
            } catch (error){
                this.errorMessage = "Greška u dodavanju komentara";
                console.error(error);
            }
        },
            
        selectedCommentToEdit(comment){
            this.commentText = comment.text;
            this.selectedHouseName = comment.houseName;
            this.selectedHouseId = comment.houseId;
            this.selectedComment = comment;
    },
        async editComment(){
            if (this.commentText && this.selectedComment){
                if(this.selectedComment.userId !== this.$store.state.userId){
                    this.errorMessage ="Niste autor ovog komentara, ne možete ga izmijeniti!";
                    return;
                }
              try {
                const updatedComment = {text: this.commentText};
                const response = await fetch('http://localhost:8000/comments/${this.selectedComment.id}', {
                    method: "PUT",
                    headers:{
                        "Content-Type": "application/json",
                        "Authorization": 'Bearer ${localStorage.getItem("authToken")}'
                    },
                    body: JSON.stringify(updatedComment)
                });  
                if (!response.ok){
                    throw new Error("Greška prilikom izmjene komentara!")
                }
                this.successMessage = "Komentar je uspješno izmijenjen!";
                this.commentText =  "";
                this.fetchComments();
            } catch (error){
                this.errorMessage = "Greška prilikom izmjene komentara!";
            }
        }
    },
           
        async deleteComment(){
            if(this.selectedComment.userId !== this.$store.state.userId){
                    this.errorMessage ="Niste autor ovog komentara, ne možete ga izbrisati!";
                    return;
            }
            try {
                const response = await fetch('http://localhost:8000/comments/${this.selectedComment.id}', {
                    method: "DELETE",
                    headers:{
                        "Content-Type": "application/json",
                        "Authorization": 'Bearer ${localStorage.getItem("authToken")}'
                    }
                });  
                if (!response.ok){
                    throw new Error("Greška prilikom brisanja komentara!")
                }
                this.successMessage = "Komentar je uspješno obrisan!";
                this.fetchComments();           
             } catch (error){
                this.errorMessage = 'Greška pri brisanju komentara';
                console.error(error);
            }
      }
    }
}
    


</script>
<style scoped>
.container{
    display: grid;
    place-items: center;
    position: absolute;
    top:30%;
    left: 0%;
    transform: translate(-8%, 20%);
}
.row{
    display: flex;
    justify-content: center;
    width: 100%;
}
.comment-box{
    border: 1px solid black;
    border-radius: 6px;
    padding: 20px;
    margin-bottom: 5px;
    display: flex;
    position: relative;
    flex-direction: column;    
    justify-content: flex-start;  
    align-items: flex-start;
    width: 100%;
}

.comment-text{
    font-size: 16px;
    width: 100%;
    white-space: pre-wrap;
    margin-left: 0px;
    position: relative;
    left: 0px;
    text-align: left;


}
.btn-izmjeni{
    background-color: #71CFF2;;
    border-radius: 5px;
    border: none;
    position:absolute;
    right: 10px;
    bottom: 10px;
    padding: 8px, 16px;
    cursor: pointer;
}

.house-post{
    border: 1px solid black;
    padding: 10px;
    margin: 10px 0;
}
</style>