const {ref} = Vue;
globalThis.Main = {
    setup() {
        const showModal = ref(false)
        const frameSrc = ref('')

        function history(url) {
            showModal.value = true
            frameSrc.value = url
        }

        return {
            history,
            bodyStyle: {
                width: '600px'
            },
            segmented: {
                content: 'soft',
                footer: 'soft'
            },
            showModal,
            frameSrc
        }
    }
}