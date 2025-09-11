const path = require('path');

module.exports = {
    entry: './custom-ckeditor.js',
    output: {
        path: path.resolve(__dirname, 'build'),
        filename: 'custom-ckeditor.js',
        library: 'ClassicEditor',
        libraryTarget: 'umd',
        libraryExport: 'default'
    },
    module: {
        rules: [
            {
                test: /\.svg$/,
                use: ['raw-loader']
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            }
        ]
    }
};
