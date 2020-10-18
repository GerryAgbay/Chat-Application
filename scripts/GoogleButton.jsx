import * as React from 'react';
import { Socket } from './Socket';
import ReactDOM from 'react-dom';
import GoogleLogin from 'react-google-login';
 
const responseGoogle = (response) => {
  console.log(response);
}

function handleGoogleOAuthSubmit(response) {
    console.log(response.nt.Wt);
    console.log(response.nt.Ad);
    let name = response.nt.Ad;
    let email = response.nt.Wt;
    Socket.emit('new google user', 
    { 'name': name, 'email': email }
    );
    
    console.log('Sent the name ' + name + ' to server!');
    console.log('Sent the email ' + email + ' to server!');
}

export function GoogleButton() {
    return <GoogleLogin
        clientId="216345235263-sah770h9t0rnqinfc47gia9mm6dhrs55.apps.googleusercontent.com"
        buttonText="Login with Google!"
        onSuccess={handleGoogleOAuthSubmit}
        cookiePolicy={'single_host_origin'}/>;
}
