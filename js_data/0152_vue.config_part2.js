// vue.config.js
module.exports = {
    configureWebpack: {
        output: {
            libraryExport: 'default'
        },
        plugins:[
            // new ManifestPlugin()
        ],
        externals: {
            'axios': 'Axios',
            'moment': 'moment',
            'popper.js': 'Popper'
        }
    },
    pages: {
        index: {
            // entry for the page
            entry: './src/main.js',
            // the source template
            template: './public/index.html',
            // the output filename
            filename: 'index.html'
        }
    },
    publicPath: '/',
    outputDir: './dist',
    devServer: {
        
    }
};
