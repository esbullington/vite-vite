#!/bin/bash


usage()
{
    cat << EOF
    usage: $0 options

OPTIONS:
   -h      Show this message
   -b      Build Flag (debug or release)
   -c      Config File (default is build.cfg)
   -a      Install to connected Android device
EOF
}

ROOT_DIR=$PWD
BUILD_FLAG=debug
CONFIG_FILE=
INSTALL_FLAG=false

#Process the build arguments, if any
while getopts "h:b:c:a" opt
do
    case "${opt}" in
        h) usage 
            exit 1 ;;
        b) BUILD_FLAG=$OPTARG;;
        c) CONFIG_FILE=$OPTARG;;
        a) INSTALL_FLAG=true ;;
        \?) usage 
            exit 1;;
    esac
done

if [ -z "$CONFIG_FILE" ] ; then 
    source "$PWD"/build.cfg
else
    source "${PWD}"/"${CONFIG_FILE}"
fi

$PYTHON_FOR_ANDROID_DIR/distribute.sh -m $PYTHON_MODULES
cd $PYTHON_FOR_ANDROID_DIR/dist/default
python $PYTHON_FOR_ANDROID_DIR/dist/default/build.py --package $PACKAGE_NAME --name $APP_NAME --version $VERSION --dir $APP_DIR --permission $PERMISSION --orientation $ORIENTATION $BUILD_FLAG --icon $ICON --icon-name "$ICON_NAME"
if $INSTALL_FLAG ; then
    adb uninstall $PACKAGE_NAME 
    adb install $PYTHON_FOR_ANDROID_DIR/dist/default/bin/$APP_NAME-$VERSION-$BUILD_FLAG.apk
fi
cp $PYTHON_FOR_ANDROID_DIR/dist/default/bin/$APP_NAME-$VERSION-$BUILD_FLAG.apk $ROOT_DIR/bin
