const {reactive, unref, ref, watch, computed, toRefs, h} = Vue
const {NAvatar, NInputNumber} = naive;
import {fotmat_input} from "/static/naive-ui/js/mock/self.js"

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
globalThis.Main = {
    setup() {
        const getGrid = computed(() => {
            if (isInline.value === false) {
                return {"cols": "1 s:1 m:2 l:2 xl:2 2xl:3", "collapsed": false, "responsive": "screen"}
            } else {
                return {"cols": "1 s:2 m:3 l:3 xl:3 2xl:4", "collapsed": false, "responsive": "screen"}
            }
        })
        const formElRef = reactive({
            username: ''
        })
        const overflow = ref(false)
        const isInline = ref(true)
        const getBindValue = reactive({
            "labelWidth": 80,
            "layout": "inline",
            "size": "medium",
            "labelPlacement": "left",
        })
        watch(
            overflow, (newValue, oldValue) => {
                isInline.value = oldValue !== false;
            }
        )
        const loadingSub = ref(false)

        //时间转化
        function mk_time(timestamp) {
            const date = new Date(timestamp);
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0'); // 使用padStart来确保月份是两位数
            const day = String(date.getDate()).padStart(2, '0'); // 使用padStart来确保日期是两位数
            const formattedTime = date.toLocaleTimeString();
            const formattedDate = `${year}-${month}-${day}`;
            return formattedDate + ' ' + formattedTime
        }

        const resetFields = () => {
            for (const i in state.filters) {
                if (state.filters[i]['value']) {
                    state.filters[i]['value'] = null
                }
            }
        }

        // 新建
        function addTable() {

        }

        // 刷新数据
        function reloadTable() {

        }

        function reload() {
        }

        const densityOptions = [{"type": "menu", "label": "紧凑", "key": "small"}, {
            "type": "menu",
            "label": "默认",
            "key": "medium"
        }, {"type": "menu", "label": "宽松", "key": "large"}]

        const state = reactive({
            tableSize: unref({
                "width": 220,
                "title": "操作",
                "key": "action",
                "fixed": "right"
            }).size || 'medium',
            isColumnSetting: false,
        });

        if (globalThis.file_format) {
            state.file_format = globalThis.file_format
        } else {
            state.file_format = []
        }

        if (globalThis.list_max_show_all) {
            state.list_max_show_all = globalThis.list_max_show_all
        } else {
            state.list_max_show_all = 200
        }
        if (globalThis.search_name) {
            state.search_name = '可以输入 ' + globalThis.search_name + '的关键字'
        } else {
            state.search_name = ''
        }

        const pagination = reactive({
            "page": 1, //第几页
            "pageSize": state.list_max_show_all, //每页显示的数量
            "pageSizes": [1, 10, 20, 50, 100, 500, 1000], //选择每页显示的数量
            "showSizePicker": true,
            "showQuickJumper": true,
            "pageCount": 60,
            "itemCount": 600,
            onChange: (page) => {
                pagination.page = page;
            },
            onUpdatePageSize: (pageSize) => {
                pagination.pageSize = pageSize;
                pagination.page = 1;
            }
        })
        const isStriped = ref(false);
        const setStriped = (value) => (
            isStriped.value = value
        );

        function render(row) {
            return h(NAvatar, {
                size: 48,
                src: row.avatar
            });
        }

        const checkedRowKeysRef = ref([]);

        function handleCheck(rowKeys) {
            checkedRowKeysRef.value = rowKeys;

        }

        //页码切换
        // function updatePage(page) {
        //     console.log(page)
        //     setPagination({page: page});
        //     reload();
        // }

        //分页数量切换
        // function updatePageSize(size) {
        //     setPagination({page: 1, pageSize: size});
        //     reload();
        // }

        //密度切换
        function densitySelect(e) {
            state.tableSize = e;
        }

        const results = ref(globalThis.results)

        function render_data(row) {
            return h({template: row})
        }

        for (const i in results.value.data) {
            for (const o in results.value.data[i]) {
                if (results.value.data[i].hasOwnProperty(o)) {
                    if (o === 'spruce_ui') {
                        continue;
                    }
                }
                results.value.data[i][o] = render_data(results.value.data[i][o])
            }
        }

        if (globalThis.filters) {
            state.filters = globalThis.filters
        }
        if (globalThis.search) {
            state.search = globalThis.search
        } else {
            state.search = null
        }

        function delete_a(name) {
            const params = new URLSearchParams();
            params.append('action', name)
            params.append('index', 0)
            params.append('select_across', 0)
            if (checkedRowKeysRef.value.length > 0) {
                for (const i in checkedRowKeysRef.value) {
                    params.append('_selected_action', checkedRowKeysRef.value[i])
                }
            } else {
                dialog.error({
                    title: '错误提示',
                    content: '请选择数据'
                })
                return
            }

            const encodedString = params.toString();
            axios({
                method: 'post',
                url: '',
                data: encodedString,
                headers: {'X-CSRFToken': csrftoken},
            }).then(function (res) {
                dialog.warning({
                    title: '警告',
                    content: '你确定删除？',
                    positiveText: '确定',
                    negativeText: '不确定',
                    onPositiveClick: () => {
                        message.success('正在删除')
                        message.destroyAll();
                        params.append('post', 'yes')
                        const yes_encodedString = params.toString();
                        axios({
                            method: 'post',
                            url: '',
                            data: yes_encodedString,
                            headers: {'X-CSRFToken': csrftoken},
                        }).then(function (res) {
                            message.success('删除成功')
                            message.destroyAll();
                            window.location.reload()
                        }).catch(function (error) {
                            dialog.error({
                                title: '错误提示',
                                content: '删除失败' + error,
                            })
                        })
                    },
                    onNegativeClick: () => {
                        message.error('不确定')
                    }
                })
            }).catch(function (error) {
                dialog.error({
                    title: '错误提示',
                    content: '删除失败' + error,
                })
            });
        }

        function bc(name) {
            const params = new URLSearchParams();
            params.append('action', name)
            params.append('index', 0)
            params.append('select_across', 0)
            for (const i in checkedRowKeysRef.value) {
                params.append('_selected_action', checkedRowKeysRef.value[i])
            }
            const encodedString = params.toString();
            axios({
                method: 'post',
                url: '',
                data: encodedString,
                headers: {'X-CSRFToken': csrftoken},
            }).then(function (res) {
                dialog.success({
                    title: '提示',
                    content: '操作成功',
                })
                message.destroyAll()
                window.location.reload()
            }).catch(function (error) {
                dialog.warning({
                    title: '错误提示',
                    content: error,
                })
            })
        }

        function handleUpdateValue(value, option) {
            message.info("option: " + JSON.stringify(option));
        }

        const options = ref([])

        const sl_options = ref([
            {
                label: 'Drive My Car',
                value: 'song1'
            },
            {
                label: 'Norwegian Wood',
                value: 'song2'
            },
            {
                label: "You Won't See",
                value: 'song3'
            },
            {
                label: 'Nowhere Man',
                value: 'song4'
            },
            {
                label: 'Think For Yourself',
                value: 'song5'
            },
            {
                label: 'The Word',
                value: 'song6'
            },
            {
                label: 'Michelle',
                value: 'song7'
            },
            {
                label: 'What goes on',
                value: 'song8'
            },
            {
                label: 'Girl',
                value: 'song9'
            },
            {
                label: "I'm looking through you",
                value: 'song10'
            },
            {
                label: 'In My Life',
                value: 'song11'
            },
            {
                label: 'Wait',
                value: 'song12'
            }
        ])

        // 点击查询
        const handleSubmit = () => {
            let query
            query = ''
            for (const i in state.filters) {
                if (state.filters[i]['value']) {
                    if (state.filters[i]['value'] !== '?') {
                        if (state.filters[i]['field_generic']) {
                            if (query === '') {
                                query += state.filters[i]['key'] + 'gte=' + mk_time(state.filters[i]['value'][0]) + '&' +
                                    state.filters[i]['key'] + 'lt=' + mk_time(state.filters[i]['value'][1])
                            } else {
                                query += '&' + state.filters[i]['key'] + 'gte=' + mk_time(state.filters[i]['value'][0]) + '&' +
                                    state.filters[i]['key'] + 'lt=' + mk_time(state.filters[i]['value'][1])
                            }
                            continue
                        }
                        if (query === '') {
                            query += state.filters[i]['key'] + '=' + state.filters[i]['value']
                        } else {
                            query += '&' + state.filters[i]['key'] + '=' + state.filters[i]['value']

                        }

                    }
                }
            }
            if (state.search) {
                if (query !== '') {
                    query += '&' + 'q=' + state.search
                } else {
                    query += 'q=' + state.search
                }
            }

            if (query) {
                location.href = '?' + query
            } else {
                location.href = window.location.pathname
            }
        }
        const showModal = ref(false)

        function exports(url) {
            console.log(state.file_format)
            if (checkedRowKeysRef.value.length > 0) {
                showModal2.value = true
            } else {
                message.error('请选择要导出的数据')
            }

        }

        function imports(url) {
            // showModal.value = true
            location.href = url
        }

        const showModal2 = ref(false)
        const selectedValues = ref()
        const selectedValues2 = ref()
        const uploadRef = ref()

        function handleClick() {
            if (selectedValues.value) {
                uploadRef.value?.submit()
            } else {
                message.error('请先选择类型')
            }

        }

        const fileListLengthRef = ref(0);

        function handleChange(options) {
            fileListLengthRef.value = options.fileList.length;
        }

        function exports_all(url) {
            location.href = url
        }

        function handleClick2() {
            if (!selectedValues2.value) {
                message.error('先选择文件类型，才能导出')
                return
            }
            const form = document.createElement("form");
            form.style.display = 'none'
            form.method = "POST"; // 或 "GET"，取决于你的需求
            form.action = ""; // 指定提交的URL


            form.appendChild(fotmat_input('text', 'action', 'export_admin_action'));
            form.appendChild(fotmat_input('text', 'csrfmiddlewaretoken', csrftoken));
            form.appendChild(fotmat_input('text', 'select_across', 0));
            form.appendChild(fotmat_input('text', 'file_format', selectedValues2.value));
            form.appendChild(fotmat_input('text', 'index', 0));
            form.appendChild(fotmat_input('text', 'index', 0));


            for (const i in checkedRowKeysRef.value) {
                form.appendChild(fotmat_input('text', '_selected_action', checkedRowKeysRef.value[i]));
            }

            document.body.appendChild(form);

            form.submit();
        }

        return Object.assign(Object.assign({}, toRefs(state)), {
            exports_all,
            selectedValues2,
            handleClick2,
            showModal2,
            upload: uploadRef,
            fileListLength: fileListLengthRef,
            handleChange,
            handleClick,
            selectedValues,
            sl_options,
            exports,
            imports,
            handleSubmit,
            delete_a,
            options,
            results,
            checkedRowKeysRef,
            handleUpdateValue,
            densityOptions,
            reload,
            bc,
            handleCheck,
            rowKey: (row) => row.spruce_ui,
            pagination,
            // getBindValues,
            // updatePage,
            // updatePageSize,
            densitySelect,
            setStriped,
            isStriped,
            resetFields,
            loadingSub,
            getBindValue,
            addTable,
            reloadTable,
            isInline,
            formElRef,
            overflow,
            getGrid,
            showModal,
            formValue: reactive({})
        })
    }
}