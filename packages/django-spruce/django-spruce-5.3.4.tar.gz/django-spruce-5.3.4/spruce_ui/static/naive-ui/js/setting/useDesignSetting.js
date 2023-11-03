const { computed } = Vue;
import {designStore} from "/static/naive-ui/js/setupNaiveDiscreteApi.js";
export function useDesignSetting() {
    const getDarkTheme = computed(() => designStore.darkTheme);
    const getAppTheme = computed(() => designStore.appTheme);
    const getAppThemeList = computed(() => designStore.appThemeList);
    return {
        getDarkTheme,
        getAppTheme,
        getAppThemeList,
    };
}