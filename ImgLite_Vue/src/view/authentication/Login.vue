<template>
  <div class="card">
    <div class="container">
      <div class="back-button" @click="this.$router.push('/home')">X</div>
      <div class="title">登录</div>
      <div class="card-input">
        <input type="text" placeholder="请输入账户" v-model="userAccount"><br>
        <input type="password" placeholder="请输入密码" v-model="userPassword"><br>
        <div><input type="checkbox" id="autologin" v-model="autoLogin"><label>自动登录</label></div>
      </div>
      <div v-if="loginErrorStatus" class="card-error-msg">{{this.loginErrorMsg}}</div>
      <div class="card-submit">
        <input type="button" value="登录" @click="onLoginSubmit" />
      </div>
    </div>
  </div>
</template>

<script>
import "@/css/card.css"
import {axiosDefaultInstance} from "@/utils/axios.js";
import Rsa from '@/utils/crypt.js'

export default{
  name: "Login",
  data() {
    return {
      loginErrorMsg: '',
      loginErrorStatus: false,
      userAccount: '',
      userPassword: '',
      autoLogin: false
    }
  },
  mounted() {
    window.addEventListener("keydown", this.keyDown)
  },
  unmounted() {
    window.removeEventListener('keydown', this.keyDown, false)
  },
  methods: {
    keyDown(e) {
      if (e.keyCode === 13) {
        this.onLoginSubmit(this.userAccount, this.userPassword, this.autoLogin)
      }
    },
    onLoginSubmit() {
      if (this.userAccount === '' || this.userPassword === '') {
        this.loginErrorStatus = true
        this.loginErrorMsg = '请输入账号和密码!'
        return
      }
      let account = Rsa.rsaPublicData(this.userAccount)
      let password = Rsa.rsaPublicData(this.userPassword)
      axiosDefaultInstance.get('auth/login?userAccount='+account+'&userPassword='+password)
          .then(response => {
            this.loginErrorStatus = false
            if (this.autoLogin) {
              this.$cookies.set('userUUID', response.data['userUUID'],"7d")
              this.$cookies.set('status', response.data['status'], "7d")
            }
            else {
              sessionStorage.setItem('userUUID', response.data['userUUID'])
              sessionStorage.setItem('status', response.data['status'])
            }
              this.$router.push('/title')
          })
          .catch(err => {
            this.loginErrorStatus = true
            try {
              if (err.response.data['message'] !== undefined) {
                this.loginErrorMsg = err.response.data['message']
                this.$cookies.set('status', 'false', "3d")
              }
            }
            catch (e) {
              this.loginErrorMsg = '登录失败，请检查网络状况!'
              console.log(e)
            }
          })
    }
  }
}
</script>

<style scoped>

  #autologin {
    margin: 0 3px 0 0;
  }

</style>