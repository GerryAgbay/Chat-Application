import * as React from 'react';
import ReactDOM from 'react-dom';
import GoogleLogin from 'react-google-login';
import { Socket } from './Socket';

function handleGoogleOAuthSubmit(response) {
  const name = response.profileObj.givenName;
  const { email } = response.profileObj;
  Socket.emit('new google user', { name, email });
  Socket.emit('new google user 2', { name, email });
  console.log(`Sent the name ${name} to server!`);
  console.log(`Sent the email ${email} to server!`);
}
export function GoogleButton() {
  return (
    <GoogleLogin
      clientId="216345235263-sah770h9t0rnqinfc47gia9mm6dhrs55.apps.googleusercontent.com"
      buttonText="Login with Google!"
      onSuccess={handleGoogleOAuthSubmit}
      cookiePolicy="single_host_origin"
    />
  );
}
