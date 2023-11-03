const {onMounted, ref} = Vue;
const {Random} = Mock;
const {NCard} = naive;
import {renderFontClassIcon} from "/static/naive-ui/fontawesome-free-6.4.2-web/js/Icon.js";
import {countTo,withInstall} from "/static/naive-ui/js/components/CountTo.js";

globalThis.Main = {
    setup() {
        const loading = ref(true);
        const visits = ref({});
        const saleroom = ref({});
        const orderLarge = ref({});
        const volume = ref({});
        // 图标列表
        const iconList = [
            {
                icon: renderFontClassIcon('fa-solid fa-user-group'),
                size: '32',
                title: '用户',
                color: '#69c0ff',
                eventObject: {
                    click: () => {
                    },
                },
            },
            {
                icon: renderFontClassIcon('fa-solid fa-chart-column'),
                size: '32',
                title: '分析',
                color: '#69c0ff',
                eventObject: {
                    click: () => {
                    },
                },
            },
            {
                icon: renderFontClassIcon('fa-solid fa-cart-shopping'),
                size: '32',
                title: '商品',
                color: '#ff9c6e',
                eventObject: {
                    click: () => {
                    },
                },
            },
            {
                icon: renderFontClassIcon('fa-solid fa-file-invoice'),
                size: '32',
                title: '订单',
                color: '#b37feb',
                eventObject: {
                    click: () => {
                    },
                },
            },
            {
                icon: renderFontClassIcon('fa-regular fa-credit-card'),
                size: '32',
                title: '票据',
                color: '#ffd666',
                eventObject: {
                    click: () => {
                    },
                },
            },
            {
                icon: renderFontClassIcon('fa-regular fa-envelope'),
                size: '32',
                title: '消息',
                color: '#5cdbd3',
                eventObject: {
                    click: () => {
                    },
                },
            },
            {
                icon: renderFontClassIcon('fa-solid fa-tag'),
                size: '32',
                title: '标签',
                color: '#ff85c0',
                eventObject: {
                    click: () => {
                    },
                },
            },
            {
                icon: renderFontClassIcon('fa-solid fa-bars'),
                size: '32',
                title: '配置',
                color: '#ffc069',
                eventObject: {
                    click: () => {
                    },
                },
            },
        ];

        const consoleInfo = {
            //访问量
            visits: {
                dayVisits: Random.float(10000, 99999, 2, 2),
                rise: Random.float(10, 99),
                decline: Random.float(10, 99),
                amount: Random.float(99999, 999999, 3, 5),
            },
            //销售额
            saleroom: {
                weekSaleroom: Random.float(10000, 99999, 2, 2),
                amount: Random.float(99999, 999999, 2, 2),
                degree: Random.float(10, 99),
            },
            //订单量
            orderLarge: {
                weekLarge: Random.float(10000, 99999, 2, 2),
                rise: Random.float(10, 99),
                decline: Random.float(10, 99),
                amount: Random.float(99999, 999999, 2, 2),
            },
            //成交额度
            volume: {
                weekLarge: Random.float(10000, 99999, 2, 2),
                rise: Random.float(10, 99),
                decline: Random.float(10, 99),
                amount: Random.float(99999, 999999, 2, 2),
            },
        };
        onMounted( async () => {
            const data = consoleInfo;
            visits.value = data.visits;
            saleroom.value = data.saleroom;
            orderLarge.value = data.orderLarge;
            volume.value = data.volume;
            loading.value = false;
        });
        return {
            iconList,
            loading,
            volume,
            orderLarge,
            saleroom,
            visits,
        }
    },
    components: {
        'ncard': NCard,
        'countto': withInstall(countTo)
    }
}