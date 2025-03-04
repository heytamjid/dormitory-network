const path = require('path');

module.exports = {
  entry: './assets/index.jsx',
  output: {
    filename: 'index-bundle.jsx',
    path: path.resolve(__dirname, './static'),
  },
  
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader', "postcss-loader"],
      },
      {
        test: /\.(js|jsx|ts|tsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: [
              '@babel/preset-env',
              ['@babel/preset-react', { runtime: 'automatic' }],
              '@babel/preset-typescript'

            ]
          }
        }
      },

    ]
  },
  resolve: {
    alias: {
      // '@' points to the assets folder
      '@': path.resolve(__dirname, 'assets'), //mane ./assets
      // Define the "components" alias correctly (without '@' in the path)
      components: path.resolve(__dirname, 'assets/shadcn/components'),
      // Optionally, if you want to support imports using "@/components/..."
      //'@/components': path.resolve(__dirname, 'assets/shadcn/components'),
      utils: path.resolve(__dirname, 'assets/shadcn/lib/utils'),
      ui: path.resolve(__dirname, 'assets/shadcn/components/ui'),
      lib: path.resolve(__dirname, 'assets/shadcn/lib'),
      hooks: path.resolve(__dirname, 'assets/shadcn/hooks'),
    },
    extensions: ['.js', '.jsx', '.ts', '.tsx']
  }
};