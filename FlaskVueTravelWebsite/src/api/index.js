// 各种api
// 负责用instance和服务端进行交互

import axios from 'axios'
import store from '../store'
// axios.defaults.headers.common['Authorization'] = 'dailu';
axios.defaults.headers.post['Content-Type'] = 'application/json'

const instance = axios.create()
const front_instance = axios.create()
instance.defaults.headers.post['Content-Type'] = 'application/json'
if (localStorage.getItem('jwt')) {
  /* localStorage.getItem('jwt')是带引号的字符串
    Bearer token(通过Authorization头部字段发送到服务端便于验证)的格式：Bearer XXXXXXXXXX
  */
  instance.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('jwt').replace(/(^\")|(\"$)/g, '')
}
// axios拦截请求
axios.interceptors.request.use = instance.interceptors.request.use = front_instance.interceptors.request.use
front_instance.interceptors.request.use(config => {
  store.dispatch('showProgress', 20)
  return config
}, err => {
  // store.dispatch('showProgress',100)
  return Promise.reject(err)
})
// axios拦截响应
front_instance.interceptors.response.use(response => {
  store.dispatch('showProgress', 100)
  return response
}, err => {
  store.dispatch('showProgress', 100)
  return Promise.reject(err)
})
export default {
  // 注册
  localReg (data) {
    return axios.post('/api/admin/register', data)
  },
  // 登录
  localLogin (data) {
    return axios.post('/api/admin/login', data)
  },
  localMemberReg (data) {
    return axios.post('/api/member/register', data)
  },
  // 登录
  localMemberLogin (data) {
    return axios.post('/api/member/login', data)
  },
  // 获取游记列表{带分页获取}
  getArticleList (data) {
    return instance.post('/api/article/list', data)
  },
  // 不带分页获取游记
  getArticleLists (params) {
    return front_instance.post('/api/article/list', params)
  },
  // 根据classify获取游记列表
  getArticlesByClassify (params) {
    return front_instance.post('/api/article/article_by_classify/' + String(params.id), params)
  },
  // 创建游记
  createArticle (params) {
    return instance.post('/api/article/create', params)
  },
// 删除一篇游记
  removeOneArticle (params) {
    return instance.post('/api/article/delete/' + String(params.id), params)
  },
// 根据postID获取一篇游记(带权限)
  getOneArticle (params) {
    // console.log(params)
    return instance.post('/api/article/' + String(params.id), params)
  },
// 根据postID获取一篇游记(不带权限)
  getOneArticleNoAuth (params) {
    return front_instance.post('/api/article/noAuth', params)
  },
// 编辑一篇游记
  editArticle (params) {
    return instance.post('/api/article/update', params)
  },
  // 获取景区列表
  getClassify () {
    return instance.get('/api/classify/list')
  },
  getOneClassify (params) {
    return instance.post('/api/classify/' + String(params.id), params)
  },
  // 根据classify获取游记列表
  getClassifyByMember (params) {
    return front_instance.post('/api/classify/classify_by_member/' + String(params.id), params)
  },
  // 根据classify获取游记列表
  getClassifyByPlace (params) {
    return front_instance.post('/api/classify/classify_by_place/' + String(params.id), params)
  },
  getNoAuthClass () {
    return front_instance.get('/api/classify/list')
  },

  // 删除某一个景区
  removeOneClassify (params) {
    return instance.post('/api/classify/delete/' + String(params.id), params)
  },
  // 添加景区
  addClassify (params) {
    return instance.post('/api/classify/create', params)
  },

  // 编辑景区
  editClassfy (params) {
    return instance.post('/api/classify/update', params)
  },

   // 获取地区列表{带分页获取}
  getPlaceList (data) {
    return instance.post('/api/place/list')
  },
  // 不带分页获取地区
  getPlaceLists (params) {
    return front_instance.post('/api/place/list', params)
  },
  // 根据classify获取地区列表
  getPlacesByClassify (params) {
    return front_instance.post('/api/place/list', params)
  },
  // 创建地区
  createPlace (params) {
    return instance.post('/api/place/create', params)
  },
// 删除地区
  removeOnePlace (params) {
    console.log(params)
    return instance.post('/api/place/delete/' + String(params['id']), params)
  },
// 根据postID获取一地区(带权限)
  getOnePlace (params) {
    return instance.post('/api/place/onePage', params)
  },
// 根据postID获取一地区(不带权限)
  getOnePlaceNoAuth (params) {
    return front_instance.post('/api/place/noAuth', params)
  },
// 编辑一地区
  editPlace (params) {
    return instance.post('/api/place/update', params)
  },

  // 获取会员列表{带分页获取}
  getMemberList (data) {
    return instance.post('/api/member/list')
  },
  // 不带分页获取会员
  getMemberLists (params) {
    return front_instance.post('/api/member/list', params)
  },
  // 根据classify获取会员列表
  getMembersByClassify (params) {
    return front_instance.post('/api/member/list', params)
  },
  // 创建会员
  createMember (params) {
    return instance.post('/api/member/create', params)
  },
// 删除会员
  removeOneMember (params) {
    console.log(params)
    return instance.post('/api/member/delete/' + String(params.id), params)
  },
// 根据postID获取一会员(带权限)
  getOneMember (params) {
    return instance.post('/api/member/' + String(params.id), params)
  },
// 根据postID获取一会员(不带权限)
  getOneMemberNoAuth (params) {
    return front_instance.post('/api/member/noAuth', params)
  },
// 编辑一会员
  editMember (params) {
    return instance.post('/api/member/update', params)
  },
  addMark (params) {
    return front_instance.post('/api/mark/create', params)
  },
  deleteMark (params) {
    return front_instance.post('/api/mark/delete/' + String(params.classify), params)
  }
}
