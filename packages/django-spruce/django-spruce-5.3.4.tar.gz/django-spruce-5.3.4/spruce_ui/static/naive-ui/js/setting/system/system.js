globalThis.Main = {
    setup() {
        const {reactive, toRefs, ref} = Vue;
        const typeTabList = [
            {
                name: '基本设置',
                desc: '系统常规设置',
                key: 1,
            },
            {
                name: '显示设置',
                desc: '系统显示设置',
                key: 2,
            },
            {
                name: '邮件设置',
                desc: '系统邮件设置',
                key: 3,
            },
        ];
        const rules = {
            name: {
                required: true,
                message: '请输入网站名称',
                trigger: 'blur',
            },
            mobile: {
                required: true,
                message: '请输入联系电话',
                trigger: 'input',
            },
        };
        const formRef = ref(null);
        const state = reactive({
            type: 1,
            typeTitle: '基本设置',
            formValue: {
                name: '',
                mobile: '',
                icpCode: '',
                address: '',
                loginCode: 0,
                closeText: '网站维护中，暂时无法访问！本网站正在进行系统维护和技术升级，网站暂时无法访问，敬请谅解！',
                systemOpen: true,
                bigWidth: '',
                bigHeight: '',
                smallWidth: '',
                smallHeight: '',
                watermarkClarity: null,
                pricePrecise: 1,
                isMarketPrice: true,
                pricePreciseNum: null,
            },
        });

        function systemOpenChange(value) {
            if (!value) {
                dialog.warning({
                    title: '提示',
                    content: '您确定要关闭系统访问吗？该操作立马生效，请慎重操作！',
                    positiveText: '确定',
                    negativeText: '取消',
                    onPositiveClick: () => {
                        message.success('操作成功');
                    },
                    onNegativeClick: () => {
                        state.formValue.systemOpen = true;
                    },
                });
            }
        }

        function formSubmit() {
            formRef.value.validate((errors) => {
                if (!errors) {
                    message.success('验证成功');
                } else {
                    message.error('验证失败，请填写完整信息');
                }
            });
        }

        function resetForm() {
            formRef.value.restoreValidation();
        }

        function switchType(e) {
            state.type = e.key;
            state.typeTitle = e.name;
        }

        const watermarkPlaceList = [
            {
                label: '左上',
                value: 1,
            },
            {
                label: '右上',
                value: 2,
            },
            {
                label: '居中',
                value: 3,
            },
            {
                label: '右下',
                value: 4,
            },
        ];

        const pricePreciseNumList = [
            {
                label: '2位',
                value: 1,
            },
            {
                label: '3位',
                value: 2,
            },
            {
                label: '4位',
                value: 3,
            },
        ];
        const pricePreciseList = [
            {
                label: '四舍五入',
                value: 1,
            },
            {
                label: '向上取整',
                value: 2,
            },
            {
                label: '向下取整',
                value: 3,
            },
        ];
        return Object.assign(Object.assign({formRef}, toRefs(state)), {
            pricePreciseList,
            pricePreciseNumList,
            watermarkPlaceList,
            switchType,
            rules,
            formSubmit,
            resetForm,
            systemOpenChange,
            typeTabList,
        });
    }
}