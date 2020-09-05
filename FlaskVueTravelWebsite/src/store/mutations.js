import {ADMIN_SIGNIN, ADMIN_SIGNOUT, ADMIN_REG, MEMBER_SIGNIN, MEMBER_SIGNOUT, MEMBER_REG, SHOW_PROGRESS, HEAD_LINE} from './types'
export default {
  [ADMIN_REG] (state, token) {
    localStorage.setItem('jwt', token)
    state.token = token
  },
  [ADMIN_SIGNIN] (state, dict) {
    localStorage.setItem('jwt', dict.token)
    localStorage.setItem('current_admin', dict.data)
    state.token = dict.token
    state.current_admin_id = dict.data.id
    state.current_admin_user = dict.data.user
  },
  [ADMIN_SIGNOUT] (state) {
    localStorage.removeItem('jwt')
    localStorage.removeItem('current_admin')
    state.token = null
    state.current_admin_id = null
    state.current_admin_user = null
  },
  [MEMBER_REG] (state, token) {
    localStorage.setItem('jwt_member', token)
    state.token = token
  },
  [MEMBER_SIGNIN] (state, dict) {
    localStorage.setItem('jwt_member', dict.token)
    localStorage.setItem('current_member', dict.data)
    state.token = dict.token
    state.current_member_id = dict.data.id
    state.current_member_user = dict.data.user
  },
  [MEMBER_SIGNOUT] (state) {
    localStorage.removeItem('jwt_member')
    localStorage.removeItem('current_member')
    state.token = null
    state.current_member_id = null
    state.current_member_user = null
  },
  [SHOW_PROGRESS] (state, number) {
    state.progress = number
  },
  [HEAD_LINE] (state, headline) {
    state.headline = headline
  }
}
