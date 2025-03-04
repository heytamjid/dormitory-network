import { useState, useEffect } from 'react';
import axios from 'axios';

import { Button } from 'components/button.tsx'
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from 'components/select.tsx'



const Timer = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [startTime, setStartTime] = useState(null);
  const [currentTime, setCurrentTime] = useState(null);
  const [selectedCourse, setSelectedCourse] = useState('');
  const [selectedTopic, setSelectedTopic] = useState('');
  const [courses, setCourses] = useState([]);
  const [topics, setTopics] = useState([]);



  useEffect(() => {
    let interval;
    if (isRunning) {
      interval = setInterval(() => { //setInterval(func, delay in ms) is a built-in JavaScript function that calls the function or evaluates an expression at specified intervals indefinitely unless clearInterval() is called
        setCurrentTime(Date.now());
        setCurrentTime(Date.now());
      }, 1000);
    }
    return () => clearInterval(interval); //https://telegra.ph/clearInterval-02-26
  }, [isRunning]);

  // Fetch courses with Axios
  useEffect(() => {
    axios.get('/api/courses/', { withCredentials: true })  // Sending session cookie. for session based authentication backend.
      .then(res => setCourses(res.data))  //.then() always takes a function as an argument. That function receives the resolved value of the previous Promise. //res for response. res, data are just variable names representing the resolved value of the previous . 
      .catch(console.error);  // res.data will contain the response from the Django API converted into JSON (you dont need to call .json like fetch API), which can be a topic or an array of topics for the selected course. The structure of the data will depend on how you've set up your Django API
  }, []);

  // Fetch topics with Axios
  useEffect(() => {
    if (selectedCourse) {
      axios.get(`/api/courses/${selectedCourse}/topics/`, { withCredentials: true })
        .then(res => setTopics(res.data)) // see here: https://telegra.ph/what-is-then-02-26
        .catch(console.error);
    } else {
      setTopics([]);
    }
    setSelectedTopic('');
  }, [selectedCourse]);

  useEffect(() => {
    // Save the original method
    const originalScrollIntoView = Element.prototype.scrollIntoView;
    // Override scrollIntoView to ignore smooth scrolling
    Element.prototype.scrollIntoView = function (options) {
      if (options && options.behavior === 'smooth') {
        // Prevent smooth scrolling (which causes the jump)
        return;
      }
      return originalScrollIntoView.call(this, options);
    };

    return () => {
      // Restore the original method on cleanup
      Element.prototype.scrollIntoView = originalScrollIntoView;
    };
  }, []);



  const handleStartStop = () => {
    if (!isRunning) {
      setStartTime(Date.now());
      setCurrentTime(Date.now());
      setIsRunning(!isRunning);
    }
    else {
      const endTime = Date.now();
      const csrfToken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];

      // Axios POST request
      axios.post('/api/create/tracked-time/', {
        startTime: new Date(startTime).toISOString(), //This creates a new Date object in JavaScript. The Date constructor takes the endTime timestamp as an argument, converting it into a date and time representation that JavaScript can work with. .toISOString(): This method is called on the Date object. It converts the date and time represented by the Date object into an ISO 8601 formatted string. The resulting string will look something like "YYYY-MM-DDTHH:mm:ss.sssZ" (e.g., "2023-10-27T14:30:00.000Z").
        endTime: new Date(endTime).toISOString(),
        course: selectedCourse,
        topic: selectedTopic
      }, {
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        withCredentials: true
      })
        .then(() => {
          console.log('Time tracked successfully');
          setSelectedCourse(selectedCourse);
          setSelectedTopic(selectedTopic);
        })
        .catch(error => {
          console.error('Error tracking time:', error);
        })
        .finally(() => {
          setStartTime(null);
          setCurrentTime(null);
          setIsRunning(!isRunning);
        }); //.then -> successful response, .catch -> error response, .finally -> always runs
    }
  };

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
    <div className="timer-container ">
      <div className="timer-controls">
        <p>in Timer.jsx</p>


        {/* Courses Select */}
        <Select value={selectedCourse} onValueChange={setSelectedCourse}>
          <SelectTrigger className="w-[180px]" disabled={isRunning}>
            <SelectValue placeholder="Select Course" />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              <SelectLabel>Courses</SelectLabel>
              {courses.map((course) => (
                <SelectItem key={course.id} value={course.id}>
                  {course.name}
                </SelectItem>
              ))}
            </SelectGroup>
          </SelectContent>
        </Select>

        {/* Topics Select */}
        <Select value={selectedTopic} onValueChange={setSelectedTopic}>
          <SelectTrigger className="w-[180px]" disabled={isRunning}>
            <SelectValue placeholder="Select Topic" />
          </SelectTrigger>
          <SelectContent>
            <SelectGroup>
              <SelectLabel>Topics</SelectLabel>
              {topics.map((topic) => (
                <SelectItem key={topic.id} value={topic.id}>
                  {topic.name}
                </SelectItem>
              ))}
            </SelectGroup>
          </SelectContent>
        </Select>

        <Button
          onClick={handleStartStop}
          disabled={!selectedCourse || !selectedTopic}
        >
          {isRunning ? 'Stop Timer' : 'Start Timer'}
        </Button>
      </div>

      <div className="timer-display">
        {formatTime()}
      </div>
    </div>
  );
};

export default Timer;