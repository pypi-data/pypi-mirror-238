import {designStore, lighten} from "/static/naive-ui/js/setupNaiveDiscreteApi.js";
const {zhCN, dateZhCN, darkTheme, NDialogProvider, NNotificationProvider, NMessageProvider} = naive;
const {computed} = Vue;
app.component('ui-app', {
    template: `<NConfigProvider
    :locale="zhCN"
    :theme-overrides="getThemeOverrides"
    :date-locale="dateZhCN"
  >
    <AppProvider>
      <slot name="default"></slot>
    </AppProvider>
  </NConfigProvider>`,
    setup() {
        const getThemeOverrides = computed(() => {
            const appTheme = designStore.appTheme;
            const lightenStr = lighten(designStore.appTheme, 6);
            return {
                common: {
                    primaryColor: appTheme,
                    primaryColorHover: lightenStr,
                    primaryColorPressed: lightenStr,
                    primaryColorSuppl: appTheme,
                },
                LoadingBar: {
                    colorLoading: appTheme,
                },
            };
        });
        return {
            zhCN, dateZhCN, darkTheme,getThemeOverrides
        }
    },
    components: {
        'AppProvider': {
            template: `<n-dialog-provider>
                        <n-notification-provider>
                          <n-message-provider>
                            <slot name="default"></slot>
                          </n-message-provider>
                        </n-notification-provider>
                      </n-dialog-provider>`,
            setup() {
                return undefined;
            },
            components: {
                NDialogProvider,
                NNotificationProvider,
                NMessageProvider,
            },
        }
    }
})

