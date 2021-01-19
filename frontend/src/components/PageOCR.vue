<template>
  <a-layout class="layer">
    <a-layout-sider width="250" theme="light">
      <div class="uploader">
        <a-upload
          name="pic"
          :action="uploadURL"
          :multiple="EnableMultiple"
          list-type="picture"
          @preview="handlePreview"
          @change="handleChange"
          :file-list="bindFileList"
          :beforeUpload="beforeUpload"
          accept=".png,.jpg"
        >
          <a-button type="primary" class="upload-button">
            <a-icon type="upload" /> 选择文件
          </a-button>
        </a-upload>
        <a-button v-if="typeSelect === '2'"
                  type="primary"
                  :disabled="bindFileList.length === 0"
                  :loading="uploading"
                  style="margin-top: 16px;margin-right: 16px;"
                  @click="handleClear"
        >
          清除
        </a-button>
        <a-button v-if="typeSelect === '2'"
                type="primary"
                :disabled="bindFileList.length === 0"
                :loading="uploading"
                style="margin-top: 16px"
                @click="handleUpload"
        >
          {{ uploading ? '上传中' : '上传' }}
        </a-button>
      </div>
    </a-layout-sider>
    <a-layout>
      <a-layout-header class="header">
        <div class="title">
          <h1>在线演示系统</h1>
        </div>
        <div class="toolbar-right">
          <a-button v-if="this.typeSelect === '2'" @click="showDrawer" theme="primary">
            选择工单
          </a-button>
<!--          <a-radio-group v-model="typeSelect" button-style="solid">-->
<!--            <a-radio-button value="2"> 工单识别 </a-radio-button>-->
<!--            <a-radio-button value="1"> 文字识别 </a-radio-button>-->
<!--          </a-radio-group>-->
          <a-drawer
            title="选择工单"
            placement="right"
            :closable="false"
            :visible="drawerVisible"
            @close="closeDrawer"
            width=400
          >
            <a-radio-group v-model="tableSelect">
              <a-radio v-for="one in tablesInf" :key="one.id" class="vertical-radio" :value="one.id">{{one.name}}</a-radio>
<!--              <a-radio class="vertical-radio" :value="2">福州供电公司现场工作任务派工单</a-radio>-->
<!--              <a-radio class="vertical-radio" :value="3">福州供电公司现场工作任务派工单</a-radio>-->


            </a-radio-group>
          </a-drawer>
        </div>
      </a-layout-header>
      <a-layout-content class="content">
        <div class="info" v-if="typeSelect === '2'">
          <p>当前选择工单：{{tablesInf[parseInt(tableSelect) -1].name}}</p>
          <p>工单识别状态：{{requestStatus === 'handling'
                                      ? '----'
                                      : requestStatus === 'finished'
                                          ? '识别完成'
                                          : '识别错误'}}</p>
          <p>工单识别用时：{{timeCost}}s</p>
        </div>
        <div class="qyf"></div>
        <result-present-text
          v-if="typeSelect === '1'"
          ref="childResultPresent"
          :preview-image="previewImage"
          :axios-result="axiosResult"
          class="present-box"
        />
        <result-table
          v-else-if="typeSelect === '2'"
          ref="childResultPresent"
          :preview-image="previewImage"
          :axios-result="axiosResult"
          class="present-box"
        />
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script>
import resultPresentText from "./resultPresentText";
import { message } from "ant-design-vue";
import resultTable from "./resultTable.vue";
import {tablesInfo} from "../common/const"

const axios = require("axios");
function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = (error) => reject(error);
  });
}
// 图片 base64 url 转 blob
function dataURLtoBlob(dataurl) {
  var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
          bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }
  return new Blob([u8arr], { type: mime });
}
/*
 * 将base64转换成可用formdata提交的文件
 * @param {string} urlData base64的url
 * @return {Blob}
 */
