import React from 'react';
import '../global.css';
import '../pages/calendar.css';
import { useState } from 'react';
import Calendar from 'react-calendar';


const Calendr = () => {
	const [date, setDate] = useState(new Date());

	return (
		<div>
		<h2>Mood Board</h2>
		<div className='calendar-container'>
        	<Calendar onChange={setDate} value={date} />
      	</div>
	  </div>
	);
};

export default Calendr;
