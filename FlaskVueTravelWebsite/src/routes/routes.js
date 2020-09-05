import Reg from '../components/backEnd/Reg'
import Login from '../components/backEnd/Login'
import Admin from '../components/backEnd/Admin'
import MemberLogin from '../components/fronted/frontLogin'
import MemberReg from '../components/fronted/frontReg'
import ArticleCreate from '../components/backEnd/ArticleCreate'
import ArticleList from '../components/backEnd/ArticleList'
import ArticleEdit from '../components/backEnd/ArticleEdit'
import ClassList from '../components/backEnd/ClassList'
import MemberList from '../components/backEnd/MemberList'
import PlaceList from '../components/backEnd/PlaceList'
import Home from '../components/fronted/Home'
import Front from '../components/fronted/Front'
import About from '../components/fronted/About'
import Tags from '../components/fronted/Tags'
import Mark from '../components/fronted/Mark'
import ClassifyDetail from '../components/fronted/ClassifyDetail'
import Article from '../components/fronted/Article'
import NotFound from '../components/NotFound'
export default [

  {
    path: '/reg',
    component: Reg,
    meta: {auth: false},
    hidden: true
  },

  {
    path: '/',
    component: Front, // 这是游记页
    hidden: true,
    children: [
      {path: '', redirect: 'home', meta: {auth: false}},
      {path: 'home', component: Home, meta: {auth: false}},
      {path: 'about', component: About, meta: {auth: false}},
      {path: 'tags', component: Tags, meta: {auth: false}},
      {path: 'mark', component: Mark, meta: {auth: false}},
      {path: 'article/:id', component: Article, meta: {auth: false, scrollToTop: true}},
      {path: 'classify/:id', component: ClassifyDetail, meta: {auth: false, scrollToTop: true}}
    ]
  },
  {
    path: '/member/login',
    component: MemberLogin,
    meta: {auth: false},
    hidden: true
  },
  {
    path: '/member/reg',
    component: MemberReg,
    meta: {auth: false},
    hidden: true
  },
  {
    path: '/login',
    component: Login,
    meta: {auth: false},
    hidden: true
  },
  {
    // 后台路由
    path: '/admin',
    component: Admin,
    name: '管理面板',
    iconCls: 'el-icon-message',
    children: [
      {
        // 游记列表单独一个组件(可以删除并且编辑，编辑的时候需要跳转到另一个路由)
        path: '', hidden: true, redirect: {name: '游记管理'}
      },
      {
        // 游记列表单独一个组件(可以删除并且编辑，编辑的时候需要跳转到另一个路由)
        path: 'articleList', component: ArticleList, name: '游记管理'
      },
      {
        // 创建游记单独一个组件
        path: 'articleCreate', component: ArticleCreate, name: '创建游记', hidden: true
      },
      {
        path: 'articleEdit/:postId', component: ArticleEdit, hidden: true, name: '编辑游记'
      },
      {
        path: 'classList', component: ClassList, name: '景区管理'
        // 创建景区直接在景区列表里面出现弹层
      },
      {
        path: 'placeList', component: PlaceList, name: '地区管理'
        // 创建景区直接在景区列表里面出现弹层
      },
      {
        path: 'memberList', component: MemberList, name: '会员管理'
        // 创建景区直接在景区列表里面出现弹层
      }
    ]
  },
  {
    path: '*', component: NotFound, hidden: true
  }
  //

  // {path:'/404',component:NotFound}
]
