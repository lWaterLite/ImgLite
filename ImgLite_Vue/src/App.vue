<template>
  <div id="content">
    <div id="router-view">
      <router-view></router-view>
    </div>
    <footer style="text-align: center; position: center; width: 100%;">
      <a href="https://beian.miit.gov.cn/" class="t-link">浙ICP备2022024080号-1</a>
    </footer>
  </div>
</template>

<script>
  import router from "@/router/index.js";
  import {axiosCredentialsInstance} from "@/utils/axios.js";

  export default {
    mounted() {
      axiosCredentialsInstance.get('token')
          .catch(err => {
            this.$message.error("凭证请求失败，请检查网络状况")
            console.log(err)
          })

      if (sessionStorage.getItem('status')){
        if (sessionStorage.getItem('status') === 'true') {
          router.push('/title')
        }
        else {
          router.push('/home')
        }
      }
      else if (this.$cookies.isKey('status')) {
        if (this.$cookies.get('status') === 'true') {
          router.push('/title')
        }
        else {
          router.push('/home')
        }
      }
      else {
        this.$cookies.set('status', 'false', '3d')
        router.push('/home')
      }
    }
  }
</script>

<style scoped>
  #content {
    display: flex;
    flex-direction: column;
    min-height: 100%;
  }

  #router-view {
    display: flex;
    flex: 1;
  }
</style>
