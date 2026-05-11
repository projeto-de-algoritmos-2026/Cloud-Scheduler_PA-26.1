// -- Charts --

const chartReg = {};
function destroyChart(id) {
	if (chartReg[id]) {
		chartReg[id].destroy();
		delete chartReg[id];
	}
}

const DARK = { color: '#5C6B80', grid: { color: '#1E2835' } };
const baseOpts = {
	plugins: { legend: { labels: { color: '#9AAAB8', font: { family: 'JetBrains Mono', size: 11 } } } },
	scales: {
		x: { ticks: DARK, grid: DARK.grid },
		y: { ticks: DARK, grid: DARK.grid },
	}
};

function drawPenaltyBar(sEDF, sFIFO, sRand) {
	destroyChart('penalty');
	const ctx = document.getElementById('chart-penalty').getContext('2d');
	chartReg['penalty'] = new Chart(ctx, {
		type: 'bar',
		data: {
			labels: ['EDF', 'FIFO', 'Random'],
			datasets: [{
				data: [sEDF.totalPen, sFIFO.totalPen, sRand.totalPen],
				backgroundColor: ['rgba(0,229,160,.75)', 'rgba(255,69,96,.75)', 'rgba(245,166,35,.75)'],
				borderRadius: 6,
				borderSkipped: false,
			}]
		},
		options: {
			...baseOpts,
			plugins: { ...baseOpts.plugins, legend: { display: false } },
			scales: {
				...baseOpts.scales,
				y: { ...baseOpts.scales.y, ticks: { ...DARK, callback: v => `R$ ${(v / 1000).toFixed(0)}k` } }
			}
		}
	});
}

function drawLateBar(sEDF, sFIFO, sRand) {
	destroyChart('late');
	const ctx = document.getElementById('chart-late').getContext('2d');
	chartReg['late'] = new Chart(ctx, {
		type: 'bar',
		data: {
			labels: ['EDF', 'FIFO', 'Random'],
			datasets: [
				{
					label: 'Atrasadas',
					data: [sEDF.lateCount, sFIFO.lateCount, sRand.lateCount],
					backgroundColor: ['rgba(0,229,160,.75)', 'rgba(255,69,96,.75)', 'rgba(245,166,35,.75)'],
					borderRadius: 4,
				},
				{
					label: 'No Prazo',
					data: [sEDF.onTime, sFIFO.onTime, sRand.onTime],
					backgroundColor: ['rgba(0,229,160,.25)', 'rgba(255,69,96,.25)', 'rgba(245,166,35,.25)'],
					borderRadius: 4,
				},
			]
		},
		options: { ...baseOpts }
	});
}

function drawCumulative(edf, fifo, rand) {
	destroyChart('cum');
	const ctx = document.getElementById('chart-cumulative').getContext('2d');

	const toLine = (tasks, color) => {
		const sorted = [...tasks].sort((a, b) => a.finish - b.finish);
		let acc = 0;
		return {
			labels: sorted.map(t => t.finish.toFixed(0)),
			data: sorted.map(t => { acc += t.totalPenalty; return +acc.toFixed(0); }),
			color,
		};
	};

	const edfL  = toLine(edf,  '#00E5A0');
	const fifoL = toLine(fifo, '#FF4560');
	const randL = toLine(rand, '#F5A623');
	const allLabels = [...new Set([...edfL.labels, ...fifoL.labels, ...randL.labels])].sort((a, b) => +a - +b);

	const interp = (line) => allLabels.map(l => {
		const i = line.labels.indexOf(l);
		return i >= 0 ? line.data[i] : null;
	});

	chartReg['cum'] = new Chart(ctx, {
		type: 'line',
		data: {
			labels: allLabels,
			datasets: [
				{ label: 'EDF', data: interp(edfL), borderColor: '#00E5A0', tension: .4, borderWidth: 2, pointRadius: 0, spanGaps: true },
				{ label: 'FIFO', data: interp(fifoL), borderColor: '#FF4560', tension: .4, borderWidth: 2, pointRadius: 0, spanGaps: true },
				{ label: 'Random', data: interp(randL), borderColor: '#F5A623', tension: .4, borderWidth: 2, pointRadius: 0, spanGaps: true },
			]
		},
		options: {
			...baseOpts,
			animation: false,
			scales: {
				...baseOpts.scales,
				x: { ...baseOpts.scales.x, ticks: { ...DARK, maxTicksLimit: 10 } },
				y: { ...baseOpts.scales.y, ticks: { ...DARK, callback: v => `R$ ${(v / 1000).toFixed(0)}k` } }
			}
		}
	});
}
