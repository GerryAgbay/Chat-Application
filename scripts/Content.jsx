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
    }
    
    function updateUserCount(data) {
        console.log("Received user count from server: " + data['count']);
        setUserCount(data['count']);
    }
    
    var wrapper = document.createElement("div");
    wrapper.setAttribute("id", "scroll-box");
    function parseMsgs(messageList) {
        wrapper.style.cssText = "overflow-y:scroll; height:70%; text-align:left; margin:auto; background-color:#FFF8DC; width:70%; display: flex; flex-direction:column-reverse; border: 2px solid; border-color: #5F9EA0;";
        document.body.appendChild(wrapper);

        var x = document.createElement("OL");
        x.setAttribute("id", "display-messages");
        document.getElementById("scroll-box").appendChild(x);
        
        if (document.getElementById("display-messages").hasChildNodes()) {
            document.getElementById("display-messages").remove();
        }
        
        var arrayLength = messageList.length;
        for (var i = 0; i < arrayLength; i++) {
            if (messageList[i].startsWith("https://")) {
                if(messageList[i].endsWith(".jpg") || messageList[i].endsWith(".png") || messageList[i].endsWith(".gif")) {
                    var img = document.createElement('img');
                    img.src = messageList[i];
                    img.height = "400";
                    img.width = "500";
                    document.getElementById("display-messages").appendChild(img);
                }
                else {
                    var link = document.createElement('a');
                    link.href = messageList[i];
                    link.innerHTML = messageList[i];
                    document.getElementById("display-messages").appendChild(link);
                }
            }
            else if (messageList[i].startsWith("HALFBOT: ")) {
                var botMsg = document.createElement("botMsg");
                botMsg.innerHTML = "<h3>" + messageList[i] + "</h3>";
                document.getElementById("display-messages").appendChild(botMsg);
            }
            else {
                var usrMsg = document.createElement("usrMsg");
                usrMsg.innerHTML = "<h4>" + messageList[i] + "</h4>";
                document.getElementById("display-messages").appendChild(usrMsg);
            }
        }
    }
    
    getNewMessages();
    getUserCount();
    parseMsgs(messages);

    return (
        <div>
            <h1>CHAT APP</h1>
            <div class = "header">
                <div class = "google-button"><GoogleButton /></div>
                <div class = "num-users">number of users: {userCount}</div>
            </div>
                <Button />
        </div>
    );
}