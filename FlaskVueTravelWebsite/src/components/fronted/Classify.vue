<template lang="html">
    <div class="classify">
      <router-link tag='div' :to="{path:`/classify/${this.id}`}" class='top_img' :style="{'height':'300px', 'width': '300px', 'background-image': 'url('+img_path+')'}">
      </router-link>
      <div class='under'>
        <div class="classify_name">
          {{name}}
        </div>
        <el-button @click='markSubmit(id)' icon="el-icon-star-off" round v-if="page == 'home' || page == 'tags'  ">加收藏</el-button>
        <el-button @click="cancelSubmit(id);$emit('refresh-classify');" icon="el-icon-star-off" round v-if="page == 'mark'">取消收藏</el-button>
      </div>

    </div>

</template>

<script>
import store from '../../store'
import api from '../../api'
export default {
  props: {
    name:'',
    page:'',
    id:'',
    img_path:''
  },
  name: "Home",
  data() {
    return {
      places:[],
      classes_: [],
      selected_classify: '',
      items: [],
      loading2: true,
      loadMoreFlag: false,
      loadMoreText: "加载更多",
      loadMoreShow: false,
      // page: 1,
      limit: 10,
      
    };
  },
  components: {

  },
  computed: {
    img_background() {
      return  {"background":  "url(${this.img_path}) no-repeat center /cover;"}
    }
  },
  methods: {
    markSubmit(classify_id){
      // current_member_id = store.state.current_member_id
      if (store.state.current_member_id) {
        // console.log(store.state)
        let current_member_id = store.state.current_member_id
        api
        .addMark({"id":current_member_id, "classify":classify_id})
        .then((res) => {
          if (res.status == 200) {
            setTimeout(() => {
              // 回调 
              alert("收藏成功")
            }, 200);
          }
        });
      }
      else{
        alert("请先登录")
      }
    },
    cancelSubmit(classify_id){
      let current_member_id = store.state.current_member_id
      if (current_member_id) {
        api
        .deleteMark({"id":current_member_id, "classify":classify_id})
        .then((res) => {
          if (res.status == 200) {
            console.log(("取消收藏成功"))
            setTimeout(() => {
              // 回调 
              console.log(("取消收藏成功"))
            }, 200);
          }
        });
      }
      else{
        alert("请先登录")
      }
    }
  },
  mounted() {
    // console.log('background: url(\'' + this.img_path  + '\') no-repeat center /cover;')
  },
};
</script>
<style lang="css" scoped>
.top_img {
  width:300px;
  height:300px;
  /* background:  url('../../assets/img/classify.jpg') no-repeat center /cover; */
  /* background:  url(var(--img_background)) no-repeat center /cover; */
}
.classify {
  border-color: aqua;
  border-style: solid;
  margin: 10px
}
.under {
  display: flex;
  margin: 8px;
}
.classify_name {
  width: 80%;
  text-align: left;
  padding: 10px 20px;
  font-size: 20px;
}
</style>