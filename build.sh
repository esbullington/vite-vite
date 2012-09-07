#!/bin/bash


BUILD_FLAG=debug

usage()
{
    cat << EOF
    usage: $0 options

OPTIONS:
   -h      Show this message
   -b      Build Flag
   -c      Config File
EOF
}

BUILD_FLAG=
CONFIG_FILE=

#Process the build arguments, if any
while getopts "h:b:c:" opt
do
    case "${opt}" in
        h) usage 
            exit 1 ;;
        b) BUILD_FLAG=$OPTARG;;
        c) CONFIG_FILE=$OPTARG;;
        \?) usage 
            exit 1;;
    esac
done

if [ -z "$CONFIG_FILE" ] ; then 
    source "$PWD"/build.cfg
else
    source "${PWD}"/"${CONFIG_FILE}"
    echo "working 2"
fi

$PYTHON_FOR_ANDROID_DIR/distribute.sh -m $PYTHON_MODULES
cd $PYTHON_FOR_ANDROID_DIR/dist/default
python $PYTHON_FOR_ANDROID_DIR/dist/default/build.py --package $PACKAGE_NAME --name $APP_NAME --version $VERSION --dir $APP_DIR --permission $PERMISSION --orientation $ORIENTATION $BUILD_FLAG --icon $ICON --icon-name "$ICON_NAME"
adb uninstall $PACKAGE_NAME 
adb install $PYTHON_FOR_ANDROID_DIR/dist/default/bin/$APP_NAME-$VERSION-$BUILD_FLAG.apk
