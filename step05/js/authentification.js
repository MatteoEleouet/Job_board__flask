function utf8_to_b64( str ) {
    return window.btoa(unescape(encodeURIComponent( str )));
}
function b64_to_utf8( str ) {
    return decodeURIComponent(escape(window.atob( str )));
}
$('.recruteur').hide()
$('#flexRadioDefault1').prop("checked", true);
$('#flexRadioDefault1').click(() => {
    $('.recruteur').hide()
})
$('#flexRadioDefault2').click(() => {
    $('.recruteur').show()
})


$('#register').click((e) => {
    e.preventDefault()
    let data
    let mdp = $('#password1').val()
    let mdpverif = $('#password2').val()
    if (mdp == mdpverif) {
        if($("input:checked").val() == "0") {
            data = {
                'nom': $('#nom').val(),
                'prenom': $('#prenom').val(),
                'mail':$('#email').val(),
                'mdp': $('#password1').val(),
                'role': 0,
                'tel':$('#phone').val()
            }
        } else {
            data = {
                'nom': $('#nom').val(),
                'prenom': $('#prenom').val(),
                'mail':$('#email').val(),
                'mdp': $('#password1').val(),
                'role': 1,
                'tel':$('#phone').val(),
                'nomEntreprise': $('#nomEntreprise').val(),
                'secteur':$('#secteur').val(),
                'ville':$('#ville').val(),
                'description':$('#description').val(),
                'site_web':$('#site_web').val()
            }
        }
        let jsonConvert = JSON.stringify(data)
            $.ajax({
                method: "POST",
                url: "http://localhost:5000/api/register",
                data: jsonConvert,
                contentType: "application/json",
                dataType: 'JSON',
                success: function (datas) {
                    console.log(datas)
                    localStorage.setItem('id', utf8_to_b64(datas['id']))
                    localStorage.setItem('role', data['role'])
                    $('form').append('<div class="success">Inscription terminée ! Vous allez être redirigé dans 10 secondes :) </div>')
                    setTimeout(function(){window.location.replace("index.html")}, 5000);
                },
                error: function (request, error) {
                    alert(request.responseText);
                    alert(error)
                }
            })
    } else {
        $('form').append('<div class="error">Vous avez rentrer un mauvais mot de passe. Retentez.</div>')
    }
    
    
    
})

$("#login").click( (e) => {
    e.preventDefault();
    var data={
        mail: $('#emaillog').val(),
        mdp: $('#password').val()
       }
    let jsonConvert = JSON.stringify(data)
    $.ajax({
        method: "POST",
        url: "http://localhost:5000/api/login",
        data: jsonConvert,
        contentType: "application/json",
        dataType: 'JSON',
        success: function (data) {
            console.log(data)
            localStorage.setItem('id', utf8_to_b64(data['id']))
            localStorage.setItem('role', data['role'])
            // Redirection
            window.location.replace("index.html")
        },
        error: function (request, error) {
            alert(request.responseText);
            alert(error)
        }
    })
})

