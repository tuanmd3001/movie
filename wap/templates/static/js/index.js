var location_searchbar = app.searchbar.create({
    el: '#location_select_popup .searchbar',
    searchContainer: '#location_select_popup .list',
    searchIn: '#location_select_popup .item-title'
});

function selectLocation(id, name) {
    $$('#selected_location').text(name).css('font-weight', 'bold');
    get_cinema(id)
}

function get_cinema(location_id) {
    app.request.promise.json(api_domain + "get_cinema_by_location", {location: location_id})
        .then(function (response) {
            if (response['code'] && response['code'] === "00") {
                renderCinema(groupCinema(response['data']))
            }
            else {
                alertDialog('Kết nối máy chủ thất bại (01)');
                console.log(response)
            }
        })
        .catch(function (err) {
            alertDialog('Kết nối máy chủ thất bại (00)');
            console.log(err)
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
                '  <a href="/wap/cinema/' + cinema['cinema_id'] + '" class="item-content link external">\n' +
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