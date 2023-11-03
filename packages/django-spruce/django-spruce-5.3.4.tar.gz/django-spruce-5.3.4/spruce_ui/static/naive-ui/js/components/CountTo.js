const {ref, computed, watchEffect, unref, onMounted, watch, defineComponent} = Vue;
const {useTransition, TransitionPresets} = VueUse;
export const withInstall = (component, alias) => {
    const comp = component;
    comp.install = (app) => {
        app.component(comp.name || comp.displayName, component);
        if (alias) {
            app.config.globalProperties[alias] = component;
        }
    };
    return component;
};

export const countTo = defineComponent({
    template: `<span :style="{ color }">
                {{ value }}
              </span>`,
    props: {
        jla_start: {type: Number, default: 0},
        jla_end: {type: Number, default: 2021},
        duration: {type: Number, default: 1500},
        autoplay: {type: Boolean, default: true},
        decimals: {
            type: Number,
            default: 0,
            validator(value) {
                return value >= 0;
            },
        },
        prefix: {type: String, default: ''},
        suffix: {type: String, default: ''},
        separator: {type: String, default: ','},
        decimal: {type: String, default: '.'},
        /**
         * font color
         */
        color: {type: String},
        /**
         * Turn on digital animation
         */
        useEasing: {type: Boolean, default: true},
        /**
         * Digital animation
         */
        transition: {type: String, default: 'linear'},
    },
    emits: ['onStarted', 'onFinished'],
    setup(props, {emit}) {
        const source = ref(props.jla_start);
        const disabled = ref(false);
        let outputValue = useTransition(source);
        const value = computed(() => formatNumber(unref(outputValue)));
        watchEffect(() => {
            source.value = props.jla_start;
            // 在这里使用 props 的数据
            // ...
        });
        watch([() => props.jla_start, () => props.jla_end], () => {
            if (props.autoplay) {
                start();
            }
        });
        onMounted(() => {
            props.autoplay && start();
        });

        function start() {
            run();
            source.value = props.jla_end;
        }

        function reset() {
            source.value = props.jla_start;
            run();
        }

        function run() {
            outputValue = useTransition(source, Object.assign({
                disabled,
                duration: props.duration,
                onFinished: () => emit('onFinished'),
                onStarted: () => emit('onStarted')
            }, (props.useEasing ? {transition: TransitionPresets[props.transition]} : {})));
        }

        function formatNumber(num) {
            if (!num) {
                return '';
            }
            const {decimals, decimal, separator, suffix, prefix} = props;
            num = parseInt(num).toFixed(decimals);
            num += '';
            const x = num.split('.');
            let x1 = x[0];
            const x2 = x.length > 1 ? decimal + x[1] : '';
            const rgx = /(\d+)(\d{3})/;
            if (separator && !isFinite(separator)) {
                while (rgx.test(x1)) {
                    x1 = x1.replace(rgx, '$1' + separator + '$2');
                }
            }
            return prefix + x1 + x2 + suffix;
        }

        return {value, start, reset};
    },
});