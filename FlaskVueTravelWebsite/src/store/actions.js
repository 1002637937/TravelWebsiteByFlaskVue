import Vue from 'vue'
import api from '../api'
import router from '../routes'
import MsgAlert from './MsgAlert'
export default {
// 后台注册
  AdminReg ({commit}, data) {
    api.localReg(data)
       .then((res) => {
         if (res.status === 200) {
           commit('ADMIN_REG', res.data.token)
           router.replace({path: '/admin'})
         } else {
          //  上一个catch处理了MongoError
           MsgAlert(res.data.message)
         }
       })
       .catch((error) => {
         MsgAlert(error.toString())
       })
  },
  //  后台登录
  AdminLogin ({commit}, data) {
    api.localLogin(data)
          .then((res) => {
            if (res.status === 200) {
              // 找到用户
              commit('ADMIN_SIGNIN', {'token': res.data.token, 'data': res.data.data})
              router.replace({path: '/admin/articleList'})
            } else {
              // 没找到用户或者密码不对
              MsgAlert(res.data.message)
            }
          })
          .catch(error => {
            // 一般服务器连接不上这里就会报网络错误
            MsgAlert(error.toString())
          })
  },
  AdminLogout ({commit}) {
    commit('ADMIN_SIGNOUT')
    router.push({path: '/login'})
  },
  // 前台注册
  MemberReg ({commit}, data) {
    api.localMemberReg(data)
       .then((res) => {
         if (res.status === 200) {
           commit('MEMBER_REG', res.data.token)
           router.replace({path: '/member/login'})
         } else {
          //  上一个catch处理了MongoError
           MsgAlert(res.data.message)
         }
       })
       .catch((error) => {
         MsgAlert(error.toString())
       })
  },
  //   前台登录
  MemberLogin ({commit}, data) {
    api.localMemberLogin(data)
          .then((res) => {
            if (res.status === 200) {
              // 找到用户
              commit('MEMBER_SIGNIN', {'token': res.data.token, 'data': res.data.data})
              router.replace({path: '/'})
            } else if (res.status === 402) {
              alert('请先注册')
            } else {
              // 没找到用户或者密码不对
              MsgAlert(res.data.message)
            }
          })
          .catch(error => {
            // 一般服务器连接不上这里就会报网络错误
            MsgAlert(error.toString())
          })
  },
  MemberLogout ({commit}) {
    commit('MEMBER_SIGNOUT')
    router.push({path: '/'})
  },
  showProgress ({commit}, number) {
    commit('SHOW_PROGRESS', number)
  },
  changeHeadLine ({commit}, headline) {
    commit('HEAD_LINE', headline)
  }
}
