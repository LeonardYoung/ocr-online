<template>
    <div>
        <a-row type="flex" justify="space-around">

            <a-col span="11" class="image-area">
                <a-divider >
                    <p class="subtitle">图片预览</p>
                </a-divider>
                <div v-if="previewVisible" class="preview-box" ref="previewBox">
                    <img :src="previewImage" class="preview-img" alt="image loading" ref="previewImg">
                    <canvas id="preview-canvas" ref="previewCanvas" :style="previewCanvasStyle"
                            :height="canvasHeight + 'px'" :width="canvasWidth + 'px' "></canvas>
                </div>
                <div v-else class="preview-box">
                    <p class="message-info">请点击上传按钮上传图片</p>
                </div>
            </a-col>
            <a-col span="11" class="image-area">
                <a-divider >
                    <p class="subtitle">仪表盘识别结果</p>
                </a-divider>
                <div v-if="resultShow===0" class="result-box">
                    <p class="message-info">请选择一张图片查看识别结果</p>
                </div>
                <div v-else-if="resultShow===1" class="result-box">
                    <a-spin size="large">
                        <p class="message-info">
                            {{message}}
                        </p>
                    </a-spin>
                </div>
                <div v-else-if="resultShow===2" class="result-box"  v-bind:style="{ minHeight: resultBoxHeight + 'px' }">
                    <ul>
                        <li class="res-text" v-for="line in resultText" v-bind:key="line">
                            {{ line }}
                        </li>
                    </ul>
                </div>

            </a-col>
        </a-row>
    </div>
</template>

<script>
    export default {
        name: "resultTextOnly",
        props: ['previewImage','axiosResult'],
        data(){
            return{
                resultShow : 0,
                resultText:[],
                message : "",
                previewVisible : false,
                ocrResult:[],
                previewCtx:{},
                canvasHeight:300,
                canvasWidth:300,
                previewCanvasStyle:{
                    top: '0px',
                    height: '0px'
                },
                resultBoxHeight:600
            }
        },
        watch: {
            axiosResult: function (result) {
                console.log(result)

                //队列中
                if(result.data.status === 0){
                    this.resultShow = 1;
                    this.message = '服务器处理中，请稍后查询'
                }
                else if(result.data.status === 1){

                    // 服务器处理完成，展示结果
                    this.resultShow = 2;
                    // 设置定时执行，否则paintResult中会报错找不到canvas
                    setTimeout(()=>{
                        this.paintResult(result.data.result)
                    },1)


                }
            },
        },
        mounted() {
            console.log(window.serverConfig)
        },
        methods:{
            pictureClicked(uid){
                console.log('picture clicked uid=',uid)
                this.previewVisible = 1;
                this.resultShow = 1;
                this.message = '查询中'


                let previewDom=document.getElementById('preview-canvas')
                if( previewDom === null)
                    return
                let previewCtx = previewDom.getContext("2d");
                //清除画布
                previewCtx.clearRect(0,0,1000,1000)
            },
            //展示结果，在图片上画矩形
            paintResult(result){
                this.ocrResult = result

                let previewCtx=document.getElementById('preview-canvas')
                    .getContext("2d");

                let that = this
                // 为了获取图片的宽高，要加载图片，是否从服务器获取更好？
                let img = new Image()
                img.src = this.previewImage
                img.onload = function(){
                    // alert('width:'+img.width+',height:'+img.height)
                    //图片的宽高
                    let elt = that.$refs.previewImg
                    //盒子宽高
                    let box = that.$refs.previewBox
                    that.canvasWidth = img.width
                    that.canvasHeight = img.height

                    that.resultBoxHeight = box.offsetHeight

                    if(box.offsetHeight > elt.offsetHeight){
                        let dif = box.offsetHeight - elt.offsetHeight
                        that.previewCanvasStyle.top  = String( dif / 2 ) + 'px'
                        that.previewCanvasStyle.height = String( elt.offsetHeight ) + 'px'

                    }
                    // let wh = {
                    //     //图片像素宽高
                    //     originWidth: img.width,
                    //     originHeight : img.height,
                    //     //img标签的宽高
                    //     width : elt.offsetWidth,
                    //     height : elt.offsetHeight,
                    //     //盒子宽高
                    //     boxWidth : box.offsetWidth,
                    //     boxHeight : box.offsetHeight
                    // }

                    let _this = that
                    // 画框的操作是在canvas中进行的，所以要等DOM渲染完成后进行
                    that.resultText = new Array();
                    that.$nextTick(()=>{

                        for(let one of result){
                            _this.paintRectangle(previewCtx,one.text_box_position)
                            _this.showLine(one)
                        }
                    })

                }
            },
            showLine(line){
                this.resultText.push(line.text);
            },
            // drawText(ctx,data){
            //     // ctx.moveTo(data[0][0],data[0][1])
            //     let h = data.text_box_position[3][1] - data.text_box_position[0][1]
            //
            //     let fontSize = this.getFoneSize(h)
            //     console.log('h=',h,';fontsize=',fontSize)
            //     ctx.font="" + fontSize + "px Arial";
            //     ctx.fillText(data.text,data.text_box_position[3][0],data.text_box_position[3][1])
            // },
            getFoneSize(h){
                return h * 4 / 5;
            },
            // 画矩形
            paintRectangle(ctx,points){
                if(points.length !== 4){
                    console.log('bad rectangle')
                    return
                }

                ctx.strokeStyle="#FF0000";
                ctx.moveTo(points[0][0],points[0][1])
                for ( let i = 1; i < 4; i++){
                    ctx.lineTo(points[i][0],points[i][1])
                    ctx.stroke()
                }
                ctx.lineTo(points[0][0],points[0][1])
                ctx.stroke()
            },
            // convertPoint(originPoints,wh){
            //     wh;
            //     let len = originPoints.length
            //     let cpoint= new Array(len)
            //     for(let i = 0 ; i < len ;i++){
            //         cpoint[i] = {}
            //         cpoint[i].w = originPoints[i][0]
            //         cpoint[i].h = originPoints[i][1]
            //     }
            //     return cpoint
            // }
        }

    }
</script>

<style scoped>
    .image-area{
        height: 100%;
        line-height: 500px;
        /*text-align: center;*/
    }
    .preview-box,.result-box{
        box-sizing: content-box;
        border: 2px solid black;
        position: relative;
        min-height: 200px;
    }
    .preview-img{
        width: 100%;
        height: 100%;
        /*position: absolute;*/
        /*top : 0;*/
        /*left: 0;*/
    }
    .subtitle{
        font-size: 1.5rem;
    }
    .rectangle-box{
        position: absolute;
        border: 2px solid red;
        width: 20px;
        height: 20px;
        top: 200px;
        left: 20px;
    }
    .message-info{
        color: black;
        font-size: 20px;
        font-weight: bold;
    }
    #preview-canvas{
        width: 100%;
        height: 100%;
        position: absolute;
        top : 0;
        left: 0;
    }
    .result-box{
        /*overflow-y: scroll;*/
        /*text-align: center;*/
    }
    ul{
        position:absolute;
        top:50%;
        left: 50%;
        transform:translate(-50%,-50%);
        width: 100%;
        height: 100%;
        overflow-y: scroll;
        /*text-align: center;*/
        /*display: inline-block;*/
    }
    li{
        margin: 0.7rem;
        font-size: 1rem;
        line-height: 1rem;
        list-style: none;
        text-align: left;
        alignment: left;
        /*display: inline;*/
        /*display: inline-block;*/
    }
</style>
