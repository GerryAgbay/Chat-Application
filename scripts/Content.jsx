import * as React from 'react';
import { Button } from './Button';
import { Socket } from './Socket';
import { GoogleButton } from './GoogleButton';

export function Content(props) {
    const [messages, setMessages] = React.useState([]);
    const [userCount, setUserCount] = React.useState(0);
    
    function getNewMessages() {
        React.useEffect(() => {
            Socket.on('messages received', updateMessages);
            return () => {
                Socket.off('messages received', updateMessages);
            };
        });
    }
    
    function getUserCount() {
        React.useEffect(() => {
            Socket.on('status', updateUserCount);
            return () => {
                Socket.off('status', updateUserCount);
            };
        });
    }
    
    function updateMessages(data) {
        console.log("Received messages from server: " + data['allMessages']);
        setMessages(data['allMessages']);
        
        var arrayLength = messages.length;
        for (var i = 0; i < arrayLength; i++) {
            if (messages[i].startsWith("https://")) {
                if(messages[i].endsWith(".jpg") || messages[i].endsWith(".png") || messages[i].endsWith(".gif")) {
                    var img = document.createElement('img');
                    img.src = messages[i];
                    document.getElementById("display-messages").appendChild(img);
                }
                else {
                    var link = document.createElement('a');
                    link.href = messages[i];
                    link.innerHTML = messages[i];
                    document.getElementById("display-messages").appendChild(link);
                }
            }
            else if (messages[i].startsWith("HALFBOT: ")) {
                var botMsg = document.createElement("botMsg");
                botMsg.innerHTML = "<h3>" + messages[i] + "</h3>";
                document.getElementById("display-messages").appendChild(botMsg);
            }
            else {
                var usrMsg = document.createElement("usrMsg");
                usrMsg.innerHTML = "<h4>" + messages[i] + "</h4>";
                document.getElementById("display-messages").appendChild(usrMsg);
            }
            
        }
    }
    
    function updateUserCount(data) {
        console.log("Received user count from server: " + data['count']);
        setUserCount(data['count']);
    }
    
    getNewMessages();
    getUserCount();

    return (
        <div>
            <h1>CHAT APP</h1>
            <div class = "header">
                <div class = "google-button"><GoogleButton /></div>
                <div class = "num-users">number of users: {userCount}</div>
            </div>
            <div class = "scroll-box">
                <ol id = "display-messages">
                </ol>
            </div>
                <Button />
        </div>
    );
}
