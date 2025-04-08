<template>
  <div class="card h-100">
  
  <div class="card-body">
    <img :src="info.url" class="card-img-top" alt="slika" @click="$emit('goToSlike', info)"/>
    <p class="card-name">{{ info.houseName }}</p>
   <p class="card-text">{{ info.title }}</p>
   <div class="btn-container">
   <button @click="$emit('goToKomentar', info)" style="background-color:#71CFF2; color: black" class="btnKomentar">Komentar{{ info.komentar }}</button><br>
   <button @click.stop ="kontaktClick" style="background-color:#71CFF2; color: black" class="btn btn-primary">Kontakt{{ info.kontakt }}</button>
   
    
  </div>
</div>
</div>  
</template>

<script>
import { info } from 'sass';

export default {
  name: 'HouseCard',
  props: {
    info:{
      type: Object,
      required: true,
    },
  },
  
  methods:{
    kontaktClick(){
      this.$emit('kontakt', this.info);
    },
    },
  };

</script>

<style scoped>
.card {
 display: flex;
 flex-direction: column;
 box-shadow: 0 2px 5px;
 width: 350px;
 max-width: 350px;
 margin-bottom: 16px;

 
}

.card-item{
  display: flex;
  flex-direction: column;
  flex: 1 0 300%;
  max-width: 300px;
  max-height: 700px;
  margin-bottom: 16px;
  
  
}
.card-img-top {
  width: 100%px;
  height: 250px; 
  object-fit: cover;
  
}
.card-text {
  margin-bottom: 15px;
}
.card-body {
  padding: 15px;
}
.btn-container{
  display:flex;
  flex-direction: column;
  width: auto;
  
}
.btnKomentar, .btn-primary{
  height: 40px;
  font-size: 17px;
  border: none;
  border-radius: 5px;
}





</style>
