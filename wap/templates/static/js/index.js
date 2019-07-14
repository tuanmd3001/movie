app.searchbar.create({
    el: '#location_select_popup .searchbar',
    searchContainer: '#location_select_popup .list',
    searchIn: '#location_select_popup .item-title'
});
$$('#location_select_opener').on("click", function () {
    app.popup.open($$("#location_select_popup"), true)
});

app.searchbar.create({
    el: '#film-search .searchbar',
    searchContainer: '#film-search .list',
    searchIn: '#film-search .item-title'
});
$$('#search-film-btn').on("click", function () {
    app.popup.open($$("#film-search"), true)
});

function selectLocation(location_id) {
    if (location_id === undefined) {
        location_id = 93;
    }
    $$('[data-location="' + location_id + '"]').prop('checked', true).trigger("click");
}

function getLocation(lat, lon) {
    app.preloader.show();
    app.request.promise.json(api_url + 'get_current_location', {
        app_mobile: current_app_mobile,
        lat: lat,
        long: lon
    }).then(function (response) {
        if (response['code'] === "00") {
            selectLocation(response['data']['location_id'])
        }
    }).catch(selectLocation).then(function () {
        app.preloader.hide();
    })
}

function getPosition() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            getLocation(position.coords.latitude, position.coords.longitude)
        }, getLocation);
    }
    else {
        getLocation()
    }
}

function onLocationSelect(location_id, name) {
    app.preloader.show();
    $$('#selected_location').text(name).css('font-weight', 'bold');
    get_cinema(location_id).then(function (response) {
        if (response['code'] && response['code'] === "00") {
            renderCinema(groupCinema(response['data']), location_id)
        }
        else {
            $$('#cinema_list').empty();
            showDialog(response['message']);
        }
    }).catch(function (err) {
        showDialog('Kết nối máy chủ thất bại (00)');
        $$('#cinema_list').empty()
    }).then(function () {
        app.preloader.hide();
    })
}

function get_cinema(location_id) {
    return app.request.promise.json(api_url + "get_cinema_by_location", {
        location_id: location_id,
        app_mobile: current_app_mobile
    })
}

function groupCinema(data) {
    var dataArr = [];
    data.forEach(function (cinema) {
        if (!dataArr[cinema['groupName']]) {
            dataArr[cinema['groupName']] = [];
        }
        dataArr[cinema['groupName']].push(cinema)
    });
    return dataArr;
}

function renderCinema(data, location_id) {
    var htmlArr = [];
    for (var groupName in data) {
        var groupCinemaArr = [];
        var groupImg = "";
        data[groupName].forEach(function (cinema) {
            if (groupImg === "" && cinema['cinema_logo'] !== "") {
                groupImg = cinema['cinema_logo'];
            }
            groupCinemaArr.push(
                '<li>\n' +
                '  <a href="' + cinema_url + cinema['location_id'] + '/' + cinema['cinema_id'] + '?app_mobile=' + current_app_mobile + '&token=' + current_token + '" class="item-content link external">\n' +
                '      <div class="item-inner item-inner-custom no-padding-left">\n' +
                '      <div class="item-title color-black">' + cinema['cinema_name'] + '</div>\n' +
                '      </div>\n' +
                '  </a>\n' +
                '</li>'
            )
        });
        htmlArr.push(
            '<div class="box-c box-c-radius box-c-margin-sm">\n' +
            '    <div class="no-padding">\n' +
            '        <div class="list list-box accordion-list" style="color: black">\n' +
            '            <ul>\n' +
            '                <li class="accordion-item">\n' +
            '                    <a href="#" class="item-content item-link box-c__header">\n' +
            '                        <div>\n' +
            '                            <img src="' + groupImg + '" alt="" width="24"\n' +
            '                                 class="v-middle margin-r-xs">\n' +
            '                            <div class="inline-middle">' + groupName + '</div>\n' +
            '                        </div>\n' +
            '                        <img class="dropdown-ic" src="/static/img/ic_dropdown.svg" alt="">\n' +
            '                    </a>\n' +
            '                    <div class="accordion-item-content">\n' +
            '                        <div class="box-c__content no-padding list searchbar-found">\n' +
            '                            <ul>\n' +
            '                                ' + groupCinemaArr.join('\n') + '\n' +
            '                            </ul>\n' +
            '                        </div>\n' +
            '                    </div>\n' +
            '                </li>\n' +
            '            </ul>\n' +
            '        </div>\n' +
            '    </div>\n' +
            '</div>'
        )
    }
    $$('#cinema_list').empty().html(htmlArr.join('\n'))
}

