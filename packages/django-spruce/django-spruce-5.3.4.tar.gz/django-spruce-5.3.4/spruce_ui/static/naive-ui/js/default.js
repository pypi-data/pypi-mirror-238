globalThis.Main = {
    setup(){
        const goHome = ()=>{
            window.open('/admin/')
        }
        const activation = () => {
            if (code.value){
                location.href = `/spruce_ui/pay/?key=${code.value}`
            }else {
                message.error('请输入激活码')
            }
        }
        const code = Vue.ref()
        return{
            code,
            activation,
            goHome,
        }
    }
}