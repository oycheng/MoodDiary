import React from 'react';
import '../global.css';
import '../pages/calendar.css';
import { useState } from 'react';
import Calendar from 'react-calendar';
import moment from 'moment';
import data from './data.json';

const Calendr = () => {
	const [date, setDate] = useState(new Date());
	const [selectedDate, setSelectedDate] = useState(null);

	const handleDateClick = (date) => {
		setSelectedDate(date);
	};
	function tileClassName({ date, view }) {
		var dateConv = moment(date).format('MM-DD-YYYY');
		if (
		view === 'month' && data.hasOwnProperty(dateConv)) {
			return data[dateConv][0];
		}
	}
	const info = (date) => {
		var dateConv = moment(date).format('MM-DD-YYYY');
		if (data.hasOwnProperty(dateConv))
		{
			return <>{data[dateConv][1]}</>
		}
	}
	return (
		<div>
		<h2>Mood Board</h2>
		<div className='calendar-container'>
        	<Calendar onClickDay={handleDateClick} tileClassName={tileClassName} onChange={setDate} value={date} />
      	</div>
		<h3>
			{info(selectedDate)}
		</h3>
	  </div>
	);
};

export default Calendr;
