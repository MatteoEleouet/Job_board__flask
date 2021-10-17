$('.post').hide();
$('#up').hide();



function deroulcard(btn) {
    $('.' + btn).on("click", function() {
        $(this).parent().find(".more").toggle();
        if ($(this).parent().find(".more").is(":visible")) {
            $(this).text("En savoir -");
        } else {
            $(this).text("En savoir +");
        }
    });
}

let id = 10

function createCard(i, element) {
    $('#cardlist').append('<div class="card ' + i +'"></div>')
    $('.' + i).append('<div class="card-header ch' + i +'"></div>')
    $('.ch' + i).append(
        '<h5 class="card-title">'+ element[1] +'</h5>',
        '<h6 class="card-subtitle mb-2 text-muted">' + element[3] +'</h6>',
        '<h6 class="card-subtitle mb-2 text-muted">'+ element[8] +'</h6>'
    )
    $('.' + i).append('<div class="card-body cb' + i +'"></div>')
    $('.cb' +i).append(
    '<div class="more m'+i+'"></div>')
    $('.m'+i).append('<p class="card-text">'+ element[7] +'<p>',
    '<p class="salaire">'+ element[6] +'</p>')
    $('.cb' + i).append(
        '<a href="#" class="card-link sav s'+i+'">En savoir +</a>'
    )
    $('.cb' + i).append('<br>')
    $('.m' + i).append('<a href="#" class="card-link post" onclick="apply('+ id  +', '+ element[0] +')">Postuler</a>')
    deroulcard('s' + i)
}


$(document).ready(() => {
    $.get(
        "http://127.0.0.1:5000/api/job/list", (data) => {
            let i = 0
            data.forEach(element => {
                i++
                createCard(i, element)
                if(i > 3) {
                    $('.' + i).hide()
                }
            });
        }
    )
})









$("#down").click(() => {
    let list = document.getElementById('cardlist');
    let cards = list.getElementsByClassName('card');
    for(let i = 0; i <= cards.length; i++) {
        $(cards[i]).show();
    }
    $("#down").hide();
    $("#up").show();
})

$("#up").click(() => {
    let list = document.getElementById('cardlist');
    let cards = list.getElementsByClassName('card');
    for(let i = cards.length ; i > 1; i--) {
        $(cards[i]).hide();
    }
    $("#down").show();
    $("#up").hide();
})
