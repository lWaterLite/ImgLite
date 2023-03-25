<template>
  <div class="bedrock-page">
    <div class="bedrock-container">
      <header class="header">
        <div class="left">ImgLite</div>
        <div class="title-user right">
          <el-popover>
            <template #reference>
              <el-button :icon="User" circle size="large"/>
            </template>
            <template #default>
              <div>
                <el-popover
                    trigger="hover"
                    placement="left">
                  <template #reference>
                    <div class="title-user-item">
                      <el-icon class="title-user-item-icon" color="#409EFF" size="20"><Document /></el-icon>
                      <div class="title-user-item-text">报表</div>
                    </div>
                  </template>

                  <div class="title-form-item" @click="handleGetCsv">
                    <div>CSV</div>
                  </div>
                  <div class="title-form-item" @click="handleGetExcel">
                    <div>Excel</div>
                  </div>
                </el-popover>
              </div>
              <div class="title-user-item" @click="handleLogout">
                <el-icon class="title-user-item-icon" color="red" size="20"><SwitchButton /></el-icon>
                <div class="title-user-item-text">登出</div>
              </div>
            </template>
          </el-popover>
        </div>
      </header>
      <div class="body">
        <aside class="navi">
          <div class="ul">
            <div class="li-item" @click="toUploads()">
              <div>上传图片</div>
            </div>
            <div class="li-item" @click="toView()">
              <div>浏览图片</div>
            </div>
          </div>
        </aside>
        <main class="main">
          <router-view v-if="isRouterAlive"></router-view>
        </main>
      </div>
    </div>
  </div>
</template>

<script>
  import {User, SwitchButton} from "@element-plus/icons-vue";
  import {markRaw} from "vue";
  import {axiosDefaultInstance, baseURL} from "@/utils/axios.js";

  export default {
  name: "BedRock",
  data() {
    return {
      isRouterAlive: true,
      User: markRaw(User),
      SwitchButton: markRaw(SwitchButton)
    }
  },
  provide() {
    return {
      reload: this.reload,
      userUUID: ''
    }
  },
  methods: {
    handleGetExcel() {
      window.open(baseURL+'state/excel?userUUID='+this.userUUID, '_blank')
    },
    handleGetCsv() {
      window.open(baseURL+'state/csv?userUUID='+this.userUUID, '_blank')
    },
    handleLogout() {
      if (sessionStorage.getItem('userUUID')) {
        sessionStorage.removeItem('userUUID')
        sessionStorage.setItem('status', 'false')
      }
      else {
        this.$cookies.remove('userUUID')
        this.$cookies.set('status', 'false')
      }
      this.$router.replace('/home')
    },
    reload() {
      this.isRouterAlive = false;
      this.$nextTick(() => {
        this.isRouterAlive = true;
      })
    },
    toUploads() {
      if (this.$route.path !== '/uploads') {
        this.$router.push('/uploads')
      }
    },
    toView() {
      if (this.$route.path !== '/view') {
        this.$router.push('/view')
      }
    }
  },
  mounted() {
    if (sessionStorage.getItem('userUUID')) {
      this.userUUID = sessionStorage.getItem('userUUID')
    }
    else if (this.$cookies.isKey('userUUID')) {
      this.userUUID = this.$cookies.get('userUUID')
    }
  }
  }
</script>

<style scoped>

  .bedrock-container {
    height: 100%;
    display: flex;
    flex-direction: column;
  }

  .bedrock-page {
    width: 100%;
    margin: 0;
  }

  .header {
    width: auto;
    padding: 12px 60px 12px 60px;
    margin-bottom: 3px;
    font-size: 32px;
    background-color: #ecf5ff;
  }

  .body {
    flex-grow: 1;
    position: relative;
    display: flex;
  }

  .navi {
    width: 240px;
  }

  .main {
    flex: 1;
    margin-right: 5px;
  }

  .li-item {
    background-color: #ffffff;
    height: 54px;
    line-height: 54px;
    text-align: center;
    vertical-align: middle;
    display: block;
    font-size: 20px;
    cursor: default;
    border-bottom-style: solid;
    border-width: 1px;
    border-color: rgb(235,238,245);
  }

  .li-item:last-child {
    border-bottom-style: none;
  }

  .li-item:hover {
    background-color: #f5f7fa;
    transition: 0.4s;
  }

  .title-user {
    margin-right: 3.5em;
  }

  .left {
    float: left;
  }

  .right {
    float: right;
  }

  .title-user-item {
    display: flex;
    font-size: 16px;
    vertical-align: center;
    border-radius: 10px;
    cursor: pointer;
    padding-top: 0.7em;
    padding-bottom: 0.7em;
  }

  .title-user-item:hover {
    background-color: #f5f7fa;
    transition: 0.3s;
  }

  .title-user-item-icon {
    margin-left: 0.5em;
    padding-top: 1px;
  }

  .title-user-item-text {
    margin-bottom: 2px;
    margin-left: 1em;
  }

  .title-form-item {
    font-size: 16px;
    vertical-align: center;
    border-radius: 10px;
    cursor: pointer;
    padding-top: 0.4em;
    padding-bottom: 0.4em;
    text-align: center;
  }

  .title-form-item:hover {
    background-color: #f5f7fa;
    transition: 0.3s;
  }
</style>