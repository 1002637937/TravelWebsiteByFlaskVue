// 各种Store
export default {
  member_token: isMemberLoggedIn() || null,
  token: isLoggedIn() || null,
  progress: 0,
  headline: '',
  current_member_id: isCurrentMember().id || null,
  current_member_user: isCurrentMember().user || null,
  current_admin_id: isCurrentAdmin().id || null,
  current_admin_user: isCurrentAdmin().user || null
  // 每次刷新页面或者再次访问的时候都会重新渲染状态,
  // 这里相当于给每次刷新重新设置初始值
}

function isLoggedIn () {
  let token = localStorage.getItem('jwt')
  return token
  // if (token) {
  //   const payload = JSON.parse(window.atob(token.split('.')[1]))
  //     // 前端判断token是否过期，如果过期了访问时候会路由到login页面
  //   if (payload.exp > Date.now() / 1000) {
  //     return token
  //   }
  // } else {
  //   return false
  // }
}

function isCurrentAdmin () {
  let currentAdmin = localStorage.getItem('current_admin')
  if (!currentAdmin) {
    return {'id': null, 'user': null}
  }
  return currentAdmin
}

function isCurrentMember () {
  let currentMember = localStorage.getItem('current_member')
  if (!currentMember) {
    return {'id': null, 'user': null}
  }
  return currentMember
}

function isMemberLoggedIn () {
  let token = localStorage.getItem('jwt_member')
  return token
  // if (token) {
  //   const payload = JSON.parse(window.atob(token.split('.')[1]))
  //     // 前端判断token是否过期，如果过期了访问时候会路由到login页面
  //   if (payload.exp > Date.now() / 1000) {
  //     return token
  //   }
  // } else {
  //   return false
  // }
}
