const {reactive, ref} = Vue;
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
globalThis.Main = {
    setup() {
        const formRef = ref();
        const loading = ref(false);
        const autoLogin = ref(true);
        const formInline = reactive({
            username: 'test',
            password: 'test',
            isCaptcha: true,
        });
        const rules = {
            username: {required: true, message: '请输入用户名', trigger: 'blur'},
            password: {required: true, message: '请输入密码', trigger: 'blur'},
        };
        const handleSubmit = (e) => {
            e.preventDefault();
            formRef.value.validate(async (errors) => {
                if (!errors) {
                    message.loading('登录中...');
                    loading.value = true;
                    try {
                        message.destroyAll();
                        axios({
                            method: 'post',
                            url: '/spruce_ui/login/',
                            headers: {'X-CSRFToken': csrftoken},
                            data: JSON.stringify({
                                formInline: formInline
                            })
                        }).then((response) => {
                            message.destroyAll();
                            message.success(response.data)
                            location.reload()
                        }).catch((error)=>{
                            message.destroyAll();
                            message.error(error.response.data);
                        });
                    } finally {
                        loading.value = false;
                    }
                } else {
                    message.error('请填写完整信息，并且进行验证码校验');
                }
            });

        }
        return {
            formRef, formInline, rules, loading, autoLogin, handleSubmit
        }
    }
}