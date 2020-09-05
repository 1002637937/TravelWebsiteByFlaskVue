<template lang="html">
  <article v-loading="loading2"  element-loading-text="加载中" style='width: 60%;' class="article_wrap article">
    <header>
      <div class="home_title">{{oneArticle.title}}</div>
    <div>
      <p class="home_creatAt">{{oneArticle.created_at}}</p>
    </div>
  </header>
  <section v-html="oneArticle.content" class="home_main"></section>
</article>
</template>

<script>
import api from '../../api'
export default {
  data(){
    return {
      oneArticle:{},
      loading2:true
    }
  },
  created(){
    // 在这里调用获取一篇游记的api
    api.getOneArticle({id:this.$route.params.id})
      .then((res) => {
        if(res.status==200){
          setTimeout(()=>{
            this.loading2 = false
            this.oneArticle = res.data
          },100)
        }
      })
  }
}
</script>

<style lang="css" scoped>
article{
  margin:auto;
  /*margin-bottom:1rem;*/
  margin-top: 150px;
  width: 60%;
}

.home_title{
  font-size: 4rem;
  font-weight: 400;
  color:#404040;
  padding:1rem 0;
  margin-bottom: 20px;

}
.home_creatAt{
  font-family: "Comic Sans MS", curslve, sans-serif;
  padding:0.6rem 0;
  font-size: 1.8rem;
  color:#7f8c8d;
  /*background: red;*/
  margin:0;
}
.home_main{
  font-size: 1.6rem;
  line-height: 1.6em;
}

@media screen and (max-width:786px){
  .home_title{
    font-size: 2.2rem;
  }
  .home_creatAt{
    font-size: 1.6rem;
  }
}
@media screen and (max-width:480px){
  .home_main{
    font-size:1.4rem;
    line-height: 1.6em;
  }
}
</style>
