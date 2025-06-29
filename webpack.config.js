const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = {
    mode: process.env.NODE_ENV === 'production' ? 'production' : 'development',
    entry: {
        main: './static/js/index.js'
    },
    output: {
        filename: '[name].[contenthash].js',
        path: path.resolve(__dirname, 'static/dist'),
        clean: true
    },
    devtool: 'source-map',
    devServer: {
        static: {
            directory: path.join(__dirname, 'static'),
            watch: true
        },
        hot: true,
        port: 3000,
        proxy: {
            '/api': {
                target: 'http://localhost:5000',
                changeOrigin: true
            }
        }
    },
    module: {
        rules: [
            {
                test: /\\.(js|jsx)$/, // Process JS and JSX files
                exclude: /node_modules/, // Exclude node_modules
                use: {
                    loader: 'babel-loader', // Use Babel loader
                    options: {
                        presets: ['@babel/preset-env', '@babel/preset-react']
                    }
                }
            },
            {
                test: /\\.(css|scss)$/, // Process CSS and SCSS files
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    'sass-loader'
                ]
            },
            {
                test: /\\.(png|jpe?g|gif|svg)$/i, // Process images
                type: 'asset/resource'
            }
        ]
    },
    plugins: [
        new CleanWebpackPlugin(),
        new HtmlWebpackPlugin({
            template: './static/index.html'
        }),
        new MiniCssExtractPlugin({
            filename: '[name].[contenthash].css'
        }),
        new webpack.HotModuleReplacementPlugin()
    ],
    resolve: {
        extensions: ['.js', '.jsx', '.json'],
        alias: {
            '@': path.resolve(__dirname, 'static/js'),
            '@components': path.resolve(__dirname, 'static/js/components'),
            '@utils': path.resolve(__dirname, 'static/js/utils')
        }
    }
};
