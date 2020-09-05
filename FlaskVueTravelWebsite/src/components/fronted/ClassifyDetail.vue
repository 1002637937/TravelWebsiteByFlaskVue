<template lang="html">
    <div class="wrap" style='width: 60%;margin: auto;margin-top: 140px;' v-loading="loading2"  element-loading-text="加载中">
        <h1>简介</h1>
        <div class="describe">
          {{describe}}
        </div>
        <h1>游记</h1>
        <transition-group name="list" tag="div" >
            <article v-for='item in articleLists' v-if='show' :key="item.id" >
                <header>
                    <div>
                        <router-link :to="{path:`/article/${item.id}`}" class="tags_title" >
                        {{item.title}}
                        </router-link>
                    </div>
                    <div>
                        <p class="tags_creatAt">{{item.created_at}}</p>
                    </div>
                </header>
                <section v-html="item.content.slice(0,200) + '...'" class="tags_main" ></section>
                <footer>
                    <router-link class="tags_readMore" :to="{path:`/article/${item.id}`}">阅读全文>></router-link>
                </footer>
            </article>
        </transition-group>
    </div>
</template>

<script>
import api from '../../api'
import vfoot from './vfooter'
import Classify from "./Classify"
export default {
  name:"Tag",
  data(){
    return {
      classes_:[],
      articleLists:[],
      loading2:true, 
      show:false,
      describe:''
    }
  },
  methods: {
    getArticles(classify){
      api.getArticlesByClassify({"id":classify})
          .then((res)=>{
           
            if(res.status==200){
                this.articleLists = res.data
                setTimeout(()=>{
                    this.show = true;
                    this.loading2 = false;
                },200)

            }
          })
          .catch(err=>{
            alert(err.message)
          })
    },
    getClassifyDescribe(classify){
      api.getOneClassify({"id":classify})
          .then((res)=>{
            if(res.status==200){
                this.describe = res.data.describe
                // setTimeout(()=>{
                //     this.show = true;
                //     this.loading2 = false;
                // },200)

            }
          })
          .catch(err=>{
            alert(err.message)
          })
    }
  },
  mounted(){
      this.getArticles(this.$route.params.id)
      this.getClassifyDescribe(this.$route.params.id)
  }
}
</script>

<style>
.wrap{
    width: 60%;
    margin: auto;
    margin-top: 140px;
}
.tags_title {
  font-size: 30px;
}
footer {
  margin-top: 10px;
}
article{
  margin-bottom:40px;
}
.describe {
    margin-bottom: 50px;
    border: #467373 solid;
    font-style: italic;
    font-size: 20px;
    padding: 20px;
}
</style>