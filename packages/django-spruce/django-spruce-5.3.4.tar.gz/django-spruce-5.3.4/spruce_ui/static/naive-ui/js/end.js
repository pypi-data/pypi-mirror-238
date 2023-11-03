const meta = document.createElement('meta');
meta.name = 'naive-ui-style';
document.head.appendChild(meta);
app.use(naive)
app.mount('#app', true);
