<template>
    <a-layout>
        <a-layout-sider width="250" theme="light">
            <div class="uploader">
                <a-upload
                        name="pic"
                        :action="uploadURL"
                        :multiple="EnableMultiple"
                        list-type="picture"
                        @preview="handlePreview"
                        @change="handleChange"
                        :file-list="fileList"
                        :before-upload="beforeUpload"
                        accept=".png,.jpg"
                >
                    <a-button type="primary" class="upload-button"> <a-icon type="upload" /> 上传 </a-button>
                </a-upload>
            </div>



        </a-layout-sider>
        <a-layout>
            <a-layout-header class="header">
                <a-row type="flex">
                    <a-col flex="auto">
                        <h1> OCR 在线演示系统 </h1>
                    </a-col>

                    <a-col flex="100px">
                        <a-button type="primary" @click="showDrawer">设置</a-button>
                        <a-drawer
                                title="设置"
                                placement="bottom"
                                :visible="drawerVisible"
                                @close="closeDrawer"
                        >
                            <div>
                                <p>选择结果展示方式：</p>
                                <a-radio-group v-model="presentSelect" button-style="solid">
                                    <a-radio-button value="1">
                                        只显示文字
                                    </a-radio-button>
                                    <a-radio-button value="2">
                                        显示对比
                                    </a-radio-button>
                                    <a-radio-button value="3">
                                        文字对比
                                    </a-radio-button>

                                </a-radio-group>
                            </div>
                        </a-drawer>

                    </a-col>

                </a-row>


            </a-layout-header>
            <a-layout-content>
                <resultTextOnly v-if="this.presentSelect==='1' "
                               ref="childResultPresent"
                               :preview-image="previewImage"
                               :axios-result="axiosResult"/>
                <ResultPresent v-else-if="this.presentSelect==='2' "
                               ref="childResultPresent"
                               :preview-image="previewImage"
                               :axios-result="axiosResult"/>
                <result-present-text v-else-if="this.presentSelect==='3' "
                               ref="childResultPresent"
                               :preview-image="previewImage"
                               :axios-result="axiosResult"/>
<!--                <result-present-text v-else-if="this.presentSelect==='3' " />-->
            </a-layout-content>
        </a-layout>

    </a-layout>

</template>

<script>

    import ResultPresent from "./resultPresent";
    import resultPresentText from "./resultPresentText";
    import resultTextOnly from "./resultTextOnly";
    const axios = require('axios')
    function getBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => resolve(reader.result);
            reader.onerror = error => reject(error);
        });
    }
    import { message } from 'ant-design-vue';
    export default {
        name: "PageOCR",

        components: {
            ResultPresent,
            resultPresentText,
            resultTextOnly
        },
        data(){
            return {
                EnableMultiple:true,
                badFileType:false,
                drawerVisible: false,
                remainNum:0,
                previewVisible: false,
                //
                presentSelect: "3",
                previewImage: '',
                fileList: [
                    // {
                    //     uid: '-1',
                    //     uuid:'222',
                    //     name: 'image.png',
                    //     status: 'done',
                    //     url: 'https://yangsj-first-bucket.oss-cn-guangzhou.aliyuncs.com/markdown/image-20201108101940476.png',
                    // },


                ],
                axiosResult: {},
                // uploadURL:window.serverConfig.domain + 'api/post/picture'
                uploadURL: 'api/post/picture'
            }
        },
        methods:{
            // 上传文件前的钩子,预处理
            beforeUpload(file) {
                console.log(file,'file:')

                //--------判断文件类型和文件大小
                // const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
                // if (!isJpgOrPng) {
                //     message.error('You can only upload JPG/PNG file!');
                //     // return false
                // }
                // const isLt2M = file.size / 1024 / 1024 < 2;
                // if (!isLt2M) {
                //     message.error('Image must smaller than 2MB!');
                // }
                // console.log(this.fileList,'beforeUpload')
                // this.badFileType = !(isJpgOrPng && isLt2M)
                //----------------手动上传文件
                // let that = this
                //
                // let data = new FormData()  // 创建form对象
                // data.append('pic', file)  // 通过append向form对象添加数据
                // axios({
                //     url:'/post/picture',
                //     method:'post',
                //     headers: {
                //         'Content-Type': 'application/x-www-form-urlencoded'
                //     },
                //     data:data
                // })
                // .then(res=>{
                //     console.log(res.data)
                //     message.info('success')
                //
                //     // that.fileMapUid.set(file.uid,res.data)
                //     that.fileList.forEach(f=>{
                //         if(f.uid === file.uid){
                //             f.uuid = res.data
                //         }
                //     })
                // })
                //
                // return false;
            },
            //查询该图片识别结果

            getResultFromHost(uuid){
                // 引用配置文件中的服务器地址
                // axios.defaults.baseURL=window.serverConfig.domain;
                axios({
                    url:'/api/getResult',
                    method:'post',
                    data:{
                        'uuid':uuid
                    }
                })
                .then(res=>{
                    // console.log('res=',res)
                    this.axiosResult = res;


                })
            },
            //点击图片预览
            async handlePreview(file) {
                if (!file.url && !file.preview) {
                    file.preview = await getBase64(file.originFileObj);
                }
                this.previewImage = file.url || file.preview;
                this.previewVisible = true;

                //调用子组件方法
                this.$refs.childResultPresent.pictureClicked(file.uuid)
                this.getResultFromHost(file.uuid)


            },
            //文件状态改变的钩子
            handleChange({file, fileList }) {
                // console.log('change!!!!')
                this.fileList = fileList;
                // console.log(fileList)
                if(file.status === "done"){
                    message.info('上传成功')
                    // console.log(file,'done')
                    this.fileList.forEach(f=>{
                        if(f.uid === file.uid){
                            f.uuid = file.response
                        }
                    })
                }
            },
            // presentSelectChanged(e){
            //     console.log(e.target.value)
            // },
            showDrawer() {
                this.drawerVisible = true;
            },
            closeDrawer(){
                this.drawerVisible = false;
            }
        },
        mounted() {
        }
    }
</script>

<style scoped>
    h1{
        font-size: 40px;
        text-align: center;
        /*position: relative;*/
        /*top:40px*/
    }
    .header{
        background-color: skyblue;
        height: 10%;
        overflow: hidden;
    }
    .upload-button{
        margin-top: 30px;
    }
    .uploader{
        overflow-y: scroll;
        height: 100%;
    }



</style>
