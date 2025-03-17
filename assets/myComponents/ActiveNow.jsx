import React, { useState, useEffect } from 'react';

const ActiveNow = () => {
  // State to hold the list of active users
  const [activeUsers, setActiveUsers] = useState([]);

  // Set up WebSocket connection when the component mounts
  useEffect(() => {
    // Create a WebSocket connection to the server
    const socket = new WebSocket('ws://' + window.location.host + '/ws/active-now/');

    // Handle incoming WebSocket messages
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setActiveUsers(data.active_users); // Update state with new active users
    };

    // Optional: Log connection events for debugging
    socket.onopen = () => {
      console.log('WebSocket connection established');
    };

    socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    socket.onclose = () => {
      console.log('WebSocket connection closed');
    };

    // Cleanup: Close the WebSocket connection when the component unmounts
    return () => {
      socket.close();
    };
  }, []); // Empty dependency array ensures this runs only once on mount

  // Render the list of active users
  return (
    <div id="active-now">
      {activeUsers.map((user) => (
        <div key={user.username}>
          <p>Username: {user.username}</p>
          <p>Total Active Today: {user.total_active_today}</p>
          <p>
            Currently Studying: {user.current_course} - {user.current_topic} - {user.current_session}
          </p>
        </div>
      ))}
    </div>
  );
};

export default ActiveNow;