import React from "react";
import { Nav, NavLink, NavMenu }
	from "./NavbarElements";

const Navbar = () => {
	return (
		<>
			<Nav>
				<NavMenu>
					<NavLink to="/" activeStyle>
						Home
					</NavLink>
					<NavLink to="/about" activeStyle>
						About
					</NavLink>
					<NavLink to="/calendar" activeStyle>
						Calendar
					</NavLink>
					<NavLink to="/record" activeStyle>
						Record
					</NavLink>
				</NavMenu>
			</Nav>
		</>
	);
};

export default Navbar;