function durationFormat(num) {
    if (num) {
        var hours = (num / 60);
        var rhours = Math.floor(hours);
        var minutes = (hours - rhours) * 60;
        var rminutes = Math.round(minutes);
        return rhours + " giờ " + (rminutes ? rminutes + " phút" : "");
    }
    else {
        return 'Đang cập nhật'
    }
}

function publishDateFormat(string) {
    return string.toDate("dd/mm/yyyy hh:ii:ss").publishDate()
}

function ticketDateFormat(string) {
    return string.toDate("dd/mm/yyyy hh:ii:ss").ticketDate()
}

function imdbFormat(value) {
    return value.toFixed(1);
}

function renderFilmListItem(film, is_showing) {
    var html = '<div class="box-c box-c-margin-sm film-vert__item-wrap">\n' +
        '    <div class="box-c__content no-padding">\n' +
        '        <div class="film-vert__item">\n' +
        '            <div class="film-vert__poster lazy lazy-fade-in" data-background="' + film['poster'] + '"></div>\n' +
        '            <a class="link box-c-link external" href="' + movie_url + film['filmId'] + '?app_mobile=' + current_app_mobile + '&token=' + current_token + '"></a>\n' +
        '            <div class="film-vert__title label-main two-line">\n' +
        '                <b>\n' +
        '                    ' + (film['nameVn'] ? film['nameVn'] : "Đang cập nhật") + '\n' +
        '                </b>\n' +
        '            </div>\n' +
        '            <div class="film-vert__title font-xs clrgrey one-line">\n' +
        '                ' + (film['category'] ? film['category'] : "Đang cập nhật") + '\n' +
        '            </div>\n' +
        '            <div class="film-vert__time margin-b-xs">\n' +
        '                <div class="inline-middle">\n' +
        '                    <div class="dot dot-blue"></div>\n' +
        '                </div>\n' +
        '                <div class="inline-middle"> ' + durationFormat(film['duration']) + ' </div>\n' +
        '            </div>\n' +
        '            <div class="table table-100">\n' +
        '                <div class="td">\n' +
        '                    <div class="pills table">\n' +
        '                        <div class="pills-left ic-imdb td"></div>\n' +
        '                        <div class="pills-right td font-xs">' + imdbFormat(film['imdbPoint']) + '</div>\n' +
        '                    </div>\n' +
        '                </div>' +
        '                <div class="td right v-middle">\n';
    if (is_showing) {
        html += '                    <a href="' + movie_url + film['filmId'] + '?app_mobile=' + current_app_mobile + '&token=' + current_token + '&tab=tab-booking" class="external link button-c-xs box-c-link-inside current2">Đặt vé</a>\n';


    } else {
        html += '                    <a href="#" class="link btn-sm btn-border-blue box-c-link-inside upcoming"><div class="color-black">' + publishDateFormat(film['publishDate']) + '</div></a>';
    }
    html += '                </div>\n' +
        '            </div>\n' +
        '        </div>\n' +
        '    </div>\n' +
        '</div>';

    return html
}

function renderFilmSlideItem(film, is_showing) {
    var html = '<div class="swiper-slide">\n' +
        '    <div class="content__wrap--list-fly flex-column">\n' +
        '       <a class="link box-c-link external" href="' + movie_url + film['filmId'] + '?app_mobile=' + current_app_mobile + '&token=' + current_token + '"></a>\n' +
        '       <div class="box-list--int-1">\n' +
        '          <div class="film-poster lazy lazy-fade-in" data-background="' + film['poster'] + '"></div>\n' +
        '       </div>\n' +
        '       <div class="film-ìnfo center">\n' +
        '          <div class="film-title two-line">\n' +
        '             ' + film['nameVn'] + '\n' +
        '          </div>\n' +
        '          <div class="film-gerne font-sm one-line">\n' +
        '             ' + film['category'] + '\n' +
        '          </div>\n' +
        '          <div class="film-time font-sm">\n' +
        '             ' + durationFormat(film['duration']) + '\n' +
        '          </div>\n' +
        '       </div>\n' +
        '       <div class="margin-b-sm">\n';
    if (is_showing) {
        html += '           <a href="' + movie_url + film['filmId'] + '?app_mobile=' + current_app_mobile + '&token=' + current_token + '&tab=tab-booking" class="link button-c current external">Đặt vé</a>\n';
    }
    else {
        html += '           <a href="#" class="link btn-border-white table table-100 upcoming">\n' +
            '               <div class="td">\n' +
            '                   <div class="font-xs">Khởi chiếu</div>\n' +
            '                   <div class="label-main"><b><span class="white">' + publishDateFormat(film['publishDate']) + '</span></b></div>\n' +
            '               </div>\n' +
            '           </a>\n';
    }
    html += '       </div>' +
        '    </div>\n' +
        '</div>';
    return html
}

