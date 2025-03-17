import { useState, useEffect, useRef } from 'react';
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
} from 'shadcn/ui/select.tsx';
import { Input } from 'shadcn/ui/input';

const Timer = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [startTime, setStartTime] = useState(null);
  const [currentTime, setCurrentTime] = useState(null);
  const [selectedCourse, setSelectedCourse] = useState('');
  const [selectedTopic, setSelectedTopic] = useState('');
  const [courses, setCourses] = useState([]);
  const [topics, setTopics] = useState([]);
  const [description, setDescription] = useState('');
  const [timerId, setTimerId] = useState(null);
  const [pendingTopic, setPendingTopic] = useState(null);

  // Create a ref to store the single WebSocket instance
  const socketRef = useRef(null);

  // Establish WebSocket connection only once on component mount
  useEffect(() => {
    socketRef.current = new WebSocket('ws://' + window.location.host + '/ws/active-now/');

    socketRef.current.onopen = () => {
      console.log('WebSocket connection established');
    };

    socketRef.current.onmessage = (event) => {
      console.log('Received message:', event.data);
    };

    socketRef.current.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    socketRef.current.onclose = () => {
      console.log('WebSocket connection closed');
    };

    // Clean up when component unmounts
    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, []);

  // Timer interval
  useEffect(() => {
    let interval;
    if (isRunning) {
      interval = setInterval(() => {
        setCurrentTime(Date.now());
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isRunning]);

  // Fetch courses
  useEffect(() => {
    axios
      .get('/api/courses/', { withCredentials: true })
      .then((res) => setCourses(res.data))
      .catch(console.error);
  }, []);

  // Fetch topics when a course is selected
  useEffect(() => {
    if (selectedCourse) {
      axios
        .get(`/api/courses/${selectedCourse}/topics/`, { withCredentials: true })
        .then((res) => setTopics(res.data))
        .catch(console.error);
    } else {
      setTopics([]);
    }
    setSelectedTopic('');
  }, [selectedCourse]);

  // Check for active timer on mount
  useEffect(() => {
    const checkActiveTimer = async () => {
      try {
        const response = await axios.get('/api/get-active-timer/', { withCredentials: true });
        const data = response.data;
        if (data.id) {
          setSelectedCourse(data.course || '');
          setPendingTopic(data.topic || '');
          setDescription(data.session || '');
          setStartTime(new Date(data.startTime).getTime());
          setCurrentTime(Date.now());
          setIsRunning(true);
          setTimerId(data.id);
        }
      } catch (error) {
        console.log('No active timer or error fetching active timer');
      }
    };
    checkActiveTimer();
  }, []);

  // Set selectedTopic when topics are available
  useEffect(() => {
    if (pendingTopic !== null && topics.length > 0) {
      setSelectedTopic(pendingTopic);
      setPendingTopic(null);
    }
  }, [topics, pendingTopic]);

  const handleStartStop = () => {
    const csrfToken = document.cookie
      .split('; ')
      .find((row) => row.startsWith('csrftoken='))
      ?.split('=')[1];

    if (!isRunning) {
      setStartTime(Date.now());
      setCurrentTime(Date.now());
      setIsRunning(true);

      axios
        .post(
          '/api/start-timer/',
          {
            course: selectedCourse || null,
            topic: selectedTopic || null,
            session: description || null,
          },
          {
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken,
            },
            withCredentials: true,
          }
        )
        .then((response) => {
          setTimerId(response.data.id);
          if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
            socketRef.current.send(JSON.stringify({ action: 'start_timer' }));
          }
        })
        .catch((error) => console.error('Error starting timer:', error));
    } else {
      axios
        .post(
          '/api/stop-timer/',
          { id: timerId },
          {
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': csrfToken,
            },
            withCredentials: true,
          }
        )
        .then(() => {
          if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
            socketRef.current.send(JSON.stringify({ action: 'stop_timer' }));
          }
          setStartTime(null);
          setCurrentTime(null);
          setIsRunning(false);
          setTimerId(null);
        })
        .catch((error) => console.error('Error stopping timer:', error));
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
        <div className="mx-4 my-2">
          <Select value={selectedCourse} onValueChange={setSelectedCourse}>
            <SelectTrigger disabled={isRunning} className="w-[180px]">
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
        <div className="mx-4 my-2">
          <Select value={selectedTopic} onValueChange={setSelectedTopic}>
            <SelectTrigger disabled={isRunning} className="w-[180px]">
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
          disabled={isRunning}
          onChange={(e) => setDescription(e.target.value)}
        />

        <Button className="mx-4 my-0" onClick={handleStartStop}>
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
