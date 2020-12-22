<template>
  <a-layout>
    <a-layout-sider width="250" theme="light">
      <div class="uploader">
        <!-- <a-upload
          :file-list="fileList"
        >
          <a-button type="primary">
            <a-icon type="upload"></a-icon>上
          </a-button>
        </a-upload> -->
        <a-upload
          name="pic"
          :action="uploadURL"
          :multiple="EnableMultiple"
          list-type="picture"
          @preview="handlePreview"
          @change="handleChange"
          :file-list="bindFileList"
          accept=".png,.jpg"
        >
          <a-button type="primary" class="upload-button">
            <a-icon type="upload" /> 上传
          </a-button>
        </a-upload>
      </div>
    </a-layout-sider>
    <a-layout>
      <a-layout-header class="header">
        <a-row type="flex">
          <a-col flex="auto">
            <h1>在线演示系统</h1>
          </a-col>

          <a-col flex="300px">
            <a-radio-group v-model="typeSelect" button-style="solid">
              <a-radio-button value="1"> 文字识别 </a-radio-button>
              <a-radio-button value="2"> 工单识别 </a-radio-button>
            </a-radio-group>

          </a-col>
        </a-row>
      </a-layout-header>
      <a-layout-content class="content">
        <!-- <resultTextOnly
          v-if="this.presentSelect === '1'"
          ref="childResultPresent"
          :preview-image="previewImage"
          :axios-result="axiosResult"
        />
        <ResultPresent
          v-else-if="this.presentSelect === '2'"
          ref="childResultPresent"
          :preview-image="previewImage"
          :axios-result="axiosResult"
        /> -->
        <result-present-text
          v-if="this.typeSelect === '1'"
          ref="childResultPresent"
          :preview-image="previewImage"
          :axios-result="axiosResult"
          class="present-box"
        />
        <result-table
          v-else-if="this.typeSelect === '2'"
          ref="childResultPresent"
          :preview-image="previewImage"
          :axios-result="axiosResult"
          class="present-box"
        />
        <!--                <result-present-text v-else-if="this.presentSelect==='3' " />-->
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script>
import resultPresentText from "./resultPresentText";
import { message } from "ant-design-vue";
import resultTable from './resultTable.vue';

const axios = require("axios");
function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
  });
}

export default {
  name: "PageOCR",

  components: {
    resultPresentText,
    resultTable,
  },
  data() {
    return {
      EnableMultiple: true,
      badFileType: false,
      drawerVisible: false,
      remainNum: 0,
      previewVisible: false,
      typeSelect:"1",    // 选择“文字识别”或者“表格识别”
      //
    //   presentSelect: "3",
      previewImage: "",
      ocrFileList: [
        // {
        //     uid: '-1',
        //     uuid:'222',
        //     name: 'image.png',
        //     status: 'done',
        //     url: 'https://yangsj-first-bucket.oss-cn-guangzhou.aliyuncs.com/markdown/image-20201108101940476.png',
        // },
      ],
      tableFileList: [],
      bindFileList: [],
      axiosResult: {},
      // uploadURL:window.serverConfig.domain + 'api/post/picture'
      uploadURL: "api/post/picture",
    };
  },
  watch:{
    typeSelect: function(val){
      // console.log('val=',val)
      if(val === "1"){
        this.uploadURL = "api/post/picture";
        this.bindFileList = this.ocrFileList;
      }
      else if(val === "2"){
        this.uploadURL = "api/post/table";
        this.bindFileList = this.tableFileList;
      }
      this.previewImage = ""
    }
  },
  methods: {

    //查询该图片识别结果

    getResultFromHost(uuid) {
      // 引用配置文件中的服务器地址
      // axios.defaults.baseURL=window.serverConfig.domain;
      axios({
        url: "/api/getResult",
        method: "post",
        data: {
          uuid: uuid,
        },
      }).then((res) => {
        // console.log('res=',res)
        this.axiosResult = res;
      });
    },
    //点击图片预览
    async handlePreview(file) {
      if (!file.url && !file.preview) {
        file.preview = await getBase64(file.originFileObj);
      }
      this.previewImage = file.url || file.preview;
      this.previewVisible = true;

      //调用子组件方法
      this.$refs.childResultPresent.pictureClicked(file.uuid);
      this.getResultFromHost(file.uuid);
    },
    //文件状态改变的钩子
    handleChange({ file, fileList }) {
      if(this.typeSelect === "1"){
        this.ocrFileList = fileList;
        this.bindFileList = this.ocrFileList
      }
      else if( this.typeSelect === "2"){
        this.tableFileList = fileList;
        this.bindFileList = this.tableFileList;
      }
      if (file.status === "done") {
        message.info("上传成功");
        // console.log(file,'done')
        this.bindFileList.forEach((f) => {
          if (f.uid === file.uid) {
            f.uuid = file.response;
          }
        });
      }
    },
    // presentSelectChanged(e){
    //     console.log(e.target.value)
    // },
    showDrawer() {
      this.drawerVisible = true;
    },
    closeDrawer() {
      this.drawerVisible = false;
    },
  },
  mounted() {
    this.bindFileList = this.ocrFileList;
  },
};
</script>

<style scoped>
.content {
  background-image: url("/bg5.jpg");
  /* background-color: skyblue;; */
}
h1 {
  font-size: 40px;
  /* color: white; */
  text-align: center;
  /*position: relative;*/
  /*top:40px*/
}
.header {
  background-color: skyblue;
  /* background-image: url('/bg3.gif'); */
  height: 10%;
  overflow: hidden;
}
.upload-button {
  margin-top: 30px;
}
.uploader {
  overflow-y: scroll;
  height: 100%;
}
.present-box{
  height: 100%;
}
</style>
