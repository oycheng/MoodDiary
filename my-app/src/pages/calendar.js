import React from 'react';
import '../global.css';
import '../pages/calendar.css';
import { useState } from 'react';
import Calendar from 'react-calendar';
import { addDays, differenceInCalendarDays } from 'date-fns';

const now = new Date();
const tomorrow = addDays(now, 1);
const in3Days = addDays(now, 3);
const in5Days = addDays(now, 5);

const highlightedDates = [tomorrow, in3Days, in5Days];

function isSameDay(a, b) {
	return differenceInCalendarDays(a, b) === 0;
}

const Calendr = () => {
	const [date, setDate] = useState(new Date());
	
	function tileClassName({ date, view }) {
		if (
		view === 'month' &&
		highlightedDates.find((dDate) => isSameDay(dDate, date))
		) {
			return 'highlight';
		}
	}
	return (
		<div>
		<h2>Mood Board</h2>
		<div className='calendar-container'>
        	<Calendar tileClassName={tileClassName} onChange={setDate} value={date} />
      	</div>
	  </div>
	);
};

export default Calendr;
