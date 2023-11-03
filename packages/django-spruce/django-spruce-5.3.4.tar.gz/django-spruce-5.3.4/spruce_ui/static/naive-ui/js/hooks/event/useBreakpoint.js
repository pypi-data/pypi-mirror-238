const { ref, computed, unref } = Vue;
import { useEventListener } from '/static/naive-ui/js/hooks/event/useEventListener.js';
import { screenMap, sizeEnum, screenEnum } from '/static/naive-ui/js/hooks/enums/breakpointEnum.js';

let globalScreenRef;
let globalWidthRef;
let globalRealWidthRef;
export function useBreakpoint() {
    return {
        screenRef: computed(() => unref(globalScreenRef)),
        widthRef: globalWidthRef,
        screenEnum,
        realWidthRef: globalRealWidthRef,
    };
}
// Just call it once
export function createBreakpointListen(fn) {
    const screenRef = ref(sizeEnum.XL);
    const realWidthRef = ref(window.innerWidth);
    function getWindowWidth() {
        const width = document.body.clientWidth;
        const xs = screenMap.get(sizeEnum.XS);
        const sm = screenMap.get(sizeEnum.SM);
        const md = screenMap.get(sizeEnum.MD);
        const lg = screenMap.get(sizeEnum.LG);
        const xl = screenMap.get(sizeEnum.XL);
        if (width < xs) {
            screenRef.value = sizeEnum.XS;
        }
        else if (width < sm) {
            screenRef.value = sizeEnum.SM;
        }
        else if (width < md) {
            screenRef.value = sizeEnum.MD;
        }
        else if (width < lg) {
            screenRef.value = sizeEnum.LG;
        }
        else if (width < xl) {
            screenRef.value = sizeEnum.XL;
        }
        else {
            screenRef.value = sizeEnum.XXL;
        }
        realWidthRef.value = width;
    }
    useEventListener({
        el: window,
        name: 'resize',
        listener: () => {
            getWindowWidth();
            resizeFn();
        },
        // wait: 100,
    });
    getWindowWidth();
    globalScreenRef = computed(() => unref(screenRef));
    globalWidthRef = computed(() => screenMap.get(unref(screenRef)));
    globalRealWidthRef = computed(() => unref(realWidthRef));
    function resizeFn() {
        fn === null || fn === void 0 ? void 0 : fn({
            screen: globalScreenRef,
            width: globalWidthRef,
            realWidth: globalRealWidthRef,
            screenEnum,
            screenMap,
            sizeEnum,
        });
    }
    resizeFn();
    return {
        screenRef: globalScreenRef,
        screenEnum,
        widthRef: globalWidthRef,
        realWidthRef: globalRealWidthRef,
    };
}
