import { useState, useEffect } from 'react';
import './timer.css';

const Timer = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [startTime, setStartTime] = useState(null);
  const [currentTime, setCurrentTime] = useState(null);
  const [selectedCourse, setSelectedCourse] = useState('');
  const [selectedTopic, setSelectedTopic] = useState('');

  const [courses, setCourses] = useState([]);
  const [topics, setTopics] = useState([]);

  // Timer logic remains unchanged
  useEffect(() => {
    let interval;
    if (isRunning) {
      interval = setInterval(() => {
        setCurrentTime(Date.now());
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isRunning]);

  const handleStartStop = async () => {
    if (!isRunning) {
      // Start timer
      setStartTime(Date.now());
      setCurrentTime(Date.now());
    } else {
      // Stop timer and save session
      const endTime = Date.now();
      
      // Get CSRF token from cookies
      const csrfToken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];

      try {
        const response = await fetch('/api/tracked-times/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
          credentials: 'include', // Important for session cookies
          body: JSON.stringify({
            startTime: new Date(startTime).toISOString(),
            endTime: new Date(endTime).toISOString(),
            course: selectedCourse,
            topic: selectedTopic
          })
        });

        if (!response.ok) throw new Error('Failed to save time');
        
        console.log('Time tracked successfully');
        // Reset selections if needed
        setSelectedCourse('');
        setSelectedTopic('');
        
      } catch (error) {
        console.error('Error tracking time:', error);
      }

      // Reset timer
      setStartTime(null);
      setCurrentTime(null);
    }
    setIsRunning(!isRunning);
  };

  // Update the fetch calls to include credentials
  useEffect(() => {
    // Fetch courses
    fetch('/api/courses/', {
      credentials: 'include' // Send session cookie
    })
      .then(res => res.json())
      .then(data => setCourses(data))
      .catch(console.error);
  }, []);

  // Fetch topics when course changes
  useEffect(() => {
    if (selectedCourse) {
      fetch(`/api/topics/${selectedCourse}/`, {
        credentials: 'include' // Send session cookie
      })
        .then(res => res.json())
        .then(data => setTopics(data))
        .catch(console.error);
    } else {
      setTopics([]);
    }
    setSelectedTopic('');
  }, [selectedCourse]);


  const formatTime = () => {
    if (!startTime || !currentTime) return '00:00:00';
    
    const seconds = Math.floor((currentTime - startTime) / 1000);
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = seconds % 60;

    return [
      hours.toString().padStart(2, '0'),
      minutes.toString().padStart(2, '0'),
      remainingSeconds.toString().padStart(2, '0'),
    ].join(':');
  };

  return (
    <div className="timer-container">
      <div className="timer-controls">
        <p>in Timer.jsx</p>
        <select
          value={selectedCourse} 
          onChange={(e) => setSelectedCourse(e.target.value)}
          disabled={isRunning}
        >
          <option value="">Select Course</option>
          {courses.map((course) => (
            <option key={course.id} value={course.id}>
              {course.name}
            </option>
          ))}
        </select>

        <select
          value={selectedTopic}
          onChange={(e) => setSelectedTopic(e.target.value)}
          disabled={isRunning}
        >
          <option value="">Select Topic</option>
          {topics.map((topic) => (
            <option key={topic.id} value={topic.id}>
              {topic.name}
            </option>
          ))}
        </select>

        <button 
          onClick={handleStartStop}
          disabled={!selectedCourse || !selectedTopic}
        >
          {isRunning ? 'Stop Timer' : 'Start Timer'}
        </button>
      </div>
      
      <div className="timer-display">
        {formatTime()}
      </div>
    </div>
  );
};

export default Timer;