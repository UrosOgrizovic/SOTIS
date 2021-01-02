const path = require('path'); 

module.exports = {
    configureWebpack: {
        resolve: {
            alias: {
                '@Components': path.resolve(__dirname, 'src/components/'),
                '@Helpers': path.resolve(__dirname, 'src/helpers/')
            }
        }
    }
}