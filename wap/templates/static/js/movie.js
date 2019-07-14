var app = new Framework7({
    root: '#app',
    theme: 'md',
    name: 'Movie ticket',
    id: 'com.movie_ticket',
    lazy: {
        threshold: 50,
        sequential: false,
    }
});
const api_url = '/api/';
var $$ = Dom7;
var current_app_mobile = "";
var current_token = "";
app.lazy.create('.page');

window.onbeforeunload = function(){
    app.preloader.show()
};

var phoneSupport = app.dialog.create({
    title: "Thông báo",
    text: 'Bạn có muốn thực hiện cuộc gọi tới số 1900555520 để được hỗ trợ không?',
    buttons: [
        {text: 'Hủy'},
        {text: '<a href="tel:1900555520" class="external">Gọi</a>'}
    ],
    cssClass: "custom-dialog"
});
var introDialog = app.dialog.create({
    title: "Thông báo",
    text: 'Hệ thống đặt vé xem phim cung cấp bởi VNPAY. Thông tin đặt vé vui lòng liên hệ <a onclick="introDialog.close();phoneSupport.open();">1900555520</a>',
    buttons: [{text: 'Đồng ý'}],
    cssClass: "custom-dialog-phone"
});

function showDialog(message, level) {
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
    if(level === 'error'){

    }
}

function formatNumber(num) {
    return num.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')
}

function custom_post(path, params) {

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    const form = document.createElement('form');
    form.method = 'post';
    form.action = path;

    const csrfField = document.createElement('input');
    csrfField.type = 'hidden';
    csrfField.name = 'csrfmiddlewaretoken';
    csrfField.value = params['csrfmiddlewaretoken'];
    form.appendChild(csrfField);

    const appMobile = document.createElement('input');
    appMobile.type = 'hidden';
    appMobile.name = 'app_mobile';
    appMobile.value = params['app_mobile'];
    form.appendChild(appMobile);

    const tokenInput = document.createElement('input');
    tokenInput.type = 'hidden';
    tokenInput.name = 'token';
    tokenInput.value = params['token'];
    form.appendChild(tokenInput);

    const hiddenField = document.createElement('input');
    hiddenField.type = 'hidden';
    hiddenField.name = 'payload';
    hiddenField.value = JSON.stringify(params);
    form.appendChild(hiddenField);
    form.appendChild(hiddenField);
    document.body.appendChild(form);
    form.submit();
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
Date.prototype.publishDate = function () {
    var mm = this.getMonth() + 1;
    var dd = this.getDate();

    return [
        (dd > 9 ? '' : '0') + dd,
        (mm > 9 ? '' : '0') + mm,
        this.getFullYear()
    ].join('/');
};

Date.prototype.ticketDate = function () {
    var mm = this.getMonth() + 1;
    var dd = this.getDate();

    return (dd > 9 ? '' : '0') + dd + ' tháng ' + (mm > 9 ? '' : '0') + mm + ', ' + this.getFullYear()
};

Object.size = function (obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

