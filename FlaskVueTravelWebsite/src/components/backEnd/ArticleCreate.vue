<template lang="html">
  <el-row>
    <el-col :span="24">
      <el-form ref="articleCreate" :model="article" :rules="createRules" >
        <el-row style="margin-top:20px">
          <el-col :span='10' :push="1">
            <el-form-item label="游记标题" label-width="90px" prop="title">
              <el-input v-model="article.title" style="width:260px" placeholder="请在此处输入标题"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="10" :push="3" >
            <el-form-item label="所属景区" label-width="90px" prop="classify">
              <el-select v-model="article.classify" placeholder="请选择景区">
                <el-option v-for="item in classifyList" :label="item.classify" :value="item.id"></el-option>
            </el-select>
            </el-form-item>
          </el-col>
      </el-row>
        <el-row style="margin-top:20px">
          <el-col :span='12'>
            <!-- 编辑区 -->
            <el-form-item class="show" prop="content" >
               <el-input type="textarea" v-model="article.content" :rows="25" placeholder="请在此处编辑游记"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span='12'>
            <!-- 展示区 -->
            <div style="background:#fff;margin:0 0 0 20px;height:526px;overflow-y:auto;" v-html="markedToHtml"></div>
          </el-col>
        </el-row>
        <el-form-item style="padding:20px 20px 0 0 " >
          <el-button type="primary" style="float:right;" size='small' @click="createArticle" :loading="load">{{btnText}}</el-button>
            <el-button style="float:right;margin-right:10px" size='small' @click="cancle" :loading="load">取消</el-button>
      </el-form-item>
      </el-form>
    </el-col>
  </el-row>
</template>

<script>
import api from '../../api/index'
import marked from 'marked';
import hlj from 'highlight.js'
import  'highlight.js/styles/atom-one-dark.css'
import NProgress from 'NProgress'
export default {
  data(){
    return {
      article:{
        classify:'',//游记所属景区
        title:'',//游记标题
        content:''//游记内容
      },
      classifyList:[],
      createRules:{
        title:[
          { required: true, message: '请填写标题', trigger: 'blur' }
        ],
        content:[
          { required: true, message: '请输入内容', trigger: 'blur' }
        ],
        // classify:[
        //   { required: true, message: '请选择景区', trigger: 'change' }
        // ]
      },
      load:false,
      btnText:"立即发布"
    }
  },
  methods:{
    // 发布游记
    createArticle(){

        this.$refs.articleCreate.validate(valid=>{
          if(valid){
            this.$confirm("确认提交吗?","提示",{})
                .then(()=>{
                  NProgress.start()
                  this.load = true;
                    this.btnText = "发布中"
                    // 发送的游记信息

                    api.createArticle({
                      // contentToMark:this.markedToHtml,
                      ...this.article
                    })
                        .then(({data:{code,message}})=>{
                            this.btnText="立即发布";
                            this.editLoading = false;
                            if(code==200){
                                  this.$notify({
                                    title:'成功',
                                    message,
                                    type:'success'
                                  })
                                  NProgress.done()
                            }else if(code==401){
                              this.$notify({
                                title:'失败',
                                message,
                                type:'error'
                              })
                              NProgress.done()
                              setTimeout(()=>{
                                this.$router.push({path:'login'})
                              },500)
                              return false
                            }

                            setTimeout(()=>{
                              this.$router.push({path:'/admin/articleList'})
                            },500)
                        })
                })
                .catch((error)=>{
                })
          }
        })
    },
    // 取消
    cancle(){
      this.$router.push({path:'/admin/articleList'});
    }
  },
  computed:{
    markedToHtml(){
      marked.setOptions({
        highlight: function (code) {
        return hlj.highlightAuto(code).value;
        }
      });
      // console.log(this.article.content);
      return marked(this.article.content);
    }
  },
  mounted(){
    api.getClassify()
      .then((res)=>{
        if(res.status==200){
          this.classifyList = res.data
        }
      })
  }

}
</script>

<style lang="css" >
</style>
