import React from 'react';
import '../global.css';
import '../pages/calendar.css';
import { useState } from 'react';
import Calendar from 'react-calendar';
import moment from 'moment';

const dict = {'06-16-2023' : 'red', '06-13-2023' : 'yellow', '06-23-2023' : 'blue', '07-20-2023' : 'red',
				'06-01-2023' : 'yellow', '06-20-2023' : 'red'};

const Calendr = () => {
	const [date, setDate] = useState(new Date());
	
	function tileClassName({ date, view }) {
		var dateConv = moment(date).format('MM-DD-YYYY');
		if (
		view === 'month' && dict.hasOwnProperty(dateConv)) {
			return dict[dateConv];
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
