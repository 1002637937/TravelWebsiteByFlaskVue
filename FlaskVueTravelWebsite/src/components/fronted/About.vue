<template lang="html">
  <div class="about" v-loading="loading2" element-loading-text="加载中">
    <div v-if="shows">
      <h2>我们介绍</h2>
      我们是小星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星星

      <h2>联系我们</h2>
      <p>手机：123456678</p>
      <p>微信：12345677</p>
      <p>微博：12346767</p>
    </div>
  </div>
</template>

<script>
export default {
  data(){
    return {
      shows:false,
      loading2:true
    }
  },
  mounted(){
    this.$store.dispatch('changeHeadLine','关于我们')
    setTimeout(()=>{
      this.$store.dispatch('showProgress', 100)
      this.shows = true;
      this.loading2 = false
    },300)
  }
}
</script>

<style lang="css" scoped>
  .about{
    margin:auto;
    margin-top:150px;
    width:50%;
  }

  .about a {
    color:#4078c0;
    display:inline-block;
    padding: 0.2rem 0.4rem;
    font-size: 1.6rem;
  }
  .about a:first-child{
    padding-left: 0;
  }
  .about p{
    font-size: 1.6rem;
    line-height: 1.6em;
  }

  .about a ,.about p,.about h2{
    margin: 1rem auto;
  }
  .about h2{
    font-weight: 400;
    font-size: 3rem;
    align-self: center;
    margin-top: 2rem;
  }
  @media screen and (max-width:480px){
    .about a,.about p{
      font-size: 1.4rem;
    }
    .about h2{
      margin-top: auto;
      font-size: 2.2rem;
    }
  }
</style>
