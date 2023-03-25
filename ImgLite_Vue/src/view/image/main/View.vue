<template>
  <div class="view-page">
    <div class="view-container">
      <el-table :data="filterImgList" ref="viewTable">
        <el-table-column label="文件名称" min-width="250">
          <template #default="scope">
            <el-popover trigger="hover" placement="bottom">
              <template #reference>
                <el-link target="_blank"
                         :underline="false"
                         type="primary"
                         :href="baseURL+'r/'+ scope.row.imgUUID">{{ scope.row.imgFilename }}</el-link>
              </template>
              <el-image :src="baseURL+'image/thumb/'+ scope.row.imgUUID" fit="scale-down"  />
            </el-popover>
          </template>
        </el-table-column>
        <el-table-column prop="imgUploadDate" label="上传日期"/>
        <el-table-column width="300px">
          <template #header>
            <el-input size="small" v-model="searchData"
                      placeholder="在此输入搜索"/>
          </template>
          <template #default="scope">
            <el-button size="small" @click="onCopy(scope.row.imgUUID)">复制</el-button>
            <el-button size="small" type="primary" @click="onDownload(scope.row.imgUUID)">下载</el-button>
            <el-popconfirm
                width="150"
                @confirm="onDelete(scope.row.imgUUID)"
                confirm-button-text="确定"
                cancel-button-text="取消"
                confirm-button-type="danger"
                :icon="WarningFilled"
                icon-color="#E6A23C"
                title="你确定要删除吗">
              <template #reference>
                <el-button size="small" type="danger">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
      <div style="display: flex; justify-content: center">
        <el-pagination layout="prev, pager, next, jumper"
                       :page-count="pageCount"
                       v-model:current-page="currentPage"
                       @current-change="handleCurrentChange"/>
      </div>
    </div>
  </div>
</template>

<script>
import {ElMessage} from "element-plus";
import {axiosCredentialsInstance, axiosDefaultInstance, baseURL, deleteConfig} from "@/utils/axios.js";
import {WarningFilled} from "@element-plus/icons-vue";

export default {
  inject: ['reload'],
  mounted() {
    if (sessionStorage.getItem('userUUID')) {
      this.userUUID = sessionStorage.getItem('userUUID')
    }
    else if (this.$cookies.isKey('userUUID')) {
      this.userUUID = this.$cookies.get('userUUID')
    }
    else {
      this.$message.error('获取uuid失败，请尝试重新登录')
      return
    }

    axiosDefaultInstance.get('image/page', {
      params: {
        userUUID: this.userUUID
      }
    })
        .then(res => {
          this.pageCount = res.data['pageCount']
        })
        .catch(err => {
          this.$message.error('请求分页失败，请尝试刷新页面或检查网络状况')
          console.log(err)
        })

    axiosDefaultInstance.get('image/images', {
      params: {
        userUUID: this.userUUID,
        page: this.currentPage
      }
    })
        .then(response => {
          this.imgList = response.data
          this.filterImgList = this.imgList
        })
        .catch(err => {
          console.log(err)
          this.$message.error("获取图片数据失败，请尝试刷新页面")
        })
  },
  name: "View",
  data() {
    return {
      searchData: '',
      baseURL: baseURL,
      imgList: [
        {
          "imgUUID": "",
          "imgFilename": "",
          "imgUploadDate": ""
        },
      ],
      filterImgList: [],
      WarningFilled,
      pageCount: 0,
      currentPage: 1,
      userUUID: ''
    }
  },
  methods: {
    handleCurrentChange() {
      axiosDefaultInstance.get('image/images', {
        params: {
          userUUID: this.userUUID,
          page: this.currentPage
        }
      })
          .then(response => {
            this.imgList = response.data
            this.filterImgList = this.imgList
          })
          .catch(err => {
            console.log(err)
            this.$message.error("获取图片失败，请尝试刷新页面")
          })
    },
    onDelete(imgUUID) {
      axiosCredentialsInstance.delete(baseURL+'image/delete', {
        params: {
          imgUUID,
          userUUID: this.userUUID
        },
        headers: deleteConfig.headers
      })
          .then(res => {
            this.$message.success("图片删除成功!")
            console.log(res.data['message'])
            this.reload()
          })
          .catch(err => {
            console.log(err)
          })
    },
    onDownload(imgUUID) {
      window.open(baseURL+'d/'+imgUUID, '_blank')
    },
    onCopy(imgUUID) {
      this.$copyText(baseURL+'r/'+imgUUID)
          .then(() => {
            ElMessage({
              duration: 2000,
              type: 'success',
              'show-close': true,
              message: '复制成功'
            })
          })
          .catch(() => {
            ElMessage({
              message: '复制失败',
              type: 'warning'
            })
          })
    }
  },
  watch: {
    searchData() {
      if (this.searchData === '') {
        this.filterImgList = this.imgList
      }
      else {
        this.filterImgList = this.imgList.filter(
            data => data.imgFilename.toLowerCase().includes(this.searchData.toLowerCase())
        )
      }
    }
  }
}
</script>

<style scoped>

</style>