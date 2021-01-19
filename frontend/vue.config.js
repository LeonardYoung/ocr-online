/*
 * @Author: your name
 * @Date: 2020-12-06 15:50:28
 * @LastEditTime: 2021-01-15 11:27:50
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \ocrs\frontend\vue.config.js
 */
module.exports = {
    devServer: {
        proxy:{
            '/api':{
                // target: 'http://127.0.0.1:5000/' ,
                // target: 'http://172.17.169.235:5000/' ,//小服务器
                target: 'http://172.17.171.8:5000/' ,//大服务器
                changeOrigin:true,
                pathRewrite: {
                    '^/api': '/api'
                }
            }
        }

    },
    // 基本路径
    publicPath: './',
    // 输出文件目录
    outputDir: 'dist',
    configureWebpack: {
        externals: {
        }
    }

}

