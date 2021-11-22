const path = require('path');

module.exports = {
  entry: {
    chatroom: './src/app/chatroom.jsx',
    gameroom: './src/app/gameroom.jsx',
  },
  output: {
    path: path.resolve(__dirname, 'dist', 'js'),
    filename: '[name].js',
  },
  devtool: 'source-map',
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react']
          }
        }
      },
    ],
  },
  resolve: {
    extensions: ['*', '.js', '.jsx'],
  },
};