function renderFilmSearchItem(film) {
    return '<li>\n' +
        '    <a href="' + movie_url + film['filmId'] + '?app_mobile=' + current_app_mobile + '&token=' + current_token + '" class="link item-radio item-radio-location item-content external">\n' +
        '        <div class="item-inner item-inner-custom d-block">\n' +
        '            <div class="item-title color-black">' + film['nameVn'] + '</div>\n' +
        '            <div class="font-xs clrgrey">' + film['category'] + '</div>\n' +
        '        </div>\n' +
        '    </a>\n' +
        '</li>'
}

function renderListFilm(data) {
    var showing_films = [];
    var coming_films = [];
    var showing_films_slide = [];
    var coming_films_slide = [];
    var showing_films_search = [];
    data.forEach(function (film) {
        if (film['statusId'] === 2) {
            showing_films.push(renderFilmListItem(film, true));
            showing_films_slide.push(renderFilmSlideItem(film, true));
            showing_films_search.push(renderFilmSearchItem(film))
        }
        else if (film['statusId'] === 1) {
            coming_films.push(renderFilmListItem(film, false));
            coming_films_slide.push(renderFilmSlideItem(film, false));
        }
        else {
            console.log(film)
        }
    });
    // list film vertical
    $$("#film-showing .film-vert").html("").append(showing_films.join("\n"));
    $$("#film-coming .film-vert").html("").append(coming_films.join("\n"));
    // list film slide
    $$("#film-slide-showing .swiper-wrapper").html("").append(showing_films_slide.join("\n"));
    $$("#film-slide-coming .swiper-wrapper").html("").append(coming_films_slide.join("\n"));
    // list film in search
    $$("#list-film-search").html("").append(showing_films_search.join("\n"));
}

function getListFilm() {
    return app.request.promise.json(api_url + "get_film", {
        app_mobile: current_app_mobile
    })
}

$$("#tab-film").on('tab:show', function (event, ui) {
    app.preloader.show();
    $$('#search-film-btn').css('display', '');
    $$('#search-blank').css('display', 'none');
    $$('.film-toggle--list').trigger("click");
    getListFilm().then(function (response) {
        if (response['code'] && response['code'] === "00") {
            renderListFilm(response['data']);
            app.lazy.create('#flim-list');
        }
        else {
            showDialog(response['message']);
        }
    }).catch(function (err) {
        showDialog('Kết nối máy chủ thất bại (00)');
        console.log(err)
    }).then(function () {
        app.preloader.hide();
    });
});

$$("#tab-film").on('tab:hide', function (event, ui) {
    $$('#search-film-btn').css('display', 'none');
    $$('#search-blank').css('display', '');
});

var current_film_tab = "film-slide-showing";
var midEl;
var elScroll;

$$('.flim-list--list').on('scroll resize', function (e) {
    var docElm = document.documentElement;
    var viewportHeight = docElm.clientHeight,
        elements = $$('.film-vert__item-wrap');
    var middleElement;
    if (e && e.type === 'resize')
        viewportHeight = docElm.clientHeight;

    elements.each(function () {
        var pos = this.getBoundingClientRect().top;
        // if an element is more or less in the middle of the viewport
        if (pos > viewportHeight / 2.5 && pos < viewportHeight / 1.5) {
            middleElement = this;
            return false; // stop iteration
        }
    });
    midEl = $$(middleElement).index();
    elScroll = $$(this).scrollTop();
});

$$('.flim-list--list').on('scroll ', function (e) {
    elScroll = $$(this).scrollTop();
});

var swiper_showing = new Swiper('#film-slide-showing', {
    spaceBetween: 10,
    effect: 'coverflow',
    centeredSlides: true,
    slidesPerView: 'auto',
    threshold: 20,
    longSwipesRatio: 0.02,
    touchMoveStopPropagation: false,
    coverflowEffect: {
        rotate: 50,
        stretch: 0,
        depth: 200,
        modifier: 1,
        slideShadows: false
    }
});

var swiper_comming = new Swiper('#film-slide-coming', {
    spaceBetween: 10,
    effect: 'coverflow',
    centeredSlides: true,
    slidesPerView: 'auto',
    threshold: 20,
    longSwipesRatio: 0.02,
    touchMoveStopPropagation: false,
    coverflowEffect: {
        rotate: 50,
        stretch: 0,
        depth: 200,
        modifier: 1,
        slideShadows: false
    }
});

