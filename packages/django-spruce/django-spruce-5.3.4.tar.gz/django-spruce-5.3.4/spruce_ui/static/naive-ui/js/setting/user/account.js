globalThis.Main = {
    setup() {
        const {reactive, ref} = Vue;
        const goHome = () => {
            window.open('/admin')
        }
        const rules = {
            name: {
                required: true,
                message: '请输入昵称',
                trigger: 'blur',
            },
            email: {
                required: true,
                message: '请输入邮箱',
                trigger: 'blur',
            },
            mobile: {
                required: true,
                message: '请输入联系电话',
                trigger: 'input',
            },
        };
        const formRef = ref(null);
        const formValue = reactive({
            name: '',
            mobile: '',
            email: '',
            address: '',
        });

        function formSubmit() {
            formRef.value.validate((errors) => {
                if (!errors) {
                    message.success('验证成功');
                } else {
                    message.error('验证失败，请填写完整信息');
                }
            });
        }

        const typeTabList = [
            {
                name: '基本设置',
                desc: '个人账户信息设置',
                key: 1,
            },
            {
                name: '安全设置',
                desc: '密码，邮箱等设置',
                key: 2,
            },
        ];
        const type = ref(1);
        const typeTitle = ref('基本设置');

        function switchType(e) {
            type.value = e.key;
            typeTitle.value = e.name;
        }

        return {
            type,
            switchType,
            typeTabList,
            goHome,
            rules,
            formRef,
            formValue,
            formSubmit,
        }
    }
}