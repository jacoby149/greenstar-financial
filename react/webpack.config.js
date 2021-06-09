const path = require('path');

module.exports = {
    entry: {
        crm: './src/Crm.jsx'
    },
    output: {
        path: path.resolve(__dirname, '../static/js/reactBundles'),
        filename: '[name].bundle.js'
    },
    module: {
        rules: [
            {test: /\.(js|jsx)$/, exclude: /node_modules/, use: 'babel-loader'}
        ]
    },
    mode: 'development',
    resolve: {
        alias: {
            // Put desired import aliases here... of the form:
            //
            // AliasName: path.resolve(__dirname, './src/path/to/desired/locale),
            // AliasName$: path.resolve(__dirname, './src/path/to/specific/file.jsx)
            // 
            //
            // Will be used in files like:
            //
            // import CommonComponent from 'AliasName/CommonComponent.jsx';
            // import CommonComponent from 'AliasName$'
            Comp1$: path.resolve(__dirname, './src/crm/Comp1.jsx'),
            Comp2$: path.resolve(__dirname, './src/crm/Comp2.jsx')
        }
    }
}