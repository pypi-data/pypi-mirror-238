import {basicProps} from "/static/naive-ui/js/props/console.js";
import {useECharts} from "/static/naive-ui/js/hooks/web/useECharts.js"

const {ref, onMounted} = Vue;


app.component('visitab', {
    template: `
<div class="mt-4">
    <NRow :gutter="24">
      <NCol :span="24">
        <n-card content-style="padding: 0;" :bordered="false">
          <n-tabs type="line" size="large" :tabs-padding="20" pane-style="padding: 20px;">
            <n-tab-pane name="流量趋势">
              <FluxTrend ></FluxTrend>
            </n-tab-pane>
            <n-tab-pane name="访问量">
              <VisitAmount ></VisitAmount>
            </n-tab-pane>
          </n-tabs>
        </n-card>
      </NCol>
    </NRow>
  </div>`,
    setup() {

        return {};
    },
    components: {
        FluxTrend: {
            template: `<div ref="chartRef" :style="{ height, width }"></div>`,
            props: basicProps,
            setup() {
                const chartRef = ref(null);
                const {setOptions} = useECharts(chartRef);
                onMounted(() => {
                    setOptions({
                        tooltip: {
                            trigger: 'axis',
                            axisPointer: {
                                lineStyle: {
                                    width: 1,
                                    color: '#019680',
                                },
                            },
                        },
                        xAxis: {
                            type: 'category',
                            boundaryGap: false,
                            data: [
                                '6:00',
                                '7:00',
                                '8:00',
                                '9:00',
                                '10:00',
                                '11:00',
                                '12:00',
                                '13:00',
                                '14:00',
                                '15:00',
                                '16:00',
                                '17:00',
                                '18:00',
                                '19:00',
                                '20:00',
                                '21:00',
                                '22:00',
                                '23:00',
                            ],
                            splitLine: {
                                show: true,
                                lineStyle: {
                                    width: 1,
                                    type: 'solid',
                                    color: 'rgba(226,226,226,0.5)',
                                },
                            },
                            axisTick: {
                                show: false,
                            },
                        },
                        yAxis: [
                            {
                                type: 'value',
                                max: 80000,
                                splitNumber: 4,
                                axisTick: {
                                    show: false,
                                },
                                splitArea: {
                                    show: true,
                                    areaStyle: {
                                        color: ['rgba(255,255,255,0.2)', 'rgba(226,226,226,0.2)'],
                                    },
                                },
                            },
                        ],
                        grid: {left: '1%', right: '1%', top: '2  %', bottom: 0, containLabel: true},
                        series: [
                            {
                                smooth: true,
                                data: [
                                    111, 222, 4000, 18000, 33333, 55555, 66666, 33333, 14000, 36000, 66666, 44444,
                                    22222, 11111, 4000, 2000, 500, 333, 222, 111,
                                ],
                                type: 'line',
                                areaStyle: {},
                                itemStyle: {
                                    color: '#5ab1ef',
                                },
                            },
                            {
                                smooth: true,
                                data: [
                                    33, 66, 88, 333, 3333, 5000, 18000, 3000, 1200, 13000, 22000, 11000, 2221, 1201,
                                    390, 198, 60, 30, 22, 11,
                                ],
                                type: 'line',
                                areaStyle: {},
                                itemStyle: {
                                    color: '#019680',
                                },
                            },
                        ],
                    });
                });
                return {chartRef};
            },
        },
        VisitAmount: {
            template: `<div ref="chartRef" :style="{ height, width }"></div>`,
            props: basicProps,
            setup() {
                const chartRef = ref(null);
                const {setOptions} = useECharts(chartRef);
                onMounted(() => {
                    setOptions({
                        tooltip: {
                            trigger: 'axis',
                            axisPointer: {
                                lineStyle: {
                                    width: 1,
                                    color: '#019680',
                                },
                            },
                        },
                        grid: {left: '1%', right: '1%', top: '2  %', bottom: 0, containLabel: true},
                        xAxis: {
                            type: 'category',
                            data: [
                                '1月',
                                '2月',
                                '3月',
                                '4月',
                                '5月',
                                '6月',
                                '7月',
                                '8月',
                                '9月',
                                '10月',
                                '11月',
                                '12月',
                            ],
                        },
                        yAxis: {
                            type: 'value',
                            max: 8000,
                            splitNumber: 4,
                        },
                        series: [
                            {
                                data: [3000, 2000, 3333, 5000, 3200, 4200, 3200, 2100, 3000, 5100, 6000, 3200, 4800],
                                type: 'bar',
                                barMaxWidth: 80,
                            },
                        ],
                    });
                });
                return {chartRef};
            },
        }
    },
})

