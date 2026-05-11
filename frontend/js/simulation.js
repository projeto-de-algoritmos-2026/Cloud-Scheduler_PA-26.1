// -- Simulation engine --

function seededRng(seed) {
	let s = seed;
	return () => {
		s = (s * 1664525 + 1013904223) & 0xffffffff;
		return (s >>> 0) / 0xffffffff;
	};
}

function generateTasks(n, maxDur, slackFactor, maxPenalty, seed = 42) {
	const rng = seededRng(seed);
	return Array.from({ length: n }, (_, i) => {
		const dur      = 1 + rng() * (maxDur - 1);
		const deadline = dur * (1 + rng() * (slackFactor - 1)) + rng() * 10;
		const penalty  = 10 + rng() * (maxPenalty - 10);
		return {
			id: i + 1,
			name: `Job-${String(i + 1).padStart(3, '0')}`,
			duration: +dur.toFixed(2),
			deadline: +deadline.toFixed(2),
			penalty: +penalty.toFixed(2),
		};
	});
}

function simulate(tasks) {
	let clock = 0;
	return tasks.map(t => {
		const start  = clock;
		const finish = clock + t.duration;
		clock = finish;
		const lateness = Math.max(0, finish - t.deadline);
		return {
			...t,
			start,
			finish,
			lateness,
			isLate: lateness > 0,
			totalPenalty: lateness * t.penalty,
		};
	});
}

function stats(tasks, name) {
	const late = tasks.filter(t => t.isLate);
	return {
		algorithm: name,
		lateCount: late.length,
		onTime:    tasks.length - late.length,
		latePct:   +(100 * late.length / tasks.length).toFixed(1),
		maxLat:    +Math.max(...tasks.map(t => t.lateness)).toFixed(1),
		totalPen:  +tasks.reduce((a, t) => a + t.totalPenalty, 0).toFixed(0),
	};
}

function schedEDF(tasks)    { return simulate([...tasks].sort((a, b) => a.deadline - b.deadline)); }
function schedFIFO(tasks)   { return simulate([...tasks].sort((a, b) => a.id - b.id)); }
function schedRandom(tasks) {
	const rng = seededRng(7);
	const s = [...tasks].sort(() => rng() - 0.5);
	return simulate(s);
}
