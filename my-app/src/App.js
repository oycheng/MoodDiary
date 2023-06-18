import React from 'react';
import './App.css';
import Navbar from './components/Navbar';
import { BrowserRouter as Router, Routes, Route }
	from 'react-router-dom';
import Home from './pages';
import About from './pages/about';
import Calendr from './pages/calendar';
import Record from './pages/record';

function App() {
	return (
		<Router>
			<Navbar/>
			<Routes>
				<Route path='/' element={<Home />} />
				<Route path='/about' element={<About />} />
				<Route path='/calendar' element={<Calendr />} />
				<Route path='/record' element={<Record />} />
			</Routes>
		</Router>
	);
}

export default App;
