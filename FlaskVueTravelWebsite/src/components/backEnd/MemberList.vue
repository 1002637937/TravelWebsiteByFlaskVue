<template lang="html">
  <el-row>
    <el-row  style="padding:10px 15px;background:#fff">
      <el-col :span="24">
        <el-button size="small" type="primary" @click="addMember">添加会员</el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span='24' >
          <el-table
             style='width:100%' align="center" :data="lists"  v-loading="listLoading" element-loading-text="拼命加载中">
              <el-table-column type='index' width="60" ></el-table-column>
              <el-table-column   prop="id" min-width="180" label="id" ></el-table-column>
              <!-- <el-table-column  prop="member" min-width="100" label="所属会员" ></el-table-column> -->
              <el-table-column  prop="user" min-width="180" label="会员名称" ></el-table-column>
              <el-table-column  prop="suggestion" min-width="180" label="意见建议" ></el-table-column>
              <el-table-column  min-width="200" label="操作" >
                <template scope='scope'>
                  <!--这里点击查看进入具体页面但是路径中必须带有admin,这时具体页面里会出现评论的删除选项  -->
                  <el-button size="small" type='primary' @click="editMember(scope.row)">详情</el-button>
                  <el-button size="small" type='danger' @click="remove(scope.row.id)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
        </el-col>
    </el-row>
    <!-- 表格结束 -->
    <el-row>
        <el-col :span="24">
          <el-dialog :title="formTitle" :visible.sync="formVisible">
            <el-form :model="memberInf" label-width="120px" ref="memberInf" :rules="formRule">
                <el-form-item label="会员登录名" prop="user">
                  <el-input v-model='memberInf.user' auto-complete='off'></el-input>
                </el-form-item>
                <el-form-item label="会员登录密码" prop="pwd">
                  <el-input v-model='memberInf.pwd' auto-complete='off'></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer">
              <el-button @click="formVisible = false">取 消</el-button>
              <el-button type="primary" @click="editSubmit" :loading="editLoading" >{{btnText}}</el-button>
            </div>
          </el-dialog>
          <!-- 弹窗结束 -->
        </el-col>
    </el-row>
  </el-row>
</template>

<script>
import axios from 'axios'
import api from '../../api'
import NProgress from 'nprogress'
import {sub} from '../../assets/js/commen'
export default {
    data(){
      return {
        lists:[],
        listLoading:false,
        formTitle:'',
        formVisible:false,
        memberInf:{
          id:0,
          user:'',
          pwd:'',
          suggestion:'无'
        },
        formRule:{
          user:[
            {required:true,message:'请输入会员名称',trigger:'blur'}
          ]
        },
        editLoading:false,
        btnText:'提交'
      }
    },
    methods:{
      // 获取会员列表
      getLists(){
        this.listLoading = true
        NProgress.start()
        api.getMemberList()
            .then((result)=>{
              setTimeout(()=>{
                this.listLoading =false
                this.lists = result.data;
                NProgress.done()
              },500)
        })
      },
      remove(id){
        this.$confirm('确认要删除吗?','提醒',{
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type:'waring'
        })
        .then(()=>{
          this.listLoading = true;
          NProgress.start();
          api.removeOneMember({id})
              .then((res)=>{
                this.listLoading = false
                NProgress.done()
                // 这里需要优化
                console.log(res)
                if(res.status==200){
                  this.$notify({
                    title:'成功',
                    message:'',
                    type:'success'
                  })
                  this.getLists()
                }else if(res.status==401){
                    this.$notify({
                    title:'失败',
                    message:'',
                    type:'error'
                  })
                   setTimeout(()=>{
                      this.$router.replace({path:'/login'})
                  },500)
                  return false//阻止继续执行
                  // 需要优化
                }
                console.log('get llist')
                this.getLists()
              }).catch(err=>{
                  // 这里可以跳转到错误页面
              })
        }).catch((err) => {
        })

      },
      // 显示创建会员弹窗
      addMember(){
        this.formVisible=true;
        this.formTitle = '新增';
        this.memberInf.user='';
      },
      // 显示编辑会员弹窗
      editMember(row){
        this.formVisible=true;
        this.formTitle = '编辑';
        this.memberInf.user = row.user
        this.memberInf.id = row.id
        this.memberInf.pwd = row.pwd
      },
      editSubmit(){
        this.$refs.memberInf.validate(valid=>{
          if(valid){
            this.$confirm('确认提交吗？',"提示",{})
                .then(()=>{
                    this.btnText = "提交中"
                    this.editLoading=true
                    NProgress.start()
                    // 新增会员
                    if(this.formTitle=='新增'){
                      // 这里又是一个异步提交
                      api.createMember({
                        ...this.memberInf
                      })
                      .then((res)=>{
                          NProgress.done();
                          sub(this,res)
                      })
                    }
                    else{
                      // 编辑
                        api.editMember({
                          ...this.memberInf
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
      }
    },
      mounted(){
        this.getLists();
      }
}
</script>

<style lang="css">
  .page{
    padding:10px;
    background:#fff;
  }
</style>
