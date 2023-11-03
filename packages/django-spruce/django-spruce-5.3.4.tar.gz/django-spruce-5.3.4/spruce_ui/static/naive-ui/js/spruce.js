import {renderFontClassIcon} from "/static/naive-ui/fontawesome-free-6.4.2-web/js/Icon.js";
import {getIcon} from "/static/naive-ui/automatic/segment.js";
import {designStore, lighten, settingStore} from "/static/naive-ui/js/setupNaiveDiscreteApi.js";
if (window.self !== window.top) {
    globalThis.Main ={}
}else {
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
const {computed, ref, nextTick, watch, onMounted, reactive, unref} = Vue;

globalThis.Main = {
    setup() {
        if (default_list !== false) {
            if (menus !== false) {
                if (globalThis.First === true) {
                    menus = menus.concat(default_list)
                } else {
                    menus = default_list.concat(menus)
                }
            } else {
                menus = default_list
            }
        }
        for (const i in menus) {
            menus[i].icon = renderFontClassIcon(getIcon(menus[i].label))
        }

        function dg_menus(menus) {
            for (const i in menus) {
                menus[i].key = menus[i].name
                if (children_icon === true) {
                    menus[i].icon = renderFontClassIcon(getIcon(menus[i].label)) // 匹配子菜单图标
                }
                if (menus[i].children) {
                    dg_menus(menus[i].children)
                }
            }
            return menus
        }

        dg_menus(menus)
        const collapsed = ref(false);
        const fixedMenu = computed(() => {
            return 'absolute';
        });
        const leftMenuWidth = computed(() => {
            return 200;
        });
        const inverted = computed(() => {
            return true
        });
        const getMenuLocation = computed(() => {
            return 'left';
        });

        const new_postion = ref(null)

        //点击菜单
        function clickMenuItem(key, clickMenuItem) {
            new_postion.value = clickMenuItem
            const index = tabsList.value.indexOf(clickMenuItem);
            if (index === -1) {
                tabsList.value.push(clickMenuItem)
                tabsList.value = tabsList.value.filter((value, index, self) => self.indexOf(value) === index);
            } else {
                console.log('pass')
            }
            getSelectedKeys.value = key
            updateNavScroll(true);
        }

        const getSelectedKeys = ref(menus[0].children[0].name)

        const openKeys = ref()

        //展开菜单
        function menuExpanded(key) {
            //只展开菜单
            if (menus.find(i => i.name === [key[key.length - 1]][0])) {
                openKeys.value = [key[key.length - 1]]
            } else {
                openKeys.value = key
            }
        }

        //是否夜间模式
        const getHeaderInverted = computed(() => {
            return false;
        });

        const fixedHeader = computed(() => {
            return 'absolute';
        });

        const getDarkTheme = ref(false);

        //刷新
        const reloadPage = () => {
            refresh.value = true
            setTimeout(function () {
                refresh.value = false
            }, 500)
        };

        const iconList = globalThis.icon_list;

        const avatarOptions = [
            {
                label: '个人设置',
                key: 1,
            },
            {
                label: '退出登录',
                key: 2,
            },
        ];

        //头像下拉菜单
        const avatarSelect = (key) => {
            switch (key) {
                case 1:
                    message.info('未设置方法')
                    break;
                case 2:
                    doLogout();
                    break;
            }
        };
        const doLogout = () => {
            dialog.info({
                title: '提示',
                content: '您确定要退出登录吗',
                positiveText: '确定',
                negativeText: '取消',
                onPositiveClick: () => {
                    axios({
                        method: 'post',
                        url: '/spruce_ui/logout/',
                        headers: {'X-CSRFToken': csrftoken},
                    }).then((response) => {
                        message.destroyAll();
                        message.success(response.data)
                        location.reload()
                    })
                },
                onNegativeClick: () => {
                },
            });
        };

        function openSetting() {
            state.isDrawer = true
        }


        const breadcrumbList = computed(() => {
            if (typeof openKeys.value === 'undefined') {

            } else {
                if (typeof getSelectedKeys.value === 'undefined') {

                } else {
                    const data = menus.filter(tab => tab.name === openKeys.value[0])
                    try {
                        const children = data[0].children.filter(tab => tab.name === getSelectedKeys.value)
                        return data.concat(children);
                    } catch (error) {
                        // 处理错误情况
                        return data;
                    }
                }
            }
        });

        // 递归查询函数
        function dg_query(data, key) {
            for (const i in data) {
                if (data[i].name === key) {
                    return data[i];
                }
                const value = dg_query(data[i].children, key)
                if (value !== null) {
                    return value; // 如果未找到匹配的键值，则返回null或者其他适合的值
                }
            }
            return null
        }

        //点击
        const dropdownSelect = (key) => {
            const clickMenuItem_dg = dg_query(menus, key)
            getSelectedKeys.value = key
            clickMenuItem(key, clickMenuItem_dg)
        };


        // 切换全屏图标
        const toggleFullscreenIcon = () =>
            (
                document.fullscreenElement !== null ? 'FullscreenExitOutlined' : 'FullscreenOutlined');

        // 监听全屏切换事件
        document.addEventListener('fullscreenchange', toggleFullscreenIcon);

        const fixedMulti = computed(() => {
            return false;
        });
        const isMultiTabs = computed(() => {
            return true;
        });
        const scrollable = ref(false)
        const dropdownX = ref(0)
        const dropdownY = ref(0)
        const showDropdown = ref(false)
        const isMultiHeaderFixed = ref(false)
        const multiTabsSetting = ref({"bgColor": "#fff", "show": true, "fixed": false})
        const isMixMenuNoneSub = ref(true)
        const isMobile = ref(false)
        //tab 操作
        const closeHandleSelect = (key, item) => {
            switch (key) {
                //刷新
                case '1':
                    reloadPage();
                    showDropdown.value = false
                    break;
                //关闭
                case '2':
                    closeTabItem(new_postion.value)
                    showDropdown.value = false
                    break;
                //关闭其他
                case '3':
                    tabsList.value = [menus[0].children[0]].concat(tabsList.value.filter(i => i.name === getSelectedKeys.value))
                    showDropdown.value = false
                    break;
                //关闭所有
                case '4':
                    tabsList.value = []
                    tabsList.value.push(menus[0].children[0])
                    getSelectedKeys.value = tabsList.value[tabsList.value.length - 1].name
                    showDropdown.value = false
                    break;
            }
            updateNavScroll(true);
        };
        const navMode = 'vertical'
        const getChangeStyle = computed(() => {
            const minMenuWidth = 24
            const menuWidth = 200
            const {fixed} = multiTabsSetting.value;


            let lenNum = navMode.value === 'horizontal' || !isMixMenuNoneSub.value
                ? '0px'
                : collapsed
                    ? `${minMenuWidth}px`
                    : `${menuWidth}px`;
            if (isMobile.value) {
                return {
                    left: '0px',
                    width: '100%',
                };
            }
            return {
                left: lenNum,
                width: `calc(100% - ${!fixed ? '0px' : lenNum})`,
            };
        });

        function scrollTo(value, amplitude) {
            const currentScroll = navScroll.value.scrollLeft;
            const scrollWidth = (amplitude > 0 && currentScroll + amplitude >= value) ||
            (amplitude < 0 && currentScroll + amplitude <= value)
                ? value
                : currentScroll + amplitude;
            navScroll.value && navScroll.value.scrollTo(scrollWidth, 0);
            if (scrollWidth === value)
                return;
            return window.requestAnimationFrame(() => scrollTo(value, amplitude));
        }

        const navScroll = ref(null);
        const navWrap = ref();


        function scrollPrev() {
            const containerWidth = navScroll.value.offsetWidth;
            const currentScroll = navScroll.value.scrollLeft;

            if (!currentScroll) return;
            const scrollLeft = currentScroll > containerWidth ? currentScroll - containerWidth : 0;
            scrollTo(scrollLeft, (scrollLeft - currentScroll) / 20);
        }

        function scrollNext() {
            const containerWidth = navScroll.value.offsetWidth;
            const navWidth = navScroll.value.scrollWidth;
            const currentScroll = navScroll.value.scrollLeft;

            if (navWidth - currentScroll <= containerWidth) return;
            const scrollLeft =
                navWidth - currentScroll > containerWidth * 2
                    ? currentScroll + containerWidth
                    : navWidth - containerWidth;
            scrollTo(scrollLeft, (scrollLeft - currentScroll) / 20);
        }

        const isCurrent = ref(false);

        //tags 右侧下拉菜单
        const TabsMenuOptions = computed(() => {
            const isDisabled = ref(true)
            return [
                {
                    label: '刷新当前',
                    key: '1',
                    icon: renderFontClassIcon("fa-solid fa-rotate-right"),
                },
                {
                    label: `关闭当前`,
                    key: '2',
                    disabled: isCurrent.value || isDisabled,
                    icon: renderFontClassIcon("fa-solid fa-xmark"),
                },
                {
                    label: '关闭其他',
                    key: '3',
                    disabled: isDisabled,
                    icon: renderFontClassIcon("fa-regular fa-trash-can"),
                },
                {
                    label: '关闭全部',
                    key: '4',
                    disabled: isDisabled,
                    icon: renderFontClassIcon("fa-regular fa-closed-captioning"),
                },
            ];
            updateNavScroll(true);
        });

        function onClickOutside() {
            updateNavScroll(true);
            showDropdown.value = false;
        }

        const tabsList = ref([
            menus[0].children[0]
        ])

        //tags 跳转页面
        function goPage(e) {
            updateNavScroll(true);
            getSelectedKeys.value = e.name
            new_postion.value = e
        }

        //删除tab
        function closeTabItem(e) {
            updateNavScroll(true);
            tabsList.value = tabsList.value.filter(i => i.name !== e.name)
        }

        function handleContextMenu(e, item) {
            updateNavScroll(true);
            new_postion.value = item
            e.preventDefault();
            nextTick().then(() => {
                showDropdown.value = true;
                dropdownX.value = e.clientX;
                dropdownY.value = e.clientY;
            });
        }

        function toggleElement(i) {
            return i.name === getSelectedKeys.value;
        }

        const refresh = ref(false)
        const n = computed(() => {
            return getSelectedKeys.value
        })

        /**
         * @param autoScroll 是否开启自动滚动功能
         */
        async function updateNavScroll(autoScroll) {
            await nextTick();
            if (!navScroll.value)
                return;
            const containerWidth = navScroll.value.offsetWidth;
            const navWidth = navScroll.value.scrollWidth;
            if (containerWidth < navWidth) {
                scrollable.value = true;
                if (autoScroll) {
                    let tagList = navScroll.value.querySelectorAll('.tabs-card-scroll-item') || [];
                }
            } else {
                scrollable.value = false;
            }
        }

        onMounted(() => {
            updateNavScroll(true);


        });
        watch(
            () => designStore.darkTheme,
            (to) => {
                designStore.navTheme = to ? 'header-dark' : 'dark';
            }
        );

        const state = reactive({
            width: 280,
            title: '项目配置',
            isDrawer: false,
            placement: 'right',
            alertText: '该功能主要实时预览各种布局效果，更多完整配置在 projectSetting.ts 中设置',
            appThemeList: designStore.appThemeList,
        });
        const directionsOptions = computed(() => {
            return animateOptions.find((item) => item.value === unref(settingStore.pageAnimateType));
        });

        function openDrawer() {
            state.isDrawer = true;
        }

        function closeDrawer() {
            state.isDrawer = false;
        }

        function togNavTheme(theme) {
            settingStore.navTheme = theme;
            if (settingStore.navMode === 'horizontal' && ['light'].includes(theme)) {
                settingStore.navTheme = 'dark';
            }
        }

        function togTheme(color) {
            designStore.appTheme = color;
        }

        function togNavMode(mode) {
            settingStore.navMode = mode;
            settingStore.menuSetting.mixMenu = false;
        }

        const animateOptions = ref([{"value": "zoom-fade", "label": "渐变"}, {
            "value": "zoom-out",
            "label": "闪现"
        }, {"value": "fade-slide", "label": "滑动"}, {"value": "fade", "label": "消退"}, {
            "value": "fade-bottom",
            "label": "底部消退"
        }, {"value": "fade-scale", "label": "缩放消退"}])
        const toggleFullScreen = () => {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen();
            } else {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                }
            }
        };
        const icon_click = (url) => {
            window.open(url)
        }
        return {
            icon_click,
            toggleFullScreen,
            directionsOptions,
            togNavTheme,
            closeDrawer,
            openDrawer,
            togTheme,
            togNavMode,
            animateOptions,
            settingStore,
            designStore,
            state,
            n,
            refresh,
            handleContextMenu,
            closeTabItem,
            navScroll,
            goPage,
            tabsList,
            onClickOutside,
            isCurrent,
            TabsMenuOptions,
            scrollNext,
            scrollPrev,
            getChangeStyle,
            showDropdown,
            scrollable,
            dropdownX,
            dropdownY,
            isMultiHeaderFixed,
            closeHandleSelect,
            multiTabsSetting,
            fixedMenu,
            collapsed,
            leftMenuWidth,
            menus,
            inverted,
            getMenuLocation,
            openKeys,
            getSelectedKeys,
            clickMenuItem,
            menuExpanded,
            getHeaderInverted,
            fixedHeader,
            getDarkTheme,
            reloadPage,
            iconList,
            avatarOptions,
            doLogout,
            avatarSelect,
            openSetting,
            breadcrumbList,
            dropdownSelect,
            fixedMulti,
            isMultiTabs,
            Component: 'Component',
            toggleElement: toggleElement
        }
    },
    components: {
        'Component': {
            props: ['i', 'refresh', 'n'],
            template: `
            <n-spin :show="loading">
                <div class="frame">
                  <iframe :src="frameSrc" class="frame-iframe" ref="frameRef"></iframe>
                </div>
              </n-spin>
            `,
            setup(props, {emit}) {
                const {ref, unref, onMounted, nextTick, watch} = Vue;
                const loading = ref(false);
                const frameRef = ref(props.i.name);

                let frameSrc; // 在 if 语句之外声明变量
                // if (props.i.path.includes('https') || props.i.path.includes('https')) {

                frameSrc = ref(props.i.path);
                // } else {
                //     frameSrc = ref(`/spruce_ui/${props.i.path}`);
                // }

                function hideLoading() {
                    loading.value = false;
                }

                function init() {
                    nextTick(() => {
                        const iframe = unref(frameRef);
                        hideLoading()
                        if (!iframe)
                            return;
                        const _frame = iframe;
                    });
                }

                onMounted(() => {
                    loading.value = true;
                    init();
                })
                watch(() => props.refresh, (newValue, oldValue) => {
                    if (props.refresh === true) {
                        if (props.n === props.i.name) {
                            frameRef.value.contentWindow.location.reload();
                        }
                    }
                    // 在这里可以执行一些操作，以响应refresh的值变化
                })
                return {
                    loading,
                    frameRef,
                    frameSrc,
                }
            }
        }
    }
}}