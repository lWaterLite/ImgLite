<template>
  <div class="bedrock-page">
    <div class="bedrock-container">
      <header class="header">
        <div>ImgLite</div>
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
  export default {
  name: "BedRock",
  data() {
    return {
      isRouterAlive: true
    }
  },
  provide() {
    return {
      reload: this.reload
    }
  },
  methods: {
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
</style>