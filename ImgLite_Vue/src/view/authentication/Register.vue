<template>
  <div class="card">
    <div class="container">
      <div class="back-button" @click="this.$router.push('/home')">X</div>
      <div class="title">注册</div>
      <div class="card-input">
        <input type="text" placeholder="请输入账户" v-model="userAccount" @blur="accountCheck"><br>
        <input type="text" placeholder="请输入密码" v-model="userPassword" @blur="passwordCheck"><br>
        <input type="text" placeholder="请输入邀请码" v-model="inviteCode" @blur="inviteCodeCheck">
      </div>
      <div v-if="registerErrorStatus" class="card-error-msg">{{this.registerErrorMsg}}</div>
      <div class="card-submit">
        <input type="button" value="注册" @click="onRegisterSubmit">
      </div>
    </div>
  </div>
</template>

<script>
import {axiosCredentialsInstance, registerConfig} from "@/utils/axios.js";
import router from "@/router/index.js";
import {ElNotification} from "element-plus";
import Rsa from '@/utils/crypt.js'

export default {
  name: "Register",
  mounted() {
    window.addEventListener("keydown", this.keyDown)
  },
  unmounted() {
    window.removeEventListener('keydown', this.keyDown, false)
  },
  data() {
    return {
      userAccount: '',
      userPassword: '',
      inviteCode: '',
      registerErrorMsg: '',
      registerErrorStatus: false
    }
  },
  methods: {
    keyDown(e) {
      if (e.keyCode === 13) {
        this.onRegisterSubmit()
      }
    },
    accountCheck() {
      if (this.userAccount === '') {
        this.registerErrorStatus = true
        this.registerErrorMsg = "请输入账号!"
      }
      else if (this.userAccount.length > 10) {
        this.registerErrorStatus = true
        this.registerErrorMsg = "账号长度请小于10个字符!"
      }
      else {
        this.registerErrorStatus = false
      }
    },
    passwordCheck() {
      if (this.userPassword === '') {
        this.registerErrorStatus = true
        this.registerErrorMsg = "请输入密码!"
      }
      else if (this.userPassword.length > 15) {
        this.registerErrorStatus = true
        this.registerErrorMsg = "密码长度请小于15个字符!"
      }
      else {
        this.registerErrorStatus = false
      }
    },
    inviteCodeCheck() {
      if (this.inviteCode === '') {
        this.registerErrorStatus = true
        this.registerErrorMsg = "请输入邀请码!"
      }
      else {
        this.registerErrorStatus = false
      }
    },
    async onRegisterSubmit() {
      this.accountCheck()
      if (this.registerErrorStatus === true) return
      this.passwordCheck()
      if (this.registerErrorStatus === true) return
      this.inviteCodeCheck()
      if (this.registerErrorStatus === true) return

      await axiosCredentialsInstance.get('token')
          .catch(err => {
            ElNotification({
              title: '请求凭证错误!',
              message: '请检查网络状况',
              type: 'error'
            })
            console.log(err)
          })

      let userAccount = Rsa.rsaPublicData(this.userAccount)
      let userPassword = Rsa.rsaPublicData(this.userPassword)
      let inviteCode = Rsa.rsaPublicData(this.inviteCode)
      await axiosCredentialsInstance.post('auth/register',{
          userAccount,
          userPassword,
          inviteCode
        }, registerConfig)
          .then(() =>{
            router.replace('/home')
            ElNotification({
              title: '注册成功',
              message: '您成功注册了图床账户，请登录后使用。',
              type: 'success'
            })
          })
          .catch(err => {
            this.registerErrorStatus = true
            this.registerErrorMsg = err.response.data['message']
            this.$cookies.set('status', err.response.data['status'], '3d')
          })
    }
  }
}
</script>

<style scoped>

</style>