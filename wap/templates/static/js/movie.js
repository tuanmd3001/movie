var app = new Framework7({
    root: '#app',
    theme: 'md',
    name: 'Movie ticket',
    id: 'com.movie_ticket',
    lazy: {
        threshold: 50,
        sequential: false,
    },
});
var $$ = Dom7;
const api_domain = 'http://192.168.179.69:8000/api/';
var app_mobile = "";
app.lazy.create('.page');

function errorDialog(message) {
    app.dialog.create({
        title: 'Thông Báo',
        text: message,
        buttons: [
            {
                text: '',
                onClick: function (e) {
                    e.preventDefault()
                }
            }
        ],
        cssClass: "custom-dialog"
    }).open();
}

function showDialog(message) {
    app.dialog.create({
        title: 'Thông Báo',
        text: message,
        buttons: [
            {
                text: 'Đồng ý'
            }
        ],
        cssClass: "custom-dialog"
    }).open();
}

String.prototype.toDate = function (format) {
    var normalized = this.replace(/[^a-zA-Z0-9]/g, '-');
    var normalizedFormat = format.toLowerCase().replace(/[^a-zA-Z0-9]/g, '-');
    var formatItems = normalizedFormat.split('-');
    var dateItems = normalized.split('-');

    var monthIndex = formatItems.indexOf("mm");
    var dayIndex = formatItems.indexOf("dd");
    var yearIndex = formatItems.indexOf("yyyy");
    var hourIndex = formatItems.indexOf("hh");
    var minutesIndex = formatItems.indexOf("ii");
    var secondsIndex = formatItems.indexOf("ss");

    var today = new Date();

    var year = yearIndex > -1 ? dateItems[yearIndex] : today.getFullYear();
    var month = monthIndex > -1 ? dateItems[monthIndex] - 1 : today.getMonth() - 1;
    var day = dayIndex > -1 ? dateItems[dayIndex] : today.getDate();

    var hour = hourIndex > -1 ? dateItems[hourIndex] : today.getHours();
    var minute = minutesIndex > -1 ? dateItems[minutesIndex] : today.getMinutes();
    var second = secondsIndex > -1 ? dateItems[secondsIndex] : today.getSeconds();

    return new Date(year, month, day, hour, minute, second);
};
Date.prototype.ddmmyyyy = function () {
    var mm = this.getMonth() + 1;
    var dd = this.getDate();

    return [
        (dd > 9 ? '' : '0') + dd,
        (mm > 9 ? '' : '0') + mm,
        this.getFullYear()
    ].join('/');
};

