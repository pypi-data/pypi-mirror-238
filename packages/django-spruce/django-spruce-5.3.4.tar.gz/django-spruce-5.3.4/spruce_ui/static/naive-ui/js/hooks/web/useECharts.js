import { useTimeoutFn } from '/static/naive-ui/js/hooks/core/useTimeout.js';
const { tryOnUnmounted,useDebounceFn } = VueUse;
const { unref, nextTick, watch, computed, ref } = Vue;
import { useEventListener } from '/static/naive-ui/js/hooks/event/useEventListener.js';
import { useBreakpoint } from '/static/naive-ui/js/hooks/event/useBreakpoint.js';
import { useDesignSetting } from '/static/naive-ui/js/setting/useDesignSetting.js';

export function useECharts(elRef, theme = 'default') {
    const { getDarkTheme: getSysDarkTheme } = useDesignSetting();
    const getDarkTheme = computed(() => {
        const sysTheme = getSysDarkTheme.value ? 'dark' : 'light';
        return theme === 'default' ? sysTheme : theme;
    });
    let chartInstance = null;
    let resizeFn = resize;
    const cacheOptions = ref({});
    let removeResizeFn = () => { };
    resizeFn = useDebounceFn(resize, 200);
    const getOptions = computed(() => {
        if (getDarkTheme.value !== 'dark') {
            return cacheOptions.value;
        }
        return Object.assign({ backgroundColor: 'transparent' }, cacheOptions.value);
    });
    function initCharts(t = theme) {
        const el = unref(elRef);
        if (!el || !unref(el)) {
            return;
        }
        chartInstance = echarts.init(el, t);
        const { removeEvent } = useEventListener({
            el: window,
            name: 'resize',
            listener: resizeFn,
        });
        removeResizeFn = removeEvent;
        const { widthRef, screenEnum } = useBreakpoint();
        if (unref(widthRef) <= screenEnum.MD || el.offsetHeight === 0) {
            useTimeoutFn(() => {
                resizeFn();
            }, 30);
        }
    }
    function setOptions(options, clear = true) {
        var _a;
        cacheOptions.value = options;
        if (((_a = unref(elRef)) === null || _a === void 0 ? void 0 : _a.offsetHeight) === 0) {
            useTimeoutFn(() => {
                setOptions(unref(getOptions));
            }, 30);
            return;
        }
        nextTick(() => {
            useTimeoutFn(() => {
                if (!chartInstance) {
                    initCharts(getDarkTheme.value);
                    if (!chartInstance)
                        return;
                }
                clear && (chartInstance === void 0 ? void 0 : chartInstance.clear());
                chartInstance === void 0 ? void 0 : chartInstance.setOption(unref(getOptions));
            }, 30);
        });
    }
    function resize() {
        chartInstance === null || chartInstance === void 0 ? void 0 : chartInstance.resize();
    }
    watch(() => getDarkTheme.value, (theme) => {
        if (chartInstance) {
            chartInstance.dispose();
            initCharts(theme);
            setOptions(cacheOptions.value);
        }
    });
    tryOnUnmounted(disposeInstance);
    function getInstance() {
        if (!chartInstance) {
            initCharts(getDarkTheme.value);
        }
        return chartInstance;
    }
    function disposeInstance() {
        if (!chartInstance)
            return;
        removeResizeFn();
        chartInstance.dispose();
        chartInstance = null;
    }
    return {
        setOptions,
        resize,
        echarts,
        getInstance,
        disposeInstance,
    };
}
