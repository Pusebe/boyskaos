const socket = io();

users = []

socket.on('user_connected', (name)=>{
  socket.emit('users', name)
});

socket.on('connected_users', (data)=>{
  for (user in data){
   if (!users.includes(data[user])){
    users.push(data[user])
    }
  }
  printChallengeButtons(users);
});

socket.on('user_disconnected', (data)=>{  
  users.splice(users.indexOf(data), 1);
  printChallengeButtons(users);
});

function printChallengeButtons(users){
    $('.rivals').html('');

  users.forEach(user=>{ 
    if (user != current_user){
      $('.rivals').append(`<li style="cursor:pointer" title="Retar a ${user}"><a class="dropdown-item text-secondary" id="${user}">${user}</a></li> `);
      $(`#${user}`).click(()=>{
        socket.emit('challenge', current_user, user)
        alert(`Reto enviado. Esperando a que ${user} acepete el reto.`)
      });
    }
  });
}

socket.on('challenged', (challenger, challenged)=>{ 
  if (current_user == challenged){
    if (confirm(`${challenger} te ha retado.`)){
      socket.emit('redirect', challenger, challenged, true)
    }
    else{
      alert('Has rechazado el reto rechazado')
      socket.emit('redirect', challenger, challenged, false)
    }
  }    
})

socket.on('redirect', (challenger, challenged)=>{
  if (current_user == challenged ||current_user == challenger){
    location.href = `/battle/${challenger}/${challenged}`
  }
})

socket.on('denied', (challenger, challenged)=>{
  if (current_user == challenger){
    alert(`${challenged} no acpetó tu reto.`)
  }
})