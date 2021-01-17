<template>
  <div class="container">
    <div class="btns">
      <a-upload :fileList="vfileList" name="pic" :action="uploadURL" :multiple="EnableMultiple" :beforeUpload="beforeUpload"
        :transform-file="transformFile"
        accept=".png,.jpg">
        <a-button type="primary" class="upload-button">
          <a-icon type="upload" /> 上传1
        </a-button>
      </a-upload>
      <a-button type="primary" :disabled="bindFileList.length === 0" :loading="uploading" style="margin-top: 16px"
        @click="handleUpload">
        {{ uploading ? 'Uploading' : 'Start Upload' }}
      </a-button>
    </div>
    <div class="cardlist">
      <tiny-card-list :picList="cardList"></tiny-card-list>
    </div>
  </div>
</template>

<script>
  import TinyCardList from '../components/content/TinyCardList.vue'
  // import {
  //   message
  // } from "ant-design-vue";
  export default {
    name: 'SiderUpload',
    // props:['']
    components: {
      TinyCardList,
    },
    methods: {
      //文件状态改变的钩子
      // handleChange({
      //   file,
      //   fileList
      // }) {
      //   this.bindFileList = fileList;
      //   console.log('ss' + file.status)
      //   if (file.status === "done") {
      //     message.info("上传成功");

      //   }
      // },
      transformFile(file) {
        console.log(file)
        return new Promise(resolve => {
          const reader = new FileReader();
          reader.readAsDataURL(file);
          reader.onload = () => {
            const canvas = document.createElement('canvas');
            const img = document.createElement('img');
            img.src = reader.result;
            img.onload = () => {
              const ctx = canvas.getContext('2d');
              ctx.drawImage(img, 0, 0);
              ctx.fillStyle = 'red';
              ctx.textBaseline = 'middle';
              ctx.fillText('Ant Design', 20, 20);
              canvas.toBlob(resolve);
            };
          };
        });
      },
      beforeUpload(file) {
        this.bindFileList = [...this.bindFileList, file];
        // this.vfileList = []
        // console.log(this.bindFileList)
        return true;
      },
      handleUpload() {
        const {
          fileList
        } = this;
        const formData = new FormData();
        fileList.forEach(file => {
          formData.append('files[]', file);
        });
        this.uploading = true;

        // You can use any AJAX library you like
        // reqwest({
        //   url: 'https://www.mocky.io/v2/5cc8019d300000980a055e76',
        //   method: 'post',
        //   processData: false,
        //   data: formData,
        //   success: () => {
        //     this.fileList = [];
        //     this.uploading = false;
        //     message.success('upload successfully.');
        //   },
        //   error: () => {
        //     this.uploading = false;
        //     message.error('upload failed.');
        //   },
        // });
      },
    },
    data() {
      return {
        uploading: false,
        EnableMultiple: true,
        bindFileList: [],
        vfileList: [],
        // uploadURL:window.serverConfig.domain + 'api/post/picture'
        uploadURL: "api/post/picture",
        cardList: [{
            src: "https://yangsj-first-bucket.oss-cn-guangzhou.aliyuncs.com/markdown/image-20201222121429413.png",
            name: 'test'
          },

        ]

      }
    }
  }
</script>

<style scoped>
  .container {
    width: 100%;
    height: 100%;
  }

  .btns {
    height: 10%;
  }

  .cardlist {
    height: 90%;
  }
</style>