// function convertBase64UrlToBlob(urlData){
//   //去掉url的头，并转换为byte
//   var split = urlData.split(',');
//   var bytes=window.atob(split[1]);
//   //处理异常,将ascii码小于0的转换为大于0
//   var ab = new ArrayBuffer(bytes.length);
//   var ia = new Uint8Array(ab);
//   for (var i = 0; i < bytes.length; i++) {
//     ia[i] = bytes.charCodeAt(i);
//   }
//   return new Blob( [ab] , {type : split[0]});
// }

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
      typeSelect: "1", // 选择“文字识别”或者“表格识别”

      previewImage: "",
      ocrFileList: [],
      tableFileList: [],
      bindFileList: [],
      axiosResult: {},
      // uploadURL:window.serverConfig.domain + 'api/post/picture'
      uploadURL: "api/post/picture",
      uploading: false,

      requestStatus: 'handling',
      // statusString:'请上传工单',


      tableSelect: '1',
      tablesInf: tablesInfo,

      timer:null,
      timeCost:"--",

    };
  },
  watch: {

    typeSelect: function (val) {
      // console.log('val=',val)
      if (val === "1") {
        this.uploadURL = "api/post/picture";
        this.bindFileList = this.ocrFileList;
      } else if (val === "2") {
        this.uploadURL = "api/post/table";
        this.bindFileList = this.tableFileList;
      }
      this.previewImage = "";
    },
  },
  methods: {

    handleClear(){
      this.bindFileList =[];
    },
    async getFormData(){
        const formData = new FormData();
        for(const file of this.bindFileList){
            const bin = await getBase64(file.originFileObj);
            const blob = dataURLtoBlob(bin);
            formData.append(file.uid, blob, file.name);
        }
        formData.append('tableId',this.tableSelect);
        return formData;
    },

    requestEverySecond(){
      if(this.typeSelect === '1'){
        return;
      }
      this.timer = window.setInterval(()=>{
        console.log('auto req')
        if(this.requestStatus === 'handling'){
          this.getResultFromHost(this.bindFileList[0].uuid);
        }else{
          clearInterval(this.timer);
        }

      },1000)
    },

    handleUpload(){
      //通知子组件，表格改变了
      this.$refs.childResultPresent.chooseAnotherTable();

      this.requestStatus = 'handling';

      this.timeCost = "--"
      if(this.timer){
        clearInterval(this.timer);
      }

      this.uploading = true;
        this.getFormData().then((formData) =>{
            axios({
                url: "/api/post/table",
                method: "post",
                data: formData,
            }).then((res) => {
              this.uploading = false;
                console.log('table res=',res)
                this.bindFileList.forEach((file)=>{
                  file.uuid = res.data;
                  // console.log('uuid=',res.data)
                })
                this.requestEverySecond();
            }).catch(()=>{
              this.uploading = false;
            });
        })
    },
    beforeUpload() {
      if( this.typeSelect === '1'){
        // console.log('直接上传')
        return true;
      }
      // console.log('in beforeUpload')
      // console.log(file)
      //工单需要一起上传
      // this.bindFileList = [...this.bindFileList, file];
      return false;
    },
    //查询该图片识别结果

    getResultFromHost(uuid) {
      // 引用配置文件中的服务器地址
      // axios.defaults.baseURL=window.serverConfig.domain;
      // uuid = '15c4eaa8-5a23-11eb-b96e-2520f8b0de8e'
      axios({
        url: "/api/getResult",
        method: "post",
        data: {
          uuid: uuid,
        },
      }).then((res) => {
        // console.log('res=',res)
        this.axiosResult = res;
        if(this.axiosResult.data.status === 1){
          if(this.axiosResult.data.result.error){
            this.requestStatus = 'error';
          }
          else{
            this.requestStatus = 'finished';
            this.timeCost = "" + this.axiosResult.data.result.dtime.toFixed(2);
          }

        }
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

      if(this.requestStatus === 'handling' || this.typeSelect === '1'){
        //继续请求
        this.getResultFromHost(file.uuid);
      }
      // this.getResultFromHost(file.uuid);

    },
    //文件状态改变的钩子
    handleChange({ file, fileList }) {
        // console.log('in handleChange')
      // console.log(fileList)
      if (this.typeSelect === "1") {
        this.ocrFileList = fileList;
        this.bindFileList = this.ocrFileList;
      } else if (this.typeSelect === "2") {
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
    this.typeSelect = this.$route.query.type
    // console.log(this.$route.query.type)
  },
};
</script>

<style scoped>
  .layer{
    width: 100%;
    height: 100%;
  }
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
  position: relative;
  border-radius: 1rem;
}
.upload-button {
  margin-top: 30px;
}
.uploader {
  overflow-y: scroll;
  height: 100%;
}
.present-box {
  /*height: calc(100% - 4rem);*/
  height: 90%;
}
.title {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.toolbar-right {
  float: right;
  position: relative;
  top: 50%;
  transform: translateY(-50%);
}
.vertical-radio{
  display: block;
  font-size: 1rem;
  height: 1rem;
  line-height: 1rem;
  margin: 1rem 0;

}
.info{
  text-align: left;
  /*float: left;*/
}
  .info>p{
    font-size: 1rem;
    margin: 0 auto;

  }

</style>
