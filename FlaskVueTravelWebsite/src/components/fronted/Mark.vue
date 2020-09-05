<template lang="html">
  <div class="tags_wrap"  v-loading="loading2"  element-loading-text="加载中">
    <el-autocomplete
      v-model="selected_classify"
      :fetch-suggestions="querySearchItem"
      prefix-icon="el-icon-search"
      placeholder="搜索景区名称"
      @select="searchItemSelect"
      class='search' />
    <!-- <ul class="tags_list"> -->
    <div class='classify_wrapper'>
      <Classify v-for="class_ in classes_" v-on:refresh-classify="getMarkClassify" :name="class_.classify" page='mark' :id='class_.id' :img_path='class_.img_path'/>
    </div>
    <!-- </ul> -->
  </div>
</template>

<script>
import api from '../../api'
import vfoot from './vfooter'
import Classify from "./Classify"
import store from '../../store'
export default {
  name:"Tag",
  data(){
    return {
      classes_:[],
      articleLists:[],
      selected_classify:"",
      selected:9,
      show:true,
      loading2:true,
      list_show:true
    }
  },
  watch:{
    
  },
  components:{
    vfoot,
    Classify
  },
  methods:{
      querySearchItem(queryString, cb) {
        var classes_ = this.classes_
        // 为这个数组中每一个对象加一个value字段
        // 因为autocomplete只识别value字段并在下拉列中显示
        // 多数情况后台数据中是没有value的属性的
        // 要自己建一个数组，给每一项设置value
        for (let i of classes_) {
          i.value = i.classify
        }
        // queryString指输入框中输入的值，若无输入默认显示全部内容，有则显示匹配内容
        var results = queryString ? classes_.filter(this.createStateFilter(queryString)) : classes_
        // 设置回调时间，延迟显示列表，不设置的话直接cb(results)就可以了
        clearTimeout(this.timeout)
        this.timeout = setTimeout(() => {
          // 回调函数cb，返回匹配到的内容
          cb(results)
        }, 300 * Math.random())
    },
    // 字母模糊匹配
    createStateFilter(queryString) {
      return (state) => {
        return (state.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0)
      }
    },
    // 处理选中项
    searchItemSelect() {
      console.log('选中项')
    },
    gets(index,classify){
      this.$store.dispatch('changeHeadLine',classify)
      this.show = false;
      this.selected = index
      this.getArticles(classify)
    },
    getMarkClassify(){

      this.$store.dispatch('changeHeadLine','收藏')
      // 根据景区名获取游记列表
      let current_member_id = store.state.current_member_id
      setTimeout(()=>{
        if (current_member_id){
          api
          .getClassifyByMember({"id":current_member_id})
          .then((res)=>{
            if(res.status==200){

                this.loading2=false;
                this.classes_ = res.data
                console.log("更新完毕",this.classes_);
                // this.getArticles('Vue')
              }
            }).catch(err=>{
          alert(err.message);
        })
      }else{
        alert("请先登录")
        this.classes_ = []
        this.loading2=false;
      }
      },300)
    }
  },
  mounted(){
    this.getMarkClassify()
  }

}
</script>

<style lang="css" scoped>
.list-enter-active,.list-leave-active{
  transition: all .3s
}
.list-enter,.list-leave-active{
  opacity: 0;
}
.classify_wrapper {
  display: flex;
  flex-wrap: wrap;
}
h2,h4{
  margin:0;
}
.search {
  /* margin-top: -100px; */
  width:60%;
  margin-left: 20%;
  margin-bottom:100px;
}
p,.tags_main p{
  margin:0;
}
.classify_wrapper{
  width:100%;
  margin:auto;
}
.tags_list{
  margin:0;
  padding:0;
  list-style: none;
  display: flex;
  display:-webkit-flex;
  -webkit-flex-wrap:wrap;
  flex-wrap: wrap;
}
.tags_list li{
  margin:.4rem;
}
.tags_list li a{
  display: block;
  padding: .6rem 1.6rem;
  border:1px solid #d2d2d2;
  border-radius: .6rem;
  color:rgba(0, 0, 0, .8);
  font-size: 1.8rem;
  /*transition渐变*/
   background-color: #f7f7f7;
   transition: all .4s;
   cursor: pointer;
}
.tags_list li a:hover,.tags_list li .active{
    /*transition渐变*/
  background-color: #555555;
    color: #fff;
}
.tags_wrap{
  margin:auto;
  list-style: none;
}
.tags_wrap article{
  padding-bottom: 1rem;
  border-bottom:1px solid #d2d2d2;
}
.tags_title{
  display: block;
  font-size: 3rem;
  font-weight: 400;
  color:#404040;
  padding:1rem 0;
}
.tags_creatAt{
  font-family: "Comic Sans MS", curslve, sans-serif;
  padding:0.6rem 0;
  font-size: 1.8rem;
  color:#7f8c8d;
}
.tags_main{
  font-size: 1.6rem;
  color:#34495e;
  line-height: 1.6em;
  padding:1rem 0;
}
footer{
  text-align: right;
}
.tags_readMore{
  font-size: 2rem;
  color:#919191;
  font-weight: 600;
}
@media screen and (max-width:786px){
  .tags_title{
    font-size: 2.4rem;
  }
  .tags_creatAt{
    font-size: 1.6rem;
  }
  .tags_list li{
    margin:.2rem;
  }
  .tags_list li a{
    font-size: 1.4rem;
  }
}
@media screen and (max-width:480px){
  .tags_main{
    font-size:1.4rem;
  }
  .tags_readMore{
    font-size: 1.8rem;
  }
}
</style>
