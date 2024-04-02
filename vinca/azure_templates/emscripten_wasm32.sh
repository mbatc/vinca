
echo "Setup emscripten-forge recipes"

mkdir -p emforge-recipes
pushd emforge-recipes
echo "Clone https://github.com/emscripten-forge/recipes.git to $(cd)"
git clone https://github.com/emscripten-forge/recipes.git .

echo "-- Setup emsdk"
./emsdk/setup_emsdk.sh "3.1.45" $(pwd)/emsdk_install

echo "-- Install playwright"
playwright install

echo "-- Install custom boa"
python -m pip install git+https://github.com/DerThorsten/boa.git@python_api_v2 --no-deps --ignore-installed
popd

echo "Build robostack"
export CI=azure
export GIT_BRANCH=$BUILD_SOURCEBRANCHNAME
export FEEDSTOCK_NAME=$(basename ${BUILD_REPOSITORY_NAME})
.scripts/build_emscripten_wasm32.sh
