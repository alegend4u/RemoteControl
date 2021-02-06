var keys = [];
var mouse = [0,0];
var last_mouse_pos = [0,0];
var click = [];
var stuck = 0;

document.oncontextmenu = function() {
  return false;
}

function mouse_send(dif){
	let x = last_mouse_pos[0] - mouse[0];
	let y = last_mouse_pos[1] - mouse[1];
	if (x < 0) { x = x * -1; }
	if (y < 0) { y = y * -1; }
	if (x+y > dif) { 
		last_mouse_pos[0] = mouse[0];
		last_mouse_pos[1] = mouse[1]
		return true;
	}
	return false;
}

function send_to_server(){
	let xhr = new XMLHttpRequest();
	xhr.open("POST", "/postkeys", false);
	xhr.setRequestHeader('Content-Type', 'text');
	xhr.send(JSON.stringify({"keys" : keys, "mouse" : mouse, "click" : click}));
}

function send_size(){
	let xhr = new XMLHttpRequest();
	xhr.open("POST", "/size", false);
	xhr.setRequestHeader('Content-Type', 'text');
	xhr.send(JSON.stringify({width : document.body.clientWidth, height : document.body.clientHeight}));	
}

window.onresize = function(event) {
	send_size();
};

document.addEventListener('keydown', function(event) {
	event.preventDefault();
	let index = keys.indexOf(event.keyCode);
	if (index == -1) {
		keys.push(event.keyCode);
		send_to_server();
	}
});

document.addEventListener('keyup', function(event) {
	let index = keys.indexOf(event.keyCode);
	if (index > -1) {
		keys.splice(index, 1);
		send_to_server();
	}
});

document.addEventListener('mousemove', function(event) {
	mouse[0] = event.x;
	mouse[1] = event.y;
	index = keys.indexOf(2);
	if (mouse_send(10)) {
		send_to_server();
	}
});

document.addEventListener('mousedown', function(event) {
	event.preventDefault();
	let index = click.indexOf(event.buttons);
	mouse[0] = event.x;
	mouse[1] = event.y;
	if (index == -1) {
		click.push(event.buttons);
		send_to_server();
	}
});

document.addEventListener('mouseup', function(event) {
	let index = click.indexOf(1);
	mouse[0] = event.x;
	mouse[1] = event.y;
	if (index > -1) {
		click.splice(index, 1);
	}
	index = click.indexOf(2);
	if (index > -1) {
		click.splice(index, 1);
	}
	send_to_server();
});

send_size()