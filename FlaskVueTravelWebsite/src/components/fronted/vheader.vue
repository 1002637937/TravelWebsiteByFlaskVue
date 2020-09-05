<template lang="html">
    <header>
      <div class="bg"></div>
        <nav  class="header-bg">
          <ul>
            <li><router-link to="/home">主页</router-link></li>
            <li><router-link to="/tags">景区</router-link></li>
            <li><router-link to="/mark">收藏</router-link></li>
            <li><router-link to="/about">关于我们</router-link></li>
            <li v-if='!this.$store.state.current_member_id'><router-link to="/member/login">登陆</router-link></li>
            <li v-if='this.$store.state.current_member_id'>
              <el-dropdown trigger="click">
                <span class="el-dropdown-link" style="color:#c0ccda;cursor: pointer;font-weight:700">
                  欢迎<i class="el-icon-caret-bottom el-icon--right"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item @click.native="editAdmin">密码修改</el-dropdown-item>
                  <el-dropdown-item divided @click.native="con">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </li>
          </ul>
        </nav>
        <!-- 导航 结束-->
        <el-dialog :title="formTitle" v-model="formVisible">
          <el-form :model="memberInf" label-width="120px" ref="memberInf">
              <el-form-item label="登录名" prop="user">
                <el-input v-model='memberInf.user' auto-complete='off'></el-input>
              </el-form-item>
              <el-form-item label="密码" prop="pwd">
                <el-input v-model='memberInf.pwd' auto-complete='off'></el-input>
              </el-form-item>
          </el-form>
          <div slot="footer">
            <el-button @click="formVisible = false">取 消</el-button>
            <el-button type="primary" @click="editSubmit" :loading="editLoading" >{{btnText}}</el-button>
          </div>
        </el-dialog>
        <section class="home_title">
          <transition name='fade'>
            <!-- <h1 v-if="show_headline">{{finalheadline}}</h1> -->
          </transition>
        </section>
    </header>
</template>

<script>
import {mapState} from 'vuex'
export default {
  data(){
    return {
      finalheadline:'',
      show_headline:true, 
      formTitle:'',
      formVisible:false,
      memberInf:{
        user:'',
        pwd:''
      },
      editLoading:false,
      btnText:'提交'
    }
  },
  computed:mapState(['headline']),
  watch:{
    headline(val){
      this.show_headline= false;
      setTimeout(()=>{
        this.show_headline = true;
        this.finalheadline = val
      },200)
    }
  },
  methods: {
    con(){
      this.$confirm('确认退出吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type:'warning'
      })
        .then(()=>{
          this.$store.dispatch('MemberLogout')
        })
        .catch(()=>{

        })
    },
    edit(){
      // console.log("in")
      this.formVisible=true;
      this.formTitle = '编辑';
      this.adminInf.user = this.adminInf.user
      this.adminInf.pwd = this.adminInf.pwd
      this.adminInf.id = this.adminInf.id
    },
    editSubmit(){
      this.$refs.adminInf.validate(valid=>{
        if(valid){
        this.$confirm('确认提交吗？',"提示",{})
            .then(()=>{
                this.btnText = "提交中"
                this.editLoading=true
                NProgress.start()
                // 新增会员
                if(this.formTitle=='新增'){
                  // 这里又是一个异步提交
                  api.createAdmin({
                    ...this.adminInf
                  })
                  .then((res)=>{
                      NProgress.done();
                      sub(this,res)
                  })
                }
                else{
                  // 编辑
                    api.editAdmin({
                      ...this.adminInf
                    })
                    .then((res)=>{
                      NProgress.done();
                      sub(this,res)
                    })
                }

            })
            .catch(err=>{
                //
            })
        }
      })
    },
  },
  mounted() {
    console.log(this)
  }
}
</script>

<style lang="css" scoped>
  .fade-enter-active,.fade-leave-active{
      transition: all .4s;
  }
  .fade-enter,.fade-leave-active{
    opacity: 0;
  }
  .el-dropdown{
    padding: 10px 0;
    font-size: 20px;
  }
  header{
    height: 30rem;
    display: flex;
    flex-direction: column;
  }
  .header-bg {
    color: #000;
  }
  .bg{
    z-index:-1;
    position: absolute;
    /* padding-top:5rem; */
    height:40rem;
    width: 100%;
    left:0;
    top:0;
    background-color: yellow;
      /*background-size: cover; 必须放在background-position后面用 "/" 分割*/
    background:  url('../../assets/img/bg_top.png') no-repeat center /cover;
    /* brightness()给图片应用一种线性乘法，使其看起来更亮或更暗。如果值是0%，图像会全黑。值是100%，
    则图像无变化。其他的值对应线性乘数效果。值超过100%也是可以的，图像会比原来更亮。如果没有设定值，默认是1。*/
    filter: brightness(0.7);
  }
  nav ul{
    display: flex;
    display: -webkit-flex;
    -webkit-justify-content:flex-end;
    justify-content: flex-end;
    margin:0;
    list-style: none;
  }
  nav a {
    font-size:2.0rem;
    display: block;
    padding: 1.2rem 1.8rem;
    color:#fff;
    opacity: 1;
    transition: opacity 0.3s;
    /*解决iphone下的a景区点击会出现底色*/
  }
  nav a:hover{
    opacity: 0.7;
  }
  .home_title{
    color: #fff;
     display: flex;
     margin: auto;
     max-width: 94%;
  }
  .home_title h1{
    margin:auto;
    font-size: 4rem;
    font-weight: 400;
  }

  @media screen and (max-width:768px){
    .home_title h1{
      font-size: 2.6rem;
    }
    .bg,header{
      height: 24rem;
    }
  }
  @media screen and (max-width:480px){
  header,.bg{
      height: 25rem;
    }
    nav a{
      font-size:1.6rem;
    }
  }
</style>
