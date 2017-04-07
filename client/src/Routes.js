import React from 'react';
import {
	Switch,
	Route
} from 'react-router-dom';

import NotFound  from './containers/NotFound';

export default () => (
	<Switch>
		<Route component={NotFound} />
	</Switch>
);