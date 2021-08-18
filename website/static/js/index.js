function deleteCard(card){
    fetch("/delete-card", {
        method: 'POST',
        body: JSON.stringify({card: card}),
    }).then((_res) =>{
        window.location.reload();
    })
}
