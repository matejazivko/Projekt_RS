
import {createStore} from 'vuex'

const store = createStore ({
    state:{
    searchTerm: "",
    user: null,
    userId: null,
    houseId:null,
    isAuthenticated: false,
   
},

mutations: {
    setUser(state, user) {
      state.user = user;
      state.userId = user ? user.uid : null;
      state.isAuthenticated = !!user;
    },
    logout(state) {
      state.user = null;
    },
    setAuthenticated(state, status){
      if (status){
      state.user = state.user || {email: 'default@example.com'};
  } else {
    state.user = null;
    state.userId = null;
    }
    state.isAuthenticated = status;
  },
  setComments(state, comments){
     state.comments = comments;
  },
},
actions:{
  setAuthenticated({commit}, status){
    commit('setAuthenticated', status);
  },
  fetchComments({commit}){
    commit('setComments', fetchedComments);
  }
},
setSearchTerm(state, term){
  state.searchTerm = term;
},
getters: {
    isAuthenticated: (state) => {
       return !!state.userId;
    },
    getUserId(state){
      return state.userId;
    },
    searchTerm: state => state.searchTerm,
  }
});
export default store;