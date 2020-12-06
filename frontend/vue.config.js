module.exports = {
    devServer: {
        proxy:{
            '/api':{
                target: 'http://127.0.0.1:5000/' ,
                // target: 'http://172.17.169.235:5000/' ,
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

