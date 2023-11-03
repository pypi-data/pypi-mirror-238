const {computed} = Vue;

/**
 * 挂载 Naive-ui 脱离上下文的 API
 * 如果你想在 setup 外使用 useDialog、useMessage、useNotification、useLoadingBar，可以通过 createDiscreteApi 来构建对应的 API。
 * https://www.naiveui.com/zh-CN/dark/components/discrete
 */
"use strict";

function addLight(color, amount) {
    const cc = parseInt(color, 16) + amount;
    const c = cc > 255 ? 255 : cc;
    return c.toString(16).length > 1 ? c.toString(16) : `0${c.toString(16)}`;
}

export function lighten(color, amount) {
    color = color.indexOf('#') >= 0 ? color.substring(1, color.length) : color;
    amount = Math.trunc((255 * amount) / 100);
    return `#${addLight(color.substring(0, 2), amount)}${addLight(color.substring(2, 4), amount)}${addLight(color.substring(4, 6), amount)}`;
}

export const settingStore = {
    "$id": "app-project-setting",
    "navMode": "vertical",
    "navTheme": "dark",
    "isMobile": false,
    "headerSetting": {"bgColor": "#fff", "fixed": true, "isReload": true},
    "showFooter": true,
    "menuSetting": {
        "minMenuWidth": 64,
        "menuWidth": 200,
        "fixed": true,
        "mixMenu": false,
        "mobileWidth": 800,
        "collapsed": false
    },
    "multiTabsSetting": {"bgColor": "#fff", "show": true, "fixed": true},
    "crumbsSetting": {"show": true, "showIcon": false},
    "permissionMode": "FIXED",
    "isPageAnimate": true,
    "pageAnimateType": "zoom-fade",
    "getNavMode": "vertical",
    "getNavTheme": "dark",
    "getIsMobile": false,
    "getHeaderSetting": {"bgColor": "#fff", "fixed": true, "isReload": true},
    "getShowFooter": true,
    "getMenuSetting": {
        "minMenuWidth": 64,
        "menuWidth": 200,
        "fixed": true,
        "mixMenu": false,
        "mobileWidth": 800,
        "collapsed": false
    },
    "getMultiTabsSetting": {"bgColor": "#fff", "show": true, "fixed": true},
    "getCrumbsSetting": {"show": true, "showIcon": false},
    "getPermissionMode": "FIXED",
    "getIsPageAnimate": true,
    "getPageAnimateType": "zoom-fade",
    "_isOptionsAPI": true
}
export const designStore2 =
    {
        "$id": "app-design-setting",
        "darkTheme": true,
        "appTheme": "#2d8cf0",
        "appThemeList": ["#2d8cf0", "#0960bd", "#0084f4", "#009688", "#536dfe", "#ff5c93", "#ee4f12", "#0096c7", "#9c27b0", "#ff9800", "#FF3D68", "#00C1D4", "#71EFA3", "#171010", "#78DEC7", "#1768AC", "#FB9300", "#FC5404"],
        "getDarkTheme": true,
        "getAppTheme": "#2d8cf0",
        "getAppThemeList": ["#2d8cf0", "#0960bd", "#0084f4", "#009688", "#536dfe", "#ff5c93", "#ee4f12", "#0096c7", "#9c27b0", "#ff9800", "#FF3D68", "#00C1D4", "#71EFA3", "#171010", "#78DEC7", "#1768AC", "#FB9300", "#FC5404"],
        "_isOptionsAPI": true
    }

export const designStore = {
    "$id": "app-design-setting",
    "darkTheme": false,
    "appTheme": "#2d8cf0",
    "appThemeList": ["#2d8cf0", "#0960bd", "#0084f4", "#009688", "#536dfe", "#ff5c93", "#ee4f12", "#0096c7", "#9c27b0", "#ff9800", "#FF3D68", "#00C1D4", "#71EFA3", "#171010", "#78DEC7", "#1768AC", "#FB9300", "#FC5404"],
    "getDarkTheme": false,
    "getAppTheme": "#2d8cf0",
    "getAppThemeList": ["#2d8cf0", "#0960bd", "#0084f4", "#009688", "#536dfe", "#ff5c93", "#ee4f12", "#0096c7", "#9c27b0", "#ff9800", "#FF3D68", "#00C1D4", "#71EFA3", "#171010", "#78DEC7", "#1768AC", "#FB9300", "#FC5404"],
    "_isOptionsAPI": true
};

const configProviderPropsRef = computed(() => ({
    theme: designStore.darkTheme ? naive.darkTheme : undefined,
    themeOverrides: {
        common: {
            primaryColor: designStore.appTheme,
            primaryColorHover: lighten(designStore.appTheme, 6),
            primaryColorPressed: lighten(designStore.appTheme, 6),
        },
        LoadingBar: {
            colorLoading: designStore.appTheme,
        },
    },
}));
const {message, dialog, notification, loadingBar} = naive.createDiscreteApi(
    ['message', 'dialog', 'notification', 'loadingBar'],
    {
        configProviderProps: configProviderPropsRef,
    }
);

window['$message'] = window.message = message;
window['$dialog'] = window.dialog = dialog;
window['$notification'] = window.notification = notification;
window['$loading'] = window.loadingBar = loadingBar;

