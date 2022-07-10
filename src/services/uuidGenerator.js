export default {
    install: (app, options) => {

        app.config.globalProperties.$uuid = (type) => {

            var S4 = function () {
                return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
            };
            if (type == 'small') {
                return S4();
            } else {
                return (S4() + S4() + "-" + S4() + "-" + S4() + "-" + S4() + "-" + S4() + S4() + S4());
            }
        }
    },
}
