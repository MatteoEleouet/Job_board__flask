$("#up").hide();

//limit display div

let list = document.getElementById('cardlist');
let cards = list.getElementsByClassName('card');
for(let i = 0; i < cards.length; i++) {
    if(i > 1) {
        $(cards[i]).hide();
    }
}

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
