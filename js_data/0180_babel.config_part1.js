module.exports = {
  presets: ['module:metro-react-native-babel-preset'],
  plugins: [
    [
      'module-resolver',
      {
        root: ['.'],
        extensions: [
          '.ios.ts',
          '.android.ts',
          '.ts',
          '.ios.tsx',
          '.android.tsx',
          '.tsx',
          '.jsx',
          '.js',
          '.json',
        ],
        alias: {
          '@containers': 'passy/src/containers',
          '@componets': 'passy/src/components',
          '@utils': 'passy/src/utils',
        },
      },
    ],
  ],
  sourceMaps: true,
};
