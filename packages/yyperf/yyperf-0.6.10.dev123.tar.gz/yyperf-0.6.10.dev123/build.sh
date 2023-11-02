rm -rf ./yyperf/static/css/home.*.css
rm -rf ./yyperf/static/js/home.*.js
rm -rf ./yyperf/static/js/home.*.map
rm -rf ./yyperf/static/js/app.*.js
rm -rf ./yyperf/static/js/app.*.map
cd ./vue
npm run build
cd ..
cp ./vue/dist/index.html ./yyperf/templates/
cp -rf ./vue/dist/static ./yyperf/
#python3 setup.py sdist bdist_wheel
