app.searchbar.create({
    el: '#location_select_popup .searchbar',
    searchContainer: '#location_select_popup .list',
    searchIn: '#location_select_popup .item-title'
})

$$('#location_select_opener').on("click", function () {
    app.popup.open($$("#location_select_popup"), true)
});

function selectLocation(id, name) {
    $$('#selected_location').text(name).css('font-weight', 'bold');
    get_cinema(id).then(function (response) {
        if (response['code'] && response['code'] === "00") {
            console.log(response)
            renderCinema(groupCinema(response['data']))
        }
        else {
            showDialog(response['message']);
        }
    }).catch(function (err) {
        showDialog('Kết nối máy chủ thất bại (00)');
        console.log(err)
    })
}

function get_cinema(location_id) {
    return app.request.promise.json(api_domain + "get_cinema_by_location", {
        location_id: location_id,
        app_mobile: app_mobile
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

function renderCinema(data) {
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
                '  <a href="' + cinema_url + cinema['cinema_id'] + '?app_mobile=' + current_app_mobile + '" class="item-content link external">\n' +
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
            '        <div class="list list-box" style="color: black">\n' +
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
    var hours = (num / 60);
    var rhours = Math.floor(hours);
    var minutes = (hours - rhours) * 60;
    var rminutes = Math.round(minutes);
    return rhours + " giờ " + (rminutes ? rminutes + " phút" : "");
}

function publishDateFormat(string) {
    return string.toDate("dd/mm/yyyy hh:ii:ss").ddmmyyyy()
}

function renderFilmListItem(film, is_showing) {
    var html = '<div class="box-c box-c-margin-sm film-vert__item-wrap">\n' +
        '    <div class="box-c__content no-padding">\n' +
        '        <div class="film-vert__item">\n' +
        '            <div class="film-vert__poster lazy lazy-fade-in" data-background="' + film['poster'] + '"></div>\n' +
        '            <a class="link box-c-link external" href="' + movie_url + film['filmId'] + '?app_mobile=' + current_app_mobile + '"></a>\n' +
        '            <div class="film-vert__title label-main">\n' +
        '                <b>\n' +
        '                    ' + film['nameVn'] + '\n' +
        '                </b>\n' +
        '            </div>\n' +
        '            <div class="film-vert__title font-xs clrgrey">\n' +
        '                ' + film['category'] + '\n' +
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
        '                        <div class="pills-right td font-xs">' + film['imdbPoint'] + '</div>\n' +
        '                    </div>\n' +
        '                </div>' +
        '                <div class="td right v-middle">\n';
    if (is_showing) {
        html += '                    <a href="' + movie_url + film['filmId'] + '?app_mobile=' + current_app_mobile + '&tab=tab-booking" class="external link button-c-xs box-c-link-inside current2">Đặt vé</a>\n';


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
        '       <a class="link box-c-link external" href="' + movie_url + film['filmId'] + '?app_mobile=' + current_app_mobile + '"></a>\n' +
        '       <div class="box-list--int-1">\n' +
        '          <div class="film-poster lazy lazy-fade-in" data-background="' + film['poster'] + '"></div>\n' +
        '       </div>\n' +
        '       <div class="film-ìnfo center">\n' +
        '          <div class="film-title">\n' +
        '             ' + film['nameVn'] + '\n' +
        '          </div>\n' +
        '          <div class="film-gerne font-sm">\n' +
        '             ' + film['category'] + '\n' +
        '          </div>\n' +
        '          <div class="film-time font-sm">\n' +
        '             ' + durationFormat(film['duration']) + '\n' +
        '          </div>\n' +
        '       </div>\n' +
        '       <div class="margin-b-sm">\n';
    if (is_showing) {
        html += '           <a href="' + movie_url + film['filmId'] + '?app_mobile=' + current_app_mobile + '&tab=tab-booking" class="link button-c current external">Đặt vé</a>\n';
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

function renderListFilm(data) {
    var showing_films = [];
    var coming_films = [];
    var showing_films_slide = [];
    var coming_films_slide = [];
    data.forEach(function (film) {
        if (film['statusId'] === 2) {
            showing_films.push(renderFilmListItem(film, true));
            showing_films_slide.push(renderFilmSlideItem(film, true));
        }
        else if (film['statusId'] === 1) {
            coming_films.push(renderFilmListItem(film, false));
            coming_films_slide.push(renderFilmSlideItem(film, false));
        }
        else {
            console.log(film)
        }
    });
    $$("#film-showing .film-vert").html("").append(showing_films.join("\n"));
    $$("#film-coming .film-vert").html("").append(coming_films.join("\n"));
    $$("#film-slide-showing .swiper-wrapper").html("").append(showing_films_slide.join("\n"));
    $$("#film-slide-coming .swiper-wrapper").html("").append(coming_films_slide.join("\n"));
}

function getListFilm() {
    return app.request.promise.json(api_domain + "get_film", {
        app_mobile: app_mobile
    })
}

$$("#tab-film").on('tab:show', function (event, ui) {
    $$('#search-film').css('display', '');
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
    });
});

$$("#tab-film").on('tab:hide', function (event, ui) {
    $$('#search-film').css('display', 'none');
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