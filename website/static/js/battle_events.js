

figthers = []

socket.emit('batalla', current_user)

socket.on('batalla', fighters=>{
  if (fighters[0] == current_user){
    if(confirm(`Estás listo para romperle el culo a ${fighters[1]}`)){
      socket.emit('confirm', current_user)
    }
  }
  else{
    if(confirm(`Estás listo para romperle el culo a ${fighters[0]}`)){
      socket.emit('confirm', current_user)
    }  
  }
})

socket.on('winner', (player, ability)=>{
  alert(`Os enfrentais por ${ability} asi que el ganador es: ${player}`)
})
// socket.on('user_connected', (name)=>{
//   socket.emit('users', name)
// });

// socket.on('connected_users', (data)=>{
//   for (user in data){
//    if (!users.includes(data[user])){
//     users.push(data[user])
//     }
//   }
//   printChallengeButtons(users);
// });

// socket.on('user_disconnected', (data)=>{  
//   users.splice(users.indexOf(data), 1);
//   printChallengeButtons(users);
// });

// function printChallengeButtons(users){
//     $('.rivals').html('');

//   users.forEach(user=>{ 
//     if (user != '{{user.name}}'){
//       $('.rivals').append(`<li><a class="dropdown-item text-secondary" id="${user}">${user}</a></li> `);
//       $(`#${user}`).click(()=>{
//         socket.emit('challenge', "{{user.name}}", user)
//         alert(`Reto enviado. Esperando a que ${user} acepete el reto.`)
//       });
//     }
//   });
// }

// socket.on('challenged', (challenger, challenged)=>{  
//   if ('{{user.name}}' == challenged){
//     if (confirm(`${challenger} te ha retado.`)){
//       socket.emit('redirect', challenger, challenged, true)
//     }
//     else{
//       alert('Has rechazado el reto rechazado')
//       socket.emit('redirect', challenger, challenged, false)
//     }
//   }    
// })

// socket.on('redirect', (challenger, challenged)=>{
//   if ('{{user.name}}' == challenged ||'{{user.name}}' == challenger){
//     location.href = "/battle"
//   }
// })

// socket.on('denied', (challenger, challenged)=>{
//   if ('{{user.name}}' == challenger){
//     alert(f`${challenged} no acpetó tu reto.`)
//   }
// })