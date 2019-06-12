var app = new Framework7({
    root: '#app',
    theme: 'md',
    name: 'Movie ticket',
    // App id
    id: 'com.movie_ticket',
});
var $$ = Dom7;
const api_domain = 'http://localhost:8000/api/';
app.lazy.create('.lazy');

function alertDialog(message) {

}