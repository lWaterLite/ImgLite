<template>
    <div id="home">
      <div id="container">
        <div id="title">ImgLite</div>
        <div id="button-container">
          <button class="submit" @click="toLogin">登录</button>
          <button class="submit" @click="toRegister">注册</button>
        </div>
      </div>
    </div>
</template>

<script>
import router from "@/router/index.js";

export default {
  name: "Home",
  methods: {
    toLogin() {
      router.push('/login')
    },
    toRegister() {
      router.push('/register')
    }
  }
}
</script>

<style scoped>
  #home {
    position: relative;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    margin: auto;
    border-radius: 5px;
    border-style: solid;
    border-color: #aaaaaa;
    box-shadow: 3px 3px 10px #888888;
  }

  #container {
    margin: 72px 32px 72px;
  }

  #title {
    font-size: 64px;
    margin: 50px 50px 30px;
  }

  .submit {
    color: #f0f0f0;
    font-size: 32px;
    width: 120px;
    height: 60px;
    border-style: none;
    border-radius: 10px;
    background-color: #409EFF;
  }

  .submit:hover {
    background-color: #d9ecff;
    color: #777777;
    transition: 0.3s;
  }

  #button-container {
    display: flex;
    justify-content: space-evenly;
    margin-bottom: 32px;
  }
</style>