national_parks = {'Yellowstone': 
		{'state':'WY',
		'annual_visitors': 4116528,
		'size': 8991,
		'attractions':
			{'Old Faithful': 'geyser',
			'Grand Canyon of the Yellowstone': 'canyon',
			'Tower Fall': 'waterfall',
			'Yellowstone Lake': 'lake',
			'Mammoth Hot Springs': 'hot springs'},
		'trails':
			{'Uncle Tom\'s Trail':
				{'length': 0.1,
				'loop': False},
			'Trout Lake Trail': 
				{'length': 1.4,
				'loop': True},
			'Storm Point Trail':
				{'length': 3.3,
				'loop': True}
			}
		},
	'Yosemite':
		{'state':'CA',
		'annual_visitors': 4336890,
		'size': 3027,
		'attractions':
			{'El Capitan': 'monolith',
			'Half Dome': 'granite dome',
			'Vernal Fall': 'waterfall',
			'Yosemite Falls': 'waterfall',
			'Tuolomne Meadows': 'meadow',
			'Tunnel View': 'lookout point',
			'Cathedral Peak': 'mountain'},
		'trails':
			{'Mist Trail':
				{'length': 11,
				'loop': False},
			'Yosemite Falls Trail': 
				{'length': 11.6,
				'loop': False},
			'Panorama Trail':
				{'length': 13.5,
				'loop': False},
 			'Clouds Rest':
				{'length': 23.3,
				'loop': False}
			}
		},
	'Grand Teton':
		{'state': 'WY',
		'annual_visitors': 3270076,
		'size': 130,
		'attractions':
			{'Grand Teton': 'mountain',
			'Jenny Lake': 'lake',
			'Inspiration Point': 'lookout point',
			'Jackson Lake': 'lake',
			'Snake River': 'river'},
		'trails':
			{'String Lake Loop': 
				{'length': 6.1,
				'loop': True},
			'Cascade Canyon':
				{'length': 16.1,
				'loop': False},
			'Static Peak Divide':
				{'length': 26.2,
				'loop': False}
			}
		}
	}
print(national_parks.keys())
				     