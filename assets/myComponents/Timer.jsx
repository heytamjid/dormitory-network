import { useState, useEffect } from 'react';
import axios from 'axios';

import { Button } from 'shadcn/ui/button.tsx';
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from 'shadcn/ui/select.tsx'
import { Input } from 'shadcn/ui/input'




const Timer = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [startTime, setStartTime] = useState(null);
  const [currentTime, setCurrentTime] = useState(null);
  const [selectedCourse, setSelectedCourse] = useState('');
  const [selectedTopic, setSelectedTopic] = useState('');
  const [courses, setCourses] = useState([]);
  const [topics, setTopics] = useState([]);
  const [description, setDescription] = useState('');



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
        course: selectedCourse || null, // in JS, an empty string ('', "", ) is considered falsy.
        topic: selectedTopic || null, // in JS, || returns the first "truthy" value it encounters, or the last "falsy" value if no truthy value is found
        session: description || null // in C, C's || operator is strictly a logical operator. It evaluates expressions as boolean conditions and returns a boolean result. C does not have truthy/falsy values either
      }, {
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        withCredentials: true
      })
        .then(() => {
          console.log('Time tracked successfully');
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
    <div>
      <div className="timer-controls">

        {/* Courses Select */}
        <div className='mx-4 my-2'>
          <Select value={selectedCourse} onValueChange={setSelectedCourse}>
            <SelectTrigger className="w-[180px]">
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
        </div>

        {/* Topics Select */}
        <div className='mx-4 my-2'>
          <Select value={selectedTopic} onValueChange={setSelectedTopic}>
            <SelectTrigger className="w-[180px]">
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
        </div>

        <Input 
        className="w-[180px] mx-4 my-2" 
        type="text" 
        placeholder="Task" 
        value={description}
        onChange={(e) => setDescription(e.target.value)} />

        <Button
          className  = "mx-4 my-0" 
          onClick={handleStartStop}
        >
          {isRunning ? 'Stop Timer' : 'Start Timer'}
        </Button>
      </div>

      <div className="timer-display mx-4 my-4 border-2 border-black shadow-[2px_2px_0_0_black] text-2xl font-bold font-mono tracking-widest text-center p-4">
        {formatTime()}
      </div>
    </div>
  );
};

export default Timer;