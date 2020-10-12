    
import * as React from 'react';


import { Button } from './Button';
import { Socket } from './Socket';

export function Content() {
    const [addresses, setAddresses] = React.useState([]);
    const [userCount, setUserCount] = React.useState(0);
    
    function getNewAddresses() {
        React.useEffect(() => {
            Socket.on('messages received', updateAddresses);
            return () => {
                Socket.off('messages received', updateAddresses);
            }
        });
    }
    
    function getUserCount() {
        React.useEffect(() => {
            Socket.on('status', updateUserCount);
            return () => {
                Socket.off('status', updateUserCount)
            }
        });
    }
    
    function updateAddresses(data) {
        console.log("Received messages from server: " + data['allAddresses']);
        setAddresses(data['allAddresses']);
    }
    
    function updateUserCount(data) {
        console.log("Received user count from server: " + data['count']);
        setUserCount(data['count']);
    }
    
    getNewAddresses();
    getUserCount();

    return (
        <div>
            <h1>CHAT APP</h1>
            <h2>number of users: {userCount}</h2>
                <ol>
                    {
                        addresses.map(
                        (address, index) => <li key={index}>{address}</li>)
                    }
                </ol>
            <Button />
        </div>
    );
}
