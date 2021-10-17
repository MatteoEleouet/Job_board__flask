function utf8_to_b64(str) {
    return window.btoa(unescape(encodeURIComponent(str)));
}
function b64_to_utf8(str) {
    return decodeURIComponent(escape(window.atob(str)));
}

// console.log(b64_to_utf8(localStorage.getItem('id')))
$('.post').hide();
$('#up').hide();
$('#monespace').hide()
if (localStorage.getItem('id')) {
    $('#connexion').attr("href", "")
    $('#connexion').attr("data-bs-toggle", "")
    $('#connexion').attr("data-bs-target", "")    
    $('#connexion').attr("onclick", "deco()")
    $('#connexion').text("Logout")
    $('#monespace').show()
}


function modal(i, id, offre) {
    $.get(
        "http://127.0.0.1:5000/api/users/get/"+ id +"" , (data) => {
            $('body').append('<div class="modal fade" id="modalApplication'+i+'" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true"></div>')
            $('#modalApplication'+i+'').append('<div class="modal-dialog modal-xl mf'+i+'"></div>')
            $('.mf' +i).append('<div class="modal-content mc'+i+'"></div>')
            $('.mc' +i).append('<div class="modal-header mh'+i+'"><h2 class="modal-title ms-5" id="exampleModalLabel">Postuler pour '+ offre[1] +'</h2><button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button></div>')
            $('.mc' +i).append('<div class="modal-body container-fluid mb'+i+'"></div>')
            $('.mb' +i).append('<form class="form'+i+'"></div>')
            $('.form' + i).append('<div class="form-group row ms-5 me-5 mt-4"><label for="name" class="col-sm-2 col-form-label"><h5>Nom complet</h5></label><div class="col-sm-5"><input type="text" class="form-control" id="prenom" value="'+ data['prenom'] +'"></div><div class="col-sm-5"><input type="text" class="form-control" id="nom" value="'+ data['nom'] +'"></div></div><br><hr><br><div class="form-group row ms-5 me-5"><label for="email" class="col-sm-2 col-form-label"><h5>Email</h5></label><div class="col-sm-10"><input type="text" class="form-control" id="mailuser" value="'+ data['mail'] +'"></div></div><br><hr><br><div class="form-group row ms-5 me-5"><label for="message'+i+'" class="col-sm-2 col-form-label"><h5>Message</h5></label><div class="col-sm-10"><textarea class="form-control messageChomeur" id="message'+i+'" placeholder="Message envoyé à lemployeur"></textarea></div></div><br><hr><br><button type="button" class="btn btn-primary btn-lg ms-5 me-5" id="postuler'+i+'">Envoyer la candidature</button>')
            modalPostul(offre, i, id)
        }
    )


}

function deco() {
    localStorage.removeItem('id')
    window.location.replace('index.html')
}

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


function modalPostul(offre, i, id) {
    let nameOffre = offre[1]
    $("#postuler" + i).click((e) => {
        let annonce = {
            message : $('#message'+i).val()
        }
        let jsonConvert = JSON.stringify(annonce)
        e.preventDefault()
        $.ajax({
            method: "POST",
            url: "http://localhost:5000/api/users/applyjob/"+ id +"/"+ offre[0] +"",
            data: jsonConvert,
            contentType: "application/json",
            dataType: 'JSON',
            success: function (data) {
                $('form').append('<div class="success">Vous avez bien postulé à cette offre ' + nameOffre +' </div>')
                // Redirection
                setTimeout(function(){window.location.replace("index.html")}, 6000);
            },
            error: function (request, error) {
                alert(request.responseText);
                alert(error)
            }
        })
    })
}

function createCard(i, element) {
    $('#cardlist').append('<div class="card ' + i +'"></div>')
    $('.' + i).append('<div class="card-header ch' + i +'"></div>')
    $('.ch' + i).append(
        '<h5 class="card-title">'+ element[1] +'</h5>',
        '<h6 class="card-subtitle mb-2 text-muted">' + element[3] +'</h6>',
        '<h6 class="card-subtitle mb-2 text-muted">'+ element[8] +'</h6>')
    $('.' + i).append('<div class="card-body cb' + i +'"></div>')
    $('.cb' +i).append(
    '<div class="more m'+i+'"></div>')
    $('.m'+i).append('<p class="card-text">'+ element[7] +'<p>',
    '<p class="salaire">'+ element[6] +'</p>')
    $('.cb' + i).append(
        '<button href="#!" class="btn btn-primary card-link sav s'+i+'">En savoir +</button>'
    )
    $('.cb' + i).append('<br>')
    $('.m' + i).append('<button type="button" class="btn btn-success mb-3" id="btnpost'+i+'" data-bs-toggle="modal" data-bs-target="#modalApplication'+i+'">Postuler</button>')
    deroulcard('s' + i)
}

function numberCandidat(i, idAd) {
    $.get(
        "http://127.0.0.1:5000/api/job/count/"+ idAd +"" , (data) => {
            $('.ch' + i).append(
                '<h6 class="card-subtitle mb-2 text-muted">'+ data[0] +' Candidat(s)</h6>'  )
        }
    )
}


$(document).ready(() => {
    $.get(
        "http://127.0.0.1:5000/api/job/list", (data) => {
            let i = 0
            data.forEach(element => {
                i++
                let idAd = element[0]
                createCard(i, element)
                numberCandidat(i, idAd)
                if(i > 2) {
                    $('.' +i).hide()
                }
                if(localStorage.getItem('id')) {
                    const uid = b64_to_utf8(localStorage.getItem('id'))
                    modal(i, uid, element)
                } else {
                    $("#btnpost"+i).hide()
                }
                if (localStorage.getItem('role') != 0 ) {
                    $("#btnpost"+i).hide()
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