$$('.film-toggle--list').on('click', function () {
    $$('#flim-list').css('display', 'block');
    $$('#flim-slide').css('display', 'none');
    $$(this).css('display', 'none');
    $$('.film-toggle--slide').css('display', 'block');
    var swiper;
    if (current_film_tab === 'film-slide-showing') {
        swiper = swiper_showing;
    }
    else {
        swiper = swiper_comming;
    }
    if (swiper.activeIndex === 0) {
        $$('.flim-list--list').scrollTo(0, 0)
    }
    else {
        $$('.flim-list--list').scrollTo(0, $$('.film-vert__item-wrap').eq(swiper.activeIndex)[0].offsetTop - $$('.flim-list--list').height() / 2.5)
    }
});
$$('.film-toggle--slide').on('click', function () {
    $$('#flim-slide').css('display', 'block');
    $$('#flim-list').css('display', 'none');
    $$(this).css('display', 'none');
    $$('.film-toggle--list').css('display', 'block');
    var swiper;
    if (current_film_tab === 'film-slide-showing') {
        swiper = swiper_showing;
    }
    else {
        swiper = swiper_comming;
    }
    swiper.update();
    if (elScroll === 0) {
        swiper.slideTo(0, 600);
    }
    else {
        swiper.slideTo(midEl, 600);
    }
    swiper.update()

});

function currentUpcomingChange(is_checked, checked, unchecked) {
    if (is_checked) {
        $$('#' + checked).css('display', '');
        $$('#' + unchecked).css('display', 'none');
        current_film_tab = checked;
    }
    else {
        $$('#' + checked).css('display', 'none');
        $$('#' + unchecked).css('display', '');
        current_film_tab = unchecked;
    }
}

currentUpcomingChange(true, 'film-showing', 'film-coming');
currentUpcomingChange(true, 'film-slide-showing', 'film-slide-coming');

$$('#showing_tab_header').on('change', function (e) {
    currentUpcomingChange(e.target.checked, 'film-showing', 'film-coming');
    currentUpcomingChange(e.target.checked, 'film-slide-showing', 'film-slide-coming');
    swiper_showing.update()
});
$$('#coming_tab_header').on('change', function (e) {
    currentUpcomingChange(e.target.checked, 'film-coming', 'film-showing');
    currentUpcomingChange(e.target.checked, 'film-slide-coming', 'film-slide-showing');
    swiper_comming.update()
});

function getTicketList() {
    return app.request.promise.json(api_url + "get_my_ticket", {
        app_mobile: current_app_mobile
    })
}

function renderTicketList(data) {
    var html = '<div class="margin-b-md">Lịch sử giao dịch hiển thị trong vòng 2 tháng.</div>';
    if (data) {
        var listhtml = [];
        data.forEach(function (ticket) {
            console.log(ticket)
            listhtml.push('<a href="' + ticket_url + ticket['query_id'] + '?app_mobile=' + current_app_mobile + '&token=' + current_token + '" class="box-c__item external">\n' +
                '    <div class="table table-100">\n' +
                '        <div class="td">\n' +
                '            <div class="label-main two-line"><b>' + (ticket['film_name'] ? ticket['film_name'] : 'Đang cập nhật') + '</b></div>\n' +
                '            <div class="font-xs clrgrey margin-v-xxs one-line">' + (ticket['cinema_name'] ? ticket['cinema_name'] : 'Đang cập nhật') + '</div>\n' +
                '            <div class="font-xs clrgrey">' + (ticket['session_time'] ? ticketDateFormat(ticket['session_time']) : 'Đang cập nhật') + '</div>\n' +
                '        </div>\n' +
                '        <div class="td fitwidth right">\n' +
                '            <div class="label-main">\n' +
                '                <div class="clrorange"><b>' + formatNumber(ticket['amount']) + ' VND</b></div>\n' +
                '            </div>\n' +
                '        </div>\n' +
                '    </div>\n' +
                '</a>')
        });
        html += '<div class="box-c">\n' +
            '    <div class="box-c__content no-padding-bottom">\n' +
            listhtml.join('\n') +
            '    </div>\n' +
            '</div>'
    }
    else {
        html += '<div class="box-c p-blank p-blank--history">\n' +
            '    <div class="box-c__content">\n' +
            '        <div class="box-c__item center">\n' +
            '            <img src="/static/img/history-blank.svg" alt="">\n' +
            '            <div class="p-plank__text">Không tìm thấy dữ liệu. Vui lòng thử lại sau</div>\n' +
            '        </div>\n' +
            '    </div>\n' +
            '</div>'
    }
    $$('#ticket-list').empty().html(html);
}

$$("#tab-ticket").on('tab:show', function (event, ui) {
    app.preloader.show();
    getTicketList().then(function (response) {
        if (response['data'] && response['data'].length) {
            renderTicketList(response['data'])
        }
        else {
            renderTicketList()
        }
    }).catch(function (err) {
        renderTicketList()
    }).then(function () {
        app.preloader.hide();
    })
});