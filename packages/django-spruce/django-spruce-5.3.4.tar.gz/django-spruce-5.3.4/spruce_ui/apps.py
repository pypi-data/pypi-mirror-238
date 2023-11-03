from django.apps import AppConfig


class SpruceUiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spruce_ui'

    def ready(self):
        # 如果是django3+ 就使用中间件，删除header中的X-Frame-Options
        from spruce_ui.views import custom_404_view, custom_403_view, custom_500_view
        from django.conf import urls
        urls.handler404 = custom_404_view
        urls.handler403 = custom_403_view
        urls.handler500 = custom_500_view
        try:
            import django
            from django.conf import settings
            version = django.get_version()
            if int(version.split('.')[0]) >= 3:
                for index, item in enumerate(settings.MIDDLEWARE):
                    if item == 'django.middleware.clickjacking.XFrameOptionsMiddleware':
                        settings.MIDDLEWARE.pop(index)
        except Exception as e:
            raise e