    
import * as React from 'react';


import { Button } from './Button';
import { Socket } from './Socket';

export function Content() {
    const [addresses, setAddresses] = React.useState([]);
    
    function getNewAddresses() {
        React.useEffect(() => {
            Socket.on('messages received', updateAddresses);
            return () => {
                Socket.off('messages received', updateAddresses);
            }
        });
    }
    
    function updateAddresses(data) {
        console.log("Received messages from server: " + data['allAddresses']);
        setAddresses(data['allAddresses']);
    }
    
    getNewAddresses();

    return (
        <div>
            <h1>CHAT APP</h1>
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
