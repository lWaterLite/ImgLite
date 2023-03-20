<template>
  <div class="upload-page">
    <div class="upload-container">
      <div class="el-upload-container">
        <el-upload
            ref="upload"
            accept=".jpg, .png, .bmp"
            :auto-upload="false"
            :on-change="handleChange"
            :action="baseURL + 'image/upload'"
            :http-request="handleHttpRequest"
            class="upload-demo"
            drag
            multiple>
          <el-icon class="el-icon--upload"><upload-filled/></el-icon>
          <div class="el-upload__text">
            拖动文件或<em>点击开始上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              仅支持jpg、png、bmp格式，文件大小不超过5MB
            </div>
          </template>
        </el-upload>
        <el-button size="large" type="primary" @click="onSubmit">上传</el-button>
      </div>
      <div class="display-list-container">
        <el-table :data="imgList" v-show="!(imgList.length === 0)">
          <el-table-column prop="imgFilename" label="文件名称"/>
          <el-table-column label="直链地址">
            <template #default="scope">
              <el-link target="_blank"
                       :underline="false"
                       type="primary"
                       :href="baseURL+'p/'+ scope.row.imgUUID">{{baseURL+'p/'+ scope.row.imgUUID}}</el-link>
            </template>
          </el-table-column>
          <el-table-column width="300px" label="操作">
            <template #default="scope">
              <el-button size="small" @click="onCopy(scope.row.imgUUID)">复制</el-button>
              <el-button size="small" type="primary" @click="onDownload(scope.row.imgUUID)">下载</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script>
import {axiosCredentialsInstance, baseURL, uploadConfig} from "@/utils/axios.js";
import {ElNotification} from "element-plus";

export default {
  name: "Uploads",
  data() {
    return {
      baseURL: baseURL,
      imgList: []
    }
  },
  methods: {
    onDownload(imgUUID) {
      window.open(baseURL+'d/'+imgUUID, '_blank')
    },
    onCopy(imgUUID) {
      this.$copyText(baseURL+'p/'+imgUUID)
          .then(() => {
            this.$message.success('复制成功!')
          })
          .catch((err) => {
            this.$message.error('复制失败!')
            console.log(err)
          })
    },
    async handleHttpRequest(fileObject) {
      let userUUID
      if (sessionStorage.getItem('userUUID')) {
        userUUID = sessionStorage.getItem('userUUID')
      }
      else if (this.$cookies.isKey('userUUID')) {
        userUUID = this.$cookies.get('userUUID')
      }
      else {
        this.$message.error('获取uuid失败，请尝试重新登录!')
        return
      }

      let formData = new FormData()
      formData.append('file', fileObject.file)
      formData.append('userUUID', userUUID)
      await axiosCredentialsInstance.post('image/upload', formData, uploadConfig)
          .then(response => {
            this.imgList.push(response.data)
          })
          .catch(err => {
            ElNotification({
              title: '上传失败!',
              message: '请检查网络状况',
              type: 'error'
            })
            console.log(err)
          })
    },
    async onSubmit() {
      await axiosCredentialsInstance.get('token')
          .catch(err => {
            ElNotification({
              title: '请求凭证错误!',
              message: '请检查网络状况',
              type: 'error'
            })
            console.log(err)
          })
      await this.$refs.upload.submit()
    },
    handleChange(file, fileList) {
      if (file.name.substring(0, file.name.lastIndexOf('.')).length > 127) {
        this.$message.error('文件名太长，请修改')
        fileList.pop()
      }
      if (file.size / 1024 / 1024 > 5) {
        this.$message.error('文件太大了，请小于5MB.')
        fileList.pop()
      }
    }
  }
}
</script>

<style scoped>
  .el-upload-container {
    margin-left: 20%;
    margin-right: 20%;
    text-align: center;
  }

  .display-list-container {
    margin-left: 10%;
    margin-right: 10%;
  }
</style>