// -- KPIs and entry point --

function updateKPIs(sEDF, sRand) {
	const saved = sRand.totalPen - sEDF.totalPen;
	const pct   = (100 * saved / sRand.totalPen).toFixed(1);
	document.getElementById('kpi-saving').textContent     = `R$ ${saved.toLocaleString('pt-BR')}`;
	document.getElementById('kpi-saving-pct').textContent = `${pct}% menos que Random`;
	document.getElementById('kpi-lmax').textContent       = `${sEDF.maxLat}s`;
	document.getElementById('kpi-late').textContent       = sEDF.lateCount;
	document.getElementById('kpi-late-pct').textContent   = `${sEDF.latePct}% das tarefas`;
	document.getElementById('kpi-penalty').textContent    = `${sEDF.totalPen.toLocaleString('pt-BR')}`;
}

function runSimulation() {
	const n       = +document.getElementById('n-range').value;
	const maxDur  = +document.getElementById('max-dur').value;
	const slack   = +document.getElementById('slack').value;
	const maxPen  = +document.getElementById('max-pen').value;

	const tasks = generateTasks(n, maxDur, slack, maxPen);

	const edf  = schedEDF(tasks);
	const fifo = schedFIFO(tasks);
	const rand = schedRandom(tasks);

	const sEDF  = stats(edf, 'EDF');
	const sFIFO = stats(fifo, 'FIFO');
	const sRand = stats(rand, 'Random');

	updateKPIs(sEDF, sRand);
	drawPenaltyBar(sEDF, sFIFO, sRand);
	drawLateBar(sEDF, sFIFO, sRand);
	drawCumulative(edf, fifo, rand);
	drawTable(sEDF, sFIFO, sRand);
	drawGantt(edf, Math.min(n, 35));
}

// Run on load
runSimulation();